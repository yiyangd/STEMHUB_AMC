# 2025 AMC 8 题目分类

- 题量：25
- 比赛：AMC 8
- form：空字符串（AMC 8 无 A/B 卷）
- 答案：逐题按 AoPS Wiki Answer Key 核验

## 一级分类统计

| 一级分类 | 题量 |
| --- | ---: |
| 几何与测量 | 7 |
| 数论 | 5 |
| 组合数学 | 5 |
| 代数 | 3 |
| 概率与统计 | 3 |
| 算术与数感 | 2 |

## 二级分类统计

| 一级分类 | 二级分类 | 题量 |
| --- | --- | ---: |
| 代数 | 数列 | 2 |
| 代数 | 方程 | 1 |
| 几何与测量 | 体积 | 1 |
| 几何与测量 | 四边形 | 1 |
| 几何与测量 | 圆 | 2 |
| 几何与测量 | 路径与距离 | 1 |
| 几何与测量 | 面积 | 2 |
| 数论 | 余数 | 1 |
| 数论 | 因数与倍数 | 1 |
| 数论 | 数字问题 | 1 |
| 数论 | 整除 | 1 |
| 数论 | 质数 | 1 |
| 概率与统计 | 中位数 | 1 |
| 概率与统计 | 图表与数据 | 1 |
| 概率与统计 | 平均数 | 1 |
| 算术与数感 | 比例 | 2 |
| 组合数学 | 分类讨论 | 1 |
| 组合数学 | 构造 | 3 |
| 组合数学 | 计数 | 1 |

## 逐题分类

### Problem 1 · 几何与测量 / 面积

The eight-pointed star shown in a 4-by-4 grid covers what percent of the grid? (A) 40 (B) 50 (C) 60 (D) 75 (E) 80

- 答案：B
- 标签：网格;面积;百分比
- 核心思路：把星形分割为单位三角形并与 16 个单位方格比较。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未嵌入题图；按 AoPS Wiki 同年题页核验

### Problem 2 · 数论 / 数字问题

Ancient Egyptian hieroglyphs represent powers of ten. What number is represented by the shown combination? (A) 1,423 (B) 10,423 (C) 14,023 (D) 14,203 (E) 14,230

- 答案：B
- 标签：位值;古埃及数字
- 核心思路：按每种象形符号的位值计数并相加。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 3 · 算术与数感 / 比例

Annika and 3 friends share 60 cards equally, 15 each. If 2 more friends join, how many cards does each of the 6 players receive? (A) 8 (B) 9 (C) 10 (D) 11 (E) 12

- 答案：C
- 标签：平均分配;比例
- 核心思路：先由原人数和每人张数求总牌数，再按新人数平均分。
- 备注：无

### Problem 4 · 代数 / 数列

Lucius counts backward by 7: 100, 93, 86, ... What is his 10th number? (A) 30 (B) 37 (C) 42 (D) 44 (E) 47

- 答案：B
- 标签：等差数列
- 核心思路：第十项比第一项少九个公差。
- 备注：无

### Problem 5 · 几何与测量 / 路径与距离

On a unit street grid, B=(0,0), C=(2,4), A=(7,3), and factory F=(6,5). Betty drives F to A to B to C to F. What is the shortest total distance in blocks? (A) 20 (B) 22 (C) 24 (D) 26 (E) 28

- 答案：C
- 标签：网格距离;曼哈顿距离
- 核心思路：逐段使用横向与纵向位移绝对值之和。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 6 · 数论 / 整除

Sekou writes 15, 16, 17, 18, and 19. He erases one number so the sum of the remaining four is a multiple of 4. Which number is erased? (A) 15 (B) 16 (C) 17 (D) 18 (E) 19

- 答案：C
- 标签：整除;余数
- 核心思路：先求总和的模 4 余数，再匹配要删去的数。
- 备注：源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 7 · 概率与统计 / 图表与数据

On an exam, 5 students scored at least 95%, 13 at least 90%, 27 at least 85%, and 50 at least 80%. How many scored at least 80% but less than 90%? (A) 8 (B) 14 (C) 22 (D) 37 (E) 45

- 答案：D
- 标签：累计频数;区间人数
- 核心思路：用至少 80% 的累计人数减去至少 90% 的人数。
- 备注：无

