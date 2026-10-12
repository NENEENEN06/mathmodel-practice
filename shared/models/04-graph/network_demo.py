"""图与网络算法（NetworkX 版）：路径、流量、连通、中心性一网打尽。

解决什么问题
    问题里有"节点 + 边"的结构：交通网、电力网、通信网、社交关系、任务依赖、
    供应链。常见问法：最短路径、最大流/最小割、最小生成树、关键节点、
    最优指派。

本文件给的示例
    1. 最短路（Dijkstra / Bellman-Ford）与路径还原
    2. 最小生成树（Kruskal）
    3. 最大流 / 最小割
    4. 中心性（度、介数、接近）——找"关键节点"
    5. 二分图最大匹配（指派问题）

用法
    python network_demo.py
"""
from __future__ import annotations

import networkx as nx
import numpy as np


def shortest_path_demo(verbose=True):
    """最短路：边权是距离。Dijkstra 要求非负权；有负权用 Bellman-Ford。"""
    G = nx.Graph()
    edges = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5),
             ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6),
             ("E", "F", 3)]
    G.add_weighted_edges_from(edges)

    dist = nx.dijkstra_path_length(G, "A", "F", weight="weight")
    path = nx.dijkstra_path(G, "A", "F", weight="weight")
    all_dist = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight"))
    if verbose:
        print(f"A→F 最短距离 {dist}，路径 {path}")
        print(f"A 到各点距离：{all_dist['A']}")
    return dist, path, all_dist


def mst_demo(verbose=True):
    """最小生成树：用最少的总边长把所有点连通（铺管道、架线路）。"""
    G = nx.Graph()
    G.add_weighted_edges_from([("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
                               ("B", "D", 5), ("C", "D", 8), ("D", "E", 2)])
    mst = nx.minimum_spanning_tree(G, weight="weight")
    total = mst.size(weight="weight")
    if verbose:
        print(f"MST 边：{sorted(mst.edges(data=True))}")
        print(f"总权重 = {total}")
    return mst, total


def maxflow_demo(verbose=True):
    """最大流 / 最小割：管道容量、通量上限、瓶颈在哪。"""
    D = nx.DiGraph()
    D.add_edge("s", "a", capacity=10)
    D.add_edge("s", "b", capacity=5)
    D.add_edge("a", "b", capacity=4)
    D.add_edge("a", "t", capacity=8)
    D.add_edge("b", "t", capacity=10)
    flow_value, flow = nx.maximum_flow(D, "s", "t")
    cut_value, (S, T) = nx.minimum_cut(D, "s", "t")
    if verbose:
        print(f"最大流 = {flow_value}（等于最小割 {cut_value}）")
        print(f"分片 S={sorted(S)}, T={sorted(T)}")
        print("各路流量：", {f"{u}->{v}": f for u, d in flow.items() for v, f in d.items() if f > 0})
    return flow_value, (S, T)


def centrality_demo(verbose=True):
    """中心性：找网络里的关键节点（度中心=连接多，介数中心=最短路径必经）。"""
    G = nx.karate_club_graph()
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G)
    clo = nx.closeness_centrality(G)
    top_betweenness = sorted(bet.items(), key=lambda kv: -kv[1])[:3]
    if verbose:
        print("介数中心性前三：", [(n, round(v, 4)) for n, v in top_betweenness])
        print("度中心性前三：", sorted(deg.items(), key=lambda kv: -kv[1])[:3])
    return deg, bet, clo


def assignment_demo(cost, verbose=True):
    """指派问题（二分图最大权匹配）：n 个人 n 个任务，总成本最小。

    cost[i][j] 是"人 i 做任务 j"的成本。求解用匈牙利算法的 networkx 实现：
    max_weight_matching 求最大权，所以把成本取负、并加成完全图。
    """
    cost = np.asarray(cost, dtype=float)
    n, m = cost.shape
    G = nx.Graph()
    workers = [f"w{i}" for i in range(n)]
    tasks = [f"t{j}" for j in range(m)]
    G.add_nodes_from(workers, bipartite=0)
    G.add_nodes_from(tasks, bipartite=1)
    w_max = cost.max()
    for i in range(n):
        for j in range(m):
            G.add_edge(workers[i], tasks[j], weight=float(w_max - cost[i, j]))  # 转成最大权

    matching = nx.max_weight_matching(G, maxcardinality=True)
    pairs = []
    for u, v in matching:
        w, t = (u, v) if u in workers else (v, u)
        if w in workers and t in tasks:
            pairs.append((w, t))
    pairs.sort()
    total = sum(cost[int(u[1:]), int(v[1:])] for u, v in pairs)
    if verbose:
        print("指派结果：", [(u, v, float(cost[int(u[1:]), int(v[1:])])) for u, v in pairs])
        print(f"总成本 = {total:.1f}")
    return pairs, total


def assignment_bruteforce(cost, verbose=True):
    """小规模（n <= 8）用全排列暴力枚举，验证上面的匹配结果是否最优。"""
    from itertools import permutations

    cost = np.asarray(cost, dtype=float)
    n = cost.shape[0]
    best, best_perm = np.inf, None
    for perm in permutations(range(cost.shape[1]), n):
        s = cost[np.arange(n), perm].sum()
        if s < best:
            best, best_perm = s, perm
    if verbose:
        print(f"暴力枚举最优：{best:.1f}，指派 {best_perm}")
    return best, best_perm


if __name__ == "__main__":
    print("== 1. 最短路")
    shortest_path_demo()
    print("\n== 2. 最小生成树")
    mst_demo()
    print("\n== 3. 最大流 / 最小割")
    maxflow_demo()
    print("\n== 4. 中心性（karate 网络）")
    centrality_demo()
    print("\n== 5. 指派问题")
    cost = np.array([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]])
    pairs, total = assignment_demo(cost)
    best, perm = assignment_bruteforce(cost)
    assert abs(total - best) < 1e-9, "匹配结果不是最优，检查图的构造"
    print("与暴力枚举结果一致 ✓")
