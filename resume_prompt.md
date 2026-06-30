请继续 STEMHUB AMC problem teaching pages 批量生成任务。

当前状态：
- Batch 10 已生成并本地验证通过，内容为 2003 AMC 10B Problems 1-3, 5-10。
- 2003 AMC 10B Problem 4 因缺少 flower-bed 图形被跳过。
- Batch 10 的 commit/push 如果还没完成，请先检查 git status，提交信息使用：Add problem teaching pages batch 10。
- Batch 10 完成提交推送后，下一批从 2003 AMC 10B Problem 11 开始。

继续策略：
- 每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过。
- 更新 problem_pages_manifest.json、problem_pages_report.md、problem_pages_progress.md、resume_prompt.md。
- 验证页面存在、详情链接可打开、MathJax 正文没有错误的 \\[ 或 \\]、每题至少 4 个 teaching steps。
- 每批验证后 commit 并 push。
