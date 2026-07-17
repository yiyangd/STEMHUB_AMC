# 2024 AMC 8 题目分类

- 题量：25
- 比赛：AMC 8
- form：空字符串（AMC 8 无 A/B 卷）
- 答案：逐题按 AoPS Wiki Answer Key 核验

## 一级分类统计

| 一级分类 | 题量 |
| --- | ---: |
| 几何与测量 | 8 |
| 组合数学 | 6 |
| 数论 | 4 |
| 代数 | 3 |
| 算术与数感 | 3 |
| 概率与统计 | 1 |

## 二级分类统计

| 一级分类 | 二级分类 | 题量 |
| --- | --- | ---: |
| 代数 | 函数初步 | 1 |
| 代数 | 方程 | 1 |
| 代数 | 模式规律 | 1 |
| 几何与测量 | 三角形 | 1 |
| 几何与测量 | 周长与长度 | 1 |
| 几何与测量 | 圆 | 1 |
| 几何与测量 | 坐标 | 2 |
| 几何与测量 | 空间几何 | 1 |
| 几何与测量 | 面积 | 2 |
| 数论 | 数字问题 | 3 |
| 数论 | 整除 | 1 |
| 概率与统计 | 概率 | 1 |
| 算术与数感 | 分数与小数 | 1 |
| 算术与数感 | 比例 | 2 |
| 组合数学 | 分类讨论 | 1 |
| 组合数学 | 容斥 | 1 |
| 组合数学 | 构造 | 2 |
| 组合数学 | 计数 | 2 |

## 逐题分类

### Problem 1 · 数论 / 数字问题

What is the ones digit of 222,222 - 22,222 - 2,222 - 222 - 22 - 2? (A) 0 (B) 2 (C) 4 (D) 6 (E) 8

- 答案：B
- 标签：个位数;位值
- 核心思路：只追踪各项的个位数并在模 10 下计算。
- 备注：无

### Problem 2 · 算术与数感 / 分数与小数

What is the value of 44/11 + 110/44 + 44/1100 in decimal form? (A) 6.4 (B) 6.504 (C) 6.54 (D) 6.9 (E) 6.94

- 答案：C
- 标签：分数;小数;化简
- 核心思路：先约分各分数，再统一用小数相加。
- 备注：无

### Problem 3 · 几何与测量 / 面积

Four squares of side length 4, 7, 9, and 10 are arranged in increasing size order so that their left and bottom edges align. They alternate white-gray-white-gray. What is the visible gray area? (A) 42 (B) 45 (C) 49 (D) 50 (E) 52

- 答案：E
- 标签：正方形;重叠面积
- 核心思路：把可见灰色区域写成两个正方形面积差之和。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 4 · 数论 / 数字问题

Yunji added the integers from 1 to 9 but left out one number. Her incorrect sum was a square. Which number was omitted? (A) 5 (B) 6 (C) 7 (D) 8 (E) 9

- 答案：E
- 标签：平方数;整数和
- 核心思路：先求 1 到 9 的总和，再检查与相邻平方数的差。
- 备注：无

### Problem 5 · 数论 / 整除

Aaliyah rolls two standard six-sided dice. Their product is a multiple of 6. Which integer cannot be their sum? (A) 5 (B) 6 (C) 7 (D) 8 (E) 9

- 答案：B
- 标签：骰子;整除;枚举
- 核心思路：按乘积同时含因子 2 和 3 的条件枚举可行点数对。
- 备注：无

### Problem 6 · 几何与测量 / 周长与长度

Four skating paths P, Q, R, and S are shown. What is their order from shortest to longest? (A) P, Q, R, S (B) P, R, S, Q (C) Q, S, P, R (D) R, P, S, Q (E) R, S, P, Q

- 答案：D
- 标签：路径;弧长;比较
- 核心思路：把每条路径分解为可直接比较的线段或圆弧。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 7 · 组合数学 / 构造

