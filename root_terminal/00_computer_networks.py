from manim import *
from config import *
from pathlib import Path
import random

class Network(Scene):
    def construct(self):

        matrix_style = MatrixStyle()
        red_style = RedStyle()
        yellow_style = YellowStyle()
        blue_style = BlueStyle()
        purple_style = PurpleStyle()
        pink_style = PinkStyle()
        white_style = WhiteStyle()
        amber_style = AmberStyle()

        self.camera.background_color = VOID_BLACK
        current_dir = Path(__file__).parent

        hero = Text("What is a Network?", **matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(hero, DOWN)
        subhero = Text("(Computer Networks)", **matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        self.play(Write(hero), Create(underline), Write(subhero))
        self.wait(1.5)
        self.play(FadeOut(underline), FadeOut(subhero), hero.animate.to_edge(UP).scale(0.7))

        # Define Nodes
        hub = 0
        star_nodes = [1, 2, 3, 4, 5]
        branch_a = [6, 7]  # From node 1
        branch_b = [8, 9]  # From node 3
        all_vertices = [hub] + star_nodes + branch_a + branch_b
        
        # Define Edges
        edges = []
        for n in star_nodes:
            edges.append((hub, n))
        for n in branch_a:
            edges.append((1, n))
        for n in branch_b:
            edges.append((3, n))

        layout = {
            0: DOWN * 0.5,
            1: UP * 1.5 + DOWN * 0.5,
            2: UR * 2 + DOWN * 0.5,
            3: RIGHT * 2 + DOWN * 0.5,
            4: DL * 2 + DOWN * 0.5,
            5: LEFT * 2 + DOWN * 0.5,
            # Branch A
            6: UP * 2.5 + LEFT * 0.7 + DOWN * 0.5,
            7: UP * 2.5 + RIGHT * 0.7 + DOWN * 0.5,
            # Branch B
            8: RIGHT * 3.2 + UP * 0.3 + DOWN * 0.5,
            9: RIGHT * 3.2 + DOWN * 0.3 + DOWN * 0.5,
        }

        network = Graph(
            all_vertices, 
            edges, 
            layout=layout,
            vertex_config={"fill_color": MATRIX_GREEN, "radius": 0.15},
            edge_config={"stroke_width": 3, "stroke_color": GRAY_A}
        )

        self.play(Create(network), run_time=3)

        vertex_objects = list(network.vertices.values())

        MCOLORS = [
            MATRIX_GREEN, ELECTRIC_RED, NEON_YELLOW, 
            CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE, VAPOR_PINK, ALERT_AMBER
        ]

        flashes = [
            Indicate(random.choice(vertex_objects), color=random.choice(MCOLORS), scale_factor=1.5) 
            for _ in range(120)
        ]

        self.play(
            AnimationGroup(*flashes, lag_ratio=0.5),
            run_time=60
        )

        self.wait(10)