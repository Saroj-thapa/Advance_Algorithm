"""The problem is solved by modelling the cities and roads as a graph where each city represents a 
state and each road represents a connection between states. The robot starts from Glogow and the goal is to reach Plock. 
First, based on diagram (a), the state space is constructed using the real road distances between cities. Using this state space, 
the Depth First Search (DFS) algorithm is applied by using a stack as the open list and a closed list to store visited cities. 
DFS explores one path deeply before backtracking and finds a valid path to the goal, but it does not guarantee the shortest path. 
Next, the Breadth First Search (BFS) algorithm is applied using a queue as the open list. 
BFS explores cities level by level and guarantees the shortest path in terms of number of steps from the start city to the goal city."""

"""For the A* algorithm, diagram (b) is used as required by the question. From diagram (b), a heuristic function is designed that 
estimates the remaining distance from any city to the goal city, Plock. This heuristic represents an estimated straight-line distance 
and helps guide the search efficiently. The A* algorithm uses this heuristic along with the path cost to expand the most promising city
first by evaluating the function f(n) = g(n) + h(n). The open list is implemented as a priority queue, while the closed list stores the expanded cities.
By using the heuristic information from diagram (b), A* efficiently finds an optimal path from Glogow to Plock. 
Thus, DFS and BFS are solved using diagram (a), while A* is solved using diagram (b), exactly following the requirements of the problem."""

import matplotlib.pyplot as plt
from collections import deque
import heapq
# START and GOAL (where the robot starts and where it must go)
start, goal = "Glogow", "Plock"
# Diagram (a) = REAL ROAD MAP
# We use this for:
#   1) State space
#   2) DFS
#   3) BFS
# Each edge has the real road distance.
GA = {
 "Glogow": [("Leszno",45),("Wroclaw",140)],
 "Leszno": [("Glogow",45),("Poznan",90),("Kalisz",140),("Wroclaw",100)],
 "Poznan": [("Leszno",90),("Kalisz",130),("Bydgoszcz",140)],
 "Bydgoszcz":[("Poznan",140),("Konin",120),("Wloclawek",110)],
 "Wloclawek":[("Bydgoszcz",110),("Plock",55)],
 "Plock":[("Wloclawek",55),("Warsaw",130)],
 "Warsaw":[("Plock",130),("Lodz",150),("Radom",105)],
 "Radom":[("Warsaw",105),("Lodz",165),("Kielce",82)],
 "Kielce":[("Radom",82),("Krakow",120)],
 "Krakow":[("Kielce",120),("Katowice",85),("Lodz",280)],
 "Katowice":[("Krakow",85),("Opole",118),("Czestochowa",80)],
 "Opole":[("Wroclaw",100),("Katowice",118)],
 "Wroclaw":[("Glogow",140),("Leszno",100),("Opole",100)],
 "Kalisz":[("Leszno",140),("Poznan",130),("Lodz",120),("Czestochowa",160)],
 "Czestochowa":[("Kalisz",160),("Lodz",128),("Katowice",80)],
 "Lodz":[("Kalisz",120),("Konin",120),("Warsaw",150),("Radom",165),("Czestochowa",128),("Krakow",280)],
 "Konin":[("Bydgoszcz",120),("Lodz",120)],
}
# Diagram (b) = HEURISTIC MAP (estimated / straight line style)
# Your question says:
#   "Based on diagram (b), design the heuristic function
#    and solve using A*"
# So for the A* part, we use GB.
GB = {
 "Glogow": [("Leszno",40),("Wroclaw",89)],
 "Leszno": [("Glogow",40),("Poznan",67),("Kalisz",103),("Wroclaw",87)],
 "Poznan": [("Leszno",67),("Kalisz",107),("Bydgoszcz",108)],
 "Bydgoszcz":[("Poznan",108),("Konin",102),("Wloclawek",90)],
 "Wloclawek":[("Bydgoszcz",90),("Plock",44)],
 "Plock":[("Wloclawek",44),("Warsaw",95)],
 "Warsaw":[("Plock",95),("Lodz",118),("Radom",91)],
 "Radom":[("Warsaw",91),("Lodz",124),("Kielce",70)],
 "Kielce":[("Radom",70),("Krakow",102)],
 "Krakow":[("Kielce",102),("Katowice",68),("Lodz",190)],
 "Katowice":[("Krakow",68),("Czestochowa",61),("Opole",90)],
 "Opole":[("Wroclaw",80),("Katowice",90)],
 "Wroclaw":[("Glogow",89),("Leszno",87),("Opole",80)],
 "Kalisz":[("Leszno",103),("Poznan",107),("Lodz",95),("Czestochowa",128)],
 "Czestochowa":[("Kalisz",128),("Lodz",107),("Katowice",61)],
 "Lodz":[("Kalisz",95),("Konin",96),("Warsaw",118),("Radom",124),("Czestochowa",107),("Krakow",190)],
 "Konin":[("Bydgoszcz",102),("Lodz",96)],
}
# Positions for drawing (just to make a nice graph picture)
# These are not part of the algorithm, only for visualization.
pos = {
 "Glogow": (0, 3), "Leszno": (2, 4), "Wroclaw": (2, 2),
 "Poznan": (4, 6), "Kalisz": (5, 4), "Bydgoszcz": (6, 8),
 "Konin": (7, 6), "Lodz": (8, 4), "Wloclawek": (8, 7),
 "Plock": (10, 7), "Warsaw": (12, 6), "Radom": (12, 4),
 "Kielce": (12, 3), "Krakow": (11, 1), "Katowice": (8, 1),
 "Czestochowa": (7, 3), "Opole": (4, 1),
}
# Helper: rebuild the final path using the parent dictionary
# Example: if parent[Poznan] = Leszno, it means we came to
# Poznan from Leszno.
def build_path(parent, end):
    if end not in parent:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]  # reverse to make it start -> goal