A 3-by-7 rectangle is tiled without overlap using 2-by-2, 1-by-4, and 1-by-1 tiles. What is the minimum possible number of 1-by-1 tiles? (A) 1 (B) 2 (C) 3 (D) 4 (E) 5

- 答案：E
- 标签：铺砖;奇偶性;构造
- 核心思路：先用面积和行列限制给出下界，再展示达到下界的铺法。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 8 · 代数 / 模式规律

On Monday Taye has $2. Each day he either gains $3 or doubles the previous amount. How many different amounts could he have on Thursday? (A) 3 (B) 4 (C) 5 (D) 6 (E) 7

- 答案：D
- 标签：状态枚举;重复值
- 核心思路：逐日列出可达金额并合并重复结果。
- 备注：无

### Problem 9 · 算术与数感 / 比例

Maria's marbles are red, green, or blue. She has half as many red as green and twice as many blue as green. Which could be the total number of marbles? (A) 24 (B) 25 (C) 26 (D) 27 (E) 28

- 答案：E
- 标签：比例;整数约束
- 核心思路：把三种数量写成同一整数参数的倍数。
- 备注：无

### Problem 10 · 代数 / 函数初步

Carbon dioxide was 338 ppm in January 1980 and increases about 1.515 ppm per year. What is the expected January 2030 level, rounded to the nearest integer? (A) 399 (B) 414 (C) 420 (D) 444 (E) 459

- 答案：B
- 标签：线性增长;估算
- 核心思路：用初值加上年数乘年增长率建立线性模型。
- 备注：无

### Problem 11 · 几何与测量 / 坐标

Triangle ABC has A(5,7), B(11,7), and C(3,y), where y > 7. Its area is 12. What is y? (A) 8 (B) 9 (C) 10 (D) 11 (E) 12

- 答案：D
- 标签：坐标;三角形面积
- 核心思路：把 AB 作为水平底边，由面积求点 C 到底边的高。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 12 · 代数 / 方程

Rohan has 90 guppies in four tanks. Tank 2 has 1 more than tank 1, tank 3 has 2 more than tank 2, and tank 4 has 3 more than tank 3. How many are in tank 4? (A) 20 (B) 21 (C) 23 (D) 24 (E) 26

- 答案：E
- 标签：一元方程;应用题
- 核心思路：设第一缸数量为未知数，用总数建立一次方程。
- 备注：无

### Problem 13 · 组合数学 / 计数

Buzz Bunny starts on the ground, makes six one-step hops up or down a staircase, never going below the ground, and ends on the ground. How many hop sequences are possible? (A) 4 (B) 5 (C) 6 (D) 8 (E) 12

- 答案：B
- 标签：路径计数;上下步
- 核心思路：枚举含三个上步和三个下步且前缀不低于地面的序列。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 14 · 组合数学 / 分类讨论

The directed routes have lengths A->M=8, A->X=5, X->M=2, X->Y=10, M->Y=6, M->C=14, Y->C=5, C->Z=10, Y->Z=17, and M->Z=25. What is the shortest distance from A to Z? (A) 28 (B) 29 (C) 30 (D) 31 (E) 32

- 答案：A
- 标签：有向图;最短路
- 核心思路：按可达节点逐层比较到达该节点的最短累计距离。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 15 · 数论 / 数字问题

F, L, Y, B, U, and G are distinct digits. FLYFLY is the largest number satisfying 8 x FLYFLY = BUGBUG. What is FLY + BUG? (A) 1089 (B) 1098 (C) 1107 (D) 1116 (E) 1125

- 答案：C
- 标签：位值;重复数字
- 核心思路：利用 FLYFLY=1001*FLY 和 BUGBUG=1001*BUG 化简。
- 备注：无

### Problem 16 · 组合数学 / 构造

Minh places the integers 1 through 81 in a 9-by-9 grid. What is the least number of rows and columns whose product could be divisible by 3? (A) 8 (B) 9 (C) 10 (D) 11 (E) 12

- 答案：D
- 标签：网格;覆盖;倍数
- 核心思路：把 3 的倍数集中放置，比较覆盖它们所需的最少行列数。
- 备注：无

