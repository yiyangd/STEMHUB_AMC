# 2024 AMC 12 分类题集

> 每道题只归入一个一级分类和一个二级分类。答案字段在源 PDF 中未提供，因此本文件不编造答案。

## 统计概览

- 总题量：50
- A 卷：25 题
- B 卷：25 题

| 一级分类 | 题量 |
| --- | ---: |
| 代数 | 19 |
| 几何 | 12 |
| 数论 | 9 |
| 组合数学 | 3 |
| 概率与统计 | 7 |

## 1. 代数

### 1.1 三角恒等式

- **2024 AMC 12A Problem 8**
  - 考点：先处理对数定义域，再把方程化为 sin(3theta) cos(2theta) = 1。
  - 标签：对数;三角函数;定义域;方程
  - 题面：How many angles theta with 0 <= theta <= 2pi satisfy log(sin(3theta)) + log(cos(2theta)) = 0?
- **2024 AMC 12A Problem 23**
  - 考点：利用互余角正切倒数关系和四倍角结构化简对称和。
  - 标签：三角函数;恒等式;特殊角
  - 题面：What is tan^2(pi/16)tan^2(3pi/16) + tan^2(pi/16)tan^2(5pi/16) + tan^2(3pi/16)tan^2(7pi/16) + tan^2(5pi/16)tan^2(7pi/16)?
- **2024 AMC 12B Problem 11**
  - 考点：利用 sin^2 theta 与 sin^2(90-theta) 的配对和为 1。
  - 标签：三角函数;配对;平均值
  - 题面：Let x_n = sin^2(n degrees). What is the mean of x_1, x_2, ..., x_90?

### 1.2 函数与图像

- **2024 AMC 12A Problem 13**
  - 考点：通过指数项配对找出竖直对称轴，再对点做水平反射。
  - 标签：指数函数;对称轴;点的反射
  - 题面：The graph of y = e^(x+1) + e^(-x) - 2 has an axis of symmetry. What is the reflection of the point (-1, 1/2) over this axis?
- **2024 AMC 12A Problem 25**
  - 考点：关于 y=x 对称等价于函数与其反函数图像一致，转化为参数条件并计数。
  - 标签：有理函数;反函数;对称;参数计数
  - 题面：For how many quadruples of integers (a,b,c,d), with |a|,|b|,|c|,|d| <= 5 and c,d not both 0, is the graph y = (ax+b)/(cx+d) symmetric about the line y=x?
- **2024 AMC 12B Problem 13**
  - 考点：把 h+k 写成关于 x,y 的二次式，通过配方求最小值。
  - 标签：配方;二次函数;最值
  - 题面：There are real numbers x,y,h,k satisfying x^2+y^2-6x-8y=h and x^2+y^2-10x+4y=k. What is the minimum possible value of h+k?

### 1.3 复数

- **2024 AMC 12B Problem 12**
  - 考点：用 z = 2(cos theta + i sin theta) 表示各点，并把面积写成 theta 的函数。
  - 标签：复数平面;面积;极坐标
  - 题面：Suppose z is a complex number with positive imaginary part, real part greater than 1, and |z|=2. Points 0,z,z^2,z^3 form a quadrilateral with area 15. What is the imaginary part of z?

### 1.4 多项式与根

- **2024 AMC 12A Problem 15**
  - 考点：把乘积看作在相关虚数点处的多项式值，或用对称多项式处理。
  - 标签：韦达定理;多项式;复数代入
  - 题面：The roots of x^3 + 2x^2 - x + 3 are p, q, and r. What is (p^2+4)(q^2+4)(r^2+4)?

### 1.5 数列与递推

- **2024 AMC 12A Problem 12**
  - 考点：利用 720^2 = ab，寻找大于 720 的最小整数 b 使 a 也为整数。
  - 标签：等比数列;整数;最小值
  - 题面：The first three terms of a geometric sequence are integers a, 720, and b, where a < 720 < b. What is the sum of the digits of the least possible value of b?
