# 练习成果

**每场练习一个目录**，命名 `YYYYMMDD-<竞赛><年份><题号>`，例如：

```
practices/
├── 20261015-cumcm2024A/          国赛 2024 A 题
│   ├── README.md                 分工、时间表、模型选择（由 templates/practice/ 复制）
│   ├── REVIEW.md                 复盘
│   ├── code/                     求解代码（能一键复现）
│   ├── data/                     用到的附件数据（大文件不进仓库）
│   ├── figures/                  图（由 code/ 生成）
│   └── paper/                    论文源文件与 PDF
└── 20261102-mcm2024A/            美赛 2024 A 题
```

## 怎么开一场

```bash
cp -r templates/practice practices/20261015-cumcm2024A
cd practices/20261015-cumcm2024A
# 填 README.md 里的题目、成员、分工、时间表
```

## 原则

- **一场练习一个目录**，别把两次的东西混在一起。
- 目录开出来就填 `README.md`，让另外两个人一眼知道今天干什么。
- 论文定稿后才算做完；只有代码没有论文不算完成。
- 结束后写 `REVIEW.md`，把能复用的东西搬进 `shared/models/`。
