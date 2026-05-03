import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class NetworkDesign(Scene, CommonUtils):

    # Network Architecture
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
        section_01 = self.stylize("NETWORK DESIGN/ARCHITECTURE").scale(0.7).to_edge(UL, buff=0.5)
        self.play(FadeIn(section_01))

        # legend
        legend = self.set_legend()
        pointer = Triangle(color=MATRIX_GREEN).scale(0.1).rotate(-90 * DEGREES)
        pointer.next_to(legend[0], LEFT, buff=0.2)
        self.play(FadeIn(legend, pointer))

        # two-tier architecture
        t2_network = self.get_two_tier()
        self.play(pointer.animate.next_to(legend[0], LEFT, buff=0.2))
        self.play(
            Create(t2_network["connections"]),
            FadeIn(t2_network["nodes"]),
            run_time=2
        )
        self.random_data(t2_network["connections"], 5)
        self.play(FadeOut(t2_network["all"]))

        # three-tier architecture
        t3_network = self.get_three_tier()
        self.play(pointer.animate.next_to(legend[1], LEFT, buff=0.2))
        self.play(
            Create(t3_network["connections"]),
            FadeIn(t3_network["nodes"]),
            run_time=2
        )
        self.random_data(t3_network["connections"], 5)
        self.play(FadeOut(t3_network["all"]))

        # spine-leaf architecture
        sp_network = self.get_spine_leaf()
        sp_network["all"].shift(RIGHT * 2)
        self.play(pointer.animate.next_to(legend[2], LEFT, buff=0.2))
        self.play(
            Create(sp_network["connections"]),
            FadeIn(sp_network["nodes"]),
            run_time=2
        )
        self.random_data(sp_network["connections"], 5)
        self.play(FadeOut(sp_network["all"]))

        # soho architecture
        soho_network = self.get_soho_topology()
        soho_network["all"].shift(RIGHT * 2)
        self.play(pointer.animate.next_to(legend[3], LEFT, buff=0.2))
        self.play(
            Create(soho_network["connections"]),
            FadeIn(soho_network["nodes"]),
            run_time=2
        )
        self.random_data(soho_network["connections"], 5)
        self.play(FadeOut(soho_network["all"]))


    def set_legend(self):
        labels = [ "I. Two-Tier (Collapsed Core)", "II. Three-Tier Architecture", "III. Spine-Leaf Architecture", "IV. SOHO Architecture"]
        legend_items = VGroup(*[Text(label, **self.matrix_style.LABEL_STYLE) for label in labels])
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        legend_items.to_edge(LEFT, buff=1)
        return legend_items

    def get_two_tier(self, node_count=6, radius=2.5):
        nodes = VGroup()
        connections = VGroup()
        # Distribution Layer
        dist_nodes = VGroup()
        for i in range(2):
            pos = UP * 2 + (LEFT * 1 if i == 0 else RIGHT * 5)
            node = self.create_node("switch").move_to(pos)
            dist_nodes.add(node)
        connections.add(self.connect(dist_nodes[0], dist_nodes[1]))
        # Access Layer
        access_nodes = VGroup()
        num_access = 4
        for i in range(num_access):
            pos = DOWN * 1 + (LEFT * 1 + RIGHT * 2 * i)
            node = self.create_node("device").move_to(pos)
            access_nodes.add(node)
            for dist in dist_nodes:
                connections.add(self.connect(node, dist))
        nodes.add(dist_nodes, access_nodes)
        return {"nodes": nodes, "connections": connections, "all": VGroup(connections, nodes)}

    def get_three_tier(self):
        nodes = VGroup()
        connections = VGroup()
        # Core Layer
        core_nodes = VGroup()
        for i in range(2):
            pos = UP * 2 + (LEFT * 1 if i == 0 else RIGHT * 5)
            node = self.create_node("router").move_to(pos)
            core_nodes.add(node)
        connections.add(self.connect(core_nodes[0], core_nodes[1]))
        # Distribution Layer
        dist_nodes = VGroup()
        for i in range(2):
            pos = LEFT * 1 if i == 0 else RIGHT * 5
            node = self.create_node("switch").move_to(pos)
            dist_nodes.add(node)
            for core in core_nodes:
                connections.add(self.connect(node, core))
        connections.add(self.connect(dist_nodes[0], dist_nodes[1]))
        # Access Layer
        access_nodes = VGroup()
        num_access = 4
        for i in range(num_access):
            pos = DOWN * 2 + (LEFT * 1 + RIGHT * 2 * i)
            node = self.create_node("device").move_to(pos)
            access_nodes.add(node)
            for dist in dist_nodes:
                connections.add(self.connect(node, dist))
        nodes.add(core_nodes, dist_nodes, access_nodes)
        return {"nodes": nodes, "connections": connections, "all": VGroup(connections, nodes)}

    def get_spine_leaf(self, num_spines=3, num_leaves=5):
        nodes = VGroup()
        connections = VGroup()
        spine_nodes = VGroup()
        leaf_nodes = VGroup()
        spine_spacing = 3
        for i in range(num_spines):
            pos = UP * 2 + LEFT * ((num_spines - 1) * spine_spacing / 2) + RIGHT * (i * spine_spacing)
            spine = self.create_node("switch").move_to(pos)
            spine_nodes.add(spine)
        leaf_spacing = 2
        for j in range(num_leaves):
            # Centering the leaves horizontally
            pos = DOWN * 1 + LEFT * ((num_leaves - 1) * leaf_spacing / 2) + RIGHT * (j * leaf_spacing)
            leaf = self.create_node("switch").move_to(pos)
            leaf_nodes.add(leaf)
        for leaf in leaf_nodes:
            for spine in spine_nodes:
                connections.add(self.connect(leaf, spine))
        nodes.add(spine_nodes, leaf_nodes)
        return {"nodes": nodes, "connections": connections, "all": VGroup(connections, nodes)}
    
    def get_soho_topology(self):
        nodes = VGroup()
        connections = VGroup()
        cloud = self.create_node("web").to_edge(UP, buff=1.5)
        gateway = self.create_node("router").move_to(ORIGIN)
        connections.add(self.connect(cloud, gateway))
        device_types = ["device", "server2", "device", "printer"]
        devices = VGroup()
        for i, d_type in enumerate(device_types):
            angle = (PI / (len(device_types) - 1)) * i + PI
            pos = gateway.get_center() + 2.5 * np.array([np.cos(angle), np.sin(angle), 0])
            dev = self.create_node(d_type).move_to(pos)
            devices.add(dev)
            connections.add(self.connect(gateway, dev))
        nodes.add(cloud, gateway, devices)
        return {"nodes": nodes, "connections": connections, "all": VGroup(connections, nodes)}