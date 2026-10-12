# 公用资产

三个人都会用到的东西放这里，改动前在群里说一声。

- `models/` —— 常用模型的可用实现（评价类、预测类、优化类、图论…）
- `data/` —— 公用小数据集（超过 10 MB 的别放，走 `data/attachments/`）
- `templates/` —— 表格、图表、命名规范的说明

## 模型资料库

`models/` 是**分类整理好的模型实现库**（每个模型都能直接跑，带 README 说明使用场景、输入输出和坑）：

| 目录 | 用途 |
| --- | --- |
| `models/01-evaluation/` | 评价类：AHP、熵权法、TOPSIS、模糊综合评价 |
| `models/02-forecasting/` | 预测类：灰色 GM(1,1)、ARIMA、回归/岭回归 |
| `models/03-optimization/` | 优化类：线性/整数规划、遗传算法、模拟退火、粒子群 |
| `models/04-graph/` | 图论：最短路、最大流、MST、中心性、指派 |
| `models/05-simulation/` | 仿真：ODE 数值解、蒙特卡洛、排队仿真 |
| `models/06-statistics/` | 统计：假设检验、ANOVA、相关、聚类、PCA |

入口见 [`models/README.md`](models/README.md)（含依赖、收录清单、值得收藏的开源项目）。

> 用的时候**复制到当次练习的 `code/` 里改**，别直接改公共库。