- **2024 AMC 12A Problem 21**
  - 考点：重写递推寻找显式表达式，再估计或精确求平方和的整数部分。
  - 标签：递推;望远镜;平方和
  - 题面：Suppose a1 = 2 and sequence a_n satisfies (a_n - 1)/(n - 1) = (a_{n-1}+1)/n for n >= 2. What is floor(sum_{n=1}^{100} a_n^2)?
- **2024 AMC 12B Problem 18**
  - 考点：利用斐波那契恒等式化简各项，寻找望远镜或规律。
  - 标签：斐波那契数列;恒等式;求和
  - 题面：The Fibonacci numbers are F1=1, F2=1, and Fn=F_{n-1}+F_{n-2}. What is F2/F1 + F4/F2 + F6/F3 + ... + F20/F10?

### 1.6 方程与不等式

- **2024 AMC 12A Problem 17**
  - 考点：利用三式结构消元，转向关于 ab,bc,ca 或 a,b,c 的整数约束。
  - 标签：整数方程组;对称结构;代换
  - 题面：Integers a, b, and c satisfy ab+c = 100, bc+a = 87, and ca+b = 60. What is ab+bc+ca?
- **2024 AMC 12B Problem 3**
  - 考点：把不等式化为 |x| <= 7pi/2，再用 pi 的范围确定整数个数。
  - 标签：绝对值不等式;整数解;估计
  - 题面：For how many integer values of x is |2x| <= 7pi?
- **2024 AMC 12B Problem 8**
  - 考点：换底后把表达式化成 log_6 x 的形式求解。
  - 标签：对数;换底;方程
  - 题面：What value of x satisfies (log_2 x * log_3 x)/(log_2 x + log_3 x) = 2?

### 1.7 线性模型

- **2024 AMC 12A Problem 2**
  - 考点：由两组条件建立线性关系，再求目标线性组合。
  - 标签：线性方程组;建模;比例
  - 题面：A hiking-time model has the form T = aL + bG. It gives 69 minutes for trails (L,G) = (1.5,800) and (1.2,1100). How many minutes does it estimate for (4.2,4000)?
- **2024 AMC 12A Problem 14**
  - 考点：行列均为等差数列意味着数组可写成双线性形式，代入已知位置求目标。
  - 标签：等差数列;二维线性;表格
  - 备注：题面包含 5x5 表格，HTML 中以文字说明保留。
  - 题面：Rows and columns of a 5 by 5 integer array are arithmetic progressions. Given entries (5,5)=0, (2,4)=48, (4,3)=16, and (3,1)=12, what is in position (1,2)?

### 1.8 运算与化简

- **2024 AMC 12A Problem 1**
  - 考点：利用乘法分配律和配对化简，避免直接大数计算。
  - 标签：整数运算;因式分解;算术
  - 题面：What is the value of 9901 * 101 - 99 * 10101?
- **2024 AMC 12B Problem 1**
  - 考点：总人数等于左侧位置加右侧位置再减去重复计算的本人。
  - 标签：位置计数;线性关系
  - 题面：In a long line of people, the 1013th person from the left is also the 1010th person from the right. How many people are in the line?
- **2024 AMC 12B Problem 2**
  - 考点：提取 7! 或 6! 作为公因子后快速计算。
  - 标签：阶乘;因式分解;算术
  - 题面：What is 10! - 7! * 6!?

## 2. 几何

### 2.1 三角形

- **2024 AMC 12A Problem 10**
  - 考点：比较两组勾股三角形的正切值，并用倍角关系表达角度。
  - 标签：直角三角形;三角函数;倍角
  - 题面：Let alpha be the smallest angle in a 3-4-5 right triangle and beta the smallest angle in a 7-24-25 right triangle. In terms of alpha, what is beta?
