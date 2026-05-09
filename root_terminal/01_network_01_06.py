import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDesign(Scene, CommonUtils):

    # Network Infastructure
    matrix_style = MatrixStyle()
    red_style = RedStyle()
    yellow_style = YellowStyle()
    blue_style = BlueStyle()
    purple_style = PurpleStyle()
    pink_style = PinkStyle()
    white_style = WhiteStyle()
    amber_style = AmberStyle()

    def construct(self):
        self.setup_scene()
        section_01 = self.stylize("NETWORK DESIGN/WLC MODELS & PoE STANDARDS").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeIn(section_01))
        # self.add_flicker(section_01)

        # background effects
        # back_grid = self.get_hacker_grid()
        # self.add(back_grid)
        # self.add_matrix_animation(back_grid)

        # legend
        legend = self.set_legend([ "I. Wireless LAN Controllers", "II. Power over Ethernet"])
        pointer = Triangle(color=MATRIX_GREEN).scale(0.1).rotate(-90 * DEGREES)
        pointer.next_to(legend[0], LEFT, buff=0.2)
        self.play(FadeIn(legend, pointer))
        # self.add_flicker(legend)
        # self.add_flicker(pointer)

        # wlc
        wlc = self.get_wlc()
        self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        self.play(Create(wlc["all"]), run_time=2)
        self.animate_wlc(wlc, 10)
        self.play(FadeOut(wlc["all"]))
        self.play(FadeOut(wlc["label2"]))

        # poe
        poe = self.get_poe()
        self.play(pointer.animate.next_to(legend[1], LEFT, buff=0.2))
        self.play(Create(poe["all"]),run_time=2)
        self.animate_poe(poe, 10)
        self.play(FadeOut(poe["all"]))


    def get_wlc(self):
        ap_group = VGroup()
        client_group = VGroup()
        connections = VGroup()
        switch = self.create_node("switch").move_to(UP * 1.5 + RIGHT * 2)
        wlc = self.create_node("wlc").move_to(switch.get_center() + RIGHT * 2.5)
        wlc_link = self.connect(switch, wlc)
        switch.wlc_link = wlc_link
        connections.add(wlc_link)
        client_styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        client_colors = [NEON_YELLOW, CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE]
        style_idx = 0

        # APs
        for i in range(2):
            ap_pos = switch.get_center() + (LEFT if i == 0 else RIGHT) * 2.5 + DOWN * 2
            ap = self.create_node("access").move_to(ap_pos)
            ap = apply_icon_style(ap, MATRIX_GREEN)
            ap.uplink = self.connect(switch, ap) # adding metadata
            ap_group.add(ap)
            connections.add(ap.uplink)

            # Clients
            for j in range(2):
                angle = -PI/4 if j == 0 else -3*PI/4
                client_pos = ap.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * 2
                client = self.create_node("device").move_to(client_pos)
                style = client_styles[style_idx % len(client_styles)]
                client = apply_icon_style(client, client_colors[style_idx % len(client_styles)])
                client.style = style                         # adding metadata
                client.uplink = self.connect(ap, client)     # adding metadata
                client.parent_ap = ap                        # adding metadata
                client_group.add(client)
                connections.add(client.uplink)
                style_idx += 1
        mgmt_area = RoundedRectangle(corner_radius=0.2, color=MATRIX_GREEN, fill_opacity=0.03)
        mgmt_area.surround(VGroup(switch, ap_group), buff=0.5)
        label_1 = Text("WLC Centralized Model", **self.matrix_style.LABEL_STYLE).next_to(mgmt_area, UP)
        label_2 = Text("WLC FlexConnect Model", **self.matrix_style.LABEL_STYLE).next_to(mgmt_area, UP)
        label_w = VGroup(
            Text("WLC", **self.matrix_style.LABEL_STYLE).next_to(wlc, DOWN),
            Text("AP/LAP", **self.matrix_style.LABEL_STYLE).next_to(ap_group[0], RIGHT),
            Text("AP/LAP", **self.matrix_style.LABEL_STYLE).next_to(ap_group[1], LEFT)
        )
        return {
            "center": switch,
            "wlc": wlc,
            "aps": ap_group, 
            "clients": client_group,
            "connections": connections,
            "label1": label_1,
            "label2": label_2,
            "all": VGroup(switch, wlc, ap_group, client_group, connections, label_1, label_w, mgmt_area)
        }
    
    def animate_wlc(self, wlc, loops):
        clients = wlc["clients"].submobjects
        aps = wlc["aps"].submobjects
        switch = wlc["center"]
        wlc_node = wlc["all"][1]

        def animate_packet_flow(src, dest, use_wlc=False):
            packet = Dot(**dest.style.DOT_STYLE).set_z_index(3)
            # Client -> AP -> Switch
            self.play(MoveAlongPath(packet, src.uplink, rate_func=lambda t: 1-t), run_time=0.4)
            self.play(MoveAlongPath(packet, src.parent_ap.uplink, rate_func=lambda t: 1-t), run_time=0.4)
            if use_wlc:
                # Switch -> WLC -> Switch
                self.play(MoveAlongPath(packet, switch.wlc_link, rate_func=linear), run_time=0.3)
                self.play(MoveAlongPath(packet, switch.wlc_link, rate_func=lambda t: 1-t), run_time=0.3)
            # Switch -> AP -> Client
            self.play(MoveAlongPath(packet, dest.parent_ap.uplink, rate_func=linear), run_time=0.4)
            self.play(MoveAlongPath(packet, dest.uplink, rate_func=linear), run_time=0.4)
            self.play(FadeOut(packet))

        # Centralized Mode
        for _ in range(loops):
            animate_packet_flow(*random.sample(clients, 2), use_wlc=True)

        # FlexConnect
        self.play(FadeOut(wlc["label1"]), FadeIn(wlc["label2"]))
        self.play(Indicate(wlc["label2"], color=ELECTRIC_RED))
        config_packets = VGroup(*[Dot(color=ELECTRIC_RED).move_to(wlc_node) for _ in aps])
        self.play(*[p.animate.move_to(switch) for p in config_packets], run_time=0.8)
        self.play(*[MoveAlongPath(p, ap.uplink) for p, ap in zip(config_packets, aps)], run_time=0.8)
        self.play(FadeOut(config_packets), Indicate(wlc["aps"], color=ELECTRIC_RED))
        for _ in range(5):
            animate_packet_flow(*random.sample(clients, 2), use_wlc=False)
        target_ap = aps[0]
        req_packet = Dot(color=ELECTRIC_RED).set_z_index(3).move_to(target_ap)
        self.play(Indicate(target_ap, color=ELECTRIC_RED))
        # AP -> Switch -> WLC
        self.play(MoveAlongPath(req_packet, target_ap.uplink, rate_func=lambda t: 1-t), run_time=0.5)
        self.play(MoveAlongPath(req_packet, switch.wlc_link, rate_func=linear), run_time=0.4)
        self.play(Indicate(wlc_node, color=ELECTRIC_RED))
        # WLC -> Switch -> AP
        self.play(MoveAlongPath(req_packet, switch.wlc_link, rate_func=lambda t: 1-t), run_time=0.4)
        self.play(MoveAlongPath(req_packet, target_ap.uplink, rate_func=linear), run_time=0.5)
        self.play(Indicate(target_ap, color=ELECTRIC_RED), FadeOut(req_packet))
        for _ in range(loops):
            animate_packet_flow(*random.sample(clients, 2), use_wlc=False)
    
    def get_poe(self):
        pd_group = VGroup()
        connections = VGroup()
        pse_switch = self.create_node("switch").move_to(UP * 0.5 + RIGHT * 1.5)
        pse_label = Text("PSE (Switch)", **self.matrix_style.LABEL_STYLE).next_to(pse_switch, UP)
        pd_types = ["camera", "phone", "access", "device"]
        pd_labels = ["IP Camera", "VoIP Phone", "AP", "IoT Sensor"]
        for i, (icon_name, label_text) in enumerate(zip(pd_types, pd_labels)):
            angle = PI + (i * PI / 3)
            pos = pse_switch.get_center() + np.array([np.cos(angle) * 2.5, np.sin(angle) * 2.5, 0])
            pd = self.create_node(icon_name).move_to(pos)
            pd = apply_icon_style(pd, MATRIX_GREEN if i == 1 else GHOST_WHITE)
            pd.uplink = self.connect(pse_switch, pd)
            pd.label = Text(label_text, **self.matrix_style.LABEL_STYLE).next_to(pd, DOWN * 0.5)
            pd_group.add(pd)
            connections.add(pd.uplink)
        return {
            "pse": pse_switch,
            "pse_label": pse_label,
            "pds": pd_group,
            "connections": connections,
            "all": VGroup(pse_switch, pse_label, pd_group, connections)
        }
    
    def animate_poe(self, poe, loops):
        pse = poe["pse"]
        pds = poe["pds"].submobjects
        
        poe_pds = [pd for i, pd in enumerate(pds) if i in [0, 2, 3]]
        non_poe_pds = [pd for i, pd in enumerate(pds) if i == 1]
        
        # Detection (All devices)
        detection_text = Text("DETECTING DEVICES (LOW VOLTAGE PULSE)", **self.purple_style.LABEL_STYLE).next_to(pse, UP, buff=1)
        self.play(Write(detection_text))
        detection_pulses = VGroup(*[Dot(**self.purple_style.DOT_STYLE).move_to(pse) for _ in pds])
        self.play(
            *[MoveAlongPath(p, pd.uplink, rate_func=there_and_back) for p, pd in zip(detection_pulses, pds)],
            *[Indicate(pd, color=SHOCK_PURPLE) for pd in pds],
            run_time=2)
        self.play(FadeOut(detection_pulses), FadeOut(detection_text))

        # Negotiation
        negotiation_text = Text("NEGOTIATING POWER (POE DEVICES FOUND)", **self.yellow_style.LABEL_STYLE).next_to(pse, UP, buff=1)
        self.play(Write(negotiation_text))
        negotiation_pulses = VGroup(*[Dot(**self.yellow_style.DOT_STYLE).move_to(pse) for _ in poe_pds])
        non_poe_conns = VGroup(*[pd.uplink for pd in non_poe_pds])
        poe_conns = VGroup(*[pd.uplink for pd in poe_pds])
        self.play(poe_conns.animate.set_color(NEON_YELLOW).set_stroke(width=3), run_time=1)
        self.play(
            *[MoveAlongPath(p, pd.uplink, rate_func=there_and_back) for p, pd in zip(negotiation_pulses, poe_pds)],
            *[Indicate(pd, color=NEON_YELLOW) for pd in poe_pds],
            non_poe_conns.animate.set_stroke(opacity=0.2),
            run_time=2
        )
        poe_label_1 = Text("12W", **self.white_style.LABEL_STYLE).next_to(pds[0], UP, buff=0.2)
        poe_label_2 = Text("22W", **self.white_style.LABEL_STYLE).next_to(pds[2], DOWN, buff=0.2)
        poe_label_3 = Text("60W", **self.white_style.LABEL_STYLE).next_to(pds[3], UP, buff=0.2)
        self.play(FadeIn(poe_label_1, poe_label_2, poe_label_3))
        self.play(FadeOut(negotiation_pulses), FadeOut(negotiation_text))
        
        # Energize
        self.play(poe_conns.animate.set_color(ALERT_AMBER).set_stroke(width=5), run_time=1)
        self.play(FadeOut(negotiation_pulses), FadeOut(negotiation_text))
        power_text = Text("FULL POWER DELIVERED", **self.amber_style.LABEL_STYLE).next_to(pse, UP, buff=1)
        self.play(Write(power_text))
        power_pulses = VGroup(*[Dot(**self.amber_style.DOT_STYLE).move_to(pse) for _ in poe_pds])
        self.play(
            *[MoveAlongPath(p, pd.uplink, rate_func=there_and_back) for p, pd in zip(power_pulses, poe_pds)],
            *[Indicate(pd, color=ALERT_AMBER) for pd in poe_pds],
            run_time=2
        )
        self.play(*[pd.animate.set_color(MATRIX_GREEN) for pd in pds], run_time=1)
        self.play(FadeOut(power_pulses), FadeOut(power_text))
        
        # Data
        for _ in range(loops):
            data_dots = VGroup(*[Dot(**self.matrix_style.DOT_STYLE).move_to(pd) for pd in pds])
            self.play(
                *[MoveAlongPath(d, pd.uplink, rate_func=lambda t: 1-t) for d, pd in zip(data_dots, pds)],
                run_time=2,
                rate_func=linear
            )
            self.play(FadeOut(data_dots))

        # Table
        standards_table = Table(
            [["802.3af", "PoE", "15.4W"],
             ["802.3at", "PoE+", "30W"],
             ["802.3bt", "UPoE+", "60-90W"]],
            col_labels=[Text("Standard"), Text("Type"), Text("Max Power")],
            include_outer_lines=True
        ).scale(0.3).to_corner(DL, buff=1)
        self.play(Create(standards_table))

        self.wait(2)