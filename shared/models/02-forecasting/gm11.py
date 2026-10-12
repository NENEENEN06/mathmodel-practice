"""灰色预测 GM(1,1)：小样本、贫信息序列的预测。

解决什么问题
    只有 4~10 个观测点，做不了复杂统计模型，但需要外推一两期。
    灰色模型用累加生成把随机序列变成近似指数增长的序列再建模。

输入
    x0 : 长度 >= 4 的一维序列（非负、等间隔）

输出
    预测值（含原序列的拟合值 + 未来 steps 期），以及精度检验：
    后验差比值 C 与小误差概率 P。

判定标准（后验差检验）
    C < 0.35 优，< 0.5 合格，< 0.65 勉强；P > 0.95 优，> 0.8 合格。

用法
    python gm11.py                     # 跑内置例子
    >>> from gm11 import gm11_forecast
    >>> yhat, info = gm11_forecast([...], steps=3)
"""
from __future__ import annotations

import numpy as np


def gm11_forecast(x0, steps: int = 3, verbose: bool = True):
    """返回 (预测序列（含历史拟合 + 未来 steps 期）, 检验信息字典)。"""
    x0 = np.asarray(x0, dtype=float).ravel()
    n = x0.size
    if n < 4:
        raise ValueError("至少需要 4 个数据点")
    if (x0 <= 0).any():
        raise ValueError("GM(1,1) 要求序列为正")

    # 1) 一次累加生成
    x1 = np.cumsum(x0)

    # 2) 紧邻均值生成
    z1 = 0.5 * (x1[1:] + x1[:-1])

    # 3) 最小二乘解发展系数 a、灰作用量 b
    B = np.column_stack([-z1, np.ones_like(z1)])
    Y = x0[1:]
    a, b = np.linalg.lstsq(B, Y, rcond=None)[0]

    # 4) 时间响应函数，累减还原
    k = np.arange(0, n + steps)
    x1_hat = (x0[0] - b / a) * np.exp(-a * k) + b / a
    x0_hat = np.diff(np.concatenate([[0], x1_hat]))

    # 5) 后验差检验（只用拟合段）
    resid = x0 - x0_hat[:n]
    c_ratio = resid.std(ddof=1) / x0.std(ddof=1) if x0.std(ddof=1) > 0 else np.inf
    p_small = float((np.abs(resid - resid.mean()) < 0.6745 * x0.std(ddof=1)).mean())

    info = {
        "a": float(a), "b": float(b),
        "发展系数_a": float(a),
        "预测类型": "适合中长期预测" if abs(a) < 0.3 else
                    ("适合短期预测" if abs(a) < 0.5 else "不适合预测，模型退化"),
        "后验差比值C": float(c_ratio),
        "小误差概率P": p_small,
        "精度等级": ("优" if c_ratio < 0.35 and p_small > 0.95 else
                     "合格" if c_ratio < 0.5 and p_small > 0.8 else
                     "勉强" if c_ratio < 0.65 and p_small > 0.7 else "不合格"),
        "相对误差": float(np.abs(resid / x0).mean()),
    }

    if verbose:
        print(f"a = {a:.4f}, b = {b:.4f} → {info['预测类型']}")
        print(f"拟合值：{np.round(x0_hat[:n], 3)}")
        print(f"实际值：{np.round(x0, 3)}")
        print(f"后验差比值 C = {c_ratio:.4f}，小误差概率 P = {p_small:.4f}"
              f"，平均相对误差 {info['相对误差']:.2%} → 精度 {info['精度等级']}")
        print(f"未来 {steps} 期预测：{np.round(x0_hat[n:], 3)}")

    return x0_hat, info


if __name__ == "__main__":
    # 例子：某地逐年用水量（万吨）
    data = [38.6, 42.1, 45.3, 49.8, 54.2, 58.9, 64.0]
    yhat, info = gm11_forecast(data, steps=3)
    assert np.all(np.isfinite(yhat))
    assert info["相对误差"] < 0.05
