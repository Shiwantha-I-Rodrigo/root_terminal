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
        section_01 = self.stylize("NETWORK DESIGN/WIRELESS & POE").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeIn(section_01))
        # self.add_flicker(section_01)

        # background effects
        # back_grid = self.get_hacker_grid()
        # self.add(back_grid)
        # self.add_matrix_animation(back_grid)

        # legend
        legend = self.set_legend([ "I. Wireless LAN Controllers", "II. Management Platforms", "III. Power over Ethernet"])
        pointer = Triangle(color=MATRIX_GREEN).scale(0.1).rotate(-90 * DEGREES)
        pointer.next_to(legend[0], LEFT, buff=0.2)
        self.play(FadeIn(legend, pointer))
        # self.add_flicker(legend)
        # self.add_flicker(pointer)

        # wlc
        wlc = self.get_wlc()
        self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        self.play(Create(wlc["all"]), run_time=2)
        self.animate_wlc(wlc, 2)
        self.play(FadeOut(wlc["all"]))

        # # dna
        # dna = self.get_dna("dna")
        # self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        # self.play(
        #     Create(dna["center"]),
        #     Create(dna["connections"]),
        #     FadeIn(dna["nodes"]),
        #     run_time=2
        # )
        # self.animate_dna(dna, 1)
        # self.play(FadeOut(dna["all"]))

        # # poe
        # poe = self.get_poe("poe")
        # self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        # self.play(
        #     Create(poe["center"]),
        #     Create(poe["connections"]),
        #     FadeIn(poe["nodes"]),
        #     run_time=2
        # )
        # self.animate_poe(poe, 1)
        # self.play(FadeOut(poe["all"]))


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
        for _ in range(loops):
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