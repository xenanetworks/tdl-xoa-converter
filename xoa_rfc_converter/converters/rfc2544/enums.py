from enum import Enum as CaseSensitiveEnum


class Enum(CaseSensitiveEnum):
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member


class LegacyDurationType(Enum):
    TIME = "seconds"
    FRAMES = "frames"

    @property
    def is_time_duration(self):
        return self == LegacyDurationType.TIME


class LegacyFecMode(Enum):
    ON = "on"
    OFF = "off"
    FC_FEC = "FIRECODE"


class LegacySearchType(Enum):
    BINARY_SEARCH = "binarysearch"
    FAST_BINARY_SEARCH = "fastbinarysearc"


class LegacyDurationTimeUnit(Enum):
    SECONDS = "Seconds"
    MINUTES = "Minutes"
    HOURS = "Hours"


class LegacyDurationFrameUnit(Enum):
    FRAMES = "frames"
    FIELD_10E3_FRAMES = "kframes"
    FIELD_10E6_FRAMES = "mframes"
    FIELD_10E9_FRAMES = "gframes"

    @property
    def scale(self) -> int:
        return {
            LegacyDurationFrameUnit.FRAMES: 1,
            LegacyDurationFrameUnit.FIELD_10E3_FRAMES: 1e3,
            LegacyDurationFrameUnit.FIELD_10E6_FRAMES: 1e6,
            LegacyDurationFrameUnit.FIELD_10E9_FRAMES: 1e9,
        }[self]


class LegacyTrafficDirection(Enum):
    EAST_TO_WEST = "east_west"
    WEST_TO_EAST = "west_east"
    BIDIRECTIONAL = "bidir"


class LegacyPacketSizeType(Enum):
    IETF_DEFAULT = "ieeedefault"
    CUSTOM_SIZES = "customsizes"
    SPECIFIED = "specified"
    INCREMENTING = "incrementing"
    BUTTERFLY = "butterfly"
    RANDOM = "random"
    MIXE_SIZES = "mixedsizes"


class LegacyModifierActionOption(Enum):
    INCREMENT = "inc"
    DECREMENT = "dec"
    RANDOM = "rnd"


class LegacyPortRateCapUnit(Enum):
    FIELD_1E9_BPS = "gbps"
    FIELD_1E6_BPS = "mbps"
    FIELD_1E3_BPS = "kbps"
    BPS = "bps"


class LegacyPortRateCapProfile(Enum):
    PHYSICAL_PORT_RATE = "Physical Port Rate"
    CUSTOM_RATE_CAP = "Custom Rate Cap"


class LegacyOuterLoopMode(Enum):
    ITERATIONS = "iterations"
    PACKET_SIZE = "packetsize"


class LegacyMACLearningMode(Enum):
    NEVER = "never"
    ONCE = "once"
    EVERY_TRIAL = "everytrial"


class LegacyFlowCreationType(Enum):
    STREAM_BASED = "streambased"
    MODIFIER_BASED = "modifierbased"


class LegacyTidAllocationScope(Enum):
    CONFIG_SCOPE = "configscope"
    PORT_SCOPE = "portscope"
    SOURCE_PORT_ID = "srcportid"


class LegacyRateResultScopeType(Enum):
    COMMON_RESULT = "commonresult"
    PER_SOURCE_PORT_RESULT = "persrcportresult"


class LegacyTestType(Enum):
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    LOSS = "loss"
    BACK_TO_BACK = "back2back"


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
    TCP_CHECK = "tcp_check"
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

    # @property
    # def core(self):
    #     return const.SegmentType[self.name]

    @property
    def is_raw(self) -> bool:
        return self.value.lower().startswith("raw")

    @property
    def raw_length(self) -> int:
        if not self.is_raw:
            return 0
        return int(self.value.split("_")[-1])
