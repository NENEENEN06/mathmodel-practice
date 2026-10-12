"""粒子群优化（PSO）：连续优化里最好上手的群智能算法。

解决什么问题
    连续变量的全局优化（参数标定、超参数搜索、载荷分配），
    不需要梯度，实现短、收敛快。

核心
    每个粒子记住自己的历史最优 pbest，全体共享全局最优 gbest，
    速度按 v ← w·v + c1·r1·(pbest-x) + c2·r2·(gbest-x) 更新。

参数经验
    w 0.4~0.9（也可线性递减）、c1 = c2 = 2 左右、粒子数 20~50。

用法
    python particle_swarm.py
"""
from __future__ import annotations

import numpy as np


def pso(objective, bounds, n_particles=40, iterations=200, w=0.7, c1=1.5, c2=1.5,
        seed=0, verbose=True):
    """objective 为最小化目标；bounds 形如 [(lo, hi), ...]。"""
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in bounds], dtype=float)
    hi = np.array([b[1] for b in bounds], dtype=float)
    dim = len(bounds)

    X = rng.uniform(lo, hi, size=(n_particles, dim))
    V = rng.uniform(-1, 1, size=(n_particles, dim)) * (hi - lo) * 0.1
    pbest = X.copy()
    pbest_val = np.array([objective(x) for x in X])

    g_idx = int(np.argmin(pbest_val))
    gbest, gbest_val = pbest[g_idx].copy(), float(pbest_val[g_idx])
    history = [gbest_val]

    for _ in range(iterations):
        r1, r2 = rng.random((n_particles, dim)), rng.random((n_particles, dim))
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest - X)
        X = np.clip(X + V, lo, hi)

        vals = np.array([objective(x) for x in X])
        improved = vals < pbest_val
        pbest[improved] = X[improved]
        pbest_val[improved] = vals[improved]

        g_idx = int(np.argmin(pbest_val))
        if pbest_val[g_idx] < gbest_val:
            gbest, gbest_val = pbest[g_idx].copy(), float(pbest_val[g_idx])
        history.append(gbest_val)

    if verbose:
        print(f"全局最优解：{np.round(gbest, 5)}")
        print(f"最优目标值：{gbest_val:.6f}（第 1 代 {history[0]:.6f} → 末代 {history[-1]:.6f}）")
    return gbest, gbest_val, history


def pso_multi_run(objective, bounds, runs=10, seed=0, verbose=True):
    """让模型抗随机性：多次独立运行，报均值与标准差（论文里这样写才对）。"""
    vals = []
    for r in range(runs):
        _, v, _ = pso(objective, bounds, seed=seed + r, verbose=False)
        vals.append(v)
    vals = np.array(vals)
    if verbose:
        print(f"{runs} 次独立运行：最优 {vals.min():.6f}，均值 {vals.mean():.6f}，"
              f"标准差 {vals.std():.6f}")
    return vals


if __name__ == "__main__":
    print("== 连续优化：min f(x) = (x1-3)^2 + (x2+2)^2 + 0.5*sin(4*x1)*cos(4*x2)")
    obj = lambda x: (x[0] - 3) ** 2 + (x[1] + 2) ** 2 + 0.5 * np.sin(4 * x[0]) * np.cos(4 * x[1])  # noqa: E731
    bounds = [(-10, 10), (-10, 10)]
    xb, fb, _ = pso(obj, bounds, seed=1)
    pso_multi_run(obj, bounds, runs=5, seed=100)
    assert abs(xb[0] - 3) < 0.5 and abs(xb[1] + 2) < 0.5
