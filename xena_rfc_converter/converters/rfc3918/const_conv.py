import os
import re


DEFAULT_SEGMENT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "reference/segment_refs",
    )
)


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def convert_multicast_role(string: str) -> str:
    return camel_to_snake(string)


def convert_test_topology(string: str) -> str:
    return string.lower()


def convert_traffic_direction(string: str) -> str:
    return string.lower()


def convert_igmp_version(string: str) -> str:
    return {
        "IGMP_V1": "igmp_v1",
        "IGMP_V2": "igmp_v2_or_mld_v1",
        "IGMP_V3": "igmp_v3_or_mld_v2",
    }.get(string, string)


def convert_display_unit(string: str) -> str:
    return string.lower()


def convert_protocol_option(string: str) -> str:
    return {
        "FCOEHEAD": "fcoe",
        "IP": "ipv4",
        "TCPCHECK": "tcp_check",
    }.get(string, string.lower())


def convert_port_rate_cap_profile(string: str) -> str:
    return string.replace(" ", "_").lower()


def convert_rate_type(string: str) -> str:
    return string.lower()


def convert_port_rate_cap_unit(string: str) -> str:
    return {
        "Gbps": "1e9_bps",
        "Mbps": "1e6_bps",
        "Kbps": "1e3_bps",
        "bps": "bps",
    }.get(string, string)


def convert_flow_creation_type(string: str) -> str:
    return camel_to_snake(string)


def convert_latency_mode(string: str) -> str:
    return string.lower()


def convert_tid_allocation_scope(string: str) -> str:
    return camel_to_snake(string)


def convert_mdi_mdix_mode(string: str) -> str:
    return string.lower()


def convert_brr_mode(string: str) -> str:
    return string.lower()


def convert_packet_size_type(string: str) -> str:
    return camel_to_snake(string)


def convert_payload_type(string: str) -> str:
    return string.lower()


def convert_base_mac_address(mac_address: str):
    return "".join(
        [hex(int(i)).replace("0x", "").zfill(2).upper() for i in mac_address.split(",")]
    )


MIXED_DEFAULT_WEIGHTS = [0, 0, 0, 0, 57, 3, 5, 1, 2, 5, 1, 4, 4, 18, 0, 0]
