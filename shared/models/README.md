# 模型资料库

三个人的公共弹药库：**能用、能跑、能查来源**的数学建模模型实现，按用途分类。

代码只依赖成熟开源库（SciPy / scikit-learn / statsmodels / NetworkX / PuLP / CVXPY），
算法本身按教科书标准公式写，**不抄第三方仓库的代码**，所以没有许可负担，可以直接用在论文的附录里。

## 分类

| 目录 | 用途 | 什么时候用 | 收录 |
| --- | --- | --- | --- |
| `01-evaluation/` | 评价类 | 多指标打分、排序、选优 | 层次分析法（AHP）、熵权法、TOPSIS、模糊综合评价 |
| `02-forecasting/` | 预测类 | 有序列要外推、有因果关系要拟合 | 灰色预测 GM(1,1)、ARIMA、多元回归/岭回归 |
| `03-optimization/` | 优化类 | 有目标函数和约束 | 线性/整数规划（SciPy + PuLP）、遗传算法、模拟退火、粒子群 |
| `04-graph/` | 图论与网络 | 路径、流量、连通、中心性 | 最短路、最大流、最小生成树、中心性、匹配 |
| `05-simulation/` | 微分方程与仿真 | 有动力学过程要模拟 | ODE 数值解、蒙特卡洛、排队系统仿真、元胞自动机 |
| `06-statistics/` | 统计与数据 | 要检验、要分组、要降维 | 假设检验、方差分析、相关分析、聚类、PCA |

每个目录一份 `README.md`：**什么时候用这个模型、输入输出长什么样、怎么调用、常见坑**。

## 依赖

```bash
pip install -r requirements.txt
```

主要就是：`numpy pandas scipy scikit-learn statsmodels networkx pulp cvxpy matplotlib openpyxl`。
除 `pymoo`（多目标优化，可选）外都装得上，不需要商业求解器。

## 怎么用

1. 先在对应分类的 `README.md` 里挑模型（每个文件顶部也有"解决什么问题"）。
2. 直接跑一遍看效果：

   ```bash
   cd 01-evaluation && python ahp.py
   ```

3. 改完公共库跑一次总检查（会逐个脚本执行并报告结果）：

   ```bash
   python run_all.py                 # 全部
   python run_all.py 03-optimization # 只跑某个分类
   ```

4. 用的时候**复制到当次练习的 `code/` 目录**，改成题目要求，别在公共库里改——
   公共库保持干净，别人还要用。
5. 验证过值得留的更通用实现，再挪回这里并在下表中登记。

> 状态：15 个脚本全部在本机跑通（Python 3.12 + numpy 2.5 / scipy 1.18 / statsmodels 0.15 / networkx 3.7 / scikit-learn 1.9）。

## 收录登记

| 文件 | 模型 | 依据 | 依赖 |
| --- | --- | --- | --- |
| `01-evaluation/ahp.py` | 层次分析法（含一致性检验） | Saaty 1–9 标度、特征向量法 | numpy |
| `01-evaluation/topsis.py` | 熵权法 + TOPSIS | 熵权客观赋权、优劣解距离法 | numpy, pandas |
| `01-evaluation/fuzzy_evaluation.py` | 模糊综合评价 | 隶属度矩阵 + 最大隶属原则 | numpy |
| `02-forecasting/gm11.py` | 灰色预测 GM(1,1) | 累加生成 + 最小二乘 + 后验差检验 | numpy |
| `02-forecasting/arima_demo.py` | ARIMA | Box-Jenkins，AIC 定阶 | statsmodels |
| `02-forecasting/regression_demo.py` | 多元回归 / 岭回归 | OLS、岭正则、交叉验证 | scikit-learn, statsmodels |
| `03-optimization/lp_milp.py` | 线性 / 整数规划 | 单纯形法、分支定界（SciPy milp 与 PuLP 双解法互验） | scipy, pulp |
| `03-optimization/genetic_algorithm.py` | 遗传算法 | 选择-交叉-变异，实数/二进制编码 | numpy |
| `03-optimization/simulated_annealing.py` | 模拟退火 | Metropolis 准则 + 降温表；含 TSP | numpy |
| `03-optimization/particle_swarm.py` | 粒子群 | 速度-位置更新 + 多次运行统计 | numpy |
| `04-graph/network_demo.py` | 图算法全家桶 | 最短路 / 最大流 / MST / 中心性 | networkx |
| `05-simulation/ode_demo.py` | ODE 数值解 | RK45 自适应步长 | scipy |
| `05-simulation/monte_carlo.py` | 蒙特卡洛 | 大数定律、随机模拟 | numpy |
| `06-statistics/stats_demo.py` | 检验 / 方差分析 / 相关 | t 检验、单因素 ANOVA、Pearson/Spearman | scipy, statsmodels |
| `06-statistics/clustering_pca.py` | 聚类与降维 | K-means、层次聚类、PCA | scikit-learn |

## 值得收藏的开源项目（要更专业的实现去看这些）

| 项目 | 干什么 | 地址 |
| --- | --- | --- |
| SciPy | 优化、积分、插值、统计、ODE 的底座 | https://github.com/scipy/scipy |
| scikit-learn | 机器学习与统计学习全流程 | https://github.com/scikit-learn/scikit-learn |
| statsmodels | 计量/统计模型（ARIMA、回归诊断、ANOVA） | https://github.com/statsmodels/statsmodels |
| NetworkX | 图与网络算法 | https://github.com/networkx/networkx |
| PuLP | 线性/整数规划建模（自带 CBC 求解器） | https://github.com/coin-or/pulp |
| CVXPY | 凸优化建模（含二次锥、半正定） | https://github.com/cvxpy/cvxpy |
| PyMOO | 多目标优化（NSGA-II 等现成算法） | https://github.com/anyoptimization/pymoo |
| DEAP | 进化算法框架（GA/GP/ES） | https://github.com/DEAP/deap |
| Geatpy | 国产进化算法库，中文文档全 | https://github.com/geatpy-dev/geatpy |
| OR-Tools | Google 运筹优化（路径、排程、CP-SAT） | https://github.com/google/or-tools |
| PyGAD | 遗传算法入门友好 | https://github.com/ahmedfgad/GeneticAlgorithmPython |
| pyswarm / scikit-opt | 粒子群等群智能算法 | https://github.com/guofei9987/scikit-opt |

> 引用规范：论文里用到上述库要写清版本，例如"本文使用 Python 3.11 + SciPy 1.18 + scikit-learn 1.9 求解"。
