from __future__ import annotations
import base64
import hashlib
from typing import Any, Optional
from .const_conv import (
    convert_protocol_option,
    convert_multicast_role,
    convert_brr_mode,
    convert_igmp_version,
    convert_mdi_mdix_mode,
    convert_payload_type,
    convert_port_rate_cap_profile,
    convert_port_rate_cap_unit,
    convert_rate_type,
    convert_test_topology,
    convert_traffic_direction,
    convert_flow_creation_type,
    convert_latency_mode,
    convert_base_mac_address,
    convert_display_unit,
    convert_tid_allocation_scope,
    convert_packet_size_type,
    MIXED_DEFAULT_WEIGHTS,
)
from .field import MacAddress
from .legacy import LegacyModel3918, LegacyPortEntity
import json

class Converter3918:
    def __init__(self, source_config: str) -> None:
        data = json.loads(source_config)
        self.data = LegacyModel3918.model_validate(data)

    def __gen_profile(self) -> dict:
        stream_profile_handler = self.data.legacy_stream_profile_handler
        protocol_segments_profile = {}

        for profile in stream_profile_handler.legacy_entity_list:
            header_segments = []
            for hs in profile.legacy_stream_config.legacy_header_segments:
                bytess = bytearray(base64.b64decode(hs.legacy_segment_value))
                lsv = [hex(int(i)).replace("0x", "").zfill(2) for i in bytess]
                dic = dict(
                    segment_value="".join(lsv),
                    type=convert_protocol_option(hs.legacy_segment_type),
                )
                header_segments.append(dic)

                cfg = profile.legacy_stream_config
                lpd = cfg.legacy_payload_definition
                sp = lpd.legacy_payload_pattern.split(",")
                lpt_list = [hex(int(i)).replace("0x", "").zfill(2) for i in sp]
                payload_pattern = "".join(lpt_list)

                lrt = cfg.legacy_rate_type
                rate_type = convert_rate_type(lrt)

                rate_fraction = cfg.legacy_rate_fraction

                protocol_segments_profile[profile.legacy_item_id] = dict(
                    header_segments=header_segments,
                    payload_pattern=payload_pattern,
                    payload_type=convert_payload_type(lpd.legacy_payload_type),
                    rate_fraction=rate_fraction,
                    rate_pps=cfg.legacy_rate_pps,
                    rate_type=rate_type,
                )
        return protocol_segments_profile

    def __gen_port_identity(
        self, chassis_id_map: dict[str, dict[str, Any]]
    ) -> list[dict]:
        port_identities = []
        for count, p_info in enumerate(
            self.data.legacy_port_handler.legacy_entity_list
        ):
            lpr = p_info.legacy_port_ref
            lci = chassis_id_map[lpr.legacy_chassis_id]
            port_identity = dict(
                port_index=lpr.legacy_port_index,
                module_index=lpr.legacy_module_index,
                tester_id=lci["id"],
            )
            port_identities.append(port_identity)

        return port_identities

    def __gen_chassis_id_map(self) -> dict[str, dict[str, Any]]:
        result = {}
        lcl = self.data.legacy_chassis_manager.legacy_chassis_list
        for index, chassis_info in enumerate(lcl):
            host = chassis_info.legacy_host_name
            port = chassis_info.legacy_port_number
            name = f"{host}:{port}"
            ident = hashlib.md5(name.encode("utf-8")).hexdigest()
            dic = dict(id=ident, index=index)
            result[chassis_info.legacy_chassis_id] = dic
        return result

    def __gen_port_id_map(self, chassis_id_map) -> dict[str, dict[str, str]]:
        result = {}
        lel = self.data.legacy_port_handler.legacy_entity_list
        for index, p_info in enumerate(lel):
            lpr = p_info.legacy_port_ref
            lci = chassis_id_map[lpr.legacy_chassis_id]["id"]
            lmi = lpr.legacy_module_index
            lpi = lpr.legacy_port_index
            config = f"P-{lci}-{lmi}-{lpi}"
            dic = dict(config=config, identity=f"p{index}")
            result[p_info.legacy_item_id] = dic
        return result

    def __gen_ipv4_addr(self, entity: "LegacyPortEntity"):
        gateway = (
            (entity.legacy_ip_v4_gateway)
            if entity.legacy_ip_v4_gateway
            else ("0.0.0.0")
        )
        public_address = (
            (entity.legacy_public_ip_address)
            if entity.legacy_public_ip_address
            else "0.0.0.0"
        )
        remote_loop_address = (
            (entity.legacy_remote_loop_ip_address)
            if entity.legacy_remote_loop_ip_address
            else "0.0.0.0"
        )
        return dict(
            address=(entity.legacy_ip_v4_address),
            gateway=gateway,
            public_address=public_address,
            public_routing_prefix=entity.legacy_public_ip_routing_prefix,
            remote_loop_address=remote_loop_address,
            routing_prefix=entity.legacy_ip_v4_routing_prefix,
        )

    def __gen_ipv6_addr(self, port_entity: "LegacyPortEntity") -> dict:
        ipv6_gateway = (
            port_entity.legacy_ip_v6_gateway
            if port_entity.legacy_ip_v6_gateway
            else "::"
        )
        public_address = (
            port_entity.legacy_public_ip_address_v6
            if port_entity.legacy_public_ip_address_v6
            else "::"
        )
        remote_loop_address = (
            port_entity.legacy_remote_loop_ip_address_v6
            if port_entity.legacy_remote_loop_ip_address_v6
            else "::"
        )
        public_routing_prefix = port_entity.legacy_public_ip_routing_prefix_v6
        return dict(
            address=(port_entity.legacy_ip_v6_address),
            gateway=ipv6_gateway,
            public_address=public_address,
            public_routing_prefix=public_routing_prefix,
            remote_loop_address=remote_loop_address,
            routing_prefix=port_entity.legacy_ip_v6_routing_prefix,
        )

    def __gen_port_config(
        self,
        port_id_map: dict[str, dict[str, str]],
        protocol_segment: dict,
    ) -> dict:
        result = {}
        for entity in self.data.legacy_port_handler.legacy_entity_list:
            key = port_id_map[entity.legacy_item_id]["config"]
            ligma = base64.b64decode(entity.legacy_ip_gateway_mac_address)
            lrlma = base64.b64decode(entity.legacy_remote_loop_mac_address)

            cp = entity.legacy_port_rate_cap_profile
            port_rate_cap_profile = convert_port_rate_cap_profile(cp)

            lmmm = entity.legacy_mdi_mdix_mode
            mdi_mdix_mode = convert_mdi_mdix_mode(lmmm)

            lii = f"guid_{entity.legacy_item_id}"
            lsph = self.data.legacy_stream_profile_handler
            mapp = lsph.legacy_profile_assignment_map
            profile = protocol_segment[mapp[lii]]

            brr_mode = convert_brr_mode(entity.legacy_brr_mode)

            lmr = entity.legacy_multicast_role
            multicast_role = convert_multicast_role(lmr)

            unit = convert_port_rate_cap_unit(entity.legacy_port_rate_cap_unit)

            value = dict(
                anlt_enabled=bool(entity.legacy_anlt_enabled),
                auto_neg_enabled=bool(entity.legacy_auto_neg_enabled),
                broadr_reach_mode=brr_mode,
                fec_mode=entity.legacy_enable_fec,
                inter_frame_gap=entity.legacy_inter_frame_gap,
                ipv4_properties=self.__gen_ipv4_addr(entity),
                ipv6_properties=self.__gen_ipv6_addr(entity),
                ip_gateway_mac_address=MacAddress.from_bytes(ligma),
                latency_offset_ms=entity.legacy_latency_offset,
                mdi_mdix_mode=mdi_mdix_mode,
                multicast_role=multicast_role,
                pause_mode_enabled=entity.legacy_pause_mode_on,
                port_slot=port_id_map[entity.legacy_item_id]["identity"],
                port_config_slot=port_id_map[entity.legacy_item_id]["config"],
                port_rate_cap_enabled=bool(entity.legacy_enable_port_rate_cap),
                port_rate_cap_profile=port_rate_cap_profile,
                port_rate_cap_unit=unit,
                port_rate_cap_value=entity.legacy_port_rate_cap_value,
                port_speed_mode=entity.legacy_port_speed,
                profile=profile,
                remote_loop_mac_address=MacAddress.from_bytes(lrlma),
                reply_arp_requests=bool(entity.legacy_reply_arp_requests),
                reply_ping_requests=bool(entity.legacy_reply_ping_requests),
                speed_reduction_ppm=entity.legacy_adjust_ppm,
            )
            result[key] = value
        return result

    def __gen_frame_size(self):
        packet_size = self.data.legacy_test_options.legacy_packet_sizes
        fz = packet_size.legacy_mixed_length_config.legacy_frame_sizes
        mixed_sizes_weights = (
            packet_size.legacy_mixed_sizes_weights
            if packet_size.legacy_mixed_sizes_weights
            else MIXED_DEFAULT_WEIGHTS
        )

        lpst = packet_size.legacy_packet_size_type
        packet_size_type = convert_packet_size_type(lpst)
        return dict(
            custom_packet_sizes=packet_size.legacy_custom_packet_sizes,
            fixed_packet_end_size=packet_size.legacy_sw_packet_end_size,
            fixed_packet_start_size=packet_size.legacy_sw_packet_start_size,
            fixed_packet_step_size=packet_size.legacy_sw_packet_step_size,
            mixed_length_config=dict(
                field_0=fz.get("0", 56),
                field_1=fz.get("1", 60),
                field_14=fz.get("14", 9216),
                field_15=fz.get("15", 16360),
            ),
            mixed_sizes_weights=mixed_sizes_weights,
            packet_size_type=packet_size_type,
            varying_packet_max_size=packet_size.legacy_hw_packet_max_size,
            varying_packet_min_size=packet_size.legacy_hw_packet_min_size,
        )

    def __gen_test_config(self):
        test_options = self.data.legacy_test_options
        flow_option = test_options.legacy_flow_creation_options

        lmba = flow_option.legacy_mac_base_address
        mac_base_address = convert_base_mac_address(lmba)

        maddress_offset = flow_option.legacy_multi_stream_address_offset
        maddress_increment = flow_option.legacy_multi_stream_address_increment

        lmsm = flow_option.legacy_multi_stream_mac_base_address
        multi_stream_mac_base_address = convert_base_mac_address(lmsm)

        use_micro_tpld_on_demand = flow_option.legacy_use_micro_tpld_on_demand

        lfcp = flow_option.legacy_flow_creation_type
        flow_creation_type = convert_flow_creation_type(lfcp)

        lldu = test_options.legacy_latency_display_unit
        latency_display_unit = convert_display_unit(lldu)

        latency_mode = convert_latency_mode(test_options.legacy_latency_mode)

        ljdu = test_options.legacy_jitter_display_unit
        jitter_display_unit = convert_display_unit(ljdu)

        ltas = self.data.legacy_tid_allocation_scope
        tid_allocation_scope = convert_tid_allocation_scope(ltas)
        return dict(
            enable_multi_stream=flow_option.legacy_enable_multi_stream,
            flow_creation_type=flow_creation_type,
            frame_sizes=self.__gen_frame_size(),
            mac_base_address=mac_base_address,
            jitter_display_unit=jitter_display_unit,
            latency_display_unit=latency_display_unit,
            latency_mode=latency_mode,
            multi_stream_address_increment=maddress_increment,
            multi_stream_address_offset=maddress_offset,
            multi_stream_mac_base_address=multi_stream_mac_base_address,
            per_port_stream_count=flow_option.legacy_per_port_stream_count,
            sync_off_duration=test_options.legacy_sync_off_duration,
            tid_allocation_scope=tid_allocation_scope,
            tid_offset=test_options.legacy_tid_offset,
            toggle_sync_state=test_options.legacy_toggle_sync_state,
            use_gateway_mac_as_dmac=flow_option.legacy_use_gateway_mac_as_dmac,
            use_micro_tpld_on_demand=use_micro_tpld_on_demand,
        )

    def __gen_group_join_leave_delay(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        gjld = t_options.legacy_group_join_leave_delay
        if gjld.legacy_enabled:
            return dict(
                duration=gjld.legacy_duration,
                iterations=gjld.legacy_iterations,
                join_to_traffic_delay=gjld.legacy_join_to_traffic_delay,
                leave_to_stop_delay=gjld.legacy_leave_to_stop_delay,
                rate_options=dict(
                    end_value=gjld.legacy_rate_options.legacy_end_value,
                    start_value=gjld.legacy_rate_options.legacy_start_value,
                    step_value=gjld.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=gjld.legacy_traffic_to_join_delay,
            )
        return None

    def __gen_multicast_group_capacity(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        mgc = t_options.legacy_multicast_group_capacity
        if mgc.legacy_enabled:
            return dict(
                duration=mgc.legacy_duration,
                iterations=mgc.legacy_iterations,
                group_count_end=mgc.legacy_group_count_end,
                group_count_start=mgc.legacy_group_count_start,
                group_count_step=mgc.legacy_group_count_step,
                join_to_traffic_delay=mgc.legacy_join_to_traffic_delay,
                leave_to_stop_delay=mgc.legacy_leave_to_stop_delay,
                rate_options=dict(
                    end_value=mgc.legacy_rate_options.legacy_end_value,
                    start_value=mgc.legacy_rate_options.legacy_start_value,
                    step_value=mgc.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=mgc.legacy_traffic_to_join_delay,
            )
        return None

    def __gen_aggregated_throughput(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        at = t_options.legacy_aggregated_throughput
        lro = at.legacy_rate_options
        lgc = at.legacy_group_count_def
        if at.legacy_enabled:
            return dict(
                duration=at.legacy_duration,
                group_count_def=dict(
                    group_count_end=lgc.legacy_group_count_end,
                    group_count_list=lgc.legacy_group_count_list,
                    group_count_sel=lgc.legacy_group_count_sel,
                    group_count_start=lgc.legacy_group_count_start,
                    group_count_step=lgc.legacy_group_count_step,
                ),
                iterations=at.legacy_iterations,
                join_to_traffic_delay=at.legacy_join_to_traffic_delay,
                leave_to_stop_delay=at.legacy_leave_to_stop_delay,
                rate_options=dict(
                    initial_value=lro.legacy_initial_value,
                    maximum_value=lro.legacy_maximum_value,
                    minimum_value=lro.legacy_minimum_value,
                    pass_threshold=lro.legacy_pass_threshold,
                    use_pass_threshold=lro.legacy_use_pass_threshold,
                    value_resolution=lro.legacy_value_resolution,
                ),
                traffic_to_join_delay=at.legacy_traffic_to_join_delay,
            )
        return None

    def __gen_scale_group_throughput(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        sgt = t_options.legacy_scaled_group_throughput
        if sgt.legacy_enabled:
            return dict(
                duration=sgt.legacy_duration,
                group_count_end=sgt.legacy_group_count_end,
                group_count_start=sgt.legacy_group_count_start,
                group_count_step=sgt.legacy_group_count_step,
                iterations=sgt.legacy_iterations,
                join_to_traffic_delay=sgt.legacy_join_to_traffic_delay,
                leave_to_stop_delay=sgt.legacy_leave_to_stop_delay,
                rate_options=dict(
                    end_value=sgt.legacy_rate_options.legacy_end_value,
                    start_value=sgt.legacy_rate_options.legacy_start_value,
                    step_value=sgt.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=sgt.legacy_traffic_to_join_delay,
                use_max_capacity_result=sgt.legacy_use_max_capacity_result,
            )
        return None

    def __gen_mixed_class_throughput(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        mct = t_options.legacy_mixed_class_throughput
        lro = mct.legacy_rate_options
        lgc = mct.legacy_group_count_def
        if mct.legacy_enabled:
            return dict(
                duration=mct.legacy_duration,
                iterations=mct.legacy_iterations,
                join_to_traffic_delay=mct.legacy_join_to_traffic_delay,
                leave_to_stop_delay=mct.legacy_leave_to_stop_delay,
                group_count_def=dict(
                    group_count_end=lgc.legacy_group_count_end,
                    group_count_list=lgc.legacy_group_count_list,
                    group_count_start=lgc.legacy_group_count_start,
                    group_count_step=lgc.legacy_group_count_step,
                    group_count_sel=lgc.legacy_group_count_sel,
                ),
                rate_options=dict(
                    initial_value=lro.legacy_initial_value,
                    maximum_value=lro.legacy_maximum_value,
                    minimum_value=lro.legacy_minimum_value,
                    pass_threshold=lro.legacy_pass_threshold,
                    value_resolution=lro.legacy_value_resolution,
                    use_pass_threshold=lro.legacy_use_pass_threshold,
                ),
                traffic_to_join_delay=mct.legacy_traffic_to_join_delay,
                uc_traffic_load_ratio=mct.legacy_uc_traffic_load_ratio,
            )
        return None

    def __gen_multicast_latency(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        ltc = t_options.legacy_latency
        lgc = ltc.legacy_group_count_def
        if ltc.legacy_enabled:
            return dict(
                duration=ltc.legacy_duration,
                group_count_def=dict(
                    group_count_end=lgc.legacy_group_count_end,
                    group_count_list=lgc.legacy_group_count_list,
                    group_count_sel=lgc.legacy_group_count_sel,
                    group_count_start=lgc.legacy_group_count_start,
                    group_count_step=lgc.legacy_group_count_step,
                ),
                iterations=ltc.legacy_iterations,
                join_to_traffic_delay=ltc.legacy_join_to_traffic_delay,
                leave_to_stop_delay=ltc.legacy_leave_to_stop_delay,
                rate_options=dict(
                    end_value=ltc.legacy_rate_options.legacy_end_value,
                    start_value=ltc.legacy_rate_options.legacy_start_value,
                    step_value=ltc.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=ltc.legacy_traffic_to_join_delay,
            )
        return None

    def __gen_burdened_group_join_delay(self) -> Optional[dict]:
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        bjd = t_options.legacy_burdened_join_delay
        if bjd.legacy_enabled:
            return dict(
                duration=bjd.legacy_duration,
                iterations=bjd.legacy_iterations,
                join_to_traffic_delay=bjd.legacy_join_to_traffic_delay,
                leave_to_stop_delay=bjd.legacy_leave_to_stop_delay,
                rate_options=dict(
                    start_value=bjd.legacy_rate_options.legacy_start_value,
                    end_value=bjd.legacy_rate_options.legacy_end_value,
                    step_value=bjd.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=bjd.legacy_traffic_to_join_delay,
                uc_traffic_load_ratio=bjd.legacy_uc_traffic_load_ratio,
            )
        return None

    def __gen_burdened_multicast_latency(self):
        t_options = self.data.legacy_test_options.legacy_test_type_option_map
        bdl = t_options.legacy_burdened_latency
        lgc = bdl.legacy_group_count_def
        if bdl.legacy_enabled:
            return dict(
                duration=bdl.legacy_duration,
                group_count_def=dict(
                    group_count_end=lgc.legacy_group_count_end,
                    group_count_list=lgc.legacy_group_count_list,
                    group_count_sel=lgc.legacy_group_count_sel,
                    group_count_start=lgc.legacy_group_count_start,
                    group_count_step=lgc.legacy_group_count_step,
                ),
                iterations=bdl.legacy_iterations,
                join_to_traffic_delay=bdl.legacy_join_to_traffic_delay,
                leave_to_stop_delay=bdl.legacy_leave_to_stop_delay,
                rate_options=dict(
                    end_value=bdl.legacy_rate_options.legacy_end_value,
                    start_value=bdl.legacy_rate_options.legacy_start_value,
                    step_value=bdl.legacy_rate_options.legacy_step_value,
                ),
                traffic_to_join_delay=bdl.legacy_traffic_to_join_delay,
                uc_traffic_load_ratio=bdl.legacy_uc_traffic_load_ratio,
            )
        return None

    def __gen_test_type_config(self) -> dict:
        return dict(
            aggregated_multicast_throughput=self.__gen_aggregated_throughput(),
            burdened_multicast_latency=self.__gen_burdened_multicast_latency(),
            burdened_group_join_delay=self.__gen_burdened_group_join_delay(),
            group_join_leave_delay=self.__gen_group_join_leave_delay(),
            mixed_class_throughput=self.__gen_mixed_class_throughput(),
            multicast_group_capacity=self.__gen_multicast_group_capacity(),
            multicast_latency=self.__gen_multicast_latency(),
            scaled_group_forwarding_matrix=self.__gen_scale_group_throughput(),
        )

    def __gen_mc_definition(self, protocol_segments) -> dict:
        mc_def = self.data.legacy_mc_def_handler.legacy_mc_test_def_list[0]
        mc_def_seg = mc_def.legacy_stream_definition
        uc_def = self.data.legacy_uc_def_handler.legacy_unicast_def_list[0]
        uc_def_seg = uc_def.legacy_stream_definition

        lsph = self.data.legacy_stream_profile_handler
        mapp = lsph.legacy_profile_assignment_map
        i = self.data.legacy_port_handler.legacy_entity_list[0].legacy_item_id
        lii = f"guid_{i}"
        profile_id = mapp[lii]

        mc_profile_id = mapp[f"guid_{mc_def.legacy_item_id}"]

        mc_seg_result = protocol_segments[mc_profile_id].copy()
        uc_seg_result = protocol_segments[profile_id].copy()

        lpt = mc_def_seg.legacy_payload_definition.legacy_payload_type
        mc_seg_result["payload_type"] = convert_payload_type(lpt)

        lpp = mc_def_seg.legacy_payload_definition.legacy_payload_pattern
        bytes_str = bytes([int(i) for i in lpp.split(",")]).hex()
        mc_seg_result["payload_pattern"] = bytes_str
        lrt = mc_def_seg.legacy_rate_type
        mc_seg_result["rate_type"] = convert_rate_type(lrt)
        mc_seg_result["rate_fraction"] = mc_def_seg.legacy_rate_fraction
        mc_seg_result["rate_pps"] = mc_def_seg.legacy_rate_pps

        ulpt = uc_def_seg.legacy_payload_definition.legacy_payload_type
        uc_seg_result["payload_type"] = convert_payload_type(ulpt)

        upp = uc_def_seg.legacy_payload_definition.legacy_payload_pattern
        ubytes = bytes([int(i) for i in upp.split(",")]).hex()

        uc_seg_result["payload_pattern"] = ubytes

        ulrt = convert_rate_type(uc_def_seg.legacy_rate_type)
        uc_seg_result["rate_type"] = ulrt

        uc_seg_result["rate_fraction"] = uc_def_seg.legacy_rate_fraction
        uc_seg_result["rate_pps"] = uc_def_seg.legacy_rate_pps

        ult = uc_def.legacy_topology_config.legacy_topology
        topology = convert_test_topology(ult)

        dire = uc_def.legacy_topology_config.legacy_direction
        direction = convert_traffic_direction(dire)

        force_leave = mc_def.legacy_force_leave_to_all_routers_group
        return dict(
            comments=mc_def.legacy_comments,
            force_leave_to_all_routers_group=force_leave,
            item_id=mc_def.legacy_item_id,
            max_igmp_frame_rate=mc_def.legacy_max_igmp_frame_rate,
            mc_address_step_value=mc_def.legacy_mc_address_step_value,
            mc_ip_v4_start_address=(mc_def.legacy_mc_ip_v4_start_address),
            mc_ip_v6_start_address=(mc_def.legacy_mc_ip_v6_start_address),
            igmp_join_interval=mc_def.legacy_igmp_join_interval,
            igmp_leave_interval=mc_def.legacy_igmp_leave_interval,
            igmp_version=convert_igmp_version(mc_def.legacy_igmp_version),
            stream_definition=mc_seg_result,
            uc_flow_def=dict(
                comment=uc_def.legacy_comments,
                direction=direction,
                stream_definition=uc_seg_result,
                topology=topology,
            ),
            use_igmp_shaping=mc_def.legacy_use_igmp_shaping,
            use_igmp_source_address=mc_def.legacy_use_igmp_source_address,
        )

    def gen(self) -> dict:
        tester_id_map = self.__gen_chassis_id_map()
        id_map = self.__gen_port_id_map(tester_id_map)
        segments = self.__gen_profile()
        return dict(
            config=dict(
                mc_definition=self.__gen_mc_definition(segments),
                ports_configuration=self.__gen_port_config(id_map, segments),
                protocol_segments=segments,
                test_configuration=self.__gen_test_config(),
                test_types_configuration=self.__gen_test_type_config(),
            ),
            port_identities=self.__gen_port_identity(tester_id_map),
            username="Xena3918",
        )
