import base64
from decimal import Decimal
from typing import  List, Dict, Optional
from pydantic import BaseModel, Field, validator
from .const import (
    BRRModeStr,
    LatencyMode,
    LearningPortDMacMode,
    LearningSequencePortDMacMode,
    LegacyDurationType,
    LegacyModifierActionOption,
    LegacyPortRateCapProfile,
    LegacyPortRateCapUnit,
    LegacySegmentType,
    LegacyTidAllocationScope,
    LegacyTestType,
    LegacyStreamRateType,
    LegacyDurationFrameUnit,
    LegacyTrafficDirection,
    PortGroup,
    TestPortMacMode,
    LegacyFlowCreationType,
    LegacyPacketSizeType,
    DurationTimeUnit,
    TestTopology,
    LegacyFecMode,
)


class NewRateSweepOptions(BaseModel):
    start_value: Decimal
    end_value: Decimal
    step_value: Decimal

    @validator("start_value", "end_value", "step_value")
    def to_decimal(cls, v):
        return Decimal(v)

class PortRoleConfig(BaseModel):
    is_used: bool = Field(alias="IsUsed")
    role: PortGroup = Field(alias="Role")
    peer_port_id: str = Field(alias="PeerPortId")

    @validator("role", pre=True)
    def _flexible_role(cls, v):
        if v == "TestPort":
            return PortGroup.TEST_PORT
        elif v == "LearningPort":
            return PortGroup.LEARNING_PORT
        elif v == "MonitoringPort":
            return PortGroup.MONITORING_PORT
        else:
            return v

class LegacyPortRoleHandler(BaseModel):
    role_map: Dict[str, PortRoleConfig] = Field(alias="RoleMap")

class LegacyRateIterationOptions(BaseModel):
    initial_value: float = Field(alias="InitialValue")
    minimum_value: float = Field(alias="MinimumValue")
    maximum_value: float = Field(alias="MaximumValue")
    value_resolution: float = Field(alias="ValueResolution")
    use_pass_threshold: bool = Field(alias="UsePassThreshold")
    pass_threshold: float = Field(alias="PassThreshold")


class LegacyTestCaseBaseConfiguration(BaseModel):
    type: Optional[str] = Field(alias="$type")
    test_type: LegacyTestType = Field(alias="TestType")
    enabled: bool = Field(alias="Enabled")
    duration_type: LegacyDurationType = Field(alias="DurationType")
    duration: float = Field(alias="Duration")
    duration_time_unit: DurationTimeUnit = Field(alias="DurationTimeUnit")
    duration_frames: int = Field(alias="DurationFrames")
    duration_frame_unit: LegacyDurationFrameUnit = Field(alias="DurationFrameUnit")
    iterations: int = Field(alias="Iterations")
    item_id: str = Field(alias="ItemID")
    parent_id: str = Field(alias="ParentID")
    label: str = Field(alias="Label")


class LegacyRateSweepOptions(BaseModel):
    start_value: float = Field(alias="StartValue")
    end_value: float = Field(alias="EndValue")
    step_value: float = Field(alias="StepValue")


class LegacyRateSubTest(LegacyTestCaseBaseConfiguration):
    topology: TestTopology = Field(alias="Topology")
    direction: LegacyTrafficDirection = Field(alias="Direction")
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    throughput_test_enabled: bool = Field(alias="ThroughputTestEnabled")
    rate_iteration_options: LegacyRateIterationOptions = Field(alias="RateIterationOptions")
    forwarding_test_enabled: bool = Field(alias="ForwardingTestEnabled")
    rate_sweep_options: LegacyRateSweepOptions = Field(alias="RateSweepOptions")


class RateSubTestHandler(BaseModel):
    rate_sub_tests: List[LegacyRateSubTest] = Field(alias="RateSubTests")


class LegacyRateTest(LegacyTestCaseBaseConfiguration):
    rate_sub_test_handler: RateSubTestHandler = Field(alias="RateSubTestHandler")


