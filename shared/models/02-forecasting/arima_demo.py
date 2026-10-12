"""ARIMA 时间序列预测（statsmodels 版）：带趋势/季节性的序列外推。

解决什么问题
    序列有足够长度（>= 40 个点比较稳），既想用自相关结构、又想处理趋势，
    比灰色模型适用面更宽。季节性数据用 SARIMA（本文件的 seasonal_order）。

输入
    y : 一维序列；可含趋势/季节

输出
    最优阶数 (p,d,q)（按 AIC 网格搜索）、预测值、残差检验（Ljung-Box）

用法
    python arima_demo.py
"""
from __future__ import annotations

import warnings

import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")


def select_order(y, p_range=range(0, 4), d_range=(0, 1, 2), q_range=range(0, 4), seasonal=False):
    """按 AIC 网格搜索最优 (p, d, q)。数据量大时把范围收窄。"""
    best = (None, np.inf)
    for p in p_range:
        for d in d_range:
            for q in q_range:
                try:
                    m = ARIMA(y, order=(p, d, q)).fit()
                except Exception:
                    continue
                if m.aic < best[1]:
                    best = ((p, d, q), m.aic)
    return best


def arima_forecast(y, steps: int = 5, order=None, verbose: bool = True):
    """拟合 ARIMA 并预测。order 为 None 时自动定阶。"""
    y = np.asarray(y, dtype=float).ravel()
    if order is None:
        order, aic = select_order(y)
        if verbose:
            print(f"自动定阶结果：ARIMA{order}（AIC = {aic:.2f}）")
    model = ARIMA(y, order=order).fit()
    fc = model.get_forecast(steps=steps)
    mean = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)

    # 残差白噪声检验：p 值大 = 残差像白噪声 = 模型把信息抽干净了
    lb = acorr_ljungbox(model.resid, lags=[min(10, len(y) // 5)], return_df=True)
    lb_p = float(lb["lb_pvalue"].iloc[0])

    if verbose:
        print(model.summary().tables[1])
        print(f"Ljung-Box 检验 p = {lb_p:.4f} → "
              + ("残差是白噪声，模型可用" if lb_p > 0.05 else "残差还有结构，考虑加阶或差分"))
        print(f"未来 {steps} 期预测：{np.round(mean, 3)}")
        print(f"95% 置信区间：\n{np.round(ci, 3)}")
    return mean, ci, {"order": order, "ljungbox_p": lb_p}


if __name__ == "__main__":
    # 例子：带趋势 + 季节性的月度数据
    rng = np.random.default_rng(0)
    t = np.arange(120)
    y = 50 + 0.4 * t + 8 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 2, size=t.size)

    mean, ci, info = arima_forecast(y, steps=6)
    assert len(mean) == 6
    print("\n如果是季节性明显的序列，改用 SARIMAX：")
    from statsmodels.tsa.statespace.sarimax import SARIMAX  # noqa: F401
    print("  SARIMAX(y, order=(1,1,1), seasonal_order=(1,1,1,12)).fit()")
