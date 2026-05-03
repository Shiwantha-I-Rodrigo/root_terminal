import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDevices(Scene, CommonUtils):

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

        self.pcs = self.create_end_devices()
        self.ecs = self.create_extra_devices()

        device_names = ["hub","switch","router","firewall"]
        for name in device_names:
            self.play(FadeIn(self.pcs))
            device_group = self.create_device_node(name)
            connections = self.create_connections(device_group[0])
            self.play(FadeIn(device_group), Create(connections))
            
            if name == "hub":
                self.animate_hub_behavior(connections, device_group)
            elif name == "switch":
                self.animate_switch_behavior(connections, device_group)
            elif name == "router":
                self.animate_router_behavior(connections, device_group)
            elif name == "firewall":
                self.animate_firewall_behavior(connections, device_group)
            
        self.wait(1)

    def create_end_devices(self):
        colors = [SHOCK_PURPLE, CYBER_BLUE, NEON_YELLOW]
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
        apply_icon_style(switch, ALERT_AMBER)
        switch.move_to(RIGHT * 3)
        ecs.add(switch)
        pc1 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc1, SHOCK_PURPLE)
        pc1.move_to(RIGHT * 3 + UP * 2)
        ecs.add(pc1)
        pc2 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc2, CYBER_BLUE)
        pc2.move_to(RIGHT * 3 + DOWN * 2)
        ecs.add(pc2)

        switch2 = SVGMobject(str(self.assets_path / "switch.svg"))
        apply_icon_style(switch2, ALERT_AMBER)
        switch2.move_to(LEFT * 3)
        ecs.add(switch2)
        pc3 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc3, NEON_YELLOW)
        pc3.move_to(LEFT * 3 + UP * 2)
        ecs.add(pc3)
        pc4 = SVGMobject(str(self.assets_path / "device.svg"))
        apply_icon_style(pc4, GHOST_WHITE)
        pc4.move_to(LEFT * 3 + DOWN * 2)
        ecs.add(pc4)

        label = Text("Network-1.0/24", **self.amber_style.LABEL_STYLE).next_to(switch, LEFT + UP)
        label2 = Text("Network-2.0/24", **self.amber_style.LABEL_STYLE).next_to(switch2, RIGHT + UP)

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

        table_l = Table(left_data, col_labels=[Text("Port"), Text("MAC Address")], include_outer_lines=True).scale(0.3).to_edge(LEFT, buff=0.3)
        table_r = Table(right_data, col_labels=[Text("Port"), Text("MAC Address")], include_outer_lines=True).scale(0.3).to_edge(RIGHT, buff=0.2)

        ip_data = [
            ["192.168.1.0/24", "Gi0/0", "Direct"],
            ["192.168.2.0/24", "Gi0/1", "Direct"],
            ["0.0.0.0/0", "Wan0", "10.0.0.1"]
        ]

        routing_table = Table(ip_data, col_labels=[Text("Destination"), Text("Interface"), Text("Next Hop")], include_outer_lines=True).scale(0.3).to_edge(DOWN, buff=1.5)

        ecs.add(label, label2, table_l, table_r, routing_table)
        return ecs

    def create_device_node(self, name):
        obj = SVGMobject(str(self.assets_path / f"{name}.svg"))
        apply_icon_style(obj, ELECTRIC_RED)
        label = Text(name.title(), **self.red_style.LABEL_STYLE).next_to(obj, DOWN, buff=0.2)
        return VGroup(obj, label)

    def create_connections(self, source_obj):
        targets = [self.pcs[0].get_center(),self.pcs[1].get_center(),self.pcs[2].get_center()]
        return VGroup(*[Line(source_obj.get_center(), target,**self.matrix_style.LINE_STYLE) for target in targets])
    
    def create_extra_connections(self, source_obj):
        return VGroup(Line(self.ecs[0].get_center(), self.ecs[1].get_center(), **self.matrix_style.LINE_STYLE),
        Line(self.ecs[0].get_center(), self.ecs[2].get_center(), **self.matrix_style.LINE_STYLE),
        Line(self.ecs[3].get_center(), self.ecs[4].get_center(), **self.matrix_style.LINE_STYLE),
        Line(self.ecs[3].get_center(), self.ecs[5].get_center(), **self.matrix_style.LINE_STYLE),
        Line(source_obj.get_center(), self.ecs[3].get_center(), **self.matrix_style.LINE_STYLE),
        Line(source_obj.get_center(), self.ecs[0].get_center(), **self.matrix_style.LINE_STYLE))

    def animate_hub_behavior(self, connections, device_group):
        num_conns = len(connections.submobjects)
        style_map = {
            0: self.purple_style,
            1: self.blue_style,
            2: self.yellow_style
        }
        for _ in range(1):
            in_idx, out_idx, out_idz = random.sample(range(num_conns), 3)
            in_conn = connections.submobjects[in_idx]
            out_conx = connections.submobjects[out_idx]
            out_conz = connections.submobjects[out_idz]

            style = style_map.get(out_idx, self.matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)
            p_cp = p_in.copy()
            dot_color = p_in.get_color()

            self.play(MoveAlongPath(p_in, in_conn), run_time=0.8, rate_func=lambda t: 1 - t)
            self.play(Indicate(device_group[0], color=MATRIX_GREEN, scale_factor=1.1))
            self.play(MoveAlongPath(p_in, out_conx), MoveAlongPath(p_cp, out_conz), run_time=0.8, rate_func=linear)
            self.remove(p_in,p_cp)
        
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))

    def animate_switch_behavior(self, connections, device_group):
        num_conns = len(connections.submobjects)

        data = [
            ["Fa0/23", "E0:CB:4E:71:B2"],
            ["Fa0/24", "E0:CB:4E:71:B3"],
            ["Fa0/24", "FF:EE:DD:BB:02"]
        ]
        table_l = Table(data, col_labels=[Text("Port"), Text("MAC Address")], include_outer_lines=True).scale(0.3).to_edge(LEFT, buff=2).shift(UP*1)
        self.play(FadeIn(table_l))

        row_config = {
                0: (1, SHOCK_PURPLE),
                1: (2, CYBER_BLUE),
                2: (3, NEON_YELLOW),
            }

        style_map = {
            0: self.purple_style,
            1: self.blue_style,
            2: self.yellow_style
        }
        for _ in range(1):
            in_idx, out_idx, out_idz = random.sample(range(num_conns), 3)
            row_idx, row_color = row_config[out_idx]
            in_conn = connections.submobjects[in_idx]
            out_conx = connections.submobjects[out_idx]

            style = style_map.get(out_idx, self.matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)
            dot_color = p_in.get_color()

            self.play(MoveAlongPath(p_in, in_conn), run_time=0.8, rate_func=lambda t: 1 - t)
            self.play(table_l.get_rows()[row_idx].animate.set_color(row_color).scale(1.1), run_time=1, rate_func=smooth)
            self.play(Indicate(device_group[0], color=row_color, scale_factor=1.1))
            self.play(table_l.get_rows()[row_idx].animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)
            self.play(MoveAlongPath(p_in, out_conx), run_time=0.8, rate_func=linear)
            self.remove(p_in)
        
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))

    def animate_router_behavior(self, connections, device_group):
        self.play(FadeIn(self.ecs), FadeOut(self.pcs,connections))
        extra_connections = self.create_extra_connections(device_group[0])
        self.play(Create(extra_connections))

        style_map = {
            0: self.purple_style,
            1: self.blue_style,
            2: self.yellow_style,
            3: self.white_style
        }

        for _ in range(1):
            in_idx, out_idx = random.sample(range(4), 2)
            in_conn = extra_connections.submobjects[in_idx]
            out_conn = extra_connections.submobjects[out_idx]

            style = style_map.get(out_idx, self.matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)

            self.play(MoveAlongPath(p_in, in_conn), run_time=1, rate_func=lambda t: 1 - t)

            # configuration mappings for row indices and colors
            row_config = {
                0: (9, 1, SHOCK_PURPLE),
                1: (9, 2, CYBER_BLUE),
                2: (8, 1, NEON_YELLOW),
                3: (8, 2, GHOST_WHITE)
            }

            # indices to their respective "Entry" ECS objects and connection paths
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
                highlight0 = self.ecs[ecs_idx].get_rows()[row_idx]
                self.play(highlight0.animate.set_color(row_color).scale(1.1), run_time=1, rate_func=smooth)
                self.play(Indicate(in_data["ecs"], color=row_color, scale_factor=1.1))
                self.play(highlight0.animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)

            else:
                cross_row_idx = 3
                ecs_idx, row_idx, row_color = row_config[out_idx]
                target_row_10 = 1 if ecs_idx == 9 else (2 if ecs_idx == 8 else 3)
                highlight1 = self.ecs[in_idx < 2 and 9 or 8].get_rows()[cross_row_idx]
                self.play(highlight1.animate.set_color(ELECTRIC_RED).scale(1.1), run_time=1, rate_func=smooth)
                self.play(Indicate(in_data["ecs"], color=ELECTRIC_RED, scale_factor=1.1))
                self.play(highlight1.animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)
                self.play(MoveAlongPath(p_in, extra_connections[in_data["path_idx"]]), run_time=2, rate_func=lambda t: 1 - t)
                highlight2 = self.ecs[10].get_rows()[target_row_10]
                self.play(highlight2.animate.set_color(ALERT_AMBER).scale(1.1), run_time=1, rate_func=smooth)
                self.play(Indicate(device_group[0], color=ALERT_AMBER, scale_factor=1.1))
                self.play(highlight2.animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)
                self.play(MoveAlongPath(p_in, extra_connections[out_data["path_idx"]]), run_time=2, rate_func=linear)
                highlight3 = self.ecs[ecs_idx].get_rows()[row_idx]
                self.play(highlight3.animate.set_color(row_color).scale(1.1), run_time=1, rate_func=smooth)
                self.play(Indicate(out_data["ecs"], color=row_color, scale_factor=1.1))
                self.play(highlight3.animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)

            self.play(MoveAlongPath(p_in, out_conn), run_time=1, rate_func=linear)
            self.remove(p_in)

        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))
    
    def animate_firewall_behavior(self, connections, device_group):
        num_conns = len(connections.submobjects)

        data = [
            ["Fa0/23", "OUT", "ALLOW"],
            ["Fa0/25", "IN", "ALLOW"],
            ["Fa0/23", "IN", "DENY"],
            ["Fa0/25", "OUT", "ALLOW"],
            ["Fa0/24", "IN", "ALLOW"],
            ["ALL", "IN", "DENY"],
            ["ALL", "OUT", "DENY"]
        ]

        table_l = Table(data, col_labels=[Text("Port"), Text("Direction"), Text("Action")], include_outer_lines=True).scale(0.3).to_edge(LEFT, buff=2).shift(UP*1)
        self.play(FadeIn(table_l))

        traffic_rules = {
            "OUT_PORT": {
                0: (3, ELECTRIC_RED),
                1: (5, MATRIX_GREEN),
                2: (2, MATRIX_GREEN),
            },
            "IN_PORT": {
                0: (1, MATRIX_GREEN),
                1: (7, ELECTRIC_RED),
                2: (4, MATRIX_GREEN),
            }
        }

        style_map = {
            0: self.purple_style,
            1: self.blue_style,
            2: self.yellow_style
        }

        label0 = Text("fa0/23", **self.white_style.LABEL_STYLE).next_to(self.pcs[0], DOWN, buff=0.4)
        label1 = Text("fa0/24", **self.white_style.LABEL_STYLE).next_to(self.pcs[1], RIGHT + UP, buff=0.2)
        label2 = Text("fa0/25", **self.white_style.LABEL_STYLE).next_to(self.pcs[2], LEFT + UP, buff=0.2)
        labels = VGroup(label0, label1, label2)
        self.play(FadeIn(labels))

        for _ in range(1):
            in_idx, out_idx = random.sample(range(num_conns), 2)
            in_rule, in_color = traffic_rules["IN_PORT"][in_idx]
            out_rule, out_color = traffic_rules["OUT_PORT"][out_idx]
            in_conn = connections.submobjects[in_idx]
            out_conx = connections.submobjects[out_idx]

            style = style_map.get(out_idx, self.matrix_style)
            p_in = Dot(**style.DOT_STYLE).set_z_index(3)
            dot_color = p_in.get_color()

            self.play(MoveAlongPath(p_in, in_conn), run_time=0.8, rate_func=lambda t: 1 - t)
            self.play(table_l.get_rows()[in_rule].animate.set_color(in_color).scale(1.1), run_time=1, rate_func=smooth)
            self.play(Indicate(device_group[0], color=in_color, scale_factor=1.1))
            self.play(table_l.get_rows()[in_rule].animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)
            if in_color==MATRIX_GREEN:
                self.play(table_l.get_rows()[out_rule].animate.set_color(out_color).scale(1.1), run_time=1, rate_func=smooth)
                self.play(Indicate(device_group[0], color=out_color, scale_factor=1.1))
                self.play(table_l.get_rows()[out_rule].animate.set_color(GHOST_WHITE).scale(1/1.1), run_time=1, rate_func=smooth)
                if out_color==MATRIX_GREEN:
                    self.play(MoveAlongPath(p_in, out_conx), run_time=0.8, rate_func=linear)
            self.play(FadeOut(p_in))
        
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(self.hero))