class LegacyCongestionControl(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")


class LegacyForwardPressure(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    interframe_gap_delta: int = Field(alias="InterFrameGapDelta")
    acceptable_rx_max_util_delta: float = Field(alias="AcceptableRxMaxUtilDelta")


class LegacyMaxForwardingRate(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    use_throughput_as_start_value: bool = Field(alias="UseThroughputAsStartValue")
    rate_sweep_options: LegacyRateSweepOptions = Field(alias="RateSweepOptions")


class LegacyAddressIterationOptions(BaseModel):
    initial_value: float = Field(alias="InitialValue")
    minimum_value: float = Field(alias="MinimumValue")
    maximum_value: float = Field(alias="MaximumValue")
    value_resolution: float = Field(alias="ValueResolution")
    use_pass_threshold: bool = Field(alias="UsePassThreshold")
    pass_threshold: float = Field(alias="PassThreshold")


class LegacyAddressCachingCapacity(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    rate_sweep_options: LegacyRateSweepOptions = Field(alias="RateSweepOptions")
    address_iteration_options: LegacyRateIterationOptions = Field(alias="AddressIterationOptions")
    learn_mac_base_address: str = Field(alias='LearnMacBaseAddress')
    test_port_mac_mode: TestPortMacMode = Field(alias='TestPortMacMode')
    learning_port_dmac_mode: LearningPortDMacMode = Field(alias='LearningPortDMacMode')
    learning_sequence_port_dmac_mode: LearningSequencePortDMacMode = Field(alias='LearningSequencePortDMacMode')
    learning_rate_fps: float = Field(alias='LearningRateFps')
    toggle_sync_state: bool = Field(alias='ToggleSyncState')
    sync_off_duration: int = Field(alias='SyncOffDuration')
    sync_on_duration: int = Field(alias='SyncOnDuration')
    switch_test_port_roles: bool = Field(alias='SwitchTestPortRoles')
    dut_aging_time: int = Field(alias='DutAgingTime')
    fast_run_resolution_enabled: bool = Field(alias='FastRunResolutionEnabled')


class LegacyAddressLearningRate(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    address_sweep_options: LegacyRateSweepOptions = Field(alias="AddressSweepOptions")
    rate_iteration_options: LegacyRateIterationOptions = Field(alias="RateIterationOptions")
    learn_mac_base_address: str = Field(alias='LearnMacBaseAddress')
    test_port_mac_mode: TestPortMacMode = Field(alias='TestPortMacMode')
    learning_port_dmac_mode: LearningPortDMacMode = Field(alias='LearningPortDMacMode')
    learning_sequence_port_dmac_mode: LearningSequencePortDMacMode = Field(alias='LearningSequencePortDMacMode')
    learning_rate_fps: float = Field(alias='LearningRateFps')
    toggle_sync_state: bool = Field(alias='ToggleSyncState')
    sync_off_duration: int = Field(alias='SyncOffDuration')
    sync_on_duration: int = Field(alias='SyncOnDuration')
    switch_test_port_roles: bool = Field(alias='SwitchTestPortRoles')
    dut_aging_time: int = Field(alias='DutAgingTime')
    only_use_capacity: bool = Field(alias='OnlyUseCapacity')
    set_end_address_to_capacity: bool = Field(alias='SetEndAddressToCapacity')


class LegacyErroredFramesFiltering(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    rate_sweep_options: LegacyRateSweepOptions = Field(alias="RateSweepOptions")
    oversize_test_enabled: bool = Field(alias='OversizeTestEnabled')
    max_frame_size: int = Field(alias='MaxFrameSize')
    oversize_span: int = Field(alias='OversizeSpan')
    min_frame_size: int = Field(alias='MinFrameSize')
    undersize_span: int = Field(alias='UndersizeSpan')


class LegacyBroadcastForwarding(LegacyTestCaseBaseConfiguration):
    port_role_handler: LegacyPortRoleHandler = Field(alias="PortRoleHandler")
    rate_iteration_options: LegacyRateIterationOptions = Field(alias="RateIterationOptions")


class TestTypeOptionMap(BaseModel):
    rate_test: LegacyRateTest = Field(alias="RateTest")
    congestion_control: LegacyCongestionControl = Field(alias="CongestionControl")
    forward_pressure: LegacyForwardPressure = Field(alias="ForwardPressure")
    max_forwarding_rate: LegacyMaxForwardingRate = Field(alias="MaxForwardingRate")
    address_caching_capacity: LegacyAddressCachingCapacity = Field(alias="AddressCachingCapacity")
    address_learning_rate: LegacyAddressLearningRate = Field(alias="AddressLearningRate")
    errored_frames_filtering: LegacyErroredFramesFiltering = Field(alias="ErroredFramesFiltering")
    broadcast_forwarding: LegacyBroadcastForwarding = Field(alias="BroadcastForwarding")


class LegacyRateDefinition(BaseModel):
    rate_type: LegacyStreamRateType = Field(alias="RateType")
    rate_fraction: float = Field(alias="RateFraction")
    rate_pps: float = Field(alias="RatePps")
    rate_bps_l1: float = Field(alias="RateBpsL1")
    rate_bps_l1_unit: LegacyPortRateCapUnit = Field(alias="RateBpsL2Unit")
    rate_bps_l2: float = Field(alias="RateBpsL1")
    rate_bps_l2_unit: LegacyPortRateCapUnit = Field(alias="RateBpsL2Unit")


class FlowCreationOptions(BaseModel):
    flow_creation_type: LegacyFlowCreationType = Field(alias="FlowCreationType")
    mac_base_address: str = Field(alias="MacBaseAddress")
    use_gateway_mac_as_dmac: bool = Field(alias="UseGatewayMacAsDmac")
    enable_multi_stream: bool = Field(alias="EnableMultiStream")
    per_port_stream_count: int = Field(alias="PerPortStreamCount")
    multi_stream_address_offset: int = Field(alias="MultiStreamAddressOffset")
    multi_stream_address_increment: int = Field(alias="MultiStreamAddressIncrement")
    multi_stream_mac_base_address: str = Field(alias="MultiStreamMacBaseAddress")
    use_micro_tpld_on_demand: bool = Field(alias="UseMicroTpldOnDemand")


class MixedLengthConfig(BaseModel):
    frame_sizes: Dict = Field(alias="FrameSizes")


class PacketSizes(BaseModel):
    packet_size_type: LegacyPacketSizeType = Field(alias="PacketSizeType")
    custom_packet_sizes: List = Field(alias="CustomPacketSizes")
    sw_packet_start_size: int = Field(alias="SwPacketStartSize")
    sw_packet_end_size: int = Field(alias="SwPacketEndSize")
    sw_packet_step_size: int = Field(alias="SwPacketStepSize")
    hw_packet_min_size: int = Field(alias="HwPacketMinSize")
    hw_packet_max_size: int = Field(alias="HwPacketMaxSize")
    mixed_sizes_weights: List = Field(alias="MixedSizesWeights")
    mixed_length_config: MixedLengthConfig = Field(alias="MixedLengthConfig")


class TestOptions(BaseModel):
    test_type_option_map: TestTypeOptionMap = Field(alias="TestTypeOptionMap")
    packet_sizes: PacketSizes = Field(alias="PacketSizes")
    rate_definition: LegacyRateDefinition = Field(alias="RateDefinition")
    flow_creation_options: FlowCreationOptions = Field(alias="FlowCreationOptions")
    latency_mode: LatencyMode = Field(alias="LatencyMode")
    toggle_sync_state: bool = Field(alias="ToggleSyncState")
    sync_off_duration: int = Field(alias="SyncOffDuration")
    sync_on_duration: int = Field(alias="SyncOnDuration")
    should_stop_on_los: bool = Field(alias="ShouldStopOnLos")
    port_reset_delay: int = Field(alias="PortResetDelay")
    use_port_sync_start: bool = Field(alias="UsePortSyncStart")
    port_stagger_steps: int = Field(alias="PortStaggerSteps")


class LegacyFrameSizesOptions(BaseModel):
    field_0: int = Field(56, alias="0")
    field_1: int = Field(60, alias="1")
    field_14: int = Field(9216, alias="14")
    field_15: int = Field(16360, alias="15")


class ChassisList(BaseModel):
    chassis_id: str = Field(alias="ChassisID")
    host_name: str = Field(alias="HostName")
    port_number: int = Field(alias="PortNumber")
    password: str = Field(alias="Password")
    connection_type: str = Field(alias="ConnectionType")
    used_module_list: List = Field(alias="UsedModuleList")
    resource_index: int = Field(alias="ResourceIndex")
    resource_used: bool = Field(alias="ResourceUsed")
    child_resource_used: bool = Field(alias="ChildResourceUsed")


class ChassisManager(BaseModel):
    chassis_list: List[ChassisList] = Field(alias="ChassisList")


class PortRef(BaseModel):
    chassis_id: str = Field(alias="ChassisId")
    module_index: int = Field(alias="ModuleIndex")
    port_index: int = Field(alias="PortIndex")


class LegacyPortEntity(BaseModel):
    port_ref: PortRef = Field(alias="PortRef")
    port_group: PortGroup = Field(alias="PortGroup")
    pair_peer_ref: None = Field(alias="PairPeerRef")
    pair_peer_id: str = Field(alias="PairPeerId")
    multicast_role: str = Field(alias="MulticastRole")
    port_speed: str = Field(alias="PortSpeed")
    inter_frame_gap: int = Field(alias="InterFrameGap")
    pause_mode_on: int = Field(alias="PauseModeOn")
    auto_neg_enabled: int = Field(alias="AutoNegEnabled")
    anlt_enabled: int = Field(alias="AnltEnabled")
    adjust_ppm: int = Field(alias="AdjustPpm")
    latency_offset: int = Field(alias="LatencyOffset")
    mdi_mdix_mode: str = Field(alias="MdiMdixMode")
    fec_mode: LegacyFecMode = Field(alias="FecMode")
    brr_mode: BRRModeStr = Field(alias="BrrMode")
    reply_arp_requests: int = Field(alias="ReplyArpRequests")
    reply_ping_requests: int = Field(alias="ReplyPingRequests")
    ip_v4_address: str = Field(alias="IpV4Address")
    ip_v4_routing_prefix: int = Field(alias="IpV4RoutingPrefix")
    ip_v4_gateway: str = Field(alias="IpV4Gateway")
    ip_v6_address: str = Field(alias="IpV6Address")
    ip_v6_routing_prefix: int = Field(alias="IpV6RoutingPrefix")
    ip_v6_gateway: str = Field(alias="IpV6Gateway")
    ip_gateway_mac_address: str = Field(alias="IpGatewayMacAddress")
    public_ip_address: str = Field(alias="PublicIpAddress")
    public_ip_routing_prefix: int = Field(alias="PublicIpRoutingPrefix")
    public_ip_address_v6: str = Field(alias="PublicIpAddressV6")
    public_ip_routing_prefix_v6: int = Field(alias="PublicIpRoutingPrefixV6")
    remote_loop_ip_address: str = Field(alias="RemoteLoopIpAddress")
    remote_loop_ip_address_v6: str = Field(alias="RemoteLoopIpAddressV6")
    remote_loop_mac_address: str = Field(alias="RemoteLoopMacAddress")
    enable_port_rate_cap: int = Field(alias="EnablePortRateCap")
    port_rate_cap_value: float = Field(alias="PortRateCapValue")
    port_rate_cap_profile: LegacyPortRateCapProfile = Field(alias="PortRateCapProfile")
    port_rate_cap_unit: LegacyPortRateCapUnit = Field(alias="PortRateCapUnit")
    multi_stream_map: None = Field(alias="MultiStreamMap")
    item_id: str = Field(alias="ItemID")
    parent_id: str = Field(alias="ParentID")
    label: str = Field(alias="Label")

    @validator("remote_loop_mac_address", "ip_gateway_mac_address")
    def decode_mac_address(cls, v):
        v = base64.b64decode(v)
        v = "".join([hex(int(i)).replace("0x", "").zfill(2) for i in bytearray(v)])
        return v


class PortHandler(BaseModel):
    entity_list: List[LegacyPortEntity] = Field(alias="EntityList")


class HwModifiers(BaseModel):
    offset: int = Field(alias="Offset")
    mask: str = Field(alias="Mask")
    action: LegacyModifierActionOption = Field(alias="Action")
    start_value: int = Field(alias="StartValue")
    stop_value: int = Field(alias="StopValue")
    step_value: int = Field(alias="StepValue")
    repeat_count: int = Field(alias="RepeatCount")
    segment_id: str = Field(alias="SegmentId")
    field_name: str = Field(alias="FieldName")

    @validator("mask")
    def decode_segment_value(cls, v):
        v = base64.b64decode(v)
        v = "".join([hex(int(i)).replace("0x", "").zfill(2) for i in bytearray(v)])
        return v


class FieldValueRanges(BaseModel):
    start_value: int = Field(alias="StartValue")
    stop_value: int = Field(alias="StopValue")
    step_value: int = Field(alias="StepValue")
    action: LegacyModifierActionOption = Field(alias="Action")
    reset_for_each_port: bool = Field(alias="ResetForEachPort")
    segment_id: str = Field(alias="SegmentId")
    field_name: str = Field(alias="FieldName")


class HeaderSegments(BaseModel):
    segment_value: str = Field(alias="SegmentValue")
    segment_type: LegacySegmentType = Field(alias="SegmentType")
    item_id: str = Field(alias="ItemID")
    parent_id: str = Field(alias="ParentID")
    label: str = Field(alias="Label")

    @validator("segment_type", pre=True, always=True)
    def validate_segment_type(cls, v, values):
        if isinstance(v, str):
            if v.lower().startswith("raw"):
                return LegacySegmentType(f"raw_{len(values['segment_value']) // 2}")
            else:
                return LegacySegmentType(v)
        else:
            return v

class StreamConfig(BaseModel):
    sw_modifier: None = Field(alias="SwModifier")
    hw_modifiers: List[HwModifiers] = Field(alias="HwModifiers")
    field_value_ranges: List[FieldValueRanges] = Field(alias="FieldValueRanges")
    stream_descr_prefix: str = Field(alias="StreamDescrPrefix")
    resource_index: int = Field(alias="ResourceIndex")
    tpld_id: int = Field(alias="TpldId")
    enable_state: str = Field(alias="EnableState")
    rate_type: str = Field(alias="RateType")
    packet_limit: int = Field(alias="PacketLimit")
    rate_fraction: float = Field(alias="RateFraction")
    rate_pps: float = Field(alias="RatePps")
    rate_l2_mbps: float = Field(alias="RateL2Mbps")
    use_burst_values: bool = Field(alias="UseBurstValues")
    burst_size: int = Field(alias="BurstSize")
    burst_density: int = Field(alias="BurstDensity")
    header_segments: List[HeaderSegments] = Field(alias="HeaderSegments")
    packet_length_type: str = Field(alias="PacketLengthType")
    packet_min_size: int = Field(alias="PacketMinSize")
    packet_max_size: int = Field(alias="PacketMaxSize")
    resource_used: bool = Field(alias="ResourceUsed")
    child_resource_used: bool = Field(alias="ChildResourceUsed")


class SteamEntity(BaseModel):
    stream_config: StreamConfig = Field(alias="StreamConfig")
    item_id: str = Field(alias="ItemID")
    parent_id: str = Field(alias="ParentID")
    label: str = Field(alias="Label")


class LegacyStreamProfileHandler(BaseModel):
    profile_assignment_map: Dict = Field(alias="ProfileAssignmentMap")
    entity_list: List[SteamEntity] = Field(alias="EntityList")


class ValkyrieConfiguration2889(BaseModel):
    """represent '.v2889' configuration file"""

    port_handler: PortHandler = Field(alias="PortHandler")
    stream_profile_handler: LegacyStreamProfileHandler = Field(alias="StreamProfileHandler")
    test_options: TestOptions = Field(alias="TestOptions")
    creation_date: str = Field(alias="CreationDate")
    chassis_manager: ChassisManager = Field(alias="ChassisManager")
    tid_allocation_scope: LegacyTidAllocationScope = Field(alias="TidAllocationScope")
    format_version: int = Field(alias="FormatVersion")
    application_version: str = Field(alias="ApplicationVersion")