### Problem 8 · 几何与测量 / 体积

A cube net has area 18 square centimeters. What is the cube's volume in cubic centimeters? (A) 3sqrt(3) (B) 6 (C) 9 (D) 6sqrt(3) (E) 9sqrt(3)

- 答案：A
- 标签：立方体;表面积;体积
- 核心思路：由六个正方形总面积求棱长，再求棱长的三次方。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 9 · 概率与统计 / 平均数

For the six pairs of numbers directly opposite on a clock, take each pair's average. What is the average of those six results? (A) 5 (B) 6.5 (C) 8 (D) 9.5 (E) 12

- 答案：B
- 标签：平均数;对称配对
- 核心思路：每个对面数对的和相同，因此六个平均数相同。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 10 · 几何与测量 / 面积

A 5-by-3 rectangle is rotated 90 degrees clockwise about the midpoint of a length-5 side, overlapping the original. What total area is covered by the union? (A) 21 (B) 22.25 (C) 23 (D) 23.75 (E) 25

- 答案：D
- 标签：旋转;重叠面积;并集
- 核心思路：用两矩形面积之和减去重叠区域面积。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 仅保留外链而未嵌入题图；图形按 AoPS Wiki 同年题页核验

### Problem 11 · 组合数学 / 构造

Three tetrominoes tile a 3-by-4 rectangle. At least one is an S tetromino. Which are the other two tiles? (A) I and L (B) I and T (C) L and L (D) L and S (E) O and T

- 答案：C
- 标签：四连方;铺砖
- 核心思路：根据 S 块放置后的边界缺口尝试可行拼法并排除其余组合。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 12 · 几何与测量 / 圆

A 24-unit-square cross-shaped region is shown. What is the area of the largest circle that fits inside it? (A) 3pi (B) 4pi (C) 5pi (D) 6pi (E) 8pi

- 答案：C
- 标签：内切圆;半径;网格
- 核心思路：由最窄方向上的边界距离确定最大半径。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 13 · 数论 / 余数

Each even number 2,4,6,...,50 is divided by 7. Which histogram gives counts for remainders 0 through 6? (A) [3,4,4,3,4,3,4] (B) [3,4,4,4,3,3,4] (C) [3,4,4,4,4,3,3] (D) [4,3,4,3,4,3,4] (E) [4,4,3,4,3,4,3]

- 答案：A
- 标签：模 7;周期;直方图
- 核心思路：按偶数模 7 的七项周期统计 25 个数的余数频数。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 只有题图链接；直方图频数已按 AoPS Wiki 图形转写

### Problem 14 · 概率与统计 / 中位数

A number N is inserted into 2, 6, 7, 7, 28. The new mean is twice the median. What is N? (A) 7 (B) 14 (C) 20 (D) 28 (E) 34

- 答案：E
- 标签：平均数;中位数;分类
- 核心思路：按 N 在有序表中的位置判断中位数，再用平均数条件求 N。
- 备注：无

### Problem 15 · 组合数学 / 构造

In a 6-by-6 grid, 13 cells are silver and the rest gold. Fold vertically to form 18 overlapping pairs. Let m and M be the least and greatest possible numbers of gold-gold pairs. What is m+M? (A) 12 (B) 14 (C) 16 (D) 18 (E) 20

- 答案：C
- 标签：配对;极值;构造
- 核心思路：把 13 个银格分配到 18 对中，分别最大化和最小化含银的格对数。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 16 · 组合数学 / 分类讨论

Choose five distinct integers from 1 to 10 and five from 11 to 20, with no two chosen numbers differing by 10. What is the sum of the ten chosen numbers? (A) 95 (B) 100 (C) 105 (D) 110 (E) 115

- 答案：C
- 标签：配对;不变量
- 核心思路：把 k 与 k+10 配成十对；条件迫使每对恰选一个，再求总和不变量。
- 备注：无

### Problem 17 · 算术与数感 / 比例

Cities A, B, C have populations 100, 120, 160. Commuting fractions are A->B=1/4, A->C=1/5, B->A=1/3, B->C=1/6, C->A=1/8, C->B=1/10; everyone else works where they live. How many people work in A? (A) 55 (B) 60 (C) 85 (D) 115 (E) 160

