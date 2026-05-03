from manim import *

VOID_BLACK = "#0D0D0D"
MATRIX_GREEN = "#00FF41"
ELECTRIC_RED = "#FF3131"
NEON_YELLOW = "#FFF01F"
CYBER_BLUE = "#00F0FF"
SHOCK_PURPLE = "#BF00FF"
GHOST_WHITE = "#F8F8FF"
VAPOR_PINK = "#FF00FF"
ALERT_AMBER = "#FF8C00"

CLI_FONT = "Hack"

def apply_icon_style(svg_obj,color):
    svg_obj.set_color(GHOST_WHITE)
    svg_obj.set_fill(color, opacity=0.3)
    svg_obj.set_stroke(width=1)
    return svg_obj

class BaseStyle:
    COLOR = GHOST_WHITE

    @property
    def HERO_STYLE(self):
        return {
            "font": CLI_FONT,
            "font_size": 40,
            "color": self.COLOR,
            "fill_opacity": 1,
            "stroke_width": 1,
        }

    @property
    def SUBHERO_STYLE(self):
        return {
            "font": CLI_FONT,
            "font_size": 30,
            "color": self.COLOR,
            "weight": BOLD,
        }

    @property
    def TITLE_STYLE(self):
        return {
            "font": CLI_FONT,
            "font_size": 24,
            "color": self.COLOR,
            "weight": BOLD,
        }

    @property
    def SUBTITLE_STYLE(self):
        return {
            "font": CLI_FONT,
            "font_size": 18,
            "color": self.COLOR,
            "weight": BOLD,
        }

    @property
    def LABEL_STYLE(self):
        return {
            "font": CLI_FONT,
            "font_size": 12,
            "color": self.COLOR,
            "weight": BOLD,
        }

    @property
    def LINE_STYLE(self):
        return {
            "stroke_color": self.COLOR,
            "stroke_width": 1,
            "stroke_opacity":0.3,
        }

    @property
    def DOT_STYLE(self):
        return {
            "radius": 0.1,
            "color": self.COLOR,
            "fill_opacity": 0.4,
            "stroke_width": 1,
            "stroke_color": WHITE,
        }

class MatrixStyle(BaseStyle):
    COLOR = MATRIX_GREEN

class RedStyle(BaseStyle):
    COLOR = ELECTRIC_RED

class YellowStyle(BaseStyle):
    COLOR = NEON_YELLOW

class BlueStyle(BaseStyle):
    COLOR = CYBER_BLUE

class PurpleStyle(BaseStyle):
    COLOR = SHOCK_PURPLE

class PinkStyle(BaseStyle):
    COLOR = VAPOR_PINK

class WhiteStyle(BaseStyle):
    COLOR = GHOST_WHITE

class AmberStyle(BaseStyle):
    COLOR = ALERT_AMBER
