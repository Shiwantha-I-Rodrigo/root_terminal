from pathlib import Path
from manim import *
from config import *

class CommonUtils:

    matrix_style = MatrixStyle()
    red_style = RedStyle()
    yellow_style = YellowStyle()
    blue_style = BlueStyle()
    purple_style = PurpleStyle()
    pink_style = PinkStyle()
    white_style = WhiteStyle()
    amber_style = AmberStyle()
    
    def setup_scene(self):
        self.camera.background_color = VOID_BLACK
        self.assets_path = Path(__file__).parent / "assets"

    def intro_animation(self, hero_text, subhero_text):
        self.hero = Text(hero_text, **self.matrix_style.HERO_STYLE)
        underline = Line(LEFT, RIGHT).scale(3).next_to(self.hero, DOWN)
        subhero_obj = Text(subhero_text, **self.matrix_style.SUBHERO_STYLE).next_to(underline, DOWN)
        
        self.play(Write(self.hero), Create(underline), Write(subhero_obj))
        self.wait(1.5)
        self.play(
            FadeOut(underline), 
            FadeOut(subhero_obj), 
            self.hero.animate.to_edge(UP).scale(0.7)
        )
