"""In this problem, we are asked to design an emergency network simulator that models cities or 
locations as nodes and the roads connecting them as weighted edges. Each node represents an 
important location such as a hospital, fire station, or control center, and each edge represents a 
road with a certain distance or cost. The network must be flexible so that nodes and roads can be 
added dynamically, similar to how real emergency networks grow and change over time.

The main goal of the problem is to analyze and manage the network efficiently during emergency situations. 
This includes finding the Minimum Spanning Tree (MST) to ensure that all locations remain connected using 
the minimum total road cost, which is important for reducing travel time and resource usage. 
The problem also requires the ability to simulate failures, such as when a city or road becomes 
unavailable due to a disaster, and immediately update the network to reflect this change.

Overall, the problem focuses on understanding how graph algorithms like Kruskal’s algorithm can be
applied in real-world emergency planning, allowing quick decision-making, efficient connectivity, 
and system robustness when parts of the network fail"""

"""We solve this problem by modeling the emergency system as a graph and then using simple graph algorithms +
a GUI to simulate real situations. Each location (hospital/city) is treated as a node, 
and each road is treated as a weighted edge (weight = distance or cost). In the program, 
the user can add nodes and edges through the GUI, and the network is stored using an adjacency 
structure and an edge list. To keep the network connected with minimum total cost, we compute the 
Minimum Spanning Tree (MST) using Kruskal’s algorithm, which sorts all roads by weight and keeps 
adding the cheapest roads that do not create a cycle, until all nodes are connected. 
To simulate disasters or breakdowns, the “failure” feature removes a node and automatically removes all 
roads connected to it, then redraws the updated network. In this way, the simulator shows how emergency 
networks can be built, optimized (MST), and updated quickly when failures happen.
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

# Graph Data Structures
class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.adj = {}  # neighbor_node: weight

class Graph:
    def __init__(self):
        self.nodes = {}  # name: Node
        self.edges = []  # (weight, node1, node2)

    def add_node(self, name, x, y):
        if name not in self.nodes:
            self.nodes[name] = Node(name, x, y)

    def add_edge(self, n1, n2, w):
        if n1 in self.nodes and n2 in self.nodes:
            self.nodes[n1].adj[self.nodes[n2]] = w
            self.nodes[n2].adj[self.nodes[n1]] = w
            self.edges.append((w, self.nodes[n1], self.nodes[n2]))

# Kruskal's MST Algorithm
class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]
    def union(self, n1, n2):
        p1 = self.find(n1)
        p2 = self.find(n2)
        if p1 != p2:
            self.parent[p2] = p1
            return True
        return False

def kruskal_mst(graph):
    uf = UnionFind(list(graph.nodes.values()))
    mst = []
    for w, n1, n2 in sorted(graph.edges, key=lambda x: x[0]):
        if uf.union(n1, n2):
            mst.append((n1, n2, w))
    return mst

# ------------------------
# Emergency Network Simulator GUI
# ------------------------
class EmergencySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Simulator")

        # Canvas
        self.canvas = tk.Canvas(root, width=900, height=600, bg="white")
        self.canvas.pack()

        # Graph
        self.graph = Graph()
        self.node_radius = 20
        self.selected_node = None
        self.edge_start_node = None

        # Buttons
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Button(frame, text="Add Node", command=self.add_node_dialog).pack(side='left', padx=5)
        tk.Button(frame, text="Add Edge", command=self.add_edge_dialog).pack(side='left', padx=5)
        tk.Button(frame, text="Show MST", command=self.show_mst).pack(side='left', padx=5)
        tk.Button(frame, text="Simulate Failure", command=self.simulate_failure_dialog).pack(side='left', padx=5)

        # Canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.drag_node)
        self.canvas.bind("<Double-Button-1>", self.add_node_click)

        self.draw_nodes()
        self.draw_edges()

    # ------------------------
    # Node Creation
    # ------------------------
    def add_node_dialog(self):
        name = simpledialog.askstring("Node Name", "Enter node name:")
        if name:
            x, y = 100, 100  # Default position
            self.graph.add_node(name, x, y)
            self.draw_nodes()

    def add_node_click(self, event):
        name = simpledialog.askstring("Node Name", "Enter node name:")
        if name:
            self.graph.add_node(name, event.x, event.y)
            self.draw_nodes()

    # ------------------------
    # Edge Creation
    # ------------------------
    def add_edge_dialog(self):
        if len(self.graph.nodes) < 2:
            messagebox.showwarning("Error", "Need at least two nodes to create an edge.")
            return
        n1 = simpledialog.askstring("Edge Start", "Enter start node name:")
        n2 = simpledialog.askstring("Edge End", "Enter end node name:")
        w = simpledialog.askinteger("Weight", "Enter edge weight:")
        if n1 and n2 and w is not None:
            if n1 in self.graph.nodes and n2 in self.graph.nodes:
                self.graph.add_edge(n1, n2, w)
                self.draw_edges()
            else:
                messagebox.showwarning("Error", "One or both nodes do not exist!")

    # ------------------------
    # Node and Edge Drawing
    # ------------------------
    def draw_nodes(self):
        self.canvas.delete("node")
        for node in self.graph.nodes.values():
            x, y = node.x, node.y
            self.canvas.create_oval(x-self.node_radius, y-self.node_radius,
                                    x+self.node_radius, y+self.node_radius,
                                    fill="lightblue", tags="node")
            self.canvas.create_text(x, y, text=node.name, tags="node")

    def draw_edges(self, highlight_edges=None):
        self.canvas.delete("edge")
        for e in self.graph.edges:
            w, n1, n2 = e
            color = "red" if highlight_edges and (n1, n2, w) in highlight_edges or (n2, n1, w) in highlight_edges else "black"
            self.canvas.create_line(n1.x, n1.y, n2.x, n2.y, fill=color, width=2, tags="edge")
            mid_x, mid_y = (n1.x + n2.x)//2, (n1.y + n2.y)//2
            self.canvas.create_text(mid_x, mid_y, text=str(w), tags="edge")

    # ------------------------
    # Node Dragging
    # ------------------------
    def on_canvas_click(self, event):
        for node in self.graph.nodes.values():
            if (event.x - node.x)**2 + (event.y - node.y)**2 <= self.node_radius**2:
                self.selected_node = node
                break

    def drag_node(self, event):
        if self.selected_node:
            self.selected_node.x = event.x
            self.selected_node.y = event.y
            self.draw_edges()
            self.draw_nodes()

    # ------------------------
    # MST Visualization
    # ------------------------
    def show_mst(self):
        if len(self.graph.nodes) == 0:
            messagebox.showwarning("Error", "No nodes in graph!")
            return
        mst_edges = kruskal_mst(self.graph)
        self.draw_edges(highlight_edges=mst_edges)

    # ------------------------
    # Failure Simulation
    # ------------------------
    def simulate_failure_dialog(self):
        if not self.graph.nodes:
            messagebox.showwarning("Error", "No nodes to fail.")
            return
        node_name = simpledialog.askstring("Node Failure", "Enter node to disable:")
        if node_name in self.graph.nodes:
            failed_node = self.graph.nodes[node_name]
            new_edges = []
            affected_edges = []
            for e in self.graph.edges:
                if failed_node in e[1:3]:
                    affected_edges.append(e)
                else:
                    new_edges.append(e)
            self.graph.edges = new_edges
            del self.graph.nodes[node_name]
            messagebox.showinfo("Failure", f"Node {node_name} failed. Connected edges removed.")
            self.draw_edges()
            self.draw_nodes()
        else:
            messagebox.showwarning("Error", "Node not found!")

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencySimulator(root)
    root.mainloop()