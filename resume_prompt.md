请继续 STEMHUB AMC 项目，本轮开始从修复后的数据重新生成 2021 Fall AMC 12 teaching pages。

项目目录：
D:\STEMHUB_AMC

当前状态：
- 2021 Fall 基础数据已修复并通过专项验证
- Fall A/B 各 25 题，50 个答案全部验证
- Spring/Fall 题面重复数为 0
- 31 个旧错误详情页及 manifest 记录已删除
- 当前 manifest：2,086 条
- 当前 missing/triage：264 条
- 2021 Fall triage：ready_to_generate=29，needs_diagram=5，solution_high_risk=16
- 验证报告：docs/audits/2021_fall_repair_validation.md

本轮请只从 `missing_problem_triage.csv` 中选择 5-10 道 `2021 Fall + ready_to_generate` 题，优先按 A卷题号顺序处理。

要求：
1. 先检查 git status，确认工作区干净并读取 docs/PROJECT_STATE.md。
2. 只使用修复后的 `amc12/all_problems.csv`，不得从 Git 历史恢复旧 Fall 页面或解答。
3. 逐题用 AoPS Fall Answer Key 验证答案，只作参考，不复制解答。
4. 每题生成独立详情页与原创英文 teaching solution，使用 4-6 个有标题的步骤，解释学生应如何思考。
5. 数学公式使用 LaTeX/MathJax，保留双语界面资源。
6. 本轮不要处理 `needs_diagram` 或 `solution_high_risk` 题。
7. 更新 manifest、总览详情链接、progress、report、resume_prompt 和 missing triage。
8. 验证页面、题面、答案、MathJax、双语资源、step 数和 AoPS reference。
9. 验证通过后 commit/push；建议 commit message：`Regenerate 2021 Fall teaching pages batch 1`。
10. 推送后抽查 GitHub Pages。

完成后请直接给出下一轮可复制 prompt。
