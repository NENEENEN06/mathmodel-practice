# 04 图论与网络

**什么时候来这儿**：题目里画得出"节点 + 连线"——城市与道路、站点与线路、设备与管道、任务与依赖、用户与关系。

| 问法 | 用哪个 | 函数 |
| --- | --- | --- |
| 最短/最快/最省怎么走 | 最短路（Dijkstra / Bellman-Ford / Floyd） | `nx.dijkstra_path`、`nx.floyd_warshall` |
| 最多能输送多少 | 最大流 / 最小割 | `nx.maximum_flow`、`nx.minimum_cut` |
| 用最少代价连通所有点 | 最小生成树（Kruskal / Prim） | `nx.minimum_spanning_tree` |
| 谁是关键节点（拆了最要命） | 度/介数/接近中心性、割点 | `nx.betweenness_centrality`、`nx.articulation_points` |
| 谁干什么最省 | 指派（二分图匹配 / 匈牙利算法） | `nx.max_weight_matching` |
| 有几个孤立群体 | 连通分量 / 社区发现 | `nx.connected_components`、`nx.community` |
| 一次走遍所有点（送快递） | TSP（见 `../03-optimization/simulated_annealing.py`） | — |

## 建模要点（论文里必须写）

- **节点和边各代表什么**：边权是距离、时间、成本还是容量？有向还是无向？
- **网络是从哪来的**：数据直接给？还是自己按规则建的（比如"距离 < 5km 视为连通"）——这一步要说清阈值怎么定的。
- **图的性质**：二分图？稀疏还是稠密？这决定了用哪个算法。

## 坑

- **负权边**：Dijkstra 会错，必须换 Bellman-Ford（`nx.bellman_ford_path`）。
- **有向图当无向图算**：单行道、流向性网络建错方向，结果全废。
- **最大流要容量、最小费用流要 (容量, 费用) 二元组**：`add_edge(u, v, capacity=..., weight=...)` 两个都要给。
- **不连通**：算最短路前先确认可达，否则抛异常；`nx.has_path` 先判一下。
- **指派问题的规模**：匈牙利算法适合几十到几百；上千规模考虑线性规划（`03-optimization/lp_milp.py`）或 OR-Tools。
- 一定要**把图画出来**（`nx.draw` / matplotlib）放进论文——网络题的图就是加分项。

## 跑一遍

```bash
python network_demo.py       # 最短路 / MST / 最大流 / 中心性 / 指派，五段示例
```

## 相关开源

NetworkX（本文件用）：https://github.com/networkx/networkx ，
算法清单见官方文档 https://networkx.org/documentation/stable/reference/algorithms/index.html ；
社区发现也可用 `python-louvain`，大规模图用 `igraph` / `graph-tool`。
