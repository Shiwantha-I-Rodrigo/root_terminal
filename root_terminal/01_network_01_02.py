import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDesign(Scene, CommonUtils):

    # LAN Vs WAN
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
        heading = self.intro_animation("NETWORK DESIGN", "Topologies & Architectures")
        section_01 = self.stylize("NETWORK DESIGN/LAN Vs WAN").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeOut(heading), FadeIn(section_01))

        # LAN SECTION
        lan_title = Text("Local Area Network", **self.matrix_style.TITLE_STYLE).to_edge(UP, buff=1).shift(LEFT * 3)
        switch_l = self.create_node("switch", LEFT * 3)
        pcs_l = VGroup()
        lines_l = VGroup()
        for i in range(4):
            pc = self.create_node("device")
            angle = i * 90 * DEGREES
            pc.move_to(switch_l.get_center() + 1.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            line = self.connect(switch_l, pc)
            pcs_l.add(pc)
            lines_l.add(line)

        # WAN SECTION
        wan_title = Text("Wide Area Network",**self.red_style.TITLE_STYLE).to_edge(UP, buff=1).shift(RIGHT * 3)
        lan1_center = RIGHT * 1 + UP * 1
        lan2_center = RIGHT * 4 + DOWN * 1
        lan3_center = RIGHT * 5 + UP * 1
        router1 = self.create_node("building").move_to(lan1_center)
        router2 = self.create_node("building").move_to(lan2_center)
        router3 = self.create_node("building").move_to(lan3_center)
        wan_link = self.connect(router1, router2, **self.red_style.LINE_STYLE)
        wan_link2 = ArcBetweenPoints(router2.get_center(), router3.get_center(), angle=45 * DEGREES, **self.red_style.LINE_STYLE)

        # Show LAN
        self.play(Write(lan_title))
        self.play(FadeIn(switch_l), Create(lines_l), FadeIn(pcs_l))
        packet_l = Dot(color=NEON_YELLOW)
        packet_2 = packet_l.copy()
        for i in range(10):
            path_a = random.choice(lines_l)
            path_b = random.choice(lines_l)
            speed = random.uniform(0.5, 0.7)
            if random.random() > 0.5:
                self.play(MoveAlongPath(packet_l, path_a, rate_func=lambda t: 1 - t), run_time=speed)
                self.remove(packet_l)
                self.play(MoveAlongPath(packet_l, path_b, rate_func=linear), run_time=speed)
                self.remove(packet_l)
            else:
                self.play(MoveAlongPath(packet_l, path_a, rate_func=lambda t: 1 - t),MoveAlongPath(packet_2, path_b, rate_func=lambda t: 1 - t),run_time=speed)
                self.remove(packet_l, packet_2)
                self.play(MoveAlongPath(packet_l, path_a, rate_func=linear),run_time=speed)
                self.remove(packet_l)

        self.wait(3)

        # Show WAN
        self.play(Write(wan_title))
        self.play(FadeIn(router1), FadeIn(router2), FadeIn(router3))
        self.play(Create(wan_link), Create(wan_link2))
        packet_w = Dot(color=NEON_YELLOW).move_to(router1.get_center())
        packet_x = packet_w.copy()
        for i in range(3):
            if random.random() > 0.5:
                self.play(MoveAlongPath(packet_w, wan_link, rate_func=linear), run_time=3)
                self.remove(packet_w)
                self.play(MoveAlongPath(packet_w, wan_link, rate_func=lambda t: 1 - t), MoveAlongPath(packet_x, wan_link2, rate_func=linear), run_time=3)
                self.remove(packet_w, packet_x)
                self.play(MoveAlongPath(packet_w, wan_link2, rate_func=lambda t: 1 - t), run_time=3)
                self.remove(packet_w)
            else:
                self.play(MoveAlongPath(packet_w, wan_link2, rate_func=lambda t: 1 - t), run_time=2)
                self.remove(packet_w)
                self.play(MoveAlongPath(packet_w, wan_link, rate_func=lambda t: 1 - t), run_time=4)
                self.remove(packet_w)

        self.wait(10)