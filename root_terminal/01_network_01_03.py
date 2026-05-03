import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDesign(Scene, CommonUtils):

    # Network Topologies
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
        section_01 = self.stylize("NETWORK DESIGN/TOPOLOGIES").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeIn(section_01))

        # legend
        legend = self.set_legend()
        pointer = Triangle(color=MATRIX_GREEN).scale(0.1).rotate(-90 * DEGREES)
        pointer.next_to(legend[0], LEFT, buff=0.2)
        self.play(FadeIn(legend, pointer))

        # star topology
        star_network = self.get_star_topology()
        star_network["all"].shift(RIGHT * 2)
        self.play(
            Create(star_network["connections"]),
            FadeIn(star_network["center"]),
            FadeIn(star_network["nodes"]),
            run_time=2
        )
        self.random_data(star_network["connections"], 10)
        self.play(FadeOut(star_network["all"]))

        # ring topology
        ring_network = self.get_ring_topology()
        ring_network["all"].shift(RIGHT * 2)
        self.play(pointer.animate.next_to(legend[1], LEFT, buff=0.2))
        self.play(
            Create(ring_network["connections"]),
            FadeIn(ring_network["center"]),
            FadeIn(ring_network["nodes"]),
            run_time=2
        )
        self.random_data(ring_network["connections"], 10)
        self.play(FadeOut(ring_network["all"]))

        # bus topology
        bus_network = self.get_bus_topology()
        bus_network["all"].shift(LEFT * 1)
        self.play(pointer.animate.next_to(legend[2], LEFT, buff=0.2))
        self.play(
            Create(bus_network["connections"]),
            FadeIn(bus_network["center"]),
            FadeIn(bus_network["nodes"]),
            FadeIn(bus_network["backbone"]),
            run_time=2
        )
        self.random_data(bus_network["connections"], 10)
        self.play(FadeOut(bus_network["all"]))

        # tree topology
        tree_network = self.get_tree_topology()
        tree_network["all"].shift(LEFT * 1)
        self.play(pointer.animate.next_to(legend[3], LEFT, buff=0.2))
        self.play(
            Create(tree_network["connections"]),
            FadeIn(tree_network["nodes"]),
            run_time=2
        )
        self.random_data(tree_network["connections"], 10)
        self.play(FadeOut(tree_network["all"]))
    
        # mesh topology
        mesh_network = self.get_mesh_topology()
        mesh_network["all"].shift(RIGHT * 2)
        self.play(pointer.animate.next_to(legend[4], LEFT, buff=0.2))
        self.play(
            Create(mesh_network["connections"]),
            FadeIn(mesh_network["nodes"]),
            run_time=2
        )
        self.random_data(mesh_network["connections"], 10)
        self.play(FadeOut(mesh_network["all"]))


    def set_legend(self):
        labels = [ "I. Star Topology", "II. Ring Topology", "III. Bus Topology", "IV. Tree Topology", "V. Mesh Topology"]
        legend_items = VGroup(*[Text(label, **self.matrix_style.LABEL_STYLE) for label in labels])
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        legend_items.to_edge(LEFT, buff=1)
        return legend_items

    def get_star_topology(self, node_count=6, radius=2.5):
        center = self.create_node("switch")
        nodes = VGroup()
        connections = VGroup()
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            node = self.create_node("device").move_to(pos)
            line = self.connect(center, node)
            nodes.add(node)
            connections.add(line)
        return {"center": center, "nodes": nodes, "connections": connections, "all": VGroup(center, nodes, connections)}

    def get_ring_topology(self, node_count=6, radius=2.5):
        center = Dot(radius=0.01)
        nodes = VGroup()
        connections = VGroup()
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = center.get_center()  + np.array([np.cos(angle), np.sin(angle), 0]) * radius
            node = self.create_node("device").move_to(pos)
            nodes.add(node)
        for i in range(node_count):
            line = self.connect(nodes[i], nodes[(i + 1) % node_count])
            connections.add(line)
        return {"center": center, "nodes": nodes, "connections": connections, "all": VGroup(center, nodes, connections)}

    def get_bus_topology(self, node_count=5, length=4):
        center = Dot(radius=0.01)
        nodes = VGroup()
        connections = VGroup()
        backbone = Line(ORIGIN, RIGHT * length, **self.matrix_style.LINE_STYLE)
        for i in range(node_count):
            direction = UP if i % 2 == 0 else DOWN
            node_pos = (direction * 1.5) + (RIGHT * i)
            bus_dot = Dot(RIGHT * i, radius=0.01)
            node = self.create_node("device").move_to(node_pos)
            nodes.add(node)
            line = self.connect(bus_dot, node)
            connections.add(line)
        return {"center": center, "nodes": nodes, "connections": connections, "backbone": backbone, "all": VGroup(center, nodes, connections, backbone)}

    def get_tree_topology(self, node_count=7, y_spacing=3):
        nodes = VGroup()
        connections = VGroup()
        node_list = []
        x_spacing = 2.5
        for i in range(node_count):
            if i == 0:
                pos = ORIGIN
            else:
                parent_idx = (i - 1) // 2
                parent_pos = node_list[parent_idx].get_center()
                level = int(np.log2(i + 1))
                spread = y_spacing / (2 ** (level - 1))
                direction = 1 if (i % 2 != 0) else -1
                pos = parent_pos + np.array([x_spacing, direction * (spread / 2), 0])
            is_leaf = (2 * i + 1) >= node_count
            node_type = "device" if is_leaf else "switch"
            node = self.create_node(node_type).move_to(pos)
            nodes.add(node)
            node_list.append(node)
            if i > 0:
                parent_idx = (i - 1) // 2
                line = self.connect(node_list[parent_idx], node)
                connections.add(line)
        return {"center": nodes[0], "nodes": nodes, "connections": connections, "all": VGroup(nodes, connections)}
    
    def get_mesh_topology(self, node_count=6, radius=2.5):
        nodes = VGroup()
        connections = VGroup()
        for i in range(node_count):
            angle = i * (TAU / node_count)
            pos = np.array([np.cos(angle), np.sin(angle), 0]) * radius
            node = self.create_node("device").move_to(pos)
            nodes.add(node)
        for i in range(node_count):
            for j in range(i + 1, node_count):
                line = self.connect(nodes[i], nodes[j])
                connections.add(line)   
        return {"nodes": nodes, "connections": connections, "all": VGroup(connections, nodes)}