- 答案：D
- 标签：比例;流量;应用题
- 核心思路：分别计算来自三座城市而在 A 工作的人数并相加。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；图中箭头数据由 AoPS Wiki 同年题页转写

### Problem 18 · 几何与测量 / 圆

A radius-1 circle has all four corner regions between it and an inscribed square shaded. A radius-R circle has one quarter of the corresponding region shaded. The shaded areas are equal. What is R? (A) sqrt(2) (B) 2 (C) 2sqrt(2) (D) 4 (E) 4sqrt(2)

- 答案：B
- 标签：相似;面积缩放
- 核心思路：对应区域面积按半径平方缩放；四分之一面积相等确定缩放倍数。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 19 · 代数 / 方程

A 15-mile road has consecutive 5-mile speed limits 25, 40, and 20 mph from A to B. Cars start simultaneously at A and B and drive toward each other at the local limit. How far from A do they meet? (A) 7.75 (B) 8 (C) 8.25 (D) 8.5 (E) 8.75

- 答案：D
- 标签：分段速度;相遇问题
- 核心思路：按分段行驶时间确定相遇时所在路段，再建立同时到达方程。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页

### Problem 20 · 代数 / 数列

Sarika, Dev, and Rajiv repeatedly take turns eating half of the cheese that remains, starting with Sarika. About what fraction of the original cheese does Sarika eat in total? (A) 4/7 (B) 3/5 (C) 2/3 (D) 3/4 (E) 7/8

- 答案：A
- 标签：等比数列;无限和
- 核心思路：Sarika 吃到的份额构成首项 1/2、公比 1/8 的等比级数。
- 备注：无

### Problem 21 · 组合数学 / 构造

Grades 1 through 7 are assigned once each to pods A-G. Connected pods must differ by at least 2. Edges are AB, AC, AG, AF, BC, BF, CD, CE, CF, DE, EF, and FG. What is the sum of grades at C, E, and F? (A) 12 (B) 13 (C) 14 (D) 15 (E) 16

- 答案：A
- 标签：图标号;约束满足
- 核心思路：从度数最高的节点和相邻差值限制入手构造唯一可行标号。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未嵌入题图；连边由 AoPS Wiki 图形转写

### Problem 22 · 数论 / 因数与倍数

There are 35 coat hooks. Coats are equally spaced with the same positive number of empty hooks before, after, and between coats. How many different positive numbers of coats are possible? (A) 2 (B) 4 (C) 5 (D) 7 (E) 9

- 答案：D
- 标签：整除;等间隔
- 核心思路：若有 c 件外套、每段 e 个空钩，则 35=c+(c+1)e，转化为因数分解。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 的示意图为占位文本；题面和选项经 AoPS Wiki 核验

### Problem 23 · 数论 / 质数

How many four-digit numbers end in 99, are one less than a perfect square, and are the product of exactly two primes? (A) 0 (B) 1 (C) 2 (D) 3 (E) 4

- 答案：B
- 标签：平方数;半素数;数字条件
- 核心思路：由末两位 99 推出相邻平方的末两位，再检查候选数的质因数分解。
- 备注：无

### Problem 24 · 几何与测量 / 四边形

In trapezoid ABCD, base angles B and C are 60 degrees, legs AB and DC are equal, all side lengths are positive integers, and the perimeter is 30. How many non-congruent trapezoids satisfy the conditions? (A) 0 (B) 1 (C) 2 (D) 3 (E) 4

- 答案：E
- 标签：等腰梯形;整数边;计数
- 核心思路：把较长底边写成较短底边加两条腿的水平投影，再枚举整数周长解。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 未收录本题；题面和选项由 AoPS Wiki 同年题页补全

### Problem 25 · 组合数学 / 计数

In a 5-by-5 diamond grid, paths go from bottom to top using northeast or northwest steps. For every possible path, take the area between the path and the right boundary. What is the sum of all these areas? (A) 2520 (B) 3150 (C) 3840 (D) 4730 (E) 5050

- 答案：B
- 标签：格路径;对称;面积总和
- 核心思路：利用左右反射把每条路径与镜像配对，使每对面积和固定。
- 备注：题面包含图形；图形细节已对照原题 PDF 与 AoPS 题页；源 PDF 末页未呈现 A-E 选项；题面、图形与选项按 AoPS Wiki 同年题页核验