- **2024 AMC 12B Problem 20**
  - 考点：用中线长度与第三边关系确定 x 的范围，并求面积最大时的构型。
  - 标签：中线;面积;最值;三角形不等式
  - 题面：Suppose A,B,C are points with AB=40 and AC=42. Let x be the length from A to the midpoint of BC, and f(x) be the area of triangle ABC. The domain is (p,q), and maximum r occurs at x=s. What is p+q+r+s?
- **2024 AMC 12B Problem 22**
  - 考点：由 B=2A 和正弦定理推出边长关系，再搜索最小整数周长。
  - 标签：倍角;整数边;正弦定理
  - 题面：Let triangle ABC have integer side lengths and angle B = 2 angle A. What is the least possible perimeter?
- **2024 AMC 12B Problem 24**
  - 考点：用面积与高、内切圆半径的关系把高度条件转化为可枚举的边长/半周长条件。
  - 标签：三角形;高;内切圆;整数枚举
  - 备注：主要解法是三角形几何关系，带有有限枚举。
  - 题面：How many ordered triples (a,b,c) of positive integers with a<=b<=c<=9 can be altitudes of a nondegenerate triangle with integer inradius?

### 2.2 几何变换

- **2024 AMC 12A Problem 18**
  - 考点：由矩形长宽比确定对角线角度，追踪每次旋转的角度周期。
  - 标签：旋转;矩形;角度;周期
  - 备注：题面包含卡片叠放图。
  - 题面：Identical rectangular cards with sides 1 and 2+sqrt(3) are placed successively so that diagonals line up after clockwise rotations. How many cards are needed until a vertex of a new card lands on vertex B?
- **2024 AMC 12B Problem 19**
  - 考点：把旋转后的重叠/外接六边形面积表示为 theta 的函数。
  - 标签：旋转;正三角形;面积;三角函数
  - 备注：题面包含两个正三角形旋转形成的六边形图。
  - 题面：Equilateral triangle ABC with side length 14 is rotated about its center by angle theta, 0<theta<60 degrees, to form triangle DEF. Area of hexagon ADBECF is 91sqrt(3). What is tan theta?

### 2.3 向量几何

- **2024 AMC 12A Problem 7**
  - 考点：等分点的向量和等于点数乘以平均位置，再转化为从 B 到中点的向量。
  - 标签：向量和;中点;等分点;直角三角形
  - 题面：In right isosceles triangle ABC with angle ABC = 90 degrees and BA = BC = sqrt(2), points P1 through P2024 divide hypotenuse AC into equal parts. What is the length of vector sum BP1 + BP2 + ... + BP2024?

### 2.4 圆与四边形

- **2024 AMC 12A Problem 19**
  - 考点：先在三角形 CDA 中求对角线，再利用同弧或圆内接关系处理另一条对角线。
  - 标签：圆内接四边形;余弦定理;对角线
  - 题面：Cyclic quadrilateral ABCD has BC = CD = 3 and DA = 5 with angle CDA = 120 degrees. What is the length of the shorter diagonal?

### 2.5 坐标几何

- **2024 AMC 12B Problem 15**
  - 考点：把坐标写成简单形式，用行列式或鞋带公式求面积。
  - 标签：坐标面积;对数;行列式
  - 题面：A triangle has vertices A(log_2 1, log_2 2), B(log_2 3, log_2 4), and C(log_2 7, log_2 8). What is its area?

### 2.6 空间几何

- **2024 AMC 12A Problem 24**
  - 考点：枚举最小的整数不等边三角形面，并用海伦公式比较总表面积。
  - 标签：四面体;海伦公式;整数边
  - 题面：A disphenoid is a tetrahedron whose triangular faces are congruent. What is the least total surface area of a disphenoid whose faces are scalene triangles with integer side lengths?
- **2024 AMC 12B Problem 23**
  - 考点：把底面中心到顶点距离与侧棱向量垂直条件结合，解出高度平方。
  - 标签：正八边形;棱锥;空间垂直;高度
  - 题面：A right pyramid has regular octagon ABCDEFGH with side length 1 as its base and apex V. Segments AV and DV are perpendicular. What is the square of the height?

