"""多元回归与岭回归：找自变量对因变量的影响，并做预测。

解决什么问题
    有多个解释变量，要判断谁影响大、方向如何、模型解释力多强（R²、显著性），
    自变量之间还可能有共线性（岭回归/正则化对付它）。

输入
    X : (n_samples, n_features)，y : (n_samples,)

输出
    OLS 系数与显著性、R²、VIF（共线性诊断）、岭回归交叉验证误差

用法
    python regression_demo.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler


def ols_report(X, y, feature_names=None, verbose=True):
    """最小二乘回归：系数、p 值、R²、VIF 一次给全。"""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).ravel()
    names = feature_names or [f"x{i+1}" for i in range(X.shape[1])]

    Xc = sm.add_constant(X)
    model = sm.OLS(y, Xc).fit()

    # VIF：>10 说明该变量与其他变量高度共线
    vif = {}
    for i, name in enumerate(names):
        others = np.delete(X, i, axis=1)
        if others.shape[1] == 0:
            vif[name] = 1.0
            continue
        r2 = sm.OLS(X[:, i], sm.add_constant(others)).fit().rsquared
        vif[name] = float(1 / (1 - r2)) if r2 < 1 else np.inf

    table = pd.DataFrame({
        "变量": ["const"] + names,
        "系数": model.params,
        "标准误": model.bse,
        "t值": model.tvalues,
        "p值": model.pvalues,
    })
    if verbose:
        print(table.round(4).to_string(index=False))
        print(f"R² = {model.rsquared:.4f}, 调整 R² = {model.rsquared_adj:.4f}, "
              f"F 检验 p = {model.f_pvalue:.3e}")
        print("VIF：", {k: round(v, 2) for k, v in vif.items()},
              "（>10 提示共线性严重，改用岭回归）")
    return model, vif


def ridge_cv(X, y, alphas=None, verbose=True):
    """岭回归 + 交叉验证选正则强度，用来对付共线性、或样本量小于变量数的情况。"""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).ravel()
    alphas = alphas if alphas is not None else np.logspace(-3, 3, 40)

    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    model = RidgeCV(alphas=alphas, scoring="neg_mean_squared_error").fit(Xs, y)
    rmse = np.sqrt(-cross_val_score(model, Xs, y, cv=5, scoring="neg_mean_squared_error").mean())
    if verbose:
        print(f"岭回归：最优 alpha = {model.alpha_:.4f}，5 折交叉验证 RMSE = {rmse:.4f}")
        print("标准化系数：", np.round(model.coef_, 4))
    return model, scaler, rmse


if __name__ == "__main__":
    # 例子：3 个自变量预测产出，其中 x2 与 x1 高度相关（故意造共线性）
    rng = np.random.default_rng(1)
    n = 80
    x1 = rng.normal(10, 2, n)
    x2 = 0.9 * x1 + rng.normal(0, 0.5, n)
    x3 = rng.normal(5, 1.5, n)
    y = 3 * x1 - 1.5 * x3 + rng.normal(0, 2, n)

    X = np.column_stack([x1, x2, x3])
    model, vif = ols_report(X, y, feature_names=["x1", "x2", "x3"])
    ridge, scaler, rmse = ridge_cv(X, y)
    assert vif["x1"] > 10 and rmse > 0        # 共线性确实被 VIF 抓到了
