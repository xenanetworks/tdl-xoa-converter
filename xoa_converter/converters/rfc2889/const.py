from enum import Enum as CaseSensitiveEnum
from xoa_driver.enums import (
    BRRMode,
)


class Enum(CaseSensitiveEnum):
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member


class LegacyDurationType(Enum):
    TIME = "seconds"
    FRAME = "frames"


class DurationTimeUnit(Enum):
    SECOND = "seconds"
    MINUTE = "minutes"
    HOUR = "hours"
    DAY = "days"


class LegacyDurationFrameUnit(Enum):
    FRAME = "frames"
    K_FRAME = "Kframes"
    M_FRAME = "Mframes"
    G_FRAME = "Gframes"


class LegacyTrafficDirection(Enum):
    EAST_TO_WEST = "east_west"
    WEST_TO_EAST = "west_east"
    BIDIR = "bidir"


class LegacyModifierActionOption(Enum):
    INC = "inc"
    DEC = "dec"
    RANDOM = "rnd"


class LegacyPortRateCapUnit(Enum):
    FIELD_1E9_BPS = "gbps"
    FIELD_1E6_BPS = "mbps"
    FIELD_1E3_BPS = "kbps"
    BPS = "bps"


class LegacyPortRateCapProfile(Enum):
    PHYSICAL_PORT_RATE = "Physical Port Rate"
    CUSTOM = "Custom Rate Cap"


class LegacyOuterLoopMode(Enum):
    ITERATION = "iterations"
    PACKET_SIZE = "packetsize"


class LegacyMACLearningMode(Enum):
    NEVER = "never"
    ONCE = "once"
    EVERYTRIAL = "everytrial"


class LegacyFlowCreationType(Enum):
    STREAM = "streambased"
    MODIFIER = "modifierbased"


class LegacyTidAllocationScope(Enum):
    CONFIGURATION_SCOPE = "configscope"
    RX_PORT_SCOPE = "portscope"
    SOURCE_PORT_ID = "srcportid"


class LegacyRateResultScopeType(Enum):
    COMMON = "commonresult"
    PER_SOURCE_PORT = "persrcportresult"


class LegacyTestType(Enum):
    RATE_TEST = "RateTest"
    CONGESTION_CONTROL = "CongestionControl"
    FORWARD_PRESSURE = "ForwardPressure"
    MAX_FORWARDING_RATE = "MaxForwardingRate"
    ADDRESS_CACHING_CAPACITY = "AddressCachingCapacity"
    ADDRESS_LEARNING_RATE = "AddressLearningRate"
    ERRORED_FRAMES_FILTERING = "ErroredFramesFiltering"
    BROADCAST_FORWARDING = "BroadcastForwarding"


class LegacySegmentType(Enum):
    ETHERNET = "ethernet"
    VLAN = "vlan"
    ARP = "arp"
    IPV4 = "ip"
    IPV6 = "ipv6"
    UDP = "udp"
    TCP = "tcp"
    LLC = "llc"
    SNAP = "snap"
    GTP = "gtp"
    ICMP = "icmp"
    # ICMPV6 = "icmpv6"
    RTP = "rtp"
    RTCP = "rtcp"
    STP = "stp"
    SCTP = "sctp"  # added
    MACCTRL = "macctrl"
    MPLS = "mpls"
    PBBTAG = "pbbtag"
    FCOE = "fcoe"  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    FC = "fc"
    # FCOEHEAD = "fcoehead"  # added
    FCOETAIL = "fcoetail"
    IGMPV3L0 = "igmpv3l0"
    IGMPV3L1 = "igmpv3l1"
    # IGMPV3GR = "igmpv3gr"
    # IGMPV3MR = "igmpv3mr"
    # MLDV2AR = "mldv2ar"
    UDPCHECK = "udpcheck"
    IGMPV2 = "igmpv2"
    # "MPLS_TP_OAM"
    GRE_NOCHECK = "gre_nocheck"
    GRE_CHECK = "gre_check"
    TCPCHECK = "tcp_check"
    # "GTPV1L0"
    # "GTPV1L1"
    # "GTPV2L0"
    # "GTPV2L1"
    IGMPV1 = "igmpv1"
    # "PWETHCTRL"
    VXLAN = "vxlan"
    # "ETHERNET_8023"
    NVGRE = "nvgre"

    _ignore_ = "OSegmentType i"
    OSegmentType = vars()
    for i in range(1, 65):
        OSegmentType[f"RAW_{i}"] = f"raw_{i}"  # type: ignore

    @property
    def is_raw(self) -> bool:
        return self.value.lower().startswith("raw")

    @property
    def raw_length(self) -> int:
        if not self.is_raw:
            return 0
        return int(self.value.split("_")[-1])