### 2.7 面积与相似

- **2024 AMC 12B Problem 7**
  - 考点：用坐标表示 M 和 A，结合直角条件与面积相等求目标面积。
  - 标签：矩形;面积;直角;坐标设元
  - 备注：题面包含矩形示意图。
  - 题面：In rectangle WXYZ with WX = 4 and WZ = 8, point M lies on XY, point A lies on YZ, angle WMA is right, and areas of triangles WXM and WAZ are equal. What is area of triangle WMA?

## 3. 数论

### 3.1 勾股数组

- **2024 AMC 12B Problem 21**
  - 考点：用小角的正切值和角和公式确定第三个勾股三角形。
  - 标签：勾股数组;三角函数;角和
  - 题面：The smallest angles of three different primitive Pythagorean right triangles sum to 90 degrees. Two are 3-4-5 and 5-12-13. What is the perimeter of the third triangle?

### 3.2 平方数

- **2024 AMC 12A Problem 9**
  - 考点：两平方数相差 2560，利用平方差分解并选择使 M 最大的因子对。
  - 标签：平方差;最大整数;个位数
  - 题面：Let M be the greatest integer such that both M + 1213 and M + 3773 are perfect squares. What is the units digit of M?

### 3.3 整数构造

- **2024 AMC 12A Problem 3**
  - 考点：每个两位数最大为 99，用上界估计并检查可达性。
  - 标签：两位数;最值;整数拆分
  - 题面：The number 2024 is written as the sum of not necessarily distinct two-digit numbers. What is the least number of two-digit numbers needed?
- **2024 AMC 12A Problem 6**
  - 考点：枚举因子组合并考虑负因子的配对，使总和为正且尽量小。
  - 标签：整数因子;最值;符号
  - 题面：The product of three integers is 60. What is the least possible positive sum of the three integers?
- **2024 AMC 12B Problem 5**
  - 考点：原和为 2500，每改一个符号减少两倍该项，优先选择最大奇数。
  - 标签：奇数和;贪心;最值
  - 题面：In 1 + 3 + 5 + ... + 97 + 99, Melanie changes some plus signs to minus signs. The new expression is negative. What is the least number of plus signs changed?

### 3.4 整除与同余

- **2024 AMC 12B Problem 14**
  - 考点：按整数是否被 5 整除分类，再分析模 125 的 100 次幂剩余。
  - 标签：模运算;幂剩余;125
  - 题面：How many different remainders can result when the 100th power of an integer is divided by 125?

### 3.5 质因数分解

- **2024 AMC 12A Problem 4**
  - 考点：分解 2024 并找出 n! 中首次包含所有所需质因数的位置。
  - 标签：阶乘;质因数;整除
  - 题面：What is the least value of n such that n! is a multiple of 2024?

### 3.6 进制

- **2024 AMC 12A Problem 11**
  - 考点：把 2024_b 转成关于 b 的多项式，再在模 16 下计数。
  - 标签：进制表示;同余;计数
  - 题面：There are exactly K positive integers b with 5 <= b <= 2024 such that the base-b integer 2024_b is divisible by 16. What is the sum of the digits of K?
- **2024 AMC 12B Problem 6**
  - 考点：用 base-5 位数公式 floor(log_5 N)+1，并用换底公式估计。
  - 标签：进制位数;对数;数量级
  - 题面：The national debt is on track to reach 5*10^13 dollars by 2033. How many digits does this number have in base 5? Use log_10 5 approximately 0.7.

## 4. 组合数学

### 4.1 周期与递推计数

- **2024 AMC 12B Problem 4**
  - 考点：定位 2024 落在哪个连续分组，再按分组编号模 5 判断箱子。
  - 标签：周期;三角数;分组
  - 题面：Balls numbered 1,2,3,... are deposited in five bins A-E in blocks of size 1,2,3,4,... cycling through the bins. In which bin is ball 2024 deposited?

