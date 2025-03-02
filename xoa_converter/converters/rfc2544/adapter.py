from __future__ import annotations
import hashlib
from typing import Union, TYPE_CHECKING
from .model import LegacyModel2544 as old_model
from ..common import convert_protocol_segments
import json

if TYPE_CHECKING:
    from .model import (
        LegacyBack2Back,
        LegacyLatency,
        LegacyLoss,
        LegacyRateIterationOptions,
        LegacyRateSweepOptions,
        LegacyPortEntity,
        LegacyThroughput,
    )


def convert_base_mac_address(mac_address: str) -> str:
    prefix = [hex(int(i)) for i in mac_address.split(",")]
    return "".join([p.replace("0x", "").zfill(2).upper() for p in prefix]).lower()


class Converter2544:
    def __init__(self, source_config: str) -> None:
        self.id_map = {}
        data = json.loads(source_config)
        self.data = old_model.model_validate(data)

    def __gen_frame_size(self) -> dict:
        packet_size = self.data.test_options.packet_sizes
        packet_size_type = packet_size.packet_size_type
        fz = packet_size.mixed_length_config.frame_sizes
        return dict(
            custom_packet_sizes=list(packet_size.custom_packet_sizes),
            fixed_packet_end_size=packet_size.sw_packet_end_size,
            fixed_packet_start_size=packet_size.sw_packet_start_size,
            fixed_packet_step_size=packet_size.sw_packet_step_size,
            mixed_length_config=fz,
            mixed_sizes_weights=packet_size.mixed_sizes_weights,
            packet_size_type=packet_size_type.name.lower(),
            varying_packet_max_size=packet_size.hw_packet_max_size,
            varying_packet_min_size=packet_size.hw_packet_min_size,
        )

    def __gen_multi_stream_config(self) -> dict:
        flow_option = self.data.test_options.flow_creation_options
        return dict(
            enable_multi_stream=flow_option.enable_multi_stream,
            multi_stream_address_offset=flow_option.multi_stream_address_offset,
            multi_stream_address_increment=flow_option.multi_stream_address_increment,
            multi_stream_mac_base_address=convert_base_mac_address(
                flow_option.multi_stream_mac_base_address
            ),
            per_port_stream_count=flow_option.per_port_stream_count,
        )

    def __gen_port_sync_config(self) -> dict:
        test_options = self.data.test_options
        return dict(
            delay_after_sync_on_second=test_options.sync_on_duration,
            sync_off_duration_second=test_options.sync_off_duration,
            toggle_port_sync=test_options.toggle_sync_state,
        )

    def __gen_topology_config(self) -> dict:
        topology = self.data.test_options.topology_config.topology.lower()
        direction = self.data.test_options.topology_config.direction.name.lower()
        return dict(direction=direction, topology=topology)

    def __gen_frame_size_config(self) -> dict:
        frame_size = self.__gen_frame_size()
        flow_option = self.data.test_options.flow_creation_options
        payload = self.data.test_options.payload_definition
        return dict(
            frame_sizes=frame_size,
            payload_pattern="".join(
                [
                    hex(int(i)).replace("0x", "").zfill(2)
                    for i in payload.payload_pattern.split(",")
                ]
            ),
            payload_type=payload.payload_type.lower(),
            use_micro_tpld_on_demand=flow_option.use_micro_tpld_on_demand,
        )

    def __gen_flow_creation_config(self):
        flow_option = self.data.test_options.flow_creation_options
        flow_creation_type = flow_option.flow_creation_type
        tid_allocation_scope = self.data.tid_allocation_scope
        return dict(
            flow_creation_type=flow_creation_type.name.lower(),
            mac_base_address=convert_base_mac_address(flow_option.mac_base_address),
            tid_allocation_scope=tid_allocation_scope.name.lower(),
        )

    def __gen_port_scheduling_config(self):
        test_options = self.data.test_options
        return dict(
            enable_speed_reduction_sweep=test_options.enable_speed_reduct_sweep,
            port_stagger_steps=test_options.port_stagger_steps,
            use_port_sync_start=test_options.use_port_sync_start,
        )

    def __gen_l23_learning_options(self):
        learning_options = self.data.test_options.learning_options
        flow_option = self.data.test_options.flow_creation_options
        return dict(
            arp_refresh_enabled=learning_options.arp_refresh_enabled,
            arp_refresh_period_second=learning_options.arp_refresh_period,
            learning_duration_second=learning_options.learning_duration,
            learning_rate_pct=learning_options.learning_rate_percent,
            use_gateway_mac_as_dmac=flow_option.use_gateway_mac_as_dmac,
        )

    def __gen_flow_based_learning_options(self):
        learning_options = self.data.test_options.learning_options
        return dict(
            delay_after_flow_based_learning_ms=learning_options.flow_based_learning_delay,
            flow_based_learning_frame_count=learning_options.flow_based_learning_frame_count,
            use_flow_based_learning_preamble=learning_options.use_flow_based_learning_preamble,
        )

    def __gen_mac_learning_options(self):
        learning_options = self.data.test_options.learning_options
        return dict(
            mac_learning_frame_count=learning_options.mac_learning_retries,
            mac_learning_mode=learning_options.mac_learning_mode.name.lower(),
            toggle_port_sync_config=self.__gen_port_sync_config(),
        )

    def __gen_test_execution_config(self):
        outer_loop_mode = self.data.test_options.outer_loop_mode
        return dict(
            flow_based_learning_options=self.__gen_flow_based_learning_options(),
            flow_creation_config=self.__gen_flow_creation_config(),
            l23_learning_options=self.__gen_l23_learning_options(),
            mac_learning_options=self.__gen_mac_learning_options(),
            outer_loop_mode=outer_loop_mode.name.lower(),
            port_scheduling_config=self.__gen_port_scheduling_config(),
            repeat_test_until_stopped=False,
            reset_error_handling=self.__gen_reset_error_handling(),
        )

    def __gen_reset_error_handling(self):
        test_options = self.data.test_options
        return dict(
            delay_after_port_reset_second=test_options.port_reset_delay,
            should_stop_on_los=test_options.should_stop_on_los,
        )

    def __gen_test_config(self):
        return dict(
            frame_size_config=self.__gen_frame_size_config(),
            multi_stream_config=self.__gen_multi_stream_config(),
            test_execution_config=self.__gen_test_execution_config(),
            topology_config=self.__gen_topology_config(),
        )

    def __gen_rate_sweep_option(self, rate_sweep_options: "LegacyRateSweepOptions"):
        return dict(
            end_value_pct=rate_sweep_options.end_value,
            start_value_pct=rate_sweep_options.start_value,
            step_value_pct=rate_sweep_options.step_value,
        )

    def __gen_common_option(
        self,
        test_type_conf: Union[
            "LegacyThroughput", "LegacyLatency", "LegacyLoss", "LegacyBack2Back"
        ],
    ):
        duration_type = test_type_conf.duration_type.name.lower()

        is_time_duration = test_type_conf.duration_type.value == "seconds"
        duration_unit = (
            test_type_conf.duration_time_unit.name.lower()
            if is_time_duration
            else test_type_conf.duration_frame_unit.name.lower().replace("field_", "")
        )
        duration = (
            test_type_conf.duration
            if is_time_duration
            else test_type_conf.duration_frames
        )
        return dict(
            duration=duration,
            duration_type=duration_type,
            duration_unit=duration_unit,
            repetition=test_type_conf.iterations,
        )

    # def __gen_common_option_back_to_back(
    #     self,
    #     test_type_conf: Union[
    #         "LegacyThroughput", "LegacyLatency", "LegacyLoss", "LegacyBack2Back"
    #     ],
    # ):
    #     return dict(repetition=test_type_conf.iterations)

    def __gen_rate_iteration_options(
        self, rate_iteration_options: "LegacyRateIterationOptions"
    ):
        return dict(
            initial_value_pct=rate_iteration_options.initial_value,
            maximum_value_pct=rate_iteration_options.maximum_value,
            minimum_value_pct=rate_iteration_options.minimum_value,
            result_scope=rate_iteration_options.result_scope.name.lower(),
            search_type=rate_iteration_options.search_type.name.lower(),
            value_resolution_pct=rate_iteration_options.value_resolution,
        )

    def __gen_throughput(self, throughput: "LegacyThroughput") -> dict:
        rate_iteration_options = throughput.rate_iteration_options
        return dict(
            acceptable_loss_pct=rate_iteration_options.acceptable_loss,
            common_options=self.__gen_common_option(throughput),
            collect_latency_jitter="LatencyCounters"
            in throughput.report_property_options,
            enabled=throughput.enabled,
            pass_criteria_throughput_pct=rate_iteration_options.pass_threshold,
            rate_iteration_options=self.__gen_rate_iteration_options(
                rate_iteration_options
            ),
            use_pass_criteria=rate_iteration_options.use_pass_threshold,
        )

    def __gen_latency(self, latency: "LegacyLatency") -> dict:
        return dict(
            common_options=self.__gen_common_option(latency),
            enabled=latency.enabled,
            latency_mode=latency.latency_mode.lower(),
            rate_sweep_options=self.__gen_rate_sweep_option(latency.rate_sweep_options),
            use_relative_to_throughput=latency.rate_relative_tput_max_rate,
        )

    def __gen_loss(self, loss: "LegacyLoss"):
        return dict(
            common_options=self.__gen_common_option(loss),
            enabled=loss.enabled,
            gap_monitor_start_microsec=loss.gap_monitor_start,
            gap_monitor_stop_frames=loss.gap_monitor_stop,
            pass_criteria_loss=loss.acceptable_loss,
            pass_criteria_loss_type=loss.acceptable_loss_type.lower(),
            rate_sweep_options=self.__gen_rate_sweep_option(loss.rate_sweep_options),
            use_gap_monitor=loss.use_gap_monitor,
            use_pass_criteria=loss.use_pass_fail_criteria,
        )

    def __gen_back_to_back(self, back_to_back: "LegacyBack2Back"):
        return dict(
            burst_size_iteration_options=dict(
                burst_resolution=back_to_back.burst_resolution,
                maximum_burst=back_to_back.duration_frames * back_to_back.duration_frame_unit.scale,
            ),
            common_options=self.__gen_common_option(back_to_back),
            enabled=back_to_back.enabled,
            rate_sweep_options=self.__gen_rate_sweep_option(
                back_to_back.rate_sweep_options
            ),
        )

    def __gen_test_type_config(self) -> dict:
        test_type_option_map = self.data.test_options.test_type_option_map
        return dict(
            back_to_back_test=self.__gen_back_to_back(test_type_option_map.back2_back),
            frame_loss_rate_test=self.__gen_loss(test_type_option_map.loss),
            latency_test=self.__gen_latency(test_type_option_map.latency),
            throughput_test=self.__gen_throughput(test_type_option_map.throughput),
        )

    def __gen_chassis_id_map(self) -> dict[str, str]:
        chassis_id_map = {}
        for chassis_info in self.data.chassis_manager.chassis_list:
            chassis_id = hashlib.md5(
                f"{chassis_info.host_name}:{chassis_info.port_number}".encode("utf-8")
            ).hexdigest()
            chassis_id_map[chassis_info.chassis_id] = chassis_id
        return chassis_id_map

    def __gen_port_identity(self) -> list[dict]:
        chassis_id_map = self.__gen_chassis_id_map()
        port_identity = []
        for count, p_info in enumerate(self.data.port_handler.entity_list):
            port = p_info.port_ref
            port.chassis_id = chassis_id_map[port.chassis_id]
            identity = dict(
                module_index=port.module_index,
                port_index=port.port_index,
                tester_id=port.chassis_id,
            )
            self.id_map[p_info.item_id] = (
                f"P-{identity['tester_id']}-{identity['module_index']}-{identity['port_index']}",
                count,
            )
            port_identity.append(identity)
        return port_identity

    def __gen_ipv4_addr(self, entity: "LegacyPortEntity"):
        return dict(
            address=entity.ip_v4_address,
            gateway=entity.ip_v4_gateway if entity.ip_v4_gateway else "0.0.0.0",
            public_address=entity.public_ip_address
            if entity.public_ip_address
            else "0.0.0.0",
            public_routing_prefix=entity.public_ip_routing_prefix,
            remote_loop_address=entity.remote_loop_ip_address
            if entity.remote_loop_ip_address
            else "0.0.0.0",
            routing_prefix=entity.ip_v4_routing_prefix,
        )

    def __gen_ipv6_addr(self, entity: "LegacyPortEntity"):
        return dict(
            address=entity.ip_v6_address,
            gateway=entity.ip_v6_gateway if entity.ip_v6_gateway else "::",
            public_address=entity.public_ip_address_v6
            if entity.public_ip_address_v6
            else "::",
            public_routing_prefix=entity.public_ip_routing_prefix_v6,
            remote_loop_address=entity.remote_loop_ip_address_v6
            if entity.remote_loop_ip_address_v6
            else "::",
            routing_prefix=entity.ip_v6_routing_prefix,
        )

    def __gen_port_conf(self, ip_v: str, profile_id: str, entity: "LegacyPortEntity"):
        ip_address = None
        if ip_v == "ipv4":
            ip_address = self.__gen_ipv4_addr(entity)
        elif ip_v == "ipv6":
            ip_address = self.__gen_ipv6_addr(entity)
        return dict(
            anlt_enabled=bool(entity.anlt_enabled),
            auto_neg_enabled=bool(entity.auto_neg_enabled),
            broadr_reach_mode=entity.brr_mode.lower(),
            fec_mode=entity.fec_mode.name.lower(),
            inter_frame_gap=entity.inter_frame_gap,
            ip_address=ip_address,
            ip_gateway_mac_address=entity.ip_gateway_mac_address,
            latency_offset_ms=entity.latency_offset,
            mdi_mdix_mode=entity.mdi_mdix_mode.lower(),
            peer_slot=self.id_map[entity.pair_peer_id][1]
            if entity.pair_peer_id and entity.pair_peer_id in self.id_map
            else None,
            pause_mode_enabled=entity.pause_mode_on,
            port_group=entity.port_group.lower(),
            port_slot=self.id_map[entity.item_id][1],
            port_speed_mode=entity.port_speed.lower(),
            port_rate_cap_enabled=bool(entity.enable_port_rate_cap),
            port_rate_cap_profile=entity.port_rate_cap_profile.name.lower(),
            port_rate_cap_value=entity.port_rate_cap_value,
            port_rate_cap_unit=entity.port_rate_cap_unit.name.lower().lstrip("field_"),
            protocol_segment_profile_id=profile_id,
            remote_loop_mac_address=entity.remote_loop_mac_address,
            reply_arp_requests=bool(entity.reply_arp_requests),
            reply_ping_requests=bool(entity.reply_ping_requests),
            speed_reduction_ppm=entity.adjust_ppm,
        )

    def __generate_port_config(self, protocol_names: dict) -> list[dict]:
        ip_version: list = []
        profile_ids: list = []
        port_conf: list = []
        for entity in self.data.port_handler.entity_list:
            profile_id = self.data.stream_profile_handler.profile_assignment_map.get(
                f"guid_{entity.item_id}"
            )
            profile_ids.append(profile_id)

            segment_types = protocol_names[profile_id]
            ipv4_index = segment_types.index("ipv4") if "ipv4" in segment_types else -1
            ipv6_index = segment_types.index("ipv6") if "ipv6" in segment_types else -1
            if ipv4_index == ipv6_index == -1:
                ip_version.append("none")
            elif ipv4_index > 0 and ipv6_index == -1:
                ip_version.append("ipv4")
            elif ipv6_index > 0 and ipv4_index == -1:
                ip_version.append("ipv6")
            elif ipv4_index > ipv6_index:
                ip_version.append("ipv6")
            elif ipv6_index > ipv4_index:
                ip_version.append("ipv4")

        for ip_v, profile_id, entity in zip(
            ip_version, profile_ids, self.data.port_handler.entity_list
        ):
            port_conf.append(self.__gen_port_conf(ip_v, profile_id, entity))
        return port_conf

    def gen(self) -> dict:
        # self.__gen_port_identity() also updates self.id_map, need to be called first
        port_identities = self.__gen_port_identity()
        protocol_segments = convert_protocol_segments(self.data.stream_profile_handler)
        protocol_names = {
            values["id"]: [i["type"] for i in values["segments"]]
            for values in protocol_segments
        }
        config = dict(
            ports_configuration=self.__generate_port_config(protocol_names),
            protocol_segments=protocol_segments,
            test_configuration=self.__gen_test_config(),
            test_types_configuration=self.__gen_test_type_config(),
        )
        return dict(config=config, port_identities=port_identities, username="Xena2544")
