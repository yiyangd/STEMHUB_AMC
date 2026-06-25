# 续跑 Prompt

请继续 AMC 10 题目分类与教材编写数据整理任务。

已完成年份：2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021 Spring, 2022, 2023, 2024
尚缺年份或未发现 PDF：无
上次任务开始时间：2026-06-21T22:36:18-07:00
上次已工作耗时：1:02:36

请扫描 `D:\AMC10_Codex\input\` 中新增的 PDF，继续为 ???????? 范围内的每一年生成：
- `output/{year}/{year}.html`
- `output/{year}/{year}_classified.md`
- `output/{year}/{year}_problems.csv`

然后重新运行/更新：
- `output/all_years_index.html`
- `output/all_problems.csv`
- `output/taxonomy.md`
- `output/progress_report.md`

要求：
- 每道题只有一个一级分类和一个二级分类。
- 不要加入额外等级字段。
- PDF 没有答案时 answer 留空，不要编造。
- 图形题在 notes 中说明“题面包含图形”。
- 遇到无法解析的问题，记录到 progress_report.md 后继续。
