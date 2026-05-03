import random
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
    
    def stylize(self, title):
        title = "❯ " + title
        chars_list = []
        ref_char = Text("A", font=CLI_FONT, font_size=24) 
        for char in title:
            if char == " ":
                c = Text("_", font=CLI_FONT, font_size=24, color=MATRIX_GREEN)
            else:
                c = Text(char, font=CLI_FONT, font_size=24, color=MATRIX_GREEN)
            c.align_to(ref_char, DOWN)
            chars_list.append(c)
        text_chars = VGroup(*chars_list)
        text_chars.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        self.add(text_chars)
        return text_chars

    def intro_animation(self, title, subtitle_text):
        title = "❯ " + title
        chars_list = []
        ref_char = Text("A", font=CLI_FONT, font_size=24) 
        for char in title:
            if char == " ":
                c = Text("_", font=CLI_FONT, font_size=24, color=MATRIX_GREEN).set_opacity(0)
            else:
                c = Text(char, font=CLI_FONT, font_size=24, color=MATRIX_GREEN)
            c.align_to(ref_char, DOWN)
            chars_list.append(c)
        text_chars = VGroup(*chars_list)
        text_chars.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        for i, char in enumerate(text_chars):
            if title[i] != " ":
                char.set_fill(opacity=0)
        subtitle = Text(subtitle_text, font=CLI_FONT, font_size=16, color=MATRIX_GREEN)
        subtitle.next_to(text_chars, DOWN, buff=0.4)
        cursor = Text("█", font=CLI_FONT, font_size=24, color=MATRIX_GREEN)  
        char_index = ValueTracker(0)

        def sync_terminal_updater(obj):
            idx = int(char_index.get_value())
            for i, char in enumerate(obj):
                if title[i] != " ":
                    char.set_fill(opacity=1 if i < idx else 0)
            if idx == 0:
                cursor.next_to(obj[0], LEFT, buff=0.05)
            elif idx < len(obj):
                cursor.next_to(obj[idx-1], RIGHT, buff=0.05)
            else:
                cursor.next_to(obj[-1], RIGHT, buff=0.05)
            cursor.align_to(ref_char, DOWN)

        cursor.add_updater(lambda m, dt: m.set_fill(opacity=1 if int(self.time * 3) % 2 == 0 else 0))
        text_chars.add_updater(sync_terminal_updater)
        self.add(text_chars, cursor)
        self.wait(1)
        self.play(char_index.animate.set_value(len(text_chars)), run_time=5, rate_func=linear)
        text_chars.remove_updater(sync_terminal_updater)
        for char in text_chars:
            if char.get_fill_opacity() > 0 or True:
                char.set_fill(opacity=1)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle),FadeOut(cursor),run_time=1.5)
        text_chars.generate_target()
        text_chars.target.scale(0.7)
        text_chars.target.to_edge(UL, buff=0.5)
        self.play(MoveToTarget(text_chars), run_time=1.5)
        return text_chars
    
    def create_node(self, node_type, pos=ORIGIN, color=MATRIX_GREEN, z_index=3):
        file_path = str(self.assets_path / f"{node_type}.svg")
        node = SVGMobject(file_path)
        node.move_to(ORIGIN)
        max_dimension = 1.0
        node.scale(max_dimension / max(node.width, node.height))
        apply_icon_style(node, color)
        node.set_z_index(z_index)
        node.move_to(pos)
        return node

    def connect(self, node_a, node_b, **style):
        final_style = style if style else self.matrix_style.LINE_STYLE
        return Line(node_a.get_center(), node_b.get_center(), **final_style)
    
    def connect_wifi(self, start, end, amplitude=0.1, waves=10):
        start = start.get_center()
        end = end.get_center()
        dist = np.linalg.norm(end - start)
        angle = angle_of_vector(end - start)
        wavy_line = ParametricFunction(
            lambda t: [t, amplitude * np.sin(waves * TAU * t / dist), 0],
            t_range=[0, dist],
            color=MATRIX_GREEN,
            stroke_width=1
        )
        wavy_line.rotate(angle, about_point=ORIGIN)
        wavy_line.move_to((start+ end) / 2)
        return wavy_line

    def create_table(self, table_data, row_labels=None, col_labels=None, pos=ORIGIN):
        rows = [Text(str(r)) for r in row_labels] if row_labels else None
        cols = [Text(str(c)) for c in col_labels] if col_labels else None
        table = Table(table_data, row_labels=rows, col_labels=cols, include_outer_lines=True, line_config={"stroke_width": 1, "color": MATRIX_GREEN}).scale(0.2).move_to(pos)
        table.get_entries().set_font_size(18)
        if col_labels:
            table.get_columns()[1].set_color(GREEN)
            table.get_columns()[2].set_color(RED)
        return table
    
    def random_data(self, connections, loops):
        packet = Dot(**self.matrix_style.DOT_STYLE).set_z_index(3)
        for i in range(loops):
            in_idx, out_idx, out_idz = random.sample(range(len(connections.submobjects)), 3)
            if random.choice([True, False]):
                self.play(MoveAlongPath(packet, connections[in_idx]), run_time=0.5, rate_func=lambda t: 1 - t)
                packet_copy = packet.copy()
                self.play(MoveAlongPath(packet, connections[out_idx]), MoveAlongPath(packet_copy, connections[out_idz]), run_time=0.8, rate_func=linear)
                self.remove(packet, packet_copy)
            else:
                self.play(MoveAlongPath(packet, connections[in_idx]), run_time=0.5, rate_func=lambda t: 1 - t)
                self.play(MoveAlongPath(packet, connections[out_idx]), run_time=0.5, rate_func=linear)
                self.remove(packet)
