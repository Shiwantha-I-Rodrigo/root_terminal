import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkEncapsulation(Scene, CommonUtils):

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
        self.intro_animation("Networking Devices", "Controlling the Flow of Data")

        osi_layers = [
            "7. Application",
            "6. Presentation",
            "5. Session",
            "4. Transport",
            "3. Network",
            "2. Data Link",
            "1. Physical"
        ]
        osi_colors = [ELECTRIC_RED, ORANGE, YELLOW, MATRIX_GREEN, CYBER_BLUE, SHOCK_PURPLE, NEON_YELLOW]

        # osi stacks
        osi_stack = VGroup()
        for i, (name, color) in enumerate(zip(osi_layers, osi_colors)):
            rect = Rectangle(width=3, height=0.5, fill_opacity=0.1, color=color)
            label = Text(name, **matrix_style.SUBTITLE_STYLE).move_to(rect.get_center())
            layer = VGroup(rect, label)
            if len(osi_stack) > 0:
                layer.next_to(osi_stack[-1], DOWN, buff=0)
            osi_stack.add(layer)
        pc1_path = current_dir / "assets/device.svg"
        pc1 = SVGMobject(str(pc1_path))
        apply_icon_style(pc1,NEON_YELLOW).next_to(hero, DOWN, buff=1)
        pc1.set_z_index(3)
        osi_stack.next_to(pc1, DOWN, buff=0.2)
        osi_stack.to_edge(LEFT, buff=1)
        pc1.move_to(osi_stack.get_top() + UP * 1)

        osi2_stack = VGroup()
        for i, (name, color) in enumerate(zip(osi_layers, osi_colors)):
            rect = Rectangle(width=3, height=0.5, fill_opacity=0.1, color=color)
            label = Text(name, **matrix_style.SUBTITLE_STYLE).move_to(rect.get_center())
            layer = VGroup(rect, label)
            if len(osi2_stack) > 0:
                layer.next_to(osi2_stack[-1], DOWN, buff=0)
            osi2_stack.add(layer)
        pc2_path = current_dir / "assets/device.svg"
        pc2 = SVGMobject(str(pc2_path))
        apply_icon_style(pc2,ELECTRIC_RED).next_to(hero, DOWN, buff=1)
        pc2.set_z_index(3)
        osi2_stack.next_to(pc2, DOWN, buff=0.2)
        osi2_stack.to_edge(RIGHT, buff=1)
        pc2.move_to(osi2_stack.get_top() + UP * 1)

        connection = Line(osi_stack[-1].get_corner(DOWN + RIGHT), osi2_stack[-1].get_corner(DOWN + LEFT), color=MATRIX_GREEN)
        connection_label = Text("Physical Connection", **matrix_style.SUBTITLE_STYLE).next_to(connection,DOWN)

        encap_arrow = Arrow(
            start=osi_stack.get_corner(UR) + RIGHT * 0.5, 
            end=osi_stack.get_corner(DR) + RIGHT * 0.5,
            stroke_width=4,
            tip_length=0.2,
            color=MATRIX_GREEN
        )
        encap_arrow.set_z_index(-1)
        encap_label = Text("Encapsulation", font_size=18).rotate(270*DEGREES).next_to(encap_arrow, RIGHT, buff=0.2)
        encap_label.set_z_index(-1)

        deencap_arrow = Arrow(
            start=osi2_stack.get_corner(DL) + LEFT * 0.5, 
            end=osi2_stack.get_corner(UL) + LEFT * 0.5,
            stroke_width=4,
            tip_length=0.2,
            color=MATRIX_GREEN
        )
        deencap_arrow.set_z_index(-1)
        deencap_label = Text("De-Encapsulation", font_size=18).rotate(90*DEGREES).next_to(deencap_arrow, LEFT, buff=0.2)
        deencap_label.set_z_index(-1)

        self.play(FadeIn(osi_stack, osi2_stack, pc1, pc2))
        self.play(Create(connection), Write(connection_label))
        self.wait(5)
        self.play(FadeIn(encap_arrow, encap_label))
        self.wait(5)
        self.play(FadeOut(encap_arrow, encap_label))
        self.play(FadeIn(deencap_arrow, deencap_label))
        self.wait(5)
        self.play(FadeOut(deencap_arrow, deencap_label))
        self.wait(5)

        header_stack = VGroup()
        header_stack.set_z_index(3)
        data_block = Rectangle(width=1, height=0.5, fill_opacity=0.3, color=ELECTRIC_RED)
        data_text = Text("DATA", **matrix_style.LABEL_STYLE).move_to(data_block)
        header_stack.add(data_block, data_text)
        header_stack.next_to(osi_stack[0].get_right(), buff=0.6)

        self.play(FadeIn(header_stack))
        self.wait(1)
        self.play(header_stack.animate.next_to(osi_stack[3].get_right(), buff=0.6), run_time=2.5)
        self.wait(1)

        tcp_block = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=MATRIX_GREEN).next_to(data_block, LEFT, buff=0)
        tcp_text = Text("TCP", **matrix_style.LABEL_STYLE).move_to(tcp_block)
        header_stack.add(tcp_block, tcp_text)

        self.play(FadeIn(tcp_block,tcp_text))
        self.wait(1)
        self.play(header_stack.animate.next_to(osi_stack[4].get_right(), buff=0.6), run_time=2.5)
        self.wait(1)

        ip_block = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=CYBER_BLUE).next_to(tcp_block, LEFT, buff=0)
        ip_text = Text("IP", **matrix_style.LABEL_STYLE).move_to(ip_block)
        header_stack.add(ip_block, ip_text)

        self.play(FadeIn(ip_block,ip_text))
        self.wait(1)
        self.play(header_stack.animate.next_to(osi_stack[5].get_right(), buff=0.6), run_time=2.5)
        self.wait(1)

        mac_block = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=SHOCK_PURPLE).next_to(ip_block, LEFT, buff=0)
        mac_text = Text("mac", **matrix_style.LABEL_STYLE).move_to(mac_block)
        mac_block2 = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=SHOCK_PURPLE).next_to(data_block, RIGHT, buff=0)
        mac_text2 = Text("mac", **matrix_style.LABEL_STYLE).move_to(mac_block2)
        header_stack.add(mac_block, mac_text, mac_block2, mac_text2)

        self.play(FadeIn(mac_block,mac_text, mac_block2, mac_text2))
        self.wait(1)
        self.play(header_stack.animate.next_to(osi_stack[6].get_right(), buff=0.1), run_time=2.5)
        self.wait(1)

        bin_stack = VGroup()
        bin_stack.set_z_index(3)
        bin_block = Rectangle(width=2, height=0.5, fill_opacity=0.2, color=GHOST_WHITE).next_to(osi_stack[-1], RIGHT, buff=0.1)
        bin_text = Text("1001001010010000101", **white_style.LABEL_STYLE).move_to(bin_block)
        bin_stack.add(bin_block, bin_text)

        self.play(FadeOut(header_stack))
        self.play(FadeIn(bin_stack))
        self.wait(1)
        self.play(bin_stack.animate.next_to(osi2_stack[-1], LEFT, buff=0.1), run_time=2.5)
        self.wait(5)

        header_stack.next_to(osi2_stack[-1], LEFT, buff=0.1)
        self.play(FadeOut(bin_stack))
        self.play(FadeIn(header_stack))
        self.wait(1)
        self.play(header_stack.animate.next_to(osi2_stack[-2], LEFT, buff=0.1), run_time=2.5)
        self.wait(1)
        self.play(FadeOut(mac_block, mac_text, mac_block2, mac_text2))
        header_stack.remove(mac_block, mac_text, mac_block2, mac_text2)

        self.wait(1)
        self.play(header_stack.animate.next_to(osi2_stack[-3], LEFT, buff=0.1), run_time=2.5)
        self.wait(1)
        self.play(FadeOut(ip_block, ip_text))
        header_stack.remove(ip_block, ip_text)

        self.wait(1)
        self.play(header_stack.animate.next_to(osi2_stack[-4], LEFT, buff=0.1), run_time=2.5)
        self.wait(1)
        self.play(FadeOut(tcp_block, tcp_text))
        header_stack.remove(tcp_block, tcp_text)

        self.wait(1)
        self.play(header_stack.animate.next_to(osi2_stack[0], LEFT, buff=0.1), run_time=2.5)

        self.wait(5)