class LegacyStreamRateType(Enum):
    FRACTION = "fraction"
    PPS = "pps"
    L1BPS = "l1bps"
    L2BPS = "l2bps"


class TestPortMacMode(Enum):
    USE_PORT_NATIVE_MAC = "UsePortNativeMac"
    USE_LEARNING_MAC_BASE_ADDRESS = "UseLearnMacBaseAddress"

    @property
    def is_use_learning_base_address(self):
        return self == TestPortMacMode.USE_LEARNING_MAC_BASE_ADDRESS


class LearningPortDMacMode(Enum):
    USE_TEST_PORT_MAC = "UseTestPortMac"
    USE_BROADCAST = "UseBroadcast"

    @property
    def is_use_broadcast(self):
        return self == LearningPortDMacMode.USE_BROADCAST


class LearningSequencePortDMacMode(Enum):
    USE_INCREMENTING_MAC_ADDRESSES = "UseIncrementingMacAddresses"
    USE_RANDOM_MAC_ADDRESSES = "UseRandomMacAddresses"

    @property
    def is_incr(self):
        return self == LearningSequencePortDMacMode.USE_INCREMENTING_MAC_ADDRESSES

    @property
    def is_random(self):
        return self == LearningSequencePortDMacMode.USE_RANDOM_MAC_ADDRESSES


class LegacyPacketSizeType(Enum):
    IETF_DEFAULT = "ieeedefault"
    CUSTOM_SIZES = "customsizes"
    RANGE = "specified"
    INCREMENTING = "incrementing"
    BUTTERFLY = "butterfly"
    RANDOM = "random"
    MIX = "mixedsizes"


class BRRModeStr(Enum):
    MASTER = "master"
    SLAVE = "slave"

    def to_xmp(self) -> "BRRMode":
        return BRRMode[self.name]


class PortProtocolVersion(Enum):
    ETHERNET = 0
    IPV4 = 4
    IPV6 = 6

    @property
    def is_ipv4(self) -> bool:
        return self == type(self).IPV4

    @property
    def is_ipv6(self) -> bool:
        return self == type(self).IPV6

    @property
    def is_l3(self) -> bool:
        return self != type(self).ETHERNET


class IPVersion(Enum):
    IPV4 = 4
    IPV6 = 6


class DurationType(Enum):
    TIME = "time"
    FRAME = "frames"

    @property
    def is_time_duration(self) -> bool:
        return self == type(self).TIME


class MACLearningMode(Enum):
    NEVER = "never"
    ONCE = "once"
    EVERYTRIAL = "every_trial"


class FlowCreationType(Enum):
    STREAM = "stream_based"
    MODIFIER = "modifier_based"

    @property
    def is_stream_based(self):
        return self == FlowCreationType.STREAM


class PortRateCapProfile(Enum):
    PHYSICAL = "physical_port_rate"
    CUSTOM = "custom_rate_cap"

    @property
    def is_custom(self) -> bool:
        return self == PortRateCapProfile.CUSTOM


class DurationFrameUnit(Enum):
    FRAME = "frames"
    K_FRAME = "10e3_frames"
    M_FRAME = "10e6_frames"
    G_FRAME = "10e9_frames"

    @property
    def scale(self) -> int:
        if self == type(self).FRAME:
            return 1
        elif self == type(self).K_FRAME:
            return 1_000
        elif self == type(self).M_FRAME:
            return 1_000_000
        elif self == type(self).G_FRAME:
            return 1_000_000_000
        raise ValueError("No scale!")


class PortGroup(Enum):
    EAST = "east"
    WEST = "west"
    UNDEFINED = "undefined"
    SOURCE = "source"
    DESTINATION = "destination"
    TEST_PORT = "test_port"
    LEARNING_PORT = "learning_port"
    MONITORING_PORT = "monitoring_port"

    @property
    def is_east(self):
        return self == PortGroup.EAST

    @property
    def is_west(self):
        return self == PortGroup.WEST


class TestTopology(Enum):
    PAIRS = "pairs"
    BLOCKS = "blocks"
    MESH = "mesh"

    @property
    def is_mesh_topology(self) -> bool:
        return self == type(self).MESH

    @property
    def is_pair_topology(self) -> bool:
        return self == type(self).PAIRS


class LegacyFecMode(Enum):
    ON = "on"
    OFF = "off"
    FC_FEC = "FIRECODE"


class LatencyMode(Enum):
    FIRST2LAST = "First_To_Last"
    LAST2LAST = "Last_To_Last"
    FIRST2FIRST = "First_To_First"
    LAST2FIRST = "Last_To_First"