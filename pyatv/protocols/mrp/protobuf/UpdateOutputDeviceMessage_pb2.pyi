"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.extension_dict
import google.protobuf.message
import pyatv.protocols.mrp.protobuf.Common_pb2
import pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class AVOutputDeviceSourceInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ROUTINGCONTEXTUID_FIELD_NUMBER: builtins.int
    MULTIPLEBUILTINDEVICES_FIELD_NUMBER: builtins.int
    routingContextUID: typing.Text
    multipleBuiltInDevices: builtins.bool
    def __init__(self,
        *,
        routingContextUID: typing.Optional[typing.Text] = ...,
        multipleBuiltInDevices: typing.Optional[builtins.bool] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["multipleBuiltInDevices",b"multipleBuiltInDevices","routingContextUID",b"routingContextUID"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["multipleBuiltInDevices",b"multipleBuiltInDevices","routingContextUID",b"routingContextUID"]) -> None: ...
global___AVOutputDeviceSourceInfo = AVOutputDeviceSourceInfo

class AVOutputDeviceDescriptor(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    UNIQUEIDENTIFIER_FIELD_NUMBER: builtins.int
    GROUPID_FIELD_NUMBER: builtins.int
    MODELID_FIELD_NUMBER: builtins.int
    MACADDRESS_FIELD_NUMBER: builtins.int
    CANACCESSREMOTEASSETS_FIELD_NUMBER: builtins.int
    ISREMOTECONTROLLABLE_FIELD_NUMBER: builtins.int
    ISGROUPLEADER_FIELD_NUMBER: builtins.int
    ISGROUPABLE_FIELD_NUMBER: builtins.int
    DEVICETYPE_FIELD_NUMBER: builtins.int
    DEVICESUBTYPE_FIELD_NUMBER: builtins.int
    MODELSPECIFICINFODATA_FIELD_NUMBER: builtins.int
    BATTERYLEVEL_FIELD_NUMBER: builtins.int
    ISLOCALDEVICE_FIELD_NUMBER: builtins.int
    SUPPORTSEXTERNALSCREEN_FIELD_NUMBER: builtins.int
    REQUIRESAUTHORIZATION_FIELD_NUMBER: builtins.int
    SHOULDFORCEREMOTECONTROLABILLITY_FIELD_NUMBER: builtins.int
    SOURCEINFO_FIELD_NUMBER: builtins.int
    ISDEVICEGROUPABLE_FIELD_NUMBER: builtins.int
    CANRELAYCOMMUNICATIONCHANNEL_FIELD_NUMBER: builtins.int
    LOGICALDEVICEID_FIELD_NUMBER: builtins.int
    ISPROXYGROUPPLAYER_FIELD_NUMBER: builtins.int
    FIRMWAREVERSION_FIELD_NUMBER: builtins.int
    VOLUME_FIELD_NUMBER: builtins.int
    ISVOLUMECONTROLAVAILABLE_FIELD_NUMBER: builtins.int
    CANACCESSAPPLEMUSIC_FIELD_NUMBER: builtins.int
    CANACCESSICLOUDMUSICLIBRARY_FIELD_NUMBER: builtins.int
    GROUPCONTAINSGROUPLEADER_FIELD_NUMBER: builtins.int
    SUPPORTSBUFFEREDAIRPLAY_FIELD_NUMBER: builtins.int
    CANPLAYENCRYPTEDPROGRESSIVEDOWNLOADASSETS_FIELD_NUMBER: builtins.int
    CANFETCHMEDIADATAFROMSENDER_FIELD_NUMBER: builtins.int
    RESENTSOPTIMIZEDUSERINTERFACEWHENPLAYINGFETCHEDAUDIOONLYASSETS_FIELD_NUMBER: builtins.int
    ISAIRPLAYRECEIVERSESSIONACTIVE_FIELD_NUMBER: builtins.int
    PARENTGROUPIDENTIFIER_FIELD_NUMBER: builtins.int
    PARENTGROUPCONTAINSDISCOVERABLELEADER_FIELD_NUMBER: builtins.int
    ISADDEDTOHOMEKIT_FIELD_NUMBER: builtins.int
    VOLUMECAPABILITIES_FIELD_NUMBER: builtins.int
    BLUETOOTHID_FIELD_NUMBER: builtins.int
    SUPPORTSHAP_FIELD_NUMBER: builtins.int
    USINGJSONPROTOCOL_FIELD_NUMBER: builtins.int
    CLUSTERCOMPOSITIONS_FIELD_NUMBER: builtins.int
    CLUSTERTYPE_FIELD_NUMBER: builtins.int
    PRIMARYUID_FIELD_NUMBER: builtins.int
    CONFIGUREDCLUSTERSIZE_FIELD_NUMBER: builtins.int
    PRODUCESLOWFIDELITYAUDIO_FIELD_NUMBER: builtins.int
    name: typing.Text
    uniqueIdentifier: typing.Text
    groupID: typing.Text
    modelID: typing.Text
    macAddress: builtins.bytes
    canAccessRemoteAssets: builtins.bool
    isRemoteControllable: builtins.bool
    isGroupLeader: builtins.bool
    isGroupable: builtins.bool
    deviceType: pyatv.protocols.mrp.protobuf.Common_pb2.DeviceType.Enum.ValueType
    deviceSubType: pyatv.protocols.mrp.protobuf.Common_pb2.DeviceSubType.Enum.ValueType
    modelSpecificInfoData: builtins.bytes
    batteryLevel: builtins.float
    isLocalDevice: builtins.bool
    supportsExternalScreen: builtins.bool
    requiresAuthorization: builtins.bool
    shouldForceRemoteControlabillity: builtins.bool
    @property
    def sourceInfo(self) -> global___AVOutputDeviceSourceInfo: ...
    isDeviceGroupable: builtins.bool
    canRelayCommunicationChannel: builtins.bool
    logicalDeviceID: typing.Text
    isProxyGroupPlayer: builtins.bool
    firmwareVersion: typing.Text
    volume: builtins.float
    isVolumeControlAvailable: builtins.bool
    canAccessAppleMusic: builtins.bool
    canAccessiCloudMusicLibrary: builtins.bool
    groupContainsGroupLeader: builtins.bool
    supportsBufferedAirPlay: builtins.bool
    canPlayEncryptedProgressiveDownloadAssets: builtins.bool
    canFetchMediaDataFromSender: builtins.bool
    resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets: builtins.bool
    isAirPlayReceiverSessionActive: builtins.bool
    parentGroupIdentifier: typing.Text
    parentGroupContainsDiscoverableLeader: builtins.bool
    isAddedToHomeKit: builtins.bool
    volumeCapabilities: builtins.int
    bluetoothID: typing.Text
    supportsHAP: builtins.bool
    usingJSONProtocol: builtins.bool
    @property
    def clusterCompositions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___AVOutputDeviceDescriptor]: ...
    clusterType: builtins.int
    primaryUID: typing.Text
    configuredClusterSize: builtins.int
    producesLowFidelityAudio: builtins.bool
    def __init__(self,
        *,
        name: typing.Optional[typing.Text] = ...,
        uniqueIdentifier: typing.Optional[typing.Text] = ...,
        groupID: typing.Optional[typing.Text] = ...,
        modelID: typing.Optional[typing.Text] = ...,
        macAddress: typing.Optional[builtins.bytes] = ...,
        canAccessRemoteAssets: typing.Optional[builtins.bool] = ...,
        isRemoteControllable: typing.Optional[builtins.bool] = ...,
        isGroupLeader: typing.Optional[builtins.bool] = ...,
        isGroupable: typing.Optional[builtins.bool] = ...,
        deviceType: typing.Optional[pyatv.protocols.mrp.protobuf.Common_pb2.DeviceType.Enum.ValueType] = ...,
        deviceSubType: typing.Optional[pyatv.protocols.mrp.protobuf.Common_pb2.DeviceSubType.Enum.ValueType] = ...,
        modelSpecificInfoData: typing.Optional[builtins.bytes] = ...,
        batteryLevel: typing.Optional[builtins.float] = ...,
        isLocalDevice: typing.Optional[builtins.bool] = ...,
        supportsExternalScreen: typing.Optional[builtins.bool] = ...,
        requiresAuthorization: typing.Optional[builtins.bool] = ...,
        shouldForceRemoteControlabillity: typing.Optional[builtins.bool] = ...,
        sourceInfo: typing.Optional[global___AVOutputDeviceSourceInfo] = ...,
        isDeviceGroupable: typing.Optional[builtins.bool] = ...,
        canRelayCommunicationChannel: typing.Optional[builtins.bool] = ...,
        logicalDeviceID: typing.Optional[typing.Text] = ...,
        isProxyGroupPlayer: typing.Optional[builtins.bool] = ...,
        firmwareVersion: typing.Optional[typing.Text] = ...,
        volume: typing.Optional[builtins.float] = ...,
        isVolumeControlAvailable: typing.Optional[builtins.bool] = ...,
        canAccessAppleMusic: typing.Optional[builtins.bool] = ...,
        canAccessiCloudMusicLibrary: typing.Optional[builtins.bool] = ...,
        groupContainsGroupLeader: typing.Optional[builtins.bool] = ...,
        supportsBufferedAirPlay: typing.Optional[builtins.bool] = ...,
        canPlayEncryptedProgressiveDownloadAssets: typing.Optional[builtins.bool] = ...,
        canFetchMediaDataFromSender: typing.Optional[builtins.bool] = ...,
        resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets: typing.Optional[builtins.bool] = ...,
        isAirPlayReceiverSessionActive: typing.Optional[builtins.bool] = ...,
        parentGroupIdentifier: typing.Optional[typing.Text] = ...,
        parentGroupContainsDiscoverableLeader: typing.Optional[builtins.bool] = ...,
        isAddedToHomeKit: typing.Optional[builtins.bool] = ...,
        volumeCapabilities: typing.Optional[builtins.int] = ...,
        bluetoothID: typing.Optional[typing.Text] = ...,
        supportsHAP: typing.Optional[builtins.bool] = ...,
        usingJSONProtocol: typing.Optional[builtins.bool] = ...,
        clusterCompositions: typing.Optional[typing.Iterable[global___AVOutputDeviceDescriptor]] = ...,
        clusterType: typing.Optional[builtins.int] = ...,
        primaryUID: typing.Optional[typing.Text] = ...,
        configuredClusterSize: typing.Optional[builtins.int] = ...,
        producesLowFidelityAudio: typing.Optional[builtins.bool] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["batteryLevel",b"batteryLevel","bluetoothID",b"bluetoothID","canAccessAppleMusic",b"canAccessAppleMusic","canAccessRemoteAssets",b"canAccessRemoteAssets","canAccessiCloudMusicLibrary",b"canAccessiCloudMusicLibrary","canFetchMediaDataFromSender",b"canFetchMediaDataFromSender","canPlayEncryptedProgressiveDownloadAssets",b"canPlayEncryptedProgressiveDownloadAssets","canRelayCommunicationChannel",b"canRelayCommunicationChannel","clusterType",b"clusterType","configuredClusterSize",b"configuredClusterSize","deviceSubType",b"deviceSubType","deviceType",b"deviceType","firmwareVersion",b"firmwareVersion","groupContainsGroupLeader",b"groupContainsGroupLeader","groupID",b"groupID","isAddedToHomeKit",b"isAddedToHomeKit","isAirPlayReceiverSessionActive",b"isAirPlayReceiverSessionActive","isDeviceGroupable",b"isDeviceGroupable","isGroupLeader",b"isGroupLeader","isGroupable",b"isGroupable","isLocalDevice",b"isLocalDevice","isProxyGroupPlayer",b"isProxyGroupPlayer","isRemoteControllable",b"isRemoteControllable","isVolumeControlAvailable",b"isVolumeControlAvailable","logicalDeviceID",b"logicalDeviceID","macAddress",b"macAddress","modelID",b"modelID","modelSpecificInfoData",b"modelSpecificInfoData","name",b"name","parentGroupContainsDiscoverableLeader",b"parentGroupContainsDiscoverableLeader","parentGroupIdentifier",b"parentGroupIdentifier","primaryUID",b"primaryUID","producesLowFidelityAudio",b"producesLowFidelityAudio","requiresAuthorization",b"requiresAuthorization","resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets",b"resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets","shouldForceRemoteControlabillity",b"shouldForceRemoteControlabillity","sourceInfo",b"sourceInfo","supportsBufferedAirPlay",b"supportsBufferedAirPlay","supportsExternalScreen",b"supportsExternalScreen","supportsHAP",b"supportsHAP","uniqueIdentifier",b"uniqueIdentifier","usingJSONProtocol",b"usingJSONProtocol","volume",b"volume","volumeCapabilities",b"volumeCapabilities"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["batteryLevel",b"batteryLevel","bluetoothID",b"bluetoothID","canAccessAppleMusic",b"canAccessAppleMusic","canAccessRemoteAssets",b"canAccessRemoteAssets","canAccessiCloudMusicLibrary",b"canAccessiCloudMusicLibrary","canFetchMediaDataFromSender",b"canFetchMediaDataFromSender","canPlayEncryptedProgressiveDownloadAssets",b"canPlayEncryptedProgressiveDownloadAssets","canRelayCommunicationChannel",b"canRelayCommunicationChannel","clusterCompositions",b"clusterCompositions","clusterType",b"clusterType","configuredClusterSize",b"configuredClusterSize","deviceSubType",b"deviceSubType","deviceType",b"deviceType","firmwareVersion",b"firmwareVersion","groupContainsGroupLeader",b"groupContainsGroupLeader","groupID",b"groupID","isAddedToHomeKit",b"isAddedToHomeKit","isAirPlayReceiverSessionActive",b"isAirPlayReceiverSessionActive","isDeviceGroupable",b"isDeviceGroupable","isGroupLeader",b"isGroupLeader","isGroupable",b"isGroupable","isLocalDevice",b"isLocalDevice","isProxyGroupPlayer",b"isProxyGroupPlayer","isRemoteControllable",b"isRemoteControllable","isVolumeControlAvailable",b"isVolumeControlAvailable","logicalDeviceID",b"logicalDeviceID","macAddress",b"macAddress","modelID",b"modelID","modelSpecificInfoData",b"modelSpecificInfoData","name",b"name","parentGroupContainsDiscoverableLeader",b"parentGroupContainsDiscoverableLeader","parentGroupIdentifier",b"parentGroupIdentifier","primaryUID",b"primaryUID","producesLowFidelityAudio",b"producesLowFidelityAudio","requiresAuthorization",b"requiresAuthorization","resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets",b"resentsOptimizedUserInterfaceWhenPlayingFetchedAudioOnlyAssets","shouldForceRemoteControlabillity",b"shouldForceRemoteControlabillity","sourceInfo",b"sourceInfo","supportsBufferedAirPlay",b"supportsBufferedAirPlay","supportsExternalScreen",b"supportsExternalScreen","supportsHAP",b"supportsHAP","uniqueIdentifier",b"uniqueIdentifier","usingJSONProtocol",b"usingJSONProtocol","volume",b"volume","volumeCapabilities",b"volumeCapabilities"]) -> None: ...
global___AVOutputDeviceDescriptor = AVOutputDeviceDescriptor

class UpdateOutputDeviceMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    OUTPUTDEVICES_FIELD_NUMBER: builtins.int
    ENDPOINTUID_FIELD_NUMBER: builtins.int
    CLUSTERAWAREOUTPUTDEVICES_FIELD_NUMBER: builtins.int
    @property
    def outputDevices(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___AVOutputDeviceDescriptor]: ...
    endpointUID: typing.Text
    @property
    def clusterAwareOutputDevices(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___AVOutputDeviceDescriptor]: ...
    def __init__(self,
        *,
        outputDevices: typing.Optional[typing.Iterable[global___AVOutputDeviceDescriptor]] = ...,
        endpointUID: typing.Optional[typing.Text] = ...,
        clusterAwareOutputDevices: typing.Optional[typing.Iterable[global___AVOutputDeviceDescriptor]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["endpointUID",b"endpointUID"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["clusterAwareOutputDevices",b"clusterAwareOutputDevices","endpointUID",b"endpointUID","outputDevices",b"outputDevices"]) -> None: ...
global___UpdateOutputDeviceMessage = UpdateOutputDeviceMessage

UPDATEOUTPUTDEVICEMESSAGE_FIELD_NUMBER: builtins.int
updateOutputDeviceMessage: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[pyatv.protocols.mrp.protobuf.ProtocolMessage_pb2.ProtocolMessage, global___UpdateOutputDeviceMessage]
