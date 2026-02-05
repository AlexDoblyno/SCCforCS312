import sys
import random

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(20000)


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    visited = set()
    forest = []
    clock = 0

    def dfs(u, current_tree):
        nonlocal clock
        visited.add(u)

        clock += 1
        current_tree[u] = [clock, 0]  # 记录 Pre

        if u in graph:              # This inner loop runs once for every edge (E) in the graph
            for v in graph[u]:      # over the total duration of the algorithm.
                if v not in visited:
                    dfs(v, current_tree)

        clock += 1
        current_tree[u][1] = clock  # 记录 Post

    for node in graph.keys():       # This outer loop ensures we iterate over every vertex (V).
        if node not in visited:
            tree = {}
            dfs(node, tree)
            forest.append(tree)

    return forest


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source.
    """
    visited = set()
    post_order_stack = []

    #得到 Post Order
    def dfs_pass1(u):
        visited.add(u)
        if u in graph:                   #晚点问问这个
            for v in graph[u]:
                if v not in visited:
                    dfs_pass1(v)
        post_order_stack.append(u)

    for node in graph.keys():         # because we visit each node and edge once.
        if node not in visited:
            dfs_pass1(node)

    #实现啊Transpose Graph
    reversed_graph = {u: [] for u in graph}     # iterate over all keys V and all adjacency lists E.
    for u in graph:
        for v in graph[u]:
            if v not in reversed_graph:
                reversed_graph[v] = []
            reversed_graph[v].append(u)

    # DFS 在 Transpose Graph
    visited_scc = set()
    sccs = []

    def dfs_pass2(u, current_component):     #pop V nodes, and inner DFS traverses edges in reversed_graph.
        visited_scc.add(u)
        current_component.add(u)
        if u in reversed_graph:
            for v in reversed_graph[u]:
                if v not in visited_scc:
                    dfs_pass2(v, current_component)

    while post_order_stack:
        node = post_order_stack.pop()
        if node not in visited_scc:
            component = set()
            dfs_pass2(node, component)
            sccs.append(component)

    # Kosaraju 产生的是 Source to Sink，但是要求Sink to Source！
    return sccs[::-1]


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges.
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    all_times = {}
    for tree in trees:
        all_times.update(tree)

    for u in graph:
        if u not in all_times: continue
        pre_u, post_u = all_times[u]

        for v in graph[u]:
            if v not in all_times: continue
            pre_v, post_v = all_times[v]
            edge = (u, v)

            if pre_u < pre_v and post_v < post_u:
                classification['tree/forward'].add(edge)
            elif pre_v < pre_u and post_u < post_v:
                classification['back'].add(edge)
            elif pre_v < pre_u and post_v < post_u:
                classification['cross'].add(edge)

    return classification