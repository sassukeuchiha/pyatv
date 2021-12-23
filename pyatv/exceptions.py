"""Local exceptions used by library."""
from enum import Enum

# pylint: disable=invalid-name


class PairingFailureReason(Enum):
    """Reason why pairing failed."""

    Succeeded = 1
    """Pairing succeeded, i.e. no error."""

    Unspecified = 2
    """Reason not known."""

    NoPinCode = 3
    """PIN code was not provided when it was expected."""

    Timeout = 4
    """Connection timed out while waiting for input."""


# pylint: enable=invalid-name


class NoServiceError(Exception):
    """Thrown when connecting to a device with no usable service."""


class UnsupportedProtocolError(Exception):
    """Thrown when an unsupported protocol was requested.

    DEPRECATED: Not used since 0.8.0. Will be removed in 0.10.0!
    """


class ConnectionFailedError(Exception):
    """Thrown when connection fails, e.g. refused or timed out."""


class PairingError(Exception):
    """Thrown when pairing fails."""

    def __init__(
        self,
        message: str,
        reason: PairingFailureReason = PairingFailureReason.Unspecified,
    ) -> None:
        """Initialize a new PairingError instance."""
        super().__init__(message)
        self._reason = reason

    @property
    def failure_reason(self) -> PairingFailureReason:
        """Return reason why pairing failed."""
        return self._reason


class AuthenticationError(Exception):
    """Thrown when authentication fails."""


class NotSupportedError(NotImplementedError):
    """Thrown when trying to perform an action that is not supported."""


class InvalidDmapDataError(Exception):
    """Thrown when invalid DMAP data is parsed."""


class UnknownMediaKindError(Exception):
    """Thrown when an unknown media kind is found."""


class UnknownPlayStateError(Exception):
    """Thrown when an unknown play state is found."""


class NoAsyncListenerError(Exception):
    """Thrown when starting AsyncUpdater with no listener."""


class NoCredentialsError(Exception):
    """Thrown if credentials are missing."""


class InvalidCredentialsError(Exception):
    """Thrown if credentials are invalid."""


class DeviceIdMissingError(Exception):
    """Thrown when device id is missing."""


class BackOffError(Exception):
    """Thrown when device mandates a backoff period."""


class PlaybackError(Exception):
    """Thrown when media playback failed."""


class CommandError(Exception):
    """Thrown when a command (e.g. play or pause) failed."""


class NonLocalSubnetError(Exception):
    """Thrown when address it not in any local subnet.

    DEPRECATED: Not used since 0.7.1. Will be removed in 0.9.0!
    """


class InvalidStateError(Exception):
    """Thrown when trying to perform an action not possible in the current state."""


class ProtocolError(Exception):
    """Thrown when a generic protocol error occurs.

    Generic protocol errors includes for instance missing fields, incorrect or
    unexpected types, etc. Any error that can happen when communicating with a device
    that is not covered by another exception is covered by this exception.
    """


class HttpError(ProtocolError):
    """Thrown when a HTTP error occurs."""

    def __init__(self, message: str, status_code: int) -> None:
        """Initialize a new HttpError."""
        super().__init__(message)
        self._status_code = status_code

    @property
    def status_code(self) -> int:
        """Return status code that triggered the error."""
        return self._status_code


class InvalidConfigError(Exception):
    """Thrown when something is wrong or missing in the config."""


class BlockedStateError(Exception):
    """Thrown when calling a blocked method.

    Typically, public interface methods (e.g. any method available via the object
    returned by `pyatv.connect`) becomes blocked after either calling close or because
    the connection was closed for some other reason.
    """