# DFS (Diagram a)
# Open = stack (Last In First Out)
# Closed = visited set
# DFS goes deep first.
def dfs(G):
    open_stack = [start]
    parent = {start: None}
    closed = set()

    while open_stack:
        u = open_stack.pop()     # take last item (stack behavior)
        if u in closed:
            continue
        closed.add(u)

        if u == goal:
            break

        # add neighbors (reverse sorted gives nicer, consistent order)
        for v, _ in sorted(G[u], reverse=True):
            if v not in closed and v not in parent:
                parent[v] = u
                open_stack.append(v)

    return build_path(parent, goal)
# BFS (Diagram a)
# Open = queue (First In First Out)
# Closed is tracked by "parent" (if node is in parent, it was visited)
# BFS finds the shortest path in number of steps.
def bfs(G):
    open_queue = deque([start])
    parent = {start: None}

    while open_queue:
        u = open_queue.popleft()     # take first item (queue behavior)

        if u == goal:
            break

        for v, _ in sorted(G[u]):
            if v not in parent:
                parent[v] = u
                open_queue.append(v)

    return build_path(parent, goal)

# Heuristic design (Diagram b)
# We want h(n) = estimated distance from n to the goal.
# We calculate it by running Dijkstra from the goal on diagram (b).
# That gives a good estimated cost-to-go for every city.
def heuristic_from_B(G, goal):
    h = {goal: 0}
    pq = [(0, goal)]

    while pq:
        dist, u = heapq.heappop(pq)
        if dist != h[u]:
            continue

        for v, w in G[u]:
            nd = dist + w
            if nd < h.get(v, 10**18):
                h[v] = nd
                heapq.heappush(pq, (nd, v))

    return h

# A* (Diagram b)
# Open = priority queue (we always choose smallest f = g + h)
# Closed = already expanded nodes
def astar(G):
    h = heuristic_from_B(G, goal)

    open_pq = [(h.get(start, 0), 0, start)]  # (f, g, node)
    parent = {start: None}
    best_g = {start: 0}
    closed = set()

    while open_pq:
        f, g, u = heapq.heappop(open_pq)
        if u in closed:
            continue
        closed.add(u)

        if u == goal:
            return build_path(parent, goal), g

        for v, w in G[u]:
            new_g = g + w
            if new_g < best_g.get(v, 10**18):
                best_g[v] = new_g
                parent[v] = u
                new_f = new_g + h.get(v, 0)
                heapq.heappush(open_pq, (new_f, new_g, v))

    return None, None
# Drawing function (Matplotlib)
# It draws the full graph, and highlights the final path.
def draw(title, G, path):
    plt.figure(figsize=(10, 6))

    # draw all edges (avoid duplicates)
    drawn = set()
    for u in G:
        for v, w in G[u]:
            e = tuple(sorted((u, v)))
            if e in drawn:
                continue
            drawn.add(e)

            x1, y1 = pos[u]
            x2, y2 = pos[v]
            plt.plot([x1, x2], [y1, y2], linewidth=1)
            plt.text((x1+x2)/2, (y1+y2)/2, str(w), fontsize=8)

    # highlight the path edges (make them thick)
    if path:
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            plt.plot([x1, x2], [y1, y2], linewidth=4)

    # draw nodes
    for city, (x, y) in pos.items():
        plt.scatter(x, y, s=140)

        label = city
        if city == start:
            label += " (Start)"
        if city == goal:
            label += " (Goal)"
        plt.text(x+0.1, y+0.1, label, fontsize=9)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
path_dfs = dfs(GA)                # diagram (a)
path_bfs = bfs(GA)                # diagram (a)
path_astar, cost_astar = astar(GB)  # diagram (b)

print("DFS (Diagram a):", path_dfs)
print("BFS (Diagram a):", path_bfs)
print("A*  (Diagram b):", path_astar, "Cost =", cost_astar)

draw("DFS using Diagram (a)", GA, path_dfs)
draw("BFS using Diagram (a)", GA, path_bfs)
draw("A* using Diagram (b)", GB, path_astar)

"""DFS (Diagram a): ['Glogow', 'Leszno', 'Kalisz', 'Czestochowa', 'Katowice', 'Krakow', 'Kielce', 'Radom', 'Warsaw', 'Plock']
BFS (Diagram a): ['Glogow', 'Leszno', 'Kalisz', 'Lodz', 'Warsaw', 'Plock']
A*  (Diagram b): ['Glogow', 'Leszno', 'Poznan', 'Bydgoszcz', 'Wloclawek', 'Plock'] Cost = 349"""