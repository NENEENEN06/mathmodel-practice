"""模拟退火（SA）：在解空间里"先乱走、后收敛"的通用启发式算法。

解决什么问题
    组合优化（排班、路径、装箱）或带大量局部极值的目标函数，
    梯度方法/整数规划都下不去手时，SA 用带概率的劣解接受机制跳出局部最优。

核心
    温度 T 高时敢接受差解，T 低时只接受更好的解；按 Metropolis 准则
    以 exp(-ΔE/T) 的概率接受劣解，降温系数 alpha 一般取 0.9~0.99。

用法
    python simulated_annealing.py
"""
from __future__ import annotations

import numpy as np


def simulated_annealing(objective, x0, neighbor, T0=100.0, T_end=1e-3, alpha=0.95,
                        iters_per_temp=50, seed=0, verbose=True):
    """通用 SA。

    objective : 目标函数（最小化）
    x0        : 初始解
    neighbor  : 生成邻域解的函数 neighbor(x, rng) -> 新解
    """
    rng = np.random.default_rng(seed)
    x = np.array(x0, dtype=float) if np.ndim(x0) else x0
    f = objective(x)
    best_x, best_f = x, f
    T = T0
    history = [(T, best_f)]

    while T > T_end:
        for _ in range(iters_per_temp):
            cand = neighbor(x, rng)
            fc = objective(cand)
            dE = fc - f
            if dE < 0 or rng.random() < np.exp(-dE / T):   # Metropolis 准则
                x, f = cand, fc
                if f < best_f:
                    best_x, best_f = x, f
        T *= alpha
        history.append((T, best_f))

    if verbose:
        print(f"最优解：{best_x}")
        print(f"最优目标值：{best_f:.6f}（初值 {history[0][1]:.6f}）")
    return best_x, best_f, history


def sa_tsp(distance, T0=100.0, T_end=1e-3, alpha=0.97, iters_per_temp=200, seed=0,
           verbose=True):
    """SA 解 TSP：邻域 = 2-opt（交换两段）。返回最优访问顺序与总路程。"""
    rng = np.random.default_rng(seed)
    n = distance.shape[0]

    def total(route):
        return float(sum(distance[route[i], route[(i + 1) % n]] for i in range(n)))

    route = rng.permutation(n)
    cur = total(route)
    best_route, best_len = route.copy(), cur
    T = T0

    while T > T_end:
        for _ in range(iters_per_temp):
            i, j = sorted(rng.choice(n, 2, replace=False))
            cand = route.copy()
            cand[i:j + 1] = cand[i:j + 1][::-1]
            lc = total(cand)
            if lc < cur or rng.random() < np.exp(-(lc - cur) / T):
                route, cur = cand, lc
                if cur < best_len:
                    best_route, best_len = route.copy(), cur
        T *= alpha

    if verbose:
        print(f"最优路径长度：{best_len:.3f}")
        print(f"访问顺序：{best_route}")
    return best_route, best_len


if __name__ == "__main__":
    print("== 连续函数：min f(x) = x1^2 + x2^2 + 3*sin(2*x1)（有多个局部极值）")
    obj = lambda x: x[0] ** 2 + x[1] ** 2 + 3 * np.sin(2 * x[0])       # noqa: E731
    nb = lambda x, rng: x + rng.normal(0, 0.5, size=x.shape)           # noqa: E731
    xb, fb, _ = simulated_annealing(obj, np.array([3.0, 3.0]), nb, seed=7)

    print("\n== 组合优化：10 个城市的 TSP（坐标随机）")
    rng = np.random.default_rng(0)
    pts = rng.uniform(0, 100, size=(10, 2))
    D = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1))
    route, length = sa_tsp(D, seed=3)
    assert len(set(route.tolist())) == 10
