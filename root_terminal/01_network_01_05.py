import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDesign(Scene, CommonUtils):

    # Network Devices
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
        section_01 = self.stylize("NETWORK DESIGN/DEVICES").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeIn(section_01))

        # legend
        legend = self.set_legend()
        pointer = Triangle(color=MATRIX_GREEN).scale(0.1).rotate(-90 * DEGREES)
        pointer.next_to(legend[0], LEFT, buff=0.2)
        self.play(FadeIn(legend, pointer))

        # hub
        hub = self.get_hub_switch("hub")
        self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        self.play(
            Create(hub["center"]),
            Create(hub["connections"]),
            FadeIn(hub["nodes"]),
            run_time=2
        )
        self.animate_hub(hub, 1)
        self.play(FadeOut(hub["all"]))

        # switch
        switch = self.get_hub_switch("switch")
        self.play(pointer.animate.next_to(legend[1], LEFT, buff=0.2))
        self.play(
            Create(switch["center"]),
            Create(switch["connections"]),
            FadeIn(switch["nodes"]),
            Create(switch["subnet"]),
            run_time=2
        )
        self.animate_switch(switch, 1)
        self.play(FadeOut(switch["all"]))

        # switchL3
        switchL3 = self.get_switchL3("switchL3")
        self.play(pointer.animate.next_to(legend[2], LEFT, buff=0.2))
        self.play(
            Create(switchL3["center"]),
            Create(switchL3["connections"]),
            FadeIn(switchL3["nodes"]),
            Create(switchL3["subnet"]),
            run_time=2
        )
        self.animate_switchL3(switchL3, 1)
        self.play(FadeOut(switchL3["all"]))

        # router
        router = self.get_router("router")
        self.play(pointer.animate.next_to(legend[3], LEFT, buff=0.2))
        self.play(
            Create(router["center"]),
            Create(router["connections"]),
            FadeIn(router["nodes"]),
            Create(router["subnet"]),
            run_time=2
        )
        self.animate_router(router, 1)
        self.play(FadeOut(router["all"]))

        # firewall
        firewall = self.get_firewall("firewall")
        self.play(pointer.animate.next_to(legend[4], LEFT, buff=0.2))
        self.play(
            Create(firewall["center"]),
            Create(firewall["connections"]),
            FadeIn(firewall["nodes"]),
            Create(firewall["subnet"]),
            run_time=2
        )
        self.animate_firewall(firewall, 1)
        self.play(FadeOut(firewall["all"]))

        # ids
        ids = self.get_ids()
        self.play(pointer.animate.next_to(legend[5], LEFT, buff=0.2))
        self.play(
            Create(ids["center"]),
            Create(ids["connections"]),
            FadeIn(ids["nodes"]),
            FadeIn(ids["labels"]),
            run_time=2
        )
        self.animate_ids(ids, 1)
        self.play(FadeOut(ids["all"]))

        # ips
        ips = self.get_ips()
        self.play(pointer.animate.next_to(legend[6], LEFT, buff=0.2))
        self.play(
            Create(ips["center"]),
            Create(ips["connections"]),
            FadeIn(ips["nodes"]),
            FadeIn(ips["labels"]),
            run_time=2
        )
        self.animate_ips(ips, 1)
        self.play(FadeOut(ips["all"]))

        # ap
        ap = self.get_ap()
        self.play(pointer.animate.next_to(legend[7], LEFT, buff=0.2))
        self.play(
            Create(ap["center"]),
            Create(ap["connections"]),
            FadeIn(ap["nodes"]),
            FadeIn(ap["labels"]),
            run_time=2
        )
        self.animate_ap(ap, 5)
        self.play(FadeOut(ap["all"]))


    def set_legend(self):
        labels = [ "I. Hub", "II. Switch", "III. L3 Switch", "IV. Router", "V. Firewall", "VI. IDS", "VII. IPS", "VIII. Access Point"]
        legend_items = VGroup(*[Text(label, **self.matrix_style.LABEL_STYLE) for label in labels])
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        legend_items.to_edge(LEFT, buff=1)
        return legend_items

    def get_hub_switch(self, device_type):
        center = self.create_node(device_type).shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE]
        node_count = 3
        radius = 2.5
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        subnet_area = RoundedRectangle(corner_radius=0.1, color=MATRIX_GREEN, fill_opacity=0.05).surround(VGroup(nodes[0],nodes[1],nodes[2]), stretch=True, buff=1)
        label = Text("Subnet A (192.168.1.10/24)", **self.matrix_style.LABEL_STYLE).next_to(subnet_area, LEFT)
        return {"center": center, "nodes": nodes, "connections": connections, "subnet": VGroup(subnet_area, label), "all": VGroup(center, nodes, connections, subnet_area, label)}

    def animate_hub(self, hub, loops):
        connections = hub["connections"].submobjects
        num_conns = len(connections)
        styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        if num_conns < 2:
            return
        for _ in range(loops):
            indices = list(range(num_conns))
            sender_idx = random.choice(indices)
            potential_targets = [i for i in indices if i != sender_idx]
            target_idx = random.choice(potential_targets)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
            out_packets = VGroup(*[Dot(**target_style.DOT_STYLE).set_z_index(3).move_to(hub["center"].get_center()) for _ in potential_targets])
            self.play(*[MoveAlongPath(p, connections[idx], rate_func=linear) for p, idx in zip(out_packets, potential_targets)], FadeOut(packet, shift=ORIGIN), run_time=1)
            self.play(FadeOut(out_packets))
            self.wait(1)

    def animate_switch(self, switch, loops):
        connections = switch["connections"].submobjects
        num_conns = len(connections)
        styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        if num_conns < 2:
            return
        for _ in range(loops):
            indices = list(range(num_conns))
            sender_idx = random.choice(indices)
            potential_targets = [i for i in indices if i != sender_idx]
            target_idx = random.choice(potential_targets)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
            self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
            self.play(FadeOut(packet))
            self.wait(1)
    
    def get_switchL3(self, device_type):
        center = self.create_node(device_type).shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE]
        node_count = 3
        radius = 2.5
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        subnet_area_1 = RoundedRectangle(corner_radius=0.1, color=MATRIX_GREEN, fill_opacity=0.05).surround(VGroup(nodes[0],nodes[1]), stretch=True, buff=1)
        label_1 = Text("Subnet A (192.168.1.10/24)", **self.matrix_style.LABEL_STYLE).next_to(subnet_area_1, UP)
        subnet_area_2 = RoundedRectangle(corner_radius=0.1, color=SHOCK_PURPLE, fill_opacity=0.05).surround(VGroup(nodes[2]), stretch=True, buff=1)
        label_2 = Text("Subnet B (192.168.1.20/24)", **self.purple_style.LABEL_STYLE).next_to(subnet_area_2, LEFT)
        return {"center": center, "nodes": nodes, "connections": connections, "subnet": VGroup(subnet_area_1, label_1,subnet_area_2, label_2), "all": VGroup(center, nodes, connections, subnet_area_1, label_1,subnet_area_2, label_2)}
    
    def animate_switchL3(self, switchL3, loops):
        connections = switchL3["connections"].submobjects
        num_conns = len(connections)
        styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        if num_conns < 2:
            return
        for _ in range(loops):
            indices = list(range(num_conns))
            sender_idx = random.choice(indices)
            potential_targets = [i for i in indices if i != sender_idx]
            target_idx = random.choice(potential_targets)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
            self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
            self.play(FadeOut(packet))
            self.wait(1)
    
    def get_router(self, device_type):
        center = self.create_node(device_type).shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE]
        node_count = 3
        radius = 2.5
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        subnet_area_1 = RoundedRectangle(corner_radius=0.1, color=NEON_YELLOW, fill_opacity=0.05).surround(VGroup(nodes[0]), stretch=True, buff=1)
        label_1 = Text("Subnet A (192.168.1.10/24)", **self.yellow_style.LABEL_STYLE).next_to(subnet_area_1, UP)
        subnet_area_2 = RoundedRectangle(corner_radius=0.1, color=CYBER_BLUE, fill_opacity=0.05).surround(VGroup(nodes[1]), stretch=True, buff=1)
        label_2 = Text("Subnet B (192.168.1.20/24)", **self.blue_style.LABEL_STYLE).next_to(subnet_area_2, LEFT)
        subnet_area_3 = RoundedRectangle(corner_radius=0.1, color=SHOCK_PURPLE, fill_opacity=0.05).surround(VGroup(nodes[2]), stretch=True, buff=1)
        label_3 = Text("Subnet C (192.168.1.30/24)", **self.purple_style.LABEL_STYLE).next_to(subnet_area_3, LEFT)
        return {"center": center, "nodes": nodes, "connections": connections, "subnet": VGroup(subnet_area_1, label_1,subnet_area_2, label_2,subnet_area_3, label_3), "all": VGroup(center, nodes, connections, subnet_area_1, label_1,subnet_area_2, label_2,subnet_area_3, label_3)}
    
    def animate_router(self, router, loops):
        connections = router["connections"].submobjects
        num_conns = len(connections)
        styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        if num_conns < 2:
            return
        for _ in range(loops):
            indices = list(range(num_conns))
            sender_idx = random.choice(indices)
            potential_targets = [i for i in indices if i != sender_idx]
            target_idx = random.choice(potential_targets)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
            self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
            self.play(FadeOut(packet))
            self.wait(1)

    def get_firewall(self, device_type):
        center = self.create_node(device_type).shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, SHOCK_PURPLE, GHOST_WHITE]
        node_count = 3
        radius = 2.5
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos) if i!= 2 else self.create_node("web").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        subnet_area_1 = RoundedRectangle(corner_radius=0.1, color=MATRIX_GREEN, fill_opacity=0.05).surround(VGroup(nodes[0],nodes[1]), stretch=True, buff=1.2)
        label_1 = Text("Company Network", **self.matrix_style.LABEL_STYLE).next_to(subnet_area_1, UP)
        subnet_area_2 = RoundedRectangle(corner_radius=0.1, color=ALERT_AMBER, fill_opacity=0.05).surround(VGroup(nodes[1]), stretch=True, buff=0.5)
        label_2 = Text("Demilitarized Zone (DMZ)", **self.amber_style.LABEL_STYLE).next_to(subnet_area_2, RIGHT)
        subnet_area_3 = RoundedRectangle(corner_radius=0.1, color=ELECTRIC_RED, fill_opacity=0.05).surround(VGroup(nodes[2]), stretch=True, buff=1)
        label_3 = Text("Internet", **self.red_style.LABEL_STYLE).next_to(subnet_area_3, LEFT)
        return {"center": center, "nodes": nodes, "connections": connections, "subnet": VGroup(subnet_area_1, label_1,subnet_area_2, label_2,subnet_area_3, label_3), "all": VGroup(center, nodes, connections, subnet_area_1, label_1,subnet_area_2, label_2,subnet_area_3, label_3)}
    
    def animate_firewall(self, firewall, loops):
        connections = firewall["connections"].submobjects
        num_conns = len(connections)
        styles = [self.yellow_style, self.blue_style, self.purple_style, self.white_style]
        if num_conns < 2:
            return
        for _ in range(loops):
            indices = list(range(num_conns))
            sender_idx = random.choice(indices)
            potential_targets = [i for i in indices if i != sender_idx]
            target_idx = random.choice(potential_targets)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            if target_idx == 0:
                if sender_idx == 1:
                    self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                    self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
                    self.play(FadeOut(packet))
                else:
                    self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                    self.play(Indicate(firewall["center"], color=ELECTRIC_RED, scale_factor=1.3))
                    self.play(Indicate(firewall["center"], color=ELECTRIC_RED, scale_factor=1.3))
                    self.play(FadeOut(packet))
            else :
                self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
                self.play(FadeOut(packet))
            self.wait(1)
    
    def get_ids(self):
        center = self.create_node("switch").shift(RIGHT * 2).shift(DOWN * 1)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, MATRIX_GREEN, GHOST_WHITE]
        node_count = 3
        radius = 3
        device_positions = [LEFT * radius, RIGHT * radius, UP * radius]
        for i in range(node_count):
            pos = center.get_center() + device_positions[i]
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos) if i != 2 else self.create_node("camera").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        label = Text("IDS", **self.matrix_style.LABEL_STYLE).next_to(nodes[2], RIGHT)
        return {"center": center, "nodes": nodes, "connections": connections, "labels": label,"all": VGroup(center, nodes, connections, label)}
    
    def animate_ids(self, ids, loops):
        connections = ids["connections"].submobjects
        styles = [self.yellow_style, self.blue_style, self.red_style]
        for _ in range(loops):
            sender_idx = random.randint(0, 1)
            target_idx = random.randint(0, 2)
            while target_idx == sender_idx:
                sender_idx = random.randint(0, 1)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            if target_idx == 2:
                self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                self.play(Indicate(ids["nodes"][2], color=ELECTRIC_RED, scale_factor=1.3))
                self.play(Indicate(ids["nodes"][2], color=ELECTRIC_RED, scale_factor=1.3))
                self.play(MoveAlongPath(packet, connections[target_idx - (sender_idx + 1)]), run_time=1, rate_func=linear)
                self.play(FadeOut(packet))
            else :
                self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
                self.play(FadeOut(packet))
            self.wait(1)
    
    def get_ips(self):
        center = self.create_node("ips").shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, MATRIX_GREEN, GHOST_WHITE]
        node_count = 2
        radius = 3
        device_positions = [LEFT * radius, RIGHT * radius]
        for i in range(node_count):
            pos = center.get_center() + device_positions[i]
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        label = Text("IPS", **self.matrix_style.LABEL_STYLE).next_to(center, RIGHT)
        return {"center": center, "nodes": nodes, "connections": connections, "labels": label,"all": VGroup(center, nodes, connections, label)}
    
    def animate_ips(self, ips, loops):
        connections = ips["connections"].submobjects
        styles = [self.yellow_style, self.blue_style, self.red_style]
        for _ in range(loops):
            sender_idx = 0
            target_idx = random.randint(1, 2)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)
            if target_idx == 2:
                self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                self.play(Indicate(ips["center"], color=ELECTRIC_RED, scale_factor=1.3))
                self.play(Indicate(ips["center"], color=ELECTRIC_RED, scale_factor=1.3))
                self.play(FadeOut(packet))
            else :
                self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
                self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
                self.play(FadeOut(packet))
            self.wait(1)

    def get_ap(self):
        center = self.create_node("access").shift(RIGHT * 2)
        nodes = VGroup()
        connections = VGroup()
        device_colors = [NEON_YELLOW, CYBER_BLUE, MATRIX_GREEN, GHOST_WHITE]
        node_count = 2
        radius = 3
        device_positions = [LEFT * radius, RIGHT * radius]
        for i in range(node_count):
            pos = center.get_center() + device_positions[i]
            color = device_colors[i % len(device_colors)]
            node = self.create_node("device").move_to(pos) if i == 1 else self.create_node("phone").move_to(pos)
            node = apply_icon_style(node,color) 
            line = self.connect(center, node).set_color(color) if i == 1 else self.connect_wifi(center, node).set_color(color)
            nodes.add(node)
            connections.add(line)
        label = Text("Access Point", **self.matrix_style.LABEL_STYLE).next_to(center, DOWN)
        return {"center": center, "nodes": nodes, "connections": connections, "labels": label,"all": VGroup(center, nodes, connections, label)}
    
    def animate_ap(self, ap, loops):
        connections = ap["connections"].submobjects
        styles = [self.yellow_style, self.blue_style, self.red_style]
        for _ in range(loops):
            sender_idx, target_idx = random.sample(range(2), 2)
            target_style = styles[target_idx % len(styles)]
            packet = Dot(**target_style.DOT_STYLE).set_z_index(3)

            self.play(MoveAlongPath(packet, connections[sender_idx]), run_time=1, rate_func=lambda t: 1 - t)
            self.play(MoveAlongPath(packet, connections[target_idx]), run_time=1, rate_func=linear)
            self.play(FadeOut(packet))
            self.wait(1)