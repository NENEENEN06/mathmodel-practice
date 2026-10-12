"""微分方程建模与数值求解：有"变化率"就要它。

解决什么问题
    题目里有随时间/空间演化的量：传染病扩散、温度传导、药物代谢、电路、
    种群增长、机械振动、水流。写出微分方程后多数没有解析解，用数值方法解。

本文件给的示例
    1. SIR 传染病模型（ODE 方程组 + 参数拟合思路）
    2. 弹簧阻尼振动（二阶方程转一阶方程组）
    3. 一阶衰减 + 拟合参数（scipy.optimize.curve_fit 配 solve_ivp）

用法
    python ode_demo.py
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit


def sir_model(t, y, beta, gamma):
    """SIR：dS/dt = -βSI/N, dI/dt = βSI/N - γI, dR/dt = γI。"""
    S, I, R = y
    N = S + I + R
    return [-beta * S * I / N, beta * S * I / N - gamma * I, gamma * I]


def solve_sir(N=10000, I0=10, beta=0.4, gamma=0.1, days=160, verbose=True):
    """返回时间点、各仓室序列，以及基本再生数 R0 = β/γ。"""
    y0 = [N - I0, I0, 0.0]
    t_eval = np.linspace(0, days, days * 4)
    sol = solve_ivp(sir_model, (0, days), y0, t_eval=t_eval, args=(beta, gamma),
                    method="RK45", rtol=1e-8, atol=1e-10)
    if not sol.success:
        raise RuntimeError(f"求解失败：{sol.message}")
    S, I, R = sol.y
    peak_day, peak_I = float(t_eval[int(np.argmax(I))]), float(I.max())
    if verbose:
        print(f"R0 = β/γ = {beta / gamma:.2f}")
        print(f"峰值在第 {peak_day:.1f} 天，感染人数 {peak_I:.0f}（占总人口 {peak_I / N:.1%}）")
        print(f"最终累计感染 R(∞) = {R[-1]:.0f}（{R[-1] / N:.1%}）")
    return t_eval, S, I, R


def spring_damper(t, y, m=1.0, c=0.5, k=2.0):
    """二阶方程 m x'' + c x' + k x = 0 转成一阶方程组 y = [x, v]。"""
    x, v = y
    return [v, (-c * v - k * x) / m]


def solve_spring(verbose=True):
    sol = solve_ivp(spring_damper, (0, 20), [1.0, 0.0], t_eval=np.linspace(0, 20, 400))
    if verbose:
        print(f"阻尼振动：x(0)=1, v(0)=0 → x(20)={sol.y[0][-1]:.4f}，"
              f"最大位移 {sol.y[0].max():.4f}")
    return sol


def fit_ode_params(t_data, y_data, N, I0=None, p0=(0.4, 0.1), verbose=True):
    """用实测数据反推 ODE 参数（建模题常见的"参数辨识"）。

    注意：N（总人口）必须由题目给定或另行估计，不能拿"感染人数之和"顶替——
    那样会把拟合结果带偏。
    """
    t_data = np.asarray(t_data, dtype=float)
    y_data = np.asarray(y_data, dtype=float)
    I0 = float(y_data[0]) if I0 is None else float(I0)

    def model(t, beta, gamma):
        sol = solve_ivp(sir_model, (t[0], t[-1]), [N - I0, I0, 0.0], t_eval=t,
                        args=(beta, gamma), method="RK45")
        return sol.y[1]

    popt, pcov = curve_fit(model, t_data, y_data, p0=p0, maxfev=20000)
    perr = np.sqrt(np.diag(pcov))
    if verbose:
        print(f"拟合得到 β = {popt[0]:.4f} ± {perr[0]:.4f}, "
              f"γ = {popt[1]:.4f} ± {perr[1]:.4f}, R0 = {popt[0] / popt[1]:.2f}")
    return popt, perr


if __name__ == "__main__":
    print("== 1. SIR 传染病模型")
    t, S, I, R = solve_sir()
    print("\n== 2. 阻尼振动")
    solve_spring()

    print("\n== 3. 参数辨识：假装手里只有感染人数序列（N 由题目给出）")
    obs_t = np.linspace(0, 100, 20)
    _, _, I_true, _ = solve_sir(days=100)
    idx = np.clip(np.searchsorted(t, obs_t), 0, I_true.size - 1)   # 末端点防越界
    I_obs = I_true[idx] * (1 + np.random.default_rng(0).normal(0, 0.01, obs_t.size))
    popt, _ = fit_ode_params(obs_t, I_obs, N=10000)
    assert abs(popt[0] - 0.4) < 0.05 and abs(popt[1] - 0.1) < 0.05, "参数辨识结果偏离真值太远"
