"""遗传算法（GA）：目标函数没有解析形式、或搜索空间大且不连续时用。

解决什么问题
    优化目标不能求导（仿真结果、查表、规则黑箱），或者约束很花，传统算法进不去。
    GA 靠"种群 + 选择 + 交叉 + 变异"在解空间里随机搜索，通用、好讲。

输入
    fitness : 函数，输入个体（一维数组）→ 适应度（越大越好）
    bounds / n_bits : 实数编码给上下界，二进制编码给位数

输出
    最优个体、最优适应度、收敛曲线数据

特点
    一定能跑出结果，但**不保证全局最优**——论文里要给多次运行的统计（均值/标准差）。

用法
    python genetic_algorithm.py
"""
from __future__ import annotations

import numpy as np


def ga_real(fitness, bounds, pop_size=80, generations=200, pc=0.8, pm=0.1,
            elite=2, seed=0, verbose=True):
    """实数编码 GA（适合连续变量）。"""
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in bounds], dtype=float)
    hi = np.array([b[1] for b in bounds], dtype=float)
    n = len(bounds)

    pop = rng.uniform(lo, hi, size=(pop_size, n))
    fit = np.array([fitness(ind) for ind in pop])
    history = []

    for _ in range(generations):
        # 精英保留 + 锦标赛选择
        order = np.argsort(-fit)
        new_pop = [pop[i].copy() for i in order[:elite]]
        while len(new_pop) < pop_size:
            a, b = rng.choice(pop_size, 2, replace=False)
            p1 = pop[a] if fit[a] > fit[b] else pop[b]
            a, b = rng.choice(pop_size, 2, replace=False)
            p2 = pop[a] if fit[a] > fit[b] else pop[b]

            # 算术交叉
            if rng.random() < pc:
                lam = rng.random(n)
                child = lam * p1 + (1 - lam) * p2
            else:
                child = p1.copy()
            # 高斯变异
            mask = rng.random(n) < pm
            if mask.any():
                child[mask] += rng.normal(0, 0.05 * (hi - lo)[mask])
            new_pop.append(np.clip(child, lo, hi))

        pop = np.array(new_pop)
        fit = np.array([fitness(ind) for ind in pop])
        history.append(float(fit.max()))

    best = int(np.argmax(fit))
    if verbose:
        print(f"最优个体：{np.round(pop[best], 4)}")
        print(f"最优适应度：{fit[best]:.6f}（第 1 代 {history[0]:.6f} → 末代 {history[-1]:.6f}）")
    return pop[best], float(fit[best]), history


def ga_binary(fitness, n_bits, pop_size=80, generations=200, pc=0.8, pm=None,
              seed=0, verbose=True):
    """二进制编码 GA（适合 0-1 选择、子集问题）。"""
    rng = np.random.default_rng(seed)
    pm = pm or 1.0 / n_bits

    pop = rng.integers(0, 2, size=(pop_size, n_bits))
    fit = np.array([fitness(ind) for ind in pop])
    history = []

    for _ in range(generations):
        order = np.argsort(-fit)
        new_pop = [pop[i].copy() for i in order[:2]]
        while len(new_pop) < pop_size:
            a, b = rng.choice(pop_size, 2, replace=False)
            p1 = pop[a] if fit[a] > fit[b] else pop[b]
            a, b = rng.choice(pop_size, 2, replace=False)
            p2 = pop[a] if fit[a] > fit[b] else pop[b]

            if rng.random() < pc:
                cut = rng.integers(1, n_bits)
                child = np.concatenate([p1[:cut], p2[cut:]])
            else:
                child = p1.copy()
            mask = rng.random(n_bits) < pm
            child[mask] = 1 - child[mask]
            new_pop.append(child)

        pop = np.array(new_pop)
        fit = np.array([fitness(ind) for ind in pop])
        history.append(float(fit.max()))

    best = int(np.argmax(fit))
    if verbose:
        print(f"最优 0-1 串：{pop[best]}")
        print(f"最优适应度：{fit[best]:.6f}")
    return pop[best], float(fit[best]), history


if __name__ == "__main__":
    print("== 连续优化：max f(x) = -(x1-2)^2 - (x2+1)^2 + 5, x ∈ [-5, 5]^2（理论最优 x=(2,-1)）")
    f = lambda x: -(x[0] - 2) ** 2 - (x[1] + 1) ** 2 + 5     # noqa: E731
    best, val, hist = ga_real(f, [(-5, 5), (-5, 5)], seed=42)
    assert abs(best[0] - 2) < 0.2 and abs(best[1] + 1) < 0.2

    print("\n== 0-1 问题：12 件物品里挑价值最大、总重不超过 100 的组合")
    rng = np.random.default_rng(0)
    v, w = rng.integers(10, 100, 12), rng.integers(5, 30, 12)
    fit_bin = lambda x: 0.0 if x @ w > 100 else float(x @ v)   # noqa: E731
    ga_binary(fit_bin, n_bits=12, seed=1)
