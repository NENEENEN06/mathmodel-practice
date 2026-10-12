# 03 优化类

**什么时候来这儿**：题目给了目标（最大利润、最小成本、最短路径）和约束（资源、时间、容量），要"最优方案"。

| 文件 | 方法 | 适用 | 能不能保证最优 |
| --- | --- | --- | --- |
| `lp_milp.py` | 线性 / 整数规划 | 目标与约束都是线性的，变量可连续或 0-1 | **能**（精确解） |
| `genetic_algorithm.py` | 遗传算法 | 目标不可导/黑箱、解空间大、约束花 | 不能，给近似解 |
| `simulated_annealing.py` | 模拟退火 | 组合优化（TSP、排班、装箱）、多局部极值 | 不能，给近似解 |
| `particle_swarm.py` | 粒子群 | 连续变量、参数标定 | 不能，给近似解 |

## 怎么选（报告里要写清理由）

1. **先问能不能建成线性模型**——能就用 LP/MILP，结果可验证、可讲明白，评委最认。
2. 目标里有乘积、指数、max/min → 非线性，看能不能用 CVXPY 转成凸问题（凸的就用凸优化，也是精确解）。
3. 都不行才上启发式（GA/SA/PSO）。**别一上来就 GA**，能用精确解却用随机搜索是丢分项。
4. 启发式的正确姿势：多种子多次运行，报均值 ± 标准差，再和某个基准（贪心/上界）对比。

## 建模四件套（论文必须有）

- 决策变量及其取值范围（连续/整数/0-1 要说清）
- 目标函数（单位、方向：max 还是 min）
- 约束条件（逐条编号，说明物理含义）
- 求解方法与工具（求解器名 + 版本；启发式要给参数表和运行次数）

## 坑

- SciPy `linprog` 默认是**最小化**，最大化要取负再翻回来（`lp_milp.py` 里演示了）。
- 整数规划规模大了会慢：变量上千、或需要"分钟级"出解，考虑 CP-SAT（OR-Tools）或分解算法。
- 启发式的目标函数里**不要有随机性**（比如用仿真估目标），否则算法会追噪声；必须用固定种子。
- 惩罚函数处理约束时，罚系数太小约束破、太大搜索空间被压死——给个合理量级并做灵敏度。
- 解出来了要**回代验证**：把所有约束代入检查一遍（代码里写个 `check_constraints`）。

## 跑一遍

```bash
python lp_milp.py                 # 连续 LP + 0-1 背包（PuLP/CBC）
python genetic_algorithm.py       # 实数编码 + 二进制编码 GA
python simulated_annealing.py     # 连续函数 + 10 城市 TSP
python particle_swarm.py          # PSO + 多次运行统计
```

## 想要更强的现成实现

多目标（NSGA-II/III）用 [PyMOO](https://github.com/anyoptimization/pymoo)，
进化算法框架用 [DEAP](https://github.com/DEAP/deap) 或 [Geatpy](https://github.com/geatpy-dev/geatpy)，
排程/路径/CP-SAT 用 [OR-Tools](https://github.com/google/or-tools)。
