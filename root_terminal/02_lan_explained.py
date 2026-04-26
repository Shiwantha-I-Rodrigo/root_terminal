from manim import *
from config import *
from pathlib import Path
import random

class LANExplanation(Scene): 
    def construct(self):
        self.camera.background_color = MATRIX_BLACK
        current_dir = Path(__file__).parent

        hero = Text("What is a LAN", **matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(hero, DOWN)
        subhero = Text("Local Area Network", **matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        self.play(Write(hero), Create(underline), Write(subhero))
        self.wait(1.5)
        self.play(FadeOut(underline), FadeOut(subhero), hero.animate.to_edge(UP).scale(0.7))

        # Create Switch
        switch_path = current_dir / "assets/switch.svg"
        switch = SVGMobject(str(switch_path))
        apply_icon_style(switch,MATRIX_GREEN)
        switch.move_to(DOWN * 0.5).set_z_index(3)
        
        pc_path = current_dir / "assets/device.svg"
        end_devices = VGroup(*[SVGMobject(str(pc_path)) for _ in range(3)])
        apply_icon_style(end_devices[0], MATRIX_GREEN)
        apply_icon_style(end_devices[1], MATRIX_GREEN)
        apply_icon_style(end_devices[2], MATRIX_GREEN)
        end_devices[0].move_to(UP * 2)
        end_devices[1].move_to(LEFT * 2.5 + DOWN * 2)
        end_devices[2].move_to(RIGHT * 2.5 + DOWN * 2)
        self.play(FadeIn(end_devices[0], end_devices[1], end_devices[2]))

        connection1 = Line(switch.get_center(), end_devices[0].get_bottom(), color=MATRIX_GREEN, stroke_opacity=0.5)
        connection2 = Line(switch.get_center(), end_devices[1].get_corner(UR), color=MATRIX_GREEN, stroke_opacity=0.5)
        connection3 = Line(switch.get_center(), end_devices[2].get_corner(UL), color=MATRIX_GREEN, stroke_opacity=0.5) 
        connections = VGroup(connection1, connection2, connection3)
        packet = Dot(**matrix_style.DOT_STYLE)
        packet.set_z_index(3)
        self.play(FadeIn(switch), Create(connections))

        conns = [connection1, connection2, connection3]
        for i in range(10):
            mode = random.randint(0, 1)
            match mode:
                case 0:
                    start_idx = i % 3
                    other_indices = [idx for idx in range(3) if idx != start_idx]
                    start_line = conns[start_idx]
                    out_line_a = conns[other_indices[0]]
                    out_line_b = conns[other_indices[1]]
                    self.play(MoveAlongPath(packet, start_line), run_time=0.8, rate_func=lambda t: 1 - t)
                    packet2 = packet.copy() 
                    self.play(MoveAlongPath(packet, out_line_a), MoveAlongPath(packet2, out_line_b), run_time=0.8, rate_func=linear)
                    self.play(FadeOut(packet), FadeOut(packet2), run_time=0.2)
                case 1:
                    source_idx = random.randint(0, 2)
                    dest_idx = random.choice([i for i in range(3) if i != source_idx])
                    source_line = conns[source_idx]
                    dest_line = conns[dest_idx]
                    self.play(MoveAlongPath(packet, source_line),run_time=0.6,rate_func=lambda t: 1 - t)
                    self.play(MoveAlongPath(packet, dest_line),run_time=0.6,rate_func=linear)
                    self.play(FadeOut(packet), run_time=0.2)

        self.wait(10)
