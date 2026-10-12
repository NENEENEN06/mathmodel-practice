"""线性规划与整数规划：有目标函数 + 线性约束就用它。

解决什么问题
    生产计划、配料、运输、选址、分配、排班等"在约束下最优"的问题，
    目标与约束都是线性的。

三个层次
    - 连续变量 → SciPy `linprog`（单纯形/内点法，无额外依赖）
    - 整数/0-1 变量 → SciPy `milp`（HiGHS 分支定界，同样无额外依赖）
    - 想写成"公式那样" → PuLP + CBC（自带求解器；本文件做了 PuLP 版本兼容）

用法
    python lp_milp.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import LinearConstraint, linprog, milp


def solve_lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, verbose=True):
    """求解 min c·x。注意 SciPy 的默认形式是最小化。

    最大化问题：把 c 取负，结果再取负。
    """
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"求解失败：{res.message}")
    if verbose:
        print("最优解 x =", np.round(res.x, 4))
        print(f"最优目标值 = {res.fun:.4f}（若为最大化问题取负即 {(-res.fun):.4f}）")
    return res.x, res.fun


def solve_milp_scipy(c, A, lb, ub, integrality=None, bounds=None, verbose=True):
    """一般整数规划（SciPy HiGHS）。

    min c·x   s.t.  lb <= A x <= ub；integrality[i]=1 表示 x_i 取整数（0-1 变量配 bounds (0,1)）。
    """
    from scipy.optimize import Bounds

    constraints = LinearConstraint(A, lb, ub)
    if bounds is not None and not isinstance(bounds, Bounds):
        lo = [(-np.inf if b[0] is None else b[0]) for b in bounds]
        hi = [(np.inf if b[1] is None else b[1]) for b in bounds]
        bounds = Bounds(lo, hi)
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    if not res.success:
        raise RuntimeError(f"求解失败：{res.message}")
    if verbose:
        print("最优解 x =", np.round(res.x, 4))
        print(f"最优目标值 = {res.fun:.4f}")
    return res.x, res.fun


def _new_binary_var(prob, name):
    """PuLP 版本兼容：4.0 起变量必须由模型创建，老版本用 LpVariable。"""
    import pulp

    if hasattr(prob, "add_variable"):
        return prob.add_variable(name, cat="Binary")
    return pulp.LpVariable(name, cat="Binary")


def _default_solver():
    """PuLP 版本兼容：<=3.x 用自带的 CBC，4.x 换成内置 HiGHS。"""
    import pulp

    if hasattr(pulp, "PULP_CBC_CMD"):
        return pulp.PULP_CBC_CMD(msg=False)
    return pulp.HiGHS()


def _status_label(result):
    """PuLP <=3.x 的 solve 返回状态码，4.x 返回 LpSolveStats 对象。"""
    import pulp

    if hasattr(pulp, "LpStatus"):
        return pulp.LpStatus[result]
    return getattr(result, "status_str", str(result))


def solve_milp_pulp(values, weights, capacity, verbose=True):
    """0-1 背包：PuLP 建模示例（分支定界交给自带求解器）。"""
    import pulp

    n = len(values)
    prob = pulp.LpProblem("knapsack", pulp.LpMaximize)
    x = [_new_binary_var(prob, f"x{i}") for i in range(n)]

    prob += pulp.lpSum(v * xi for v, xi in zip(values, x))              # 目标
    prob += pulp.lpSum(w * xi for w, xi in zip(weights, x)) <= capacity  # 约束

    status = _status_label(prob.solve(_default_solver()))
    chosen = [i for i, xi in enumerate(x) if xi.value() > 0.5]
    if verbose:
        print(f"求解状态：{status}")
        print(f"选中物品下标：{chosen}")
        print(f"总价值 = {pulp.value(prob.objective):.1f}, "
              f"总重量 = {sum(weights[i] for i in chosen):.1f} / {capacity}")
    assert str(status).startswith("Optimal")
    return chosen, float(pulp.value(prob.objective))


if __name__ == "__main__":
    print("== 连续线性规划：两种产品如何在资源约束下最大化利润")
    # max 40x1 + 30x2  s.t.  2x1 + x2 <= 100, x1 + 3x2 <= 90, x1,x2 >= 0
    solve_lp(c=[-40, -30], A_ub=[[2, 1], [1, 3]], b_ub=[100, 90],
             bounds=[(0, None), (0, None)])

    print("\n== 0-1 背包：同一题用 SciPy 和 PuLP 各解一遍，互相验证")
    rng = np.random.default_rng(0)
    values = rng.integers(10, 100, 12).astype(float)
    weights = rng.integers(5, 30, 12).astype(float)
    cap = 100.0

    print("-- SciPy milp（最大化取负）")
    x_sp, f_sp = solve_milp_scipy(
        c=-values, A=weights.reshape(1, -1), lb=-np.inf, ub=cap,
        integrality=np.ones_like(values), bounds=[(0, 1)] * len(values),
    )
    print(f"选中：{np.flatnonzero(x_sp > 0.5).tolist()}")

    print("-- PuLP + CBC")
    chosen_pl, val_pl = solve_milp_pulp(values, weights, cap)

    assert abs(-f_sp - val_pl) < 1e-6, "两个求解器结果不一致，先查模型"
    print(f"两个求解器一致：总价值 {val_pl:.1f}")
