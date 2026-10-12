"""聚类与降维：没有标签时怎么分组、指标太多时怎么压缩。

解决什么问题
    ① 把样本按相似度分组（客户分群、地区分级、样品归类）——无监督，没有标准答案，
       所以**要给出选择簇数的依据**；
    ② 指标太多、彼此相关，用 PCA 降维后再评价/分类，顺便看哪些指标在起作用。

本文件给的示例
    1. K-means：肘部法 + 轮廓系数选 k
    2. 层次聚类：画出树状图（论文里很好用）
    3. PCA：方差解释率 + 载荷（哪些原始指标主导各主成分）
    4. DBSCAN：按密度聚类，能识别噪声点、簇数不用预设

用法
    python clustering_pca.py
"""
from __future__ import annotations

import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def standardize(X):
    """标准化是聚类/降维前必做的一步（不然后面量纲大的指标说了算）。"""
    return StandardScaler().fit_transform(np.asarray(X, dtype=float))


def choose_k(X, k_range=range(2, 9), seed=0, verbose=True):
    """肘部法（看 inertia 拐点）+ 轮廓系数（越大越好）。"""
    Xs = standardize(X)
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(Xs)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(Xs, km.labels_))
    best_k = list(k_range)[int(np.argmax(silhouettes))]
    if verbose:
        for k, ine, sil in zip(k_range, inertias, silhouettes):
            print(f"k={k}: inertia={ine:9.2f}, 轮廓系数={sil:.4f}"
                  + ("  ← 最优" if k == best_k else ""))
    return best_k, inertias, silhouettes


def kmeans_cluster(X, k=3, seed=0, verbose=True):
    Xs = standardize(X)
    km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(Xs)
    if verbose:
        print(f"k={k}：轮廓系数 {silhouette_score(Xs, km.labels_):.4f}")
        print("各簇样本数：", np.bincount(km.labels_))
        print("各簇中心（标准化空间）：\n", np.round(km.cluster_centers_, 3))
    return km.labels_, km


def hierarchical_cluster(X, k=3, method="ward", verbose=True):
    """层次聚类：不需要预设簇数也能看结构，导出的 linkage 可以画树状图。"""
    from scipy.cluster.hierarchy import linkage

    Xs = standardize(X)
    Z = linkage(Xs, method=method)
    labels = AgglomerativeClustering(n_clusters=k, linkage=method).fit_predict(Xs)
    if verbose:
        print(f"层次聚类（{method}）：轮廓系数 {silhouette_score(Xs, labels):.4f}")
        print("linkage 矩阵形状：", Z.shape, "（用它画树状图：scipy.cluster.hierarchy.dendrogram）")
    return labels, Z


def pca_analysis(X, n_components=None, feature_names=None, verbose=True):
    """PCA：看方差解释率，决定压到几维；看载荷，解释各主成分的含义。"""
    Xs = standardize(X)
    pca = PCA(n_components=n_components).fit(Xs)
    cum = np.cumsum(pca.explained_variance_ratio_)
    n_keep = int(np.searchsorted(cum, 0.85) + 1)
    if verbose:
        print("各主成分方差解释率：", np.round(pca.explained_variance_ratio_, 4))
        print(f"累计解释率：{np.round(cum, 4)} → 保留 {n_keep} 个成分可解释 85% 以上方差")
        if feature_names:
            load = np.round(pca.components_[:n_keep], 3)
            for i in range(n_keep):
                print(f"  PC{i+1} 载荷（{feature_names}）：{load[i]}")
    return pca, Xs


def dbscan_cluster(X, eps=0.5, min_samples=5, verbose=True):
    """DBSCAN：按密度聚类，簇数自动确定，-1 表示噪声点。"""
    Xs = standardize(X)
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(Xs)
    n_noise = int((labels == -1).sum())
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if verbose:
        print(f"DBSCAN：{n_clusters} 个簇，{n_noise} 个噪声点")
        if n_clusters > 1:
            mask = labels != -1
            print(f"非噪声点轮廓系数 {silhouette_score(Xs[mask], labels[mask]):.4f}")
    return labels


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    # 造三群、四维的数据
    centers = [(0, 0, 0, 0), (5, 5, 1, 0), (0, 6, 4, 4)]
    X = np.vstack([rng.normal(c, 1.0, size=(60, 4)) for c in centers])
    names = ["指标1", "指标2", "指标3", "指标4"]

    print("== 1. 选 k（肘部法 + 轮廓系数）")
    best_k, _, _ = choose_k(X)
    assert best_k == 3, f"造的 3 群数据应该选出 k=3，得到 {best_k}"

    print("\n== 2. K-means 聚类")
    kmeans_cluster(X, k=3)

    print("\n== 3. 层次聚类")
    hierarchical_cluster(X, k=3)

    print("\n== 4. PCA 降维")
    pca_analysis(X, feature_names=names)

    print("\n== 5. DBSCAN")
    dbscan_cluster(X, eps=0.8, min_samples=5)
