import pandas as pd
import sys
import time


sys.setrecursionlimit(200000)


GRAPH = dict[str, list[str]]


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    visited = set()
    forest = []
    clock = 0

    def dfs(u, current_tree):
        nonlocal clock
        visited.add(u)
        clock += 1
        current_tree[u] = [clock, 0]
        if u in graph:
            for v in graph[u]:
                if v not in visited:
                    dfs(v, current_tree)
        clock += 1
        current_tree[u][1] = clock

    for node in graph.keys():
        if node not in visited:
            tree = {}
            dfs(node, tree)
            forest.append(tree)
    return forest


def find_sccs(graph: GRAPH) -> list[set[str]]:
    visited = set()
    post_order_stack = []

    def dfs_pass1(u):
        visited.add(u)
        if u in graph:
            for v in graph[u]:
                if v not in visited:
                    dfs_pass1(v)
        post_order_stack.append(u)

    for node in graph.keys():
        if node not in visited:
            dfs_pass1(node)

    reversed_graph = {u: [] for u in graph}
    for u in graph:
        for v in graph[u]:
            if v not in reversed_graph: reversed_graph[v] = []
            reversed_graph[v].append(u)

    visited_scc = set()
    sccs = []

    def dfs_pass2(u, current_component):
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

    return sccs[::-1]


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    classification = {'tree/forward': set(), 'back': set(), 'cross': set()}
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


def main():
    print("=== Stretch 2 Analysis based on YOUR scc.py ===")

#读取数据
    print(" Loading wikiRfA.csv...")
    try:
        df = pd.read_csv('wikiRfA.csv')
    except FileNotFoundError:
        print("please add wikiRfA.csv")
        return

    #  构建图仅保留VOTE=1
    print("Building Graph (Filtering VOTE=1)...")
    df_clean = df[(df['VOTE'] == 1) & (df['SOURCE'].notna()) & (df['TARGET'].notna())]

    graph = {}
    all_nodes = set()
    for _, row in df_clean.iterrows():
        u, v = str(row['SOURCE']), str(row['TARGET'])
        all_nodes.add(u);
        all_nodes.add(v)
        if u not in graph: graph[u] = []
        if v not in graph: graph[v] = []
        graph[u].append(v)

    #补全节点
    for node in all_nodes:
        if node not in graph: graph[node] = []

    print(f"      Graph Stats: {len(all_nodes)} Nodes, {len(df_clean)} Edges")

    #运行 SCC
    print("Running SCC")
    sccs = find_sccs(graph)
    num_sccs = len(sccs)
    largest = max(len(c) for c in sccs) if sccs else 0

    print(f"      Found {num_sccs} SCCs.")
    print(f"      Largest SCC Size: {largest}")

    # 运行边分类
    print("Classifying Edges...")
    trees = prepost(graph)
    edges = classify_edges(graph, trees)

    back_edges = len(edges['back'])
    cross_edges = len(edges['cross'])


    print(f"Total Components:     {num_sccs}")
    print(f"Largest Component:    {largest}")
    print(f"Back Edges (Cycles):  {back_edges}")
    print(f"Cross Edges:          {cross_edges}")


if __name__ == "__main__":
    main()