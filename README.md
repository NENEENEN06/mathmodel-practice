# Math Model Practice · 数学建模竞赛练手

三人协作的数学建模**实战演练仓**：真题库 + 分角色工作区 + 每场练习的完整成果。

---

## 仓库结构

```
.
├── problems/          真题库（题目原文，按竞赛/年份分）
│   ├── cumcm/         全国大学生数学建模竞赛（国赛）
│   ├── mcm-icm/       美国大学生数学建模竞赛（美赛）
│   └── shuweibei/     数维杯大学生数学建模挑战赛
├── workspace/         三个人的个人工作区（按角色分，见下）
│   ├── modeler/       建模手：拆题、选模型、推公式
│   ├── coder/         代码手：数据、求解、出图
│   └── writer/        论文手：摘要、行文、排版
├── practices/         每场练习一个目录：三人协作的全部产出
├── shared/            公用资产
│   ├── models/        **分类模型资料库**（评价/预测/优化/图论/仿真/统计，每个都有 README）
│   ├── data/          公用小数据集
│   └── templates/     图表、表格、命名规范
├── templates/         可直接套用的骨架
│   ├── practice/      一场练习的目录骨架：README + REVIEW + code/ + paper/（复制即用）
│   └── paper/         三个竞赛的赛制、时间、评分关注点
├── scripts/           工具
│   ├── build_index.py          生成 problems/README.md 真题索引
│   └── download_attachments.py 在本地拉赛题附件（不入库）
└── data/attachments/  附件数据落地目录（不进 Git，见下）
```

## 三个角色与工作区

工作区按**角色**分，一人认领一个（轮换时把名字挪过去就行）：

| 工作区 | 角色 | 干什么 | 当前认领 |
| --- | --- | --- |------|
| `workspace/modeler/` | **建模手** | 拆题、查背景、定问题分解、选模型、推公式、设计灵敏度分析 | 张博文  |
| `workspace/coder/` | **代码手** | 数据清洗、写求解代码、参数调优、扫描、出图出表 | 叶建新  |
| `workspace/writer/` | **论文手** | 摘要、行文、公式排版、图表整合、格式自查 | xxx  |

- 仓库维护：叶建新 [@NENEENEN06](https://github.com/NENEENEN06)（队友注册 GitHub 后我加协作者权限）
- **每场练习都要轮换角色**——只做一个角色，另外两边的坑永远踩不到。
- 每场练习里谁认领什么，写进那场练习的 `README.md` 分工表，别只靠嘴说。

## 一场练习怎么走

1. **选题**：从 `problems/` 里挑一道真题；想模拟真实赛程就整套 A/B/C 一起看、限时定题。
2. **开工作目录**：`cp -r templates/practice practices/<日期>-<题目简称>`，填好分工与时间表。
3. **推进节奏**（按 72 小时赛制演练）：
   - 0–6h：读题、查背景、定问题分解与候选模型
   - 6–18h：确定模型，写出求解方案，第一版结果跑通
   - 18–54h：求解、灵敏度分析、模型检验、出图表
   - 54–66h：成文（摘要最关键，先写摘要再写正文）
   - 66–72h：查格式、查数据引用、内部互评、定稿
4. **交付物**（都放在那场练习目录下）：论文 PDF、求解代码（能一键复现）、图表与结果、`REVIEW.md` 复盘。
5. **复盘**：哪里卡住、模型为什么选错、下次遇到什么特征该想到什么方法。

## 协作约定（详见 [CONTRIBUTING.md](CONTRIBUTING.md)）

- `main` 只放定稿；练习时各自开分支 `practice/<日期>-<题号>-<名字>`，做完提 PR 合并。
- 提交信息写清改了哪个部分（摘要 / 模型 / 代码 / 图表）。
- **大文件不进仓库**：附件数据、中间结果、论文中间产物都不提交；附件用 `scripts/download_attachments.py` 在本地拉。

## 真题库

题目原文（PDF）在 `problems/` 里，完整清单见 [problems/README.md](problems/README.md)。目前 **108 道题**：

| 竞赛 | 年份 | 题量 | 来源说明 |
| --- | --- | --- | --- |
| 国赛 CUMCM | 2016–2026 | 52 | 竞赛官网年度赛题包（2016–2023 官方包是 RAR5，题目取自公开镜像） |
| 美赛 MCM/ICM | 2021–2026 | 36 | COMAP 官方下载为主，个别文件官方端点传输中断改用镜像 |
| 数维杯 | 2019–2026 | 20 | 尽力收集：公开仓库 / 转载重排 / 官网页面存档，逐条标注来源 |

- 每题一行来源与备注写在 `problems/meta.json` 里，索引里可查。
- 数维杯官方只公开当年题目，历史真题缺口与可用链接见 [problems/shuweibei/SOURCES_AND_GAPS.md](problems/shuweibei/SOURCES_AND_GAPS.md)。

附件数据（国赛每年几十到几百 MB）**不入库**，用脚本在本地下载：

```bash
python3 scripts/download_attachments.py --all          # 全部下到 data/attachments/
python3 scripts/download_attachments.py --year 2024    # 只下某一年
```

## 维护

- `problems/README.md` 由 `scripts/build_index.py` 生成，**不要手改索引表**。
- 新增真题：把题目文件放进 `problems/<竞赛>/<年份>/`，在 `problems/meta.json` 里补标题，再跑一次 `build_index.py`。
