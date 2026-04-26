from manim import *
from config import *
from pathlib import Path
import random

class LanVsWan(Scene):
    def construct(self):
        self.camera.background_color = MATRIX_BLACK
        current_dir = Path(__file__).parent

        hero = Text("Types of Networks", **matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(hero, DOWN)
        subhero = Text("LAN Vs WAN", **matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        self.play(Write(hero), Create(underline), Write(subhero))
        self.wait(1.5)
        self.play(FadeOut(underline), FadeOut(subhero), FadeOut(hero))

        # LAN SECTION
        lan_title = Text("LAN", **matrix_style.HERO_STYLE).to_edge(UP).shift(LEFT * 3)
        lan_desc = Text("Local Area Network", **matrix_style.SUBHERO_STYLE).next_to(lan_title, DOWN)
        switch_l = Square(side_length=0.4, fill_opacity=1, color=MATRIX_GREEN).shift(LEFT * 3.5)
        pcs_l = VGroup()
        lines_l = VGroup()
        for i in range(4):
            pc = Dot(**matrix_style.DOT_STYLE)
            angle = i * 90 * DEGREES
            pc.move_to(switch_l.get_center() + 1.2 * np.array([np.cos(angle), np.sin(angle), 0]))
            line = Line(switch_l.get_center(), pc.get_center(),**matrix_style.LINE_STYLE).set_z_index(-1)
            pcs_l.add(pc)
            lines_l.add(line)

        # WAN SECTION
        wan_title = Text("WAN", **fire_style.HERO_STYLE).to_edge(UP).shift(RIGHT * 3)
        wan_desc = Text("Wide Area Network",**fire_style.SUBHERO_STYLE).next_to(wan_title, DOWN)
        lan1_center = RIGHT * 1 + UP * 1
        lan2_center = RIGHT * 4 + DOWN * 1
        lan3_center = RIGHT * 5 + UP * 1
        router1 = Circle(**fire_style.DOT_STYLE).move_to(lan1_center)
        router2 = Circle(**fire_style.DOT_STYLE).move_to(lan2_center)
        router3 = Circle(**fire_style.DOT_STYLE).move_to(lan3_center)
        wan_link = Line(router1.get_center(), router2.get_center(), color=CANDY_RED)
        wan_link2 = ArcBetweenPoints(router2.get_center(), router3.get_center(), angle=45 * DEGREES, color=CANDY_RED)

        # Show LAN
        self.play(Write(lan_title), FadeIn(lan_desc))
        self.play(FadeIn(switch_l), Create(lines_l), FadeIn(pcs_l))
        packet_l = Dot(color=GLITCH_GOLD)
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
        self.play(Write(wan_title), FadeIn(wan_desc))
        self.play(FadeIn(router1), FadeIn(router2), FadeIn(router3))
        self.play(Create(wan_link), Create(wan_link2))
        packet_w = Dot(color=GLITCH_GOLD).move_to(router1.get_center())
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

        self.wait(3)

        # Comparison Table
        table_data = [
            ["Faster", "Slower"],
            ["Private", "Public/Leased"],
            ["Low", "High"],
            ["Multi-Point", "Point-to-Point*"]
        ]
        routing_table = Table(
            table_data,
            col_labels=[Text("LAN", color=MATRIX_GREEN), Text("WAN", color=CANDY_RED)],
            row_labels=[Text("Speed"),Text("Ownership"),Text("Range"),Text("Topology")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": MATRIX_GREEN}
        ).scale(0.4).to_edge(DOWN, buff=0.5)
        routing_table.get_entries().set_font_size(18)
        table_group = VGroup(routing_table)
        self.play(FadeIn(table_group))

        self.wait(10)