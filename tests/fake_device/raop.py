"""Fake RAOP device for tests."""
import asyncio
from functools import wraps
from hashlib import md5
import logging
import plistlib
import random
import string
from types import SimpleNamespace
from typing import Dict, Optional, cast

from bitarray import bitarray

from pyatv.protocols.dmap import parser
from pyatv.protocols.dmap.tag_definitions import lookup_tag
from pyatv.protocols.raop.packets import RetransmitReqeust, RtpHeader, SyncPacket
from pyatv.protocols.raop.raop import parse_transport
from pyatv.support.http import (
    BasicHttpServer,
    HttpRequest,
    HttpResponse,
    HttpSimpleRouter,
    http_server,
)

_LOGGER = logging.getLogger(__name__)

INITIAL_VOLUME = -15.0

DIGEST_PAYLOAD = (
    'Digest username="{0}", realm="{1}", nonce="{2}", uri="{3}", response="{4}"'
)

REALM = "raop"


def requires_auth(method):
    @wraps(method)
    def _impl(self, request: HttpRequest, *args, **kwargs):
        if self.state.auth_required and not self.state.auth_setup_performed:
            return HttpResponse(
                "RTSP", "1.0", 403, "Forbidden", {"CSeq": request.headers["CSeq"]}, b""
            )
        return method(self, request, *args, **kwargs)

    return _impl


def verify_password(method):
    @wraps(method)
    def _impl(self, request: HttpRequest, *args, **kwargs):
        # No password required
        if not self.state.password:
            return method(self, request, *args, **kwargs)

        # Send a challenge
        if not self.state.nonce:
            nonce = self.state.nonce = "".join(
                random.choices(string.ascii_letters + string.digits, k=32)
            )
            return HttpResponse(
                "RTSP",
                "1.0",
                401,
                "Unauthorized",
                {
                    "CSeq": request.headers["CSeq"],
                    "WWW-Authenticate": f'Digest realm="{REALM}", nonce="{nonce}"',
                },
                b"",
            )

        # Verify the authentication payload send by the client
        payload_data = request.headers.get("Authorization", "").split('"')
        if len(payload_data) == 11:
            uri = request.path
            user = payload_data[1]
            actual_response = payload_data[9]
            nonce = self.state.nonce
            pwd = self.state.password
            ha1 = md5(f"{user}:{REALM}:{pwd}".encode("utf-8")).hexdigest()
            ha2 = md5(f"{request.method}:{uri}".encode("utf-8")).hexdigest()
            expected_response = md5(f"{ha1}:{nonce}:{ha2}".encode("utf-8")).hexdigest()

            if actual_response == expected_response:
                return method(self, request, *args, **kwargs)

        # Password verification failed
        return HttpResponse(
            "RTSP", "1.0", 401, "Unauthorized", {"CSeq": request.headers["CSeq"]}, b""
        )

    return _impl


def alac_decode(data: bytes) -> bytes:
    """Decode an ALAC frame and return raw audio data."""
    buffer = bitarray()
    buffer.frombytes(data)

    # Audio starts 23 bits in and last bit must be removed to keep byte alignment,
    # otherwise an additional \x00 will be present at the end
    return buffer[23:-1].tobytes()


class FakeRaopState:
    """Internal state for RAOP service."""

    def __init__(self):
        self.metadata = SimpleNamespace(title=None, artist=None, album=None)
        self.audio_packets: Dict[int, bytes] = {}  # seqo -> raw audio
        self.password: Optional[str] = None
        self.nonce: Optional[str] = None
        self.auth_required: bool = False
        self.auth_setup_performed: bool = False
        self.supports_retransmissions: bool = True
        self.supports_feedback: bool = True
        self.feedback_packets_received: int = 0
        self.sync_packets_received: int = 0
        self.drop_packets: int = 0
        self.control_port: int = 0
        self.remote_address: Optional[str] = None
        self.volume: float = INITIAL_VOLUME
        self.initial_audio_level_supported: bool = False
        self.info_supported: bool = True
        self.teardown_called: bool = False

    @property
    def raw_audio(self) -> bytes:
        if not self.audio_packets:
            return b""

        # Sort received packets according to sequence number and join audio data
        # together. If a sequence number is missing, the gap will not be filled with
        # anything.
        sorted_packets = sorted(self.audio_packets.items())
        raw_audio = b"".join(audio for _, audio in sorted_packets)
        return raw_audio


