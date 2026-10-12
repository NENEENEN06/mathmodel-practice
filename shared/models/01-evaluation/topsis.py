"""熵权法 + TOPSIS：客观赋权的多方案排序。

解决什么问题
    有 m 个方案、n 个指标（有的越大越好，有的越小越好），要给出综合排名。

两部分可以拆开用
    1. 熵权法：纯客观赋权，谁的信息量大谁权重大（指标取值差异越大越"有用"）；
    2. TOPSIS：排序——每个方案离"正理想解"越近、离"负理想解"越远越优。

输入
    X : (m, n) 原始数据矩阵
    kinds : 长度 n 的列表，'benefit' 表示越大越好，'cost' 表示越小越好

输出
    排名表（DataFrame）：各方案得分与名次

用法
    python topsis.py                    # 跑内置例子
    >>> from topsis import topsis_rank
    >>> topsis_rank(X, kinds=['benefit', 'cost'])
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def entropy_weights(X: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """熵权法求权重。要求 X 非负（负值请先做正向化/平移）。"""
    X = np.asarray(X, dtype=float)
    col_min = X.min(axis=0)
    if (col_min < 0).any():
        X = X - col_min  # 平移保证非负，不改变指标间的相对差异
    p = X / np.where(X.sum(axis=0) == 0, 1, X.sum(axis=0))
    p = np.clip(p, eps, None)
    e = -(p * np.log(p)).sum(axis=0) / np.log(X.shape[0])   # 信息熵
    d = 1 - e                                                # 差异系数
    return d / d.sum()


def topsis_rank(X, kinds=None, weights=None, names=None, verbose=True) -> pd.DataFrame:
    """TOPSIS 排序。weights 为 None 时用熵权法自动赋权。"""
    X = np.asarray(X, dtype=float)
    m, n = X.shape
    kinds = list(kinds) if kinds else ["benefit"] * n
    if len(kinds) != n:
        raise ValueError("kinds 长度必须等于指标个数")
    if weights is None:
        weights = entropy_weights(X)
    weights = np.asarray(weights, dtype=float)
    weights = weights / weights.sum()

    # 1) 正向化：成本型指标取倒数（正数数据）或做极差变换
    Z = X.copy()
    for j, k in enumerate(kinds):
        if k == "cost":
            if (X[:, j] <= 0).any():
                Z[:, j] = X[:, j].max() - X[:, j] + 1e-12
            else:
                Z[:, j] = 1.0 / X[:, j]

    # 2) 向量归一化（消除量纲）
    norm = np.sqrt((Z ** 2).sum(axis=0))
    norm[norm == 0] = 1
    Z = Z / norm

    # 3) 加权
    V = Z * weights

    # 4) 正/负理想解与距离
    v_pos, v_neg = V.max(axis=0), V.min(axis=0)
    d_pos = np.sqrt(((V - v_pos) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - v_neg) ** 2).sum(axis=1))

    # 5) 相对接近度
    score = d_neg / np.where((d_pos + d_neg) == 0, 1, d_pos + d_neg)

    df = pd.DataFrame({
        "方案": names if names else [f"方案{i+1}" for i in range(m)],
        "D+": d_pos,
        "D-": d_neg,
        "得分": score,
    })
    df["排名"] = df["得分"].rank(ascending=False).astype(int)
    df = df.sort_values("排名").reset_index(drop=True)

    if verbose:
        print("指标权重：", np.round(weights, 4))
        print(df.round(4).to_string(index=False))
    return df


if __name__ == "__main__":
    # 例子：5 个方案，4 个指标（成本、效率、稳定性、价格）
    X = np.array([
        [12.0, 88.0, 0.93, 320.0],
        [15.0, 92.0, 0.88, 280.0],
        [9.0, 80.0, 0.97, 410.0],
        [11.0, 85.0, 0.95, 350.0],
        [14.0, 90.0, 0.90, 300.0],
    ])
    kinds = ["cost", "benefit", "benefit", "cost"]
    res = topsis_rank(X, kinds, names=[f"方案{chr(65+i)}" for i in range(5)])
    assert res["排名"].tolist() == sorted(res["排名"].tolist())
