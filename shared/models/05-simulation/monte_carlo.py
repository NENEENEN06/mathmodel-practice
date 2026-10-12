"""蒙特卡洛与随机仿真：解析算不动，就大量抽样。

解决什么问题
    ① 求积分/面积的数值解（高维时比数值积分好用）；
    ② 系统有随机性，要评估"平均表现、极端情况、风险概率"——排队、库存、
       可靠性、交通、金融风险都属这一类。

本文件给的示例
    1. 随机投点估 π（练手理解收敛速度 O(1/√n)）
    2. 蒙特卡洛积分
    3. M/M/1 排队系统仿真（到达率 λ、服务率 μ、队列长度/等待时间统计）
    4. 风险仿真：不确定参数下结果落在失败区间的概率（可靠性/投资场景）

用法
    python monte_carlo.py
"""
from __future__ import annotations

import numpy as np


def estimate_pi(n=1_000_000, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    pts = rng.uniform(-1, 1, size=(n, 2))
    inside = (pts ** 2).sum(axis=1) <= 1
    pi_hat = 4 * inside.mean()
    stderr = 4 * np.sqrt(inside.mean() * (1 - inside.mean()) / n)   # 这个必须报出来
    if verbose:
        print(f"n = {n:,} → π ≈ {pi_hat:.5f}（标准误 {stderr:.5f}，误差 {abs(pi_hat - np.pi):.5f}）")
    return pi_hat, stderr


def mc_integral(func, a, b, n=200_000, seed=0, verbose=True):
    """∫_a^b f(x) dx ≈ (b-a) * mean(f(x_i))，x_i ~ U(a,b)。"""
    rng = np.random.default_rng(seed)
    x = rng.uniform(a, b, n)
    vals = func(x)
    est = (b - a) * vals.mean()
    stderr = (b - a) * vals.std(ddof=1) / np.sqrt(n)
    if verbose:
        print(f"积分估计 = {est:.5f} ± {1.96 * stderr:.5f}（95% 置信区间）")
    return est, stderr


def mm1_queue(arrival_rate=0.8, service_rate=1.0, n_customers=20_000, seed=0, verbose=True):
    """M/M/1 排队仿真：单服务台、泊松到达、指数服务时间。

    理论值：利用率 ρ=λ/μ，平均队长 L=ρ/(1-ρ)，平均等待 W=ρ/(μ-λ)。
    """
    rng = np.random.default_rng(seed)
    inter = rng.exponential(1 / arrival_rate, n_customers)
    service = rng.exponential(1 / service_rate, n_customers)

    arrival = np.cumsum(inter)
    start = np.empty(n_customers)
    finish = np.empty(n_customers)
    start[0] = arrival[0]
    finish[0] = start[0] + service[0]
    for i in range(1, n_customers):
        start[i] = max(arrival[i], finish[i - 1])   # 服务台空了就立即服务
        finish[i] = start[i] + service[i]

    wait = start - arrival
    rho = arrival_rate / service_rate
    if verbose:
        print(f"λ={arrival_rate}, μ={service_rate}, ρ={rho:.2f}")
        print(f"仿真：平均等待 {wait.mean():.4f}，最长等待 {wait.max():.4f}，"
              f"等待超 1 单位的比例 {(wait > 1).mean():.3%}")
        print(f"理论：平均等待 {rho / (service_rate - arrival_rate):.4f}"
              f"（ρ→1 时仿真误差变大，属正常）")
    return wait, dict(mean_wait=float(wait.mean()), max_wait=float(wait.max()))


def risk_simulation(verbose=True):
    """风险仿真：参数有分布时，评估"指标超限"的概率与分位数。"""
    rng = np.random.default_rng(1)
    n = 50_000
    demand = rng.normal(100, 15, n)          # 需求不确定
    lead_time = rng.gamma(2, 2, n)           # 补货提前期不确定
    capacity = 120

    shortfall = np.maximum(demand * lead_time / 10 - capacity, 0)   # 缺口
    p_short = (shortfall > 0).mean()
    var95 = np.quantile(shortfall, 0.95)
    if verbose:
        print(f"缺货概率 = {p_short:.3%}")
        print(f"缺口 95% 分位 = {var95:.2f}（可作为安全库存依据）")
        print(f"缺口均值 = {shortfall.mean():.2f}")
    return p_short, var95


if __name__ == "__main__":
    print("== 1. 投点估 π")
    estimate_pi()
    print("\n== 2. 蒙特卡洛积分 ∫_0^π sin(x) dx = 2")
    mc_integral(np.sin, 0, np.pi)
    print("\n== 3. M/M/1 排队系统仿真")
    mm1_queue()
    print("\n== 4. 风险仿真（不确定需求 + 提前期）")
    risk_simulation()
