from manim import *
from config import *
from pathlib import Path
import random

class WANExplanation(Scene):
    def construct(self):
        self.camera.background_color = MATRIX_BLACK
        current_dir = Path(__file__).parent

        hero = Text("What is a WAN", **matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(hero, DOWN)
        subhero = Text("Wide Area Network", **matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        self.play(Write(hero), Create(underline), Write(subhero))
        self.wait(1.5)
        self.play(FadeOut(underline), FadeOut(subhero), hero.animate.to_edge(UP).scale(0.7))

        # Define the Cloud
        web_path = current_dir / "assets/web.svg"
        cloud = SVGMobject(str(web_path))
        apply_icon_style(cloud,GHOST_GRAY)
        cloud.set_z_index(3)

        building_path = current_dir / "assets/building.svg"
        # Site A
        site_a = VGroup(Dot(), Dot(), Dot()).arrange_in_grid(rows=1, buff=0.5)
        rect_a = SurroundingRectangle(site_a, color=MATRIX_GREEN)
        label_a = Text("Colombo Office", **matrix_style.LABEL_STYLE).next_to(rect_a, UP)
        building = SVGMobject(str(building_path))
        apply_icon_style(building,MATRIX_GREEN)
        building.next_to(label_a,UP)
        building.set_z_index(3)
        city_a = VGroup(building, site_a, rect_a, label_a).to_edge(LEFT,buff=1)

        # Site B
        site_b = VGroup(Dot(), Dot(), Dot()).arrange_in_grid(rows=1, buff=0.5)
        rect_b = SurroundingRectangle(site_b, color=CANDY_RED)
        label_b = Text("London Office", **red_style.LABEL_STYLE).next_to(rect_b, UP)
        building2 = SVGMobject(str(building_path))
        apply_icon_style(building2,CANDY_RED)
        building2.next_to(label_b,UP)
        building2.set_z_index(3)
        city_b = VGroup(building2, site_b, rect_b, label_b).to_edge(RIGHT,buff=1)

        # Connect the sites
        link_a = Line(rect_a.get_right(), rect_b.get_left(), color=GHOST_GRAY)
        wan_label = Text("WAN Connection", **matrix_style.LABEL_STYLE).next_to(cloud, DOWN)

        # Animations
        self.play(Create(cloud), Write(wan_label))
        self.wait(0.5)
        self.play(FadeIn(city_a), FadeIn(city_b))
        self.play(Create(link_a))
        self.wait(1)

        # Data Packet Simulation
        packet = Dot(**red_style.DOT_STYLE)
        packet2 = Dot(**matrix_style.DOT_STYLE)

        for i in range(15):
            mode = random.randint(0, 1)
            match mode:
                case 0:
                    self.play(MoveAlongPath(packet, link_a), run_time=5, rate_func=linear)
                    self.play(FadeOut(packet))
                case 1:
                    self.play(MoveAlongPath(packet2, link_a), run_time=3,  rate_func=lambda t: 1 - t)
                    self.play(FadeOut(packet2))

        self.wait(5)
