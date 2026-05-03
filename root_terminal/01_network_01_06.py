import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkArchitecture(Scene, CommonUtils):

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
        osi_colors = [ELECTRIC_RED, ALERT_AMBER, NEON_YELLOW, MATRIX_GREEN, CYBER_BLUE, SHOCK_PURPLE, VAPOR_PINK]

        tcp_layers = [
            "Application",
            "Transport",
            "Network",
            "Link"
        ]
        tcp_colors = [ELECTRIC_RED, MATRIX_GREEN, CYBER_BLUE, SHOCK_PURPLE]

        hybrid_layers = [
            "7. Application",
            "4. Transport",
            "3. Network",
            "2. Data Link",
            "1. Physical"
        ]
        hybrid_colors = [ELECTRIC_RED, MATRIX_GREEN, CYBER_BLUE, SHOCK_PURPLE, VAPOR_PINK]
        
        # osi stack
        osi_stack = VGroup()
        for i, (name, color) in enumerate(zip(osi_layers, osi_colors)):
            rect = Rectangle(width=3, height=0.5, fill_opacity=0.2, color=color)
            label = Text(name, font_size=20).move_to(rect.get_center())
            layer = VGroup(rect, label)
            if len(osi_stack) > 0:
                layer.next_to(osi_stack[-1], DOWN, buff=0)
            osi_stack.add(layer)
        osi_title = Text("OSI Model\n(Standard)", **matrix_style.SUBHERO_STYLE).next_to(hero, DOWN, buff=1)
        osi_stack.next_to(osi_title, DOWN, buff=1)
        osi_title.to_edge(LEFT, buff=1)
        osi_stack.to_edge(LEFT, buff=1)

        # tcp stack
        tcp_stack = VGroup()
        for i, (name, color) in enumerate(zip(tcp_layers, tcp_colors)):
            match i:
                case 0:
                    h = 1.5
                case 3:
                    h = 1.0
                case _:
                    h = 0.5
            rect = Rectangle(width=3, height=h, fill_opacity=0.2, color=color)
            label = Text(name, font_size=20).move_to(rect.get_center())
            layer = VGroup(rect, label)
            if len(tcp_stack) > 0:
                layer.next_to(tcp_stack[-1], DOWN, buff=0)
            tcp_stack.add(layer)
        tcp_title = Text("TCP/IP Model\n(RFC1122)", **matrix_style.SUBHERO_STYLE).next_to(hero, DOWN, buff=1)
        tcp_stack.next_to(tcp_title, DOWN, buff=1)
        tcp_title.to_edge(RIGHT, buff=1)
        tcp_stack.to_edge(RIGHT, buff=1)

        # hybrid stack
        hybrid_stack = VGroup()
        for i, (name, color) in enumerate(zip(hybrid_layers, hybrid_colors)):
            match i:
                case 0:
                    h = 1.5
                case _:
                    h = 0.5
            rect = Rectangle(width=3, height=h, fill_opacity=0.2, color=color)
            label = Text(name, font_size=20).move_to(rect.get_center())
            layer = VGroup(rect, label)
            if len(hybrid_stack) > 0:
                layer.next_to(hybrid_stack[-1], DOWN, buff=0)
            hybrid_stack.add(layer)
        hybrid_title = Text("TCP/IP Model\n(Hybrid Mode)", **matrix_style.SUBHERO_STYLE).next_to(hero, DOWN, buff=1)
        hybrid_stack.next_to(hybrid_title, DOWN, buff=1)

        # animation
        self.play(Write(osi_title))
        self.play(Write(tcp_title))
        for layer in reversed(osi_stack):
            self.play(FadeIn(layer, shift=RIGHT * 0.2), run_time=0.4)
        for layer in reversed(tcp_stack):
            self.play(FadeIn(layer, shift=RIGHT * 0.2), run_time=0.4)

        self.wait(30)

        self.play(Write(hybrid_title))
        for layer in reversed(hybrid_stack):
            self.play(FadeIn(layer, shift=RIGHT * 0.2), run_time=0.4)

        self.wait(20)