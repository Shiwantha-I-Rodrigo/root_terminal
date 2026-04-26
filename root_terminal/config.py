from manim import *

MATRIX_GREEN = "#00FF41"
MATRIX_DARK = "#003B00"
MATRIX_BLACK = "#0D0D0D"
GLITCH_GOLD = "#FFD700"
CANDY_RED = "#D21404"
ELECTRIC_LIME = "#CCFF00"
GHOST_GRAY = GRAY

def apply_icon_style(svg_obj,color):
    svg_obj.set_width(0.8)
    svg_obj.set_color(WHITE)
    svg_obj.set_fill(color, opacity=0.7)
    svg_obj.set_stroke(width=1)
    return svg_obj

class matrix_style:
    # "Liberation Mono" / "Source Code Pro" / "Hack"
    HERO_STYLE = {
        "font": "Hack",
        "font_size": 40,
        "color": MATRIX_GREEN,
        "fill_opacity": 1,
        "stroke_width": 1,
    }

    SUBHERO_STYLE = {
        "font": "Hack",
        "font_size": 30,
        "color": MATRIX_GREEN,
        "weight": BOLD,
    }

    TITLE_STYLE = {
        "font": "Hack",
        "font_size": 24,
        "color": MATRIX_GREEN,
        "weight": BOLD,
    }

    SUBTITLE_STYLE = {
        "font": "Hack",
        "font_size": 18,
        "color": MATRIX_GREEN,
        "weight": BOLD,
    }

    LABEL_STYLE = {
        "font": "Hack",
        "font_size": 12,
        "color": MATRIX_GREEN,
        "weight": BOLD,
    }

    LINE_STYLE = {
        "stroke_color": MATRIX_GREEN,
        "stroke_width": 2,
        "buff": 0.1,
    }

    DOT_STYLE = {
        "radius": 0.15,
        "color": MATRIX_GREEN,
        "fill_opacity": 0.8,
        "stroke_width": 2,
        "stroke_color": WHITE,
    }

class fire_style:
    # "Liberation Mono" / "Source Code Pro" / "Hack"
    HERO_STYLE = {
        "font": "Hack",
        "font_size": 40,
        "color": CANDY_RED,
        "fill_opacity": 1,
        "stroke_width": 1,
    }

    SUBHERO_STYLE = {
        "font": "Hack",
        "font_size": 30,
        "color": CANDY_RED,
        "weight": BOLD,
    }

    TITLE_STYLE = {
        "font": "Hack",
        "font_size": 24,
        "color": CANDY_RED,
        "weight": BOLD,
    }

    SUBTITLE_STYLE = {
        "font": "Hack",
        "font_size": 18,
        "color": CANDY_RED,
        "weight": BOLD,
    }

    LABEL_STYLE = {
        "font": "Hack",
        "font_size": 12,
        "color": CANDY_RED,
        "weight": BOLD,
    }

    LINE_STYLE = {
        "stroke_color": CANDY_RED,
        "stroke_width": 2,
        "buff": 0.1,
    }

    DOT_STYLE = {
        "radius": 0.15,
        "color": CANDY_RED,
        "fill_opacity": 0.8,
        "stroke_width": 2,
        "stroke_color": WHITE,
    }

class gold_style:
    # "Liberation Mono" / "Source Code Pro" / "Hack"
    HERO_STYLE = {
        "font": "Hack",
        "font_size": 40,
        "color": GLITCH_GOLD,
        "fill_opacity": 1,
        "stroke_width": 1,
    }

    SUBHERO_STYLE = {
        "font": "Hack",
        "font_size": 30,
        "color": GLITCH_GOLD,
        "weight": BOLD,
    }

    TITLE_STYLE = {
        "font": "Hack",
        "font_size": 24,
        "color": GLITCH_GOLD,
        "weight": BOLD,
    }

    SUBTITLE_STYLE = {
        "font": "Hack",
        "font_size": 18,
        "color": GLITCH_GOLD,
        "weight": BOLD,
    }

    LABEL_STYLE = {
        "font": "Hack",
        "font_size": 12,
        "color": GLITCH_GOLD,
        "weight": BOLD,
    }

    LINE_STYLE = {
        "stroke_color": GLITCH_GOLD,
        "stroke_width": 2,
        "buff": 0.1,
    }

    DOT_STYLE = {
        "radius": 0.15,
        "color": GLITCH_GOLD,
        "fill_opacity": 0.8,
        "stroke_width": 2,
        "stroke_color": WHITE,
    }