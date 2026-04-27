from pathlib import Path
from manim import *
from config import *

class CommonUtils:
    def setup_scene(self):
        # self here refers to the NetworkingDevices instance
        self.camera.background_color = MATRIX_BLACK
        self.assets_path = Path(__file__).parent / "assets"

    def intro_animation(self, hero_text, subhero_text):
        self.hero = Text(hero_text, **matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(self.hero, DOWN)
        subhero_obj = Text(subhero_text, **matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        
        self.play(Write(self.hero), Create(underline), Write(subhero_obj))
        self.wait(1.5)
        self.play(
            FadeOut(underline), 
            FadeOut(subhero_obj), 
            self.hero.animate.to_edge(UP).scale(0.7)
        )