### 4.2 图形计数

- **2024 AMC 12A Problem 22**
  - 考点：按列或状态转移计数满足每个标号格边数限制的简单闭合回路。
  - 标签：网格路径;闭合回路;状态计数
  - 备注：题面包含 8x3 网格图。
  - 题面：On an 8 by 3 dotted grid of 1-inch squares, toothpicks are placed along grid edges to create a closed non-self-intersecting loop. Each middle-row cell is labeled 1, meaning exactly one side is covered; other cells are unrestricted. How many loops are possible?

### 4.3 排列组合

- **2024 AMC 12B Problem 16**
  - 考点：写出分组和职务安排公式，再求其中因子 3 的指数。
  - 标签：分组;职务安排;质因数指数
  - 题面：A group of 16 people is partitioned into 4 indistinguishable 4-person committees. Each committee has one chairperson and one secretary. The number of assignments is 3^r M with M not divisible by 3. What is r?

## 5. 概率与统计

### 5.1 代数概率

- **2024 AMC 12B Problem 17**
  - 考点：枚举乘积为 -6 的三 distinct 整数根，并映射到系数 (a,b) 后计数。
  - 标签：多项式根;整数根;概率计数
  - 题面：Integers a and b are randomly chosen without replacement from integers with absolute value at most 10. What is the probability that x^3 + ax^2 + bx + 6 has 3 distinct integer roots?

### 5.2 几何概率

- **2024 AMC 12A Problem 20**
  - 考点：把两个位置参数化为独立变量，面积条件转化为乘积不等式。
  - 标签：几何概率;面积比例;单位正方形
  - 题面：Points P and Q are chosen uniformly and independently on sides AB and AC of equilateral triangle ABC. Which interval contains the probability that area(APQ) is less than half area(ABC)?
- **2024 AMC 12B Problem 9**
  - 考点：识别目标为圆环区域，并与菱形靶盘比较面积。
  - 标签：几何概率;面积;圆环;菱形
  - 题面：A dartboard is |x|+|y| <= 8. Target T satisfies (x^2+y^2-25)^2 <= 49. A dart is thrown uniformly in the dartboard. The probability is m*pi/n. What is m+n?

### 5.3 平均数与数据集

- **2024 AMC 12A Problem 5**
  - 考点：用删除前后的总和建立关于 6 的个数的方程。
  - 标签：平均数;总和;数据删除
  - 题面：A data set containing 20 numbers, some of which are 6, has mean 45. When all the 6s are removed, the data set has mean 66. How many 6s were in the original data set?
- **2024 AMC 12B Problem 10**
  - 考点：由极差限制端点，再枚举中位数和总和的整数条件。
  - 标签：平均数;中位数;极差;有序三元组
  - 题面：A list of 9 real numbers consists of 1, 2.2, 3.2, 5.2, 6.2, 7, and x,y,z with x <= y <= z. The range is 7, and the mean and median are both positive integers. How many ordered triples are possible?

### 5.4 独立性

- **2024 AMC 12B Problem 25**
  - 考点：把结果看作 2x2 列联表，独立性等价于行列乘积条件，再计数所有配置。
  - 标签：独立事件;随机配置;计数;二元表
  - 题面：Pablo decorates each of 6 identical white balls with striped/dotted pattern and red/blue color, using fair coins for the 12 decisions. A ball is selected randomly. What is the numerator m of the probability that the events selected ball is red and selected ball is striped are independent?

### 5.5 组合概率

- **2024 AMC 12A Problem 16**
  - 考点：分别计数满足颜色集中条件的分配数和总分配数。
  - 标签：分配;超几何;条件计数
  - 题面：A set of 12 tokens - 3 red, 2 white, 1 blue, and 6 black - is distributed randomly to 3 players, 4 tokens per player. Find m+n if the probability that one player gets all red tokens, another all white tokens, and the remaining player the blue token is m/n.
