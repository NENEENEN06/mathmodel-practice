# 求解代码

- `main.py`：入口，`python main.py --data <数据文件> --out results`
- `utils.py`：读数据、固定随机种子、中文出图、保存图片

## 约定

1. **能一键复现**：README 里写清楚怎么跑、依赖怎么装、数据从哪来。
2. **种子固定**：`set_seed(0)`，优化/随机类模型必须写。
3. **图从代码出**：论文里的图都由脚本生成，不贴截图；统一 300dpi。
4. **结果落盘**：关键数字写进 `results/summary.json`，别只打印在屏幕上。
5. **一个模型一个文件**：`model_q1.py`、`model_q2.py`，别都塞进 `main.py`。

## 常用库

`numpy` / `pandas` / `scipy` / `scikit-learn` / `matplotlib`；优化问题用 `scipy.optimize`、`pulp`、`cvxpy`；可用 `shared/models/` 里现成的实现。
