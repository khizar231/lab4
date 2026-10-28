"""Lab 4: A* audit, UCS control and one-value heuristic overestimate.

The course campus graph was not attached in the prompt. This file therefore
uses the explicit reproducible graph in campus_graph.json and documents it in
README/report. Replace graph/heuristic if the course handout differs.
"""
import heapq
import json
from pathlib import Path

DATA = json.loads(Path(__file__).with_name("campus_graph.json").read_text(encoding="utf-8"))
GRAPH = DATA["edges"]
SUCCESSORS = DATA["successor_order"]
H_ORIGINAL = DATA["heuristic"]
START, GOAL = DATA["start"], DATA["goal"]


def true_remaining_costs():
    """Exact shortest remaining cost to goal by reverse relaxation (small graph)."""
    nodes = set(GRAPH)
    for neighbors in GRAPH.values():
        nodes.update(neighbors)
    dist = {node: float("inf") for node in nodes}
    dist[GOAL] = 0
    changed = True
    while changed:
        changed = False
        for node, neighbors in GRAPH.items():
            for child, weight in neighbors.items():
                if dist[child] != float("inf") and weight + dist[child] < dist[node]:
                    dist[node] = weight + dist[child]
                    changed = True
    return dist


def search(heuristic, start=START, goal=GOAL):
    """A* when heuristic is h; UCS when h=0.

    Convention: expansion count increments only when a non-stale node is
    removed from the priority queue and processed. Goal is counted when popped
    and processed. Stale entries are skipped and not counted.
    """
    counter = 0
    frontier = [(heuristic.get(start, 0), counter, 0, start, [start])]
    best_g = {start: 0}
    expanded_best = {}
    processed = []
    trace = []
    while frontier:
        f, _, g, node, path = heapq.heappop(frontier)
        if g != best_g.get(node):
            trace.append({"event": "STALE-SKIP", "node": node, "g": g, "f": f})
            continue
        # For this implementation, do not expand a node more than once at its
        # best known g; a strictly better g can reopen it.
        if node in expanded_best and expanded_best[node] <= g:
            trace.append({"event": "DUPLICATE-SKIP", "node": node, "g": g, "f": f})
            continue
        expanded_best[node] = g
        processed.append(node)
        trace.append({"event": "PROCESS", "node": node, "g": g,
                      "h": heuristic.get(node, 0), "f": g + heuristic.get(node, 0),
                      "frontier_after_pop": sorted([(entry[3], entry[2], entry[0]) for entry in frontier])})
        if node == goal:
            return {"path": path, "cost": g, "processed": processed,
                    "expansion_count": len(processed), "trace": trace}
        for child in SUCCESSORS[node]:
            edge_cost = GRAPH[node][child]
            new_g = g + edge_cost
            if new_g < best_g.get(child, float("inf")):
                best_g[child] = new_g
                counter += 1
                h = heuristic.get(child, 0)
                heapq.heappush(frontier, (new_g + h, counter, new_g, child, path + [child]))
    return {"path": None, "cost": float("inf"), "processed": processed,
            "expansion_count": len(processed), "trace": trace}


def print_result(name, result):
    print(f"{name}")
    print(f"  path: {' -> '.join(result['path']) if result['path'] else 'NOT FOUND'}")
    print(f"  returned_cost: {result['cost']}")
    print(f"  independent_path_cost: {path_cost(result['path']) if result['path'] else 'n/a'}")
    print(f"  processed_trace: {result['processed']}")
    print(f"  expansion_count: {result['expansion_count']}")
    print(f"  detailed_trace:")
    for row in result["trace"]:
        print(f"    {row}")


def path_cost(path):
    return sum(GRAPH[a][b] for a, b in zip(path, path[1:]))


if __name__ == "__main__":
    zeros = {node: 0 for node in H_ORIGINAL}
    overestimate = dict(H_ORIGINAL)
    overestimate["C"] = 10  # only one heuristic value changed
    print("GRAPH EDGES:")
    for node in SUCCESSORS:
        for child in SUCCESSORS[node]:
            print(f"  {node}->{child}: {GRAPH[node][child]}")
    print(f"Original heuristic: {H_ORIGINAL}")
    print(f"True remaining costs: {true_remaining_costs()}")
    print_result("A* with supplied example heuristic", search(H_ORIGINAL))
    print_result("UCS control (h=0)", search(zeros))
    print(f"Modified heuristic (only C changed): {overestimate}")
    print_result("A* with overestimate h(C)=10", search(overestimate))
