import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkingDevices(Scene, CommonUtils):
    def construct(self):
        self.setup_scene() 
        self.intro_animation("Networking Devices", "Controlling the Flow of Data")

        self.pcs = self.create_end_devices()
        self.ecs = self.create_extra_devices()

        device_names = ["hub","switch","router","firewall"]
        for name in device_names:
            self.play(FadeIn(self.pcs))
            device_group = self.create_device_node(name)
            connections = self.create_connections(device_group[0])
            self.play(FadeIn(device_group), Create(connections))
            
            if name == "hub":
                self.animate_hub_behavior(connections)
            elif name == "switch":
                self.animate_switch_behavior(connections, device_group)
            elif name == "router":
                self.animate_router_behavior(connections, device_group)
            elif name == "firewall":
                self.animate_firewall_behavior(connections)
            
            self.wait(1)

    def create_end_devices(self):
        colors = [POINT_PURPLE, CANDY_RED, GLITCH_GOLD]
        positions = [UP * 2, LEFT * 2 + DOWN * 1.5, RIGHT * 2 + DOWN * 1.5]
        pcs = VGroup()
        for color, pos in zip(colors, positions):
            pc = SVGMobject(str(self.assets_path / "device.svg"))
            apply_icon_style(pc, color)
            pc.move_to(pos)
            pcs.add(pc)
        return pcs
    
    def create_extra_devices(self):
        ecs = VGroup()
        switch = SVGMobject(str(self.assets_path / "switch.svg"))
        apply_icon_style(switch, GHOST_GRAY)
        switch.move_to(RIGHT * 4)
        ecs.add(switch)
        pc1 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc1, POINT_PURPLE)
        pc1.move_to(RIGHT * 4 + UP * 2)
        ecs.add(pc1)
        pc2 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc2, CANDY_RED)
        pc2.move_to(RIGHT * 4 + DOWN * 2)
        ecs.add(pc2)

        switch2 = SVGMobject(str(self.assets_path / "switch.svg"))
        apply_icon_style(switch2, GHOST_GRAY)
        switch2.move_to(LEFT * 4)
        ecs.add(switch2)
        pc3 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc3, GLITCH_GOLD)
        pc3.move_to(LEFT * 4 + UP * 2)
        ecs.add(pc3)
        pc4 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc4, BABY_BLUE)
        pc4.move_to(LEFT * 4 + DOWN * 2)
        ecs.add(pc4)

        label = Text("Switch", **matrix_style.LABEL_STYLE).next_to(switch, LEFT + UP)
        label2 = Text("Switch", **matrix_style.LABEL_STYLE).next_to(switch2, RIGHT + UP)

        left_data = [
            ["Fa0/1", "00:0A:95:68:16"],
            ["Fa0/2", "00:0A:95:68:17"],
            ["Gi0/1", "AA:BB:CC:EE:01 (GW)"]
        ]
        right_data = [
            ["Fa0/23", "E0:CB:4E:71:B2"],
            ["Fa0/24", "E0:CB:4E:71:B3"],
            ["Gi0/2", "FF:EE:DD:BB:02 (GW)"]
        ]
        table_l = Table(
            left_data,
            col_labels=[Text("Port"), Text("MAC Address")],
            include_outer_lines=True
        ).scale(0.2).to_edge(LEFT, buff=0.2)
        table_r = Table(
            right_data,
            col_labels=[Text("Port"), Text("MAC Address")],
            include_outer_lines=True
        ).scale(0.2).to_edge(RIGHT, buff=0.2)

        ip_data = [
            ["192.168.1.0/24", "Gi0/0", "Direct"],
            ["192.168.2.0/24", "Gi0/1", "Direct"],
            ["0.0.0.0/0", "Wan0", "10.0.0.1"]
        ]
        routing_table = Table(
            ip_data,
            col_labels=[Text("Destination"), Text("Interface"), Text("Next Hop")],
            include_outer_lines=True
        ).scale(0.2).to_edge(DOWN, buff=2.2)

        ecs.add(label, label2, table_l, table_r, routing_table)
        return ecs

    def create_device_node(self, name):
        obj = SVGMobject(str(self.assets_path / f"{name}.svg"))
        apply_icon_style(obj, MATRIX_GREEN)
        label = Text(name.title(), **matrix_style.LABEL_STYLE).next_to(obj, DOWN, buff=0.2)
        return VGroup(obj, label).center()

    def create_connections(self, source_obj):
        targets = [self.pcs[0].get_bottom(),self.pcs[1].get_corner(UR),self.pcs[2].get_corner(UL)]
        return VGroup(*[Line(source_obj.get_center(), target, color=MATRIX_GREEN, stroke_opacity=0.5) for target in targets])
    
    def create_extra_connections(self, source_obj):
        return VGroup(Line(self.ecs[0].get_top(), self.ecs[1].get_bottom(), color=MATRIX_GREEN, stroke_opacity=0.5),
        Line(self.ecs[0].get_bottom(), self.ecs[2].get_top(), color=MATRIX_GREEN, stroke_opacity=0.5),
        Line(self.ecs[3].get_top(), self.ecs[4].get_bottom(), color=MATRIX_GREEN, stroke_opacity=0.5),
        Line(self.ecs[3].get_bottom(), self.ecs[5].get_top(), color=MATRIX_GREEN, stroke_opacity=0.5),
        Line(source_obj.get_center(), self.ecs[3].get_right(), color=MATRIX_GREEN, stroke_opacity=0.5),
        Line(source_obj.get_center(), self.ecs[0].get_left(), color=MATRIX_GREEN, stroke_opacity=0.5))

    def animate_hub_behavior(self, connections):
        for _ in range(3):
            in_conn = random.choice(connections.submobjects)
            out_conns = [c for c in connections.submobjects if c is not in_conn]
            
            p_in = Dot(**matrix_style.DOT_STYLE).set_z_index(3)
            self.play(MoveAlongPath(p_in, in_conn), run_time=0.8, rate_func=lambda t: 1 - t)
            self.remove(p_in)
            p_outs = [Dot(**matrix_style.DOT_STYLE).set_z_index(3) for _ in out_conns]
            self.play(*[MoveAlongPath(p, conn) for p, conn in zip(p_outs, out_conns)],run_time=0.8, rate_func=linear)
            self.remove(*p_outs)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))

    def animate_switch_behavior(self, connections, device_group):
        num_conns = len(connections.submobjects)
        style_map = {
            0: purple_style,
            1: red_style,
            2: gold_style
        }
        for _ in range(3):
            in_idx, out_idx = random.sample(range(num_conns), 2)
            in_conn = connections.submobjects[in_idx]
            out_conn = connections.submobjects[out_idx]

            style = style_map.get(out_idx, matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)
            dot_color = p_in.get_color()

            self.play(MoveAlongPath(p_in, in_conn), run_time=0.8, rate_func=lambda t: 1 - t)
            self.play(Indicate(device_group[0], color=dot_color, scale_factor=1.5))
            self.play(MoveAlongPath(p_in, out_conn), run_time=0.8, rate_func=linear)
            self.remove(p_in)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))

    def animate_router_behavior(self, connections, device_group):
        self.wait(5)
        self.play(FadeIn(self.ecs), FadeOut(self.pcs,connections))
        extra_connections = self.create_extra_connections(device_group[0])
        self.play(Create(extra_connections))

        style_map = {
            0: purple_style,
            1: red_style,
            2: gold_style,
            3: blue_style
        }

        for _ in range(10):
            in_idx, out_idx = random.sample(range(4), 2)
            in_conn = extra_connections.submobjects[in_idx]
            out_conn = extra_connections.submobjects[out_idx]

            style = style_map.get(out_idx, matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)

            self.play(MoveAlongPath(p_in, in_conn), run_time=1, rate_func=lambda t: 1 - t)

            # Define configuration mappings for row indices and colors
            row_config = {
                0: (9, 1, POINT_PURPLE),
                1: (9, 2, CANDY_RED),
                2: (8, 1, GLITCH_GOLD),
                3: (8, 2, BABY_BLUE)
            }

            # Map indices to their respective "Entry" ECS objects and connection paths
            group_map = {
                2: {"ecs": self.ecs[3], "path_idx": 4},
                3: {"ecs": self.ecs[3], "path_idx": 4},
                0: {"ecs": self.ecs[0], "path_idx": 5},
                1: {"ecs": self.ecs[0], "path_idx": 5}
            }

            in_data = group_map[in_idx]
            out_data = group_map[out_idx]
            same_group = (in_idx in {2, 3}) == (out_idx in {2, 3})

            if same_group:
                ecs_idx, row_idx, row_color = row_config[out_idx]
                self.play(Indicate(self.ecs[ecs_idx].get_rows()[row_idx], color=row_color, scale_factor=1.1), Indicate(in_data["ecs"], color=row_color, scale_factor=1.1))

            else:
                cross_row_idx = 3
                ecs_idx, row_idx, row_color = row_config[out_idx]
                target_row_10 = 1 if ecs_idx == 9 else (2 if ecs_idx == 8 else 3)
                self.play(Indicate(self.ecs[in_idx < 2 and 9 or 8].get_rows()[cross_row_idx], color=MATRIX_GREEN, scale_factor=1.1), Indicate(in_data["ecs"], color=MATRIX_GREEN, scale_factor=1.5))
                self.play(MoveAlongPath(p_in, extra_connections[in_data["path_idx"]]), run_time=2, rate_func=lambda t: 1 - t)
                self.play(Indicate(device_group[0], color=MATRIX_GREEN, scale_factor=1.1), Indicate(self.ecs[10].get_rows()[target_row_10], color=MATRIX_GREEN, scale_factor=1.1))
                self.play(MoveAlongPath(p_in, extra_connections[out_data["path_idx"]]), run_time=2, rate_func=linear)
                self.play(Indicate(out_data["ecs"], color=row_color, scale_factor=1.1), Indicate(self.ecs[ecs_idx].get_rows()[row_idx], color=row_color, scale_factor=1.1))

            self.play(MoveAlongPath(p_in, out_conn), run_time=1, rate_func=linear)
            self.remove(p_in)

        self.wait(5)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))
    
    def animate_firewall_behavior(self, connections):
        pass