### Problem 17 · 组合数学 / 计数

A white king and a black king are placed on different squares of a 3-by-3 chessboard so that they do not attack each other. In how many ordered placements can this be done? (A) 20 (B) 24 (C) 27 (D) 28 (E) 32

- 答案：E
- 标签：棋盘;补集计数
- 核心思路：按角、边、中心位置分类统计不能相邻的第二个位置。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 18 · 几何与测量 / 圆

Three concentric circles have radii 1, 2, and 3. The annulus from radius 1 to 2 is shaded, and a sector of the annulus from radius 2 to 3 is shaded. If shaded and unshaded areas are equal, what is the sector angle BOC? (A) 108 (B) 120 (C) 135 (D) 144 (E) 150

- 答案：A
- 标签：圆环;扇形;面积
- 核心思路：用圆环面积和扇形占整圆比例建立等面积关系。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 19 · 组合数学 / 容斥

Jordan owns 15 pairs of sneakers. Nine pairs are red, six are white, ten are high-top, and five are low-top. What is the least possible fraction of the collection that is red high-top? (A) 0 (B) 1/5 (C) 4/15 (D) 1/3 (E) 2/5

- 答案：C
- 标签：集合交集;最小值
- 核心思路：用两类数量之和减去总数得到交集的最小值。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 20 · 几何与测量 / 空间几何

Any three vertices of cube PQRSTUVW form a triangle. How many equilateral triangles contain P? (A) 0 (B) 1 (C) 2 (D) 3 (E) 6

- 答案：D
- 标签：立方体;空间距离
- 核心思路：比较从 P 到其余顶点的距离并寻找三边相等的顶点组三元组。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 21 · 算术与数感 / 比例

Initially green and yellow frogs were in the ratio 3:1. Then 3 green frogs moved to the sunny side and 5 yellow frogs moved to the shady side, producing ratio 4:1. What is the current difference between green and yellow frogs? (A) 10 (B) 12 (C) 16 (D) 20 (E) 24

- 答案：E
- 标签：比例变化;应用题
- 核心思路：用初始比例参数表示两类数量并代入交换后的比例。
- 备注：无

### Problem 22 · 几何与测量 / 面积

A tape roll has outer diameter 4 inches, inner diameter 2 inches, and tape thickness 0.015 inches. If completely unrolled, approximately how long is it, to the nearest 100 inches? (A) 300 (B) 600 (C) 1200 (D) 1500 (E) 1800

- 答案：B
- 标签：圆环;体积守恒;近似
- 核心思路：令卷起胶带的截面积等于展开后长度乘厚度。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 23 · 几何与测量 / 坐标

A segment from (0,4) to (2,0) intersects the interiors of 4 grid cells. How many grid cells have interiors intersected by the segment from (2000,3000) to (5000,8000)? (A) 6000 (B) 6500 (C) 7000 (D) 7500 (E) 8000

- 答案：C
- 标签：格点线段;网格计数
- 核心思路：用横跨竖线数、横线数和穿过格点的重复计数修正。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 24 · 几何与测量 / 三角形

Two 45-45-90 mountain shapes have peak heights 8 and 12 feet and overlap. Their union area is 183 square feet. Their sides meet at height h. What is h? (A) 4 (B) 5 (C) 4sqrt(2) (D) 6 (E) 5sqrt(2)

- 答案：B
- 标签：等腰直角三角形;重叠面积
- 核心思路：用两座山的面积和减去重叠三角形面积。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 25 · 概率与统计 / 概率

An airplane has 4 rows of 3 seats. Eight passengers occupy random seats. A couple boards next. What is the probability that two adjacent seats in one row remain for them? (A) 8/15 (B) 32/55 (C) 20/33 (D) 34/55 (E) 8/11

- 答案：C
- 标签：随机座位;补集;计数
- 核心思路：等价为随机留下四个空座时至少含一对同排相邻座，按补集计数。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 末页未呈现 A-E 选项；题面、图形与选项按 AoPS Wiki 同年题页核验