class AudioReceiver(asyncio.Protocol):
    """Protocol used to receive audio packets."""

    def __init__(self, state: FakeRaopState):
        """Initialize a new AudioReceiver instance."""
        self.transport = None
        self.state: FakeRaopState = state

    def close(self):
        """Close audio receiver."""
        if self.transport:
            self.transport.close()
            self.transport = None

    @property
    def port(self):
        """Port this server listens on."""
        return self.transport.get_extra_info("socket").getsockname()[1]

    def connection_made(self, transport):
        """Handle that connection succeeded."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        """Handle incoming data."""
        _LOGGER.debug("Received audio packet from %s: %s...", addr, data[0:32])

        header = RtpHeader.decode(data, allow_excessive=True)
        packet_type = header.type & 0x7F  # Remove marker bit

        if packet_type == 0x60:  # Normal packet
            # Drop packet if requested (only for normal packets)
            if self.state.drop_packets > 0:
                _LOGGER.debug(
                    "Dropping packet (%d) %d", header.seqno, self.state.drop_packets
                )
                self.state.drop_packets -= 1

                if self.state.supports_retransmissions:
                    _LOGGER.debug("Requesting to retransmit seqno %d", header.seqno)
                    self._request_retransmit(
                        data, (self.state.remote_address, self.state.control_port)
                    )
            else:
                self.state.audio_packets[header.seqno] = alac_decode(data[12:])
        elif packet_type == 0x56:  # Retransmission
            original_packet = data[4:]  # Remove retransmission header
            self.state.audio_packets[header.seqno] = alac_decode(original_packet[12:])
        else:
            _LOGGER.debug("Unhandled packet type: %d", packet_type)

    def _request_retransmit(self, data: bytes, addr) -> None:
        header = RtpHeader.decode(data, allow_excessive=True)
        packet = RetransmitReqeust.encode(
            0x80,  # Header
            0x55 | 0x80,  # 0x55 = retransmit, 0x80 = marker bit
            0,  # Sequence number in RTP header not used(?)
            header.seqno,  # Sequence number of missing packet
            1,  # Ask for one packet
        )
        self.transport.sendto(packet, addr)
        _LOGGER.debug("Sent %s to %s", packet, addr)

    def error_received(self, exc) -> None:
        """Handle a connection error."""
        self.transport.close()
        _LOGGER.error("Audio receive error: %s", exc)

    def connection_lost(self, exc):
        """Handle that connection was lost."""
        _LOGGER.debug("Audio receiver lost connection (%s)", exc)


class TimingServer(asyncio.Protocol):
    """Protocol used for time synchronization."""

    def __init__(self):
        """Initialize a new TimingServer instance."""
        self.transport = None

    def close(self):
        """Close timing server."""
        if self.transport:
            self.transport.close()
            self.transport = None

    @property
    def port(self):
        """Port this server listens on."""
        return self.transport.get_extra_info("socket").getsockname()[1]

    def connection_made(self, transport):
        """Handle that connection succeeded."""
        self.transport = transport

    def datagram_received(self, data, addr):
        """Handle incoming data."""
        _LOGGER.debug("Received timing packet: %s", data)

    def error_received(self, exc) -> None:
        """Handle a connection error."""
        self.transport.close()
        _LOGGER.error("Timing receive error: %s", exc)

    def connection_lost(self, exc):
        """Handle that connection was lost."""
        _LOGGER.debug("Timing server lost connection (%s)", exc)


class ControlServer(asyncio.Protocol):
    """Protocol used for control channel."""

    def __init__(self, state: FakeRaopState):
        """Initialize a new ControlServer instance."""
        self.transport = None
        self.state: FakeRaopState = state

    def close(self):
        """Close control channel."""
        if self.transport:
            self.transport.close()
            self.transport = None

    @property
    def port(self):
        """Port this server listens on."""
        return self.transport.get_extra_info("socket").getsockname()[1]

    def connection_made(self, transport):
        """Handle that connection succeeded."""
        self.transport = transport

    def datagram_received(self, data, addr):
        """Handle incoming data."""
        _LOGGER.debug("Received control packet: %s", data)
        # TODO: Only decoding now, should verify some stuff as well
        SyncPacket.decode(data)
        self.state.sync_packets_received += 1

    def error_received(self, exc) -> None:
        """Handle a connection error."""
        self.transport.close()
        _LOGGER.error("Control channel receive error: %s", exc)

    def connection_lost(self, exc):
        """Handle that connection was lost."""
        _LOGGER.debug("Control channel lost connection (%s)", exc)


class FakeRaopService(HttpSimpleRouter):
    """Implementation of a fake RAOP device."""

    def __init__(self, state, app, loop):
        """Initialize a new FakeRaopService instance."""
        super().__init__()
        self.loop: asyncio.AbstractEventLoop = loop
        self.state: FakeRaopState = state
        self.server: Optional[BasicHttpServer] = None
        self.port: int = None
        self._audio_receiver: Optional[AudioReceiver] = None
        self._timing_server: Optional[TimingServer] = None
        self._control_server: Optional[ControlServer] = None
        self.add_route("ANNOUNCE", "rtsp://.*", self.handle_announce)
        self.add_route("SETUP", "rtsp://*", self.handle_setup)
        self.add_route("SET_PARAMETER", "rtsp://*", self.handle_set_parameter)
        self.add_route("POST", "/feedback", self.handle_feedback)
        self.add_route("RECORD", "rtsp://*", self.handle_record)
        self.add_route("POST", "/auth-setup", self.handle_auth_setup)
        self.add_route("GET", "/info", self.handle_info)
        self.add_route("TEARDOWN", "rtsp://*", self.handle_teardown)

    async def start(self, start_web_server: bool):
        """Start the fake RAOP service."""
        self.server, self.port = await http_server(
            lambda: BasicHttpServer(self), address="0.0.0.0"
        )

        local_addr = ("0.0.0.0", 0)
        (_, audio_receiver) = await self.loop.create_datagram_endpoint(
            lambda: AudioReceiver(self.state),
            local_addr=local_addr,
        )
        (_, timing_server) = await self.loop.create_datagram_endpoint(
            TimingServer,
            local_addr=local_addr,
        )
        (_, control_server) = await self.loop.create_datagram_endpoint(
            lambda: ControlServer(self.state),
            local_addr=local_addr,
        )

        self._audio_receiver = cast(AudioReceiver, audio_receiver)
        self._timing_server = cast(TimingServer, timing_server)
        self._control_server = cast(TimingServer, control_server)
        _LOGGER.debug(
            "Started RAOP server: port=%d, audio=%d, timing=%d, control=%d",
            self.port,
            self._audio_receiver.port,
            self._timing_server.port,
            self._control_server.port,
        )

    async def cleanup(self):
        """Clean up resources used by fake RAOP service."""
        if self.server:
            self.server.close()
        if self._audio_receiver:
            self._audio_receiver.close()
        if self._timing_server:
            self._timing_server.close()
        if self._control_server:
            self._control_server.close()

    @requires_auth
    @verify_password
    def handle_announce(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming ANNOUNCE request."""
        _LOGGER.debug("Received ANNOUNCE: %s", request)
        for line in request.body.decode("utf-8").split("\r\n"):
            if line.startswith("o="):
                self.state.remote_address = line.split()[-1]
                break

        return HttpResponse(
            "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
        )

    @requires_auth
    @verify_password
    def handle_setup(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming SETUP request."""
        _LOGGER.debug("Received SETUP: %s", request)
        _, options = parse_transport(request.headers["Transport"])
        self.state.control_port = int(options["control_port"])
        headers = {
            "Transport": (
                "RTP/AVP/UDP;unicast;mode=record;"
                f"server_port={self._audio_receiver.port};"
                f"control_port={self._control_server.port};"
                f"timing_port={self._timing_server.port}"
            ),
            "Session": "1",
            "CSeq": request.headers["CSeq"],
        }
        return HttpResponse("RTSP", "1.0", 200, "OK", headers, b"")

    @requires_auth
    @verify_password
    def handle_set_parameter(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming SET_PARAMETER request."""
        _LOGGER.debug("Received SET_PARAMETER: %s", request)
        if request.headers["Content-Type"] == "application/x-dmap-tagged":
            tags = parser.parse(request.body, lookup_tag)
            self.state.metadata.title = parser.first(tags, "mlit", "minm")
            self.state.metadata.artist = parser.first(tags, "mlit", "asar")
            self.state.metadata.album = parser.first(tags, "mlit", "asal")
        elif request.body.startswith("volume:"):
            self.state.volume = float(request.body.split(" ", maxsplit=1)[1])
            _LOGGER.debug("Changing volume to %f", self.state.volume)
        else:
            return HttpResponse(
                "RTSP",
                "1.0",
                501,
                "Not implemented",
                {"CSeq": request.headers["CSeq"]},
                b"",
            )
        return HttpResponse(
            "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
        )

    @requires_auth
    @verify_password
    def handle_feedback(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming feedback request."""
        _LOGGER.debug("Received feedback: %s", request)
        self.state.feedback_packets_received += 1
        if not self.state.supports_feedback:
            return HttpResponse(
                "RTSP",
                "1.0",
                501,
                "Not implemented",
                {"CSeq": request.headers["CSeq"]},
                b"",
            )
        return HttpResponse(
            "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
        )

    @requires_auth
    @verify_password
    def handle_record(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming RECORD request."""
        _LOGGER.debug("Received RECORD: %s", request)
        return HttpResponse(
            "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
        )

    @verify_password
    def handle_auth_setup(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming auth-setup request."""
        _LOGGER.debug("Received auth-setup: %s", request)
        # Just check if decent sized payload is there
        if len(request.body) == 1 + 32:  # auth type + public key
            self.state.auth_setup_performed = True
            return HttpResponse(
                "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
            )
        return HttpResponse(
            "RTSP", "1.0", 403, "Forbidden", {"CSeq": request.headers["CSeq"]}, b""
        )

    def handle_info(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming info request."""
        if not self.state.info_supported:
            return HttpResponse(
                "RTSP",
                "1.0",
                400,
                "Bad Request",
                {
                    "CSeq": request.headers["CSeq"],
                },
                b"",
            )
        info = {}
        if self.state.initial_audio_level_supported:
            info["initialVolume"] = self.state.volume
        return HttpResponse(
            "RTSP",
            "1.0",
            200,
            "OK",
            {
                "CSeq": request.headers["CSeq"],
                "content-type": "application/x-apple-binary-plist",
            },
            plistlib.dumps(info),
        )

    def handle_teardown(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Handle incoming TEARDOWN request."""
        self.state.teardown_called = True
        return HttpResponse(
            "RTSP", "1.0", 200, "OK", {"CSeq": request.headers["CSeq"]}, b""
        )


class FakeRaopUseCases:
    """Wrapper for altering behavior of a FakeRaopService instance."""

    def __init__(self, state):
        """Initialize a new FakeRaopUseCases instance."""
        self.state = state

    def retransmissions_enabled(self, enabled: bool) -> None:
        """Enable or disable retransmissions."""
        self.state.supports_retransmissions = enabled

    def drop_n_packets(self, packets: int) -> None:
        """Make fake device drop packets and trigger retransmission (if supported)."""
        self.state.drop_packets = packets

    def feedback_enabled(self, enabled: bool) -> None:
        """Enable or disable support for /feedback endpoint."""
        self.state.supports_feedback = enabled

    def initial_audio_level_supported(self, supported: bool) -> None:
        """Initial audio level reported in info from device."""
        self.state.initial_audio_level_supported = supported

    def require_auth(self, is_required: bool) -> None:
        """Enable or disable requirement to perform authentication."""
        self.state.auth_required = is_required

    def password(self, new_password: Optional[str]) -> None:
        """Set a new password. Pass in None to remove the password."""
        self.state.password = new_password
        self.state.nonce = None

    def supports_info(self, is_supported: bool) -> None:
        """State if /info is supported or not."""
        self.state.info_supported = is_supported
