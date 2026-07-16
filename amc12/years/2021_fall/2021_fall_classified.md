# 2021 Fall AMC 12 分类题集

> 自动批量整理草稿。每道题只归入一个一级分类和一个二级分类；answer 留空表示源 PDF 未提供答案表。

## 统计概览

- 总题量：50
- A 卷：25 题
- B 卷：25 题

| 一级分类 | 题量 |
| --- | ---: |
| 代数 | 17 |
| 几何 | 13 |
| 数论 | 11 |
| 组合数学 | 3 |
| 概率与统计 | 6 |

## 1. 代数

### 1.1 三角恒等式

- **2021 Fall AMC 12A Problem 19**
  - 考点：利用三角恒等式、周期或特殊角关系化简。
  - 标签：三角方程;周期;取整
  - 题面：Let $x$ be the least real number greater than $1$ such that $\sin(x) = \sin(x^2)$ , where the arguments are in degrees. What is $x$ rounded up to the closest integer? $\textbf{(A) } 10 \qquad \textbf{(B) } 13 \qquad \textbf{(C) } 14 \qquad \textbf{(D) } 19 \qquad \textbf{(E) } 20$
- **2021 Fall AMC 12B Problem 13**
  - 考点：利用三角恒等式、周期或特殊角关系化简。
  - 标签：正弦;周期;乘积
  - 题面：Let $c = \frac{2\pi}{11}.$ What is the value of \[\frac{\sin 3c \cdot \sin 6c \cdot \sin 9c \cdot \sin 12c \cdot \sin 15c}{\sin c \cdot \sin 2c \cdot \sin 3c \cdot \sin 4c \cdot \sin 5c}?\] $\textbf{(A)}\ {-}1 \qquad\textbf{(B)}\ {-}\frac{\sqrt{11}}{5} \qquad\textbf{(C)}\ \frac{\sqrt{11}}{5} \qquad\textbf{(D)}\ \frac{10}{11} \qquad\textbf{(E)}\ 1$

### 1.2 复数

- **2021 Fall AMC 12A Problem 15**
  - 考点：用复平面、共轭、模长或单位圆形式处理复数关系。
  - 标签：复数;共轭;坐标
  - 题面：Recall that the conjugate of the complex number $w = a + bi$ , where $a$ and $b$ are real numbers and $i = \sqrt{-1}$ , is the complex number $\overline{w} = a - bi$ . For any complex number $z$ , let $f(z) = 4i\hspace{1pt}\overline{z}$ . The polynomial \[P(z) = z^4 + 4z^3 + 3z^2 + 2z + 1\] has four complex roots: $z_1$ , $z_2$ , $z_3$ , and $z_4$ . Let \[Q(z) = z^4 + Az^3 + Bz^2 + Cz + D\] be the polynomial whose roots are $f(z_1)$ , $f(z_2)$ , $f(z_3)$ , and $f(z_4)$ , where the coefficients $A,$ $B,$ $C,$ and $D$ are complex numbers. What is $B + D?$ $(\textbf{A})\: {-}304\qquad(\textbf{B}) \: {-}208\qquad(\textbf{C}) \: 12i\qquad(\textbf{D}) \: 208\qquad(\textbf{E}) \: 304$
- **2021 Fall AMC 12B Problem 21**
  - 考点：用复平面、共轭、模长或单位圆形式处理复数关系。
  - 标签：复数;单位圆;三角函数
  - 题面：For real numbers $x$ , let \[P(x)=1+\cos(x)+i\sin(x)-\cos(2x)-i\sin(2x)+\cos(3x)+i\sin(3x)\] where $i = \sqrt{-1}$ . For how many values of $x$ with $0\leq x<2\pi$ does \[P(x)=0?\] $\textbf{(A)}\ 0 \qquad\textbf{(B)}\ 1 \qquad\textbf{(C)}\ 2 \qquad\textbf{(D)}\ 3 \qquad\textbf{(E)}\ 4$

### 1.3 多项式与根

- **2021 Fall AMC 12A Problem 12**
  - 考点：结合二项式展开、根的结构或多项式性质筛选可能性。
  - 标签：二项式展开;有理系数;指数
  - 题面：What is the number of terms with rational coefficients among the $1001$ terms in the expansion of $\left(x\sqrt[3]{2}+y\sqrt{3}\right)^{1000}?$ $\textbf{(A)}\ 0 \qquad\textbf{(B)}\ 166 \qquad\textbf{(C)}\ 167 \qquad\textbf{(D)}\ 500 \qquad\textbf{(E)}\ 501$
- **2021 Fall AMC 12A Problem 23**
  - 考点：结合二项式展开、根的结构或多项式性质筛选可能性。
  - 标签：复合多项式;实根;韦达定理
  - 题面：A quadratic polynomial with real coefficients and leading coefficient $1$ is called $\emph{disrespectful}$ if the equation $p(p(x))=0$ is satisfied by exactly three real numbers. Among all the disrespectful quadratic polynomials, there is a unique such polynomial $\tilde{p}(x)$ for which the sum of the roots is maximized. What is $\tilde{p}(1)$ ? $\textbf{(A) } \frac{5}{16} \qquad\textbf{(B) } \frac{1}{2} \qquad\textbf{(C) } \frac{5}{8} \qquad\textbf{(D) } 1 \qquad\textbf{(E) } \frac{9}{8}$
- **2021 Fall AMC 12B Problem 14**
  - 考点：结合二项式展开、根的结构或多项式性质筛选可能性。
  - 标签：多项式;复根;重根构造
  - 题面：Suppose that $P(z), Q(z)$ , and $R(z)$ are polynomials with real coefficients, having degrees $2$ , $3$ , and $6$ , respectively, and constant terms $1$ , $2$ , and $3$ , respectively. Let $N$ be the number of distinct complex numbers $z$ that satisfy the equation $P(z) \cdot Q(z)=R(z)$ . What is the minimum possible value of $N$ ? $\textbf{(A)}\: 0\qquad\textbf{(B)} \: 1\qquad\textbf{(C)} \: 2\qquad\textbf{(D)} \: 3\qquad\textbf{(E)} \: 5$

### 1.4 对数与指数

- **2021 Fall AMC 12A Problem 9**
  - 考点：使用指数规律、换底或对数恒等式化简。
  - 标签：对数;表面积;体积
  - 题面：A right rectangular prism whose surface area and volume are numerically equal has edge lengths $\log_{2}x, \log_{3}x,$ and $\log_{4}x.$ What is $x?$ $\textbf{(A)}\ 2\sqrt{6} \qquad\textbf{(B)}\ 6\sqrt{6} \qquad\textbf{(C)}\ 24 \qquad\textbf{(D)}\ 48 \qquad\textbf{(E)}\ 576$
- **2021 Fall AMC 12B Problem 4**
  - 考点：使用指数规律、换底或对数恒等式化简。
  - 标签：指数;幂;化简
  - 题面：Let $n=8^{2022}$ . Which of the following is equal to $\frac{n}{4}?$ $\textbf{(A)}\: 4^{1010}\qquad\textbf{(B)} \: 2^{2022}\qquad\textbf{(C)} \: 8^{2018}\qquad\textbf{(D)} \: 4^{3031}\qquad\textbf{(E)} \: 4^{3032}$

### 1.5 数列与递推

- **2021 Fall AMC 12B Problem 18**
  - 考点：从递推式中寻找不变量、显式规律或误差变化。
  - 标签：递推;极限;误差
  - 题面：Set $u_0 = \frac{1}{4}$ , and for $k \ge 0$ let $u_{k+1}$ be determined by the recurrence \[u_{k+1} = 2u_k - 2u_k^2.\] This sequence tends to a limit; call it $L$ . What is the least value of $k$ such that \[|u_k-L| \le \frac{1}{2^{1000}}?\] $\textbf{(A)}\: 10\qquad\textbf{(B)}\: 87\qquad\textbf{(C)}\: 123\qquad\textbf{(D)}\: 329\qquad\textbf{(E)}\: 401$

### 1.6 方程与不等式

- **2021 Fall AMC 12A Problem 17**
  - 考点：把题设转化为方程、不等式或判别式条件并求解。
  - 标签：二次方程;判别式;整数
  - 题面：For how many ordered pairs $(b,c)$ of positive integers does neither $x^2+bx+c=0$ nor $x^2+cx+b=0$ have two distinct real solutions? $\textbf{(A) } 4 \qquad \textbf{(B) } 6 \qquad \textbf{(C) } 8 \qquad \textbf{(D) } 12 \qquad \textbf{(E) } 16 \qquad$
- **2021 Fall AMC 12B Problem 7**
  - 考点：把题设转化为方程、不等式或判别式条件并求解。
  - 标签：恒等式;代入;整数
  - 题面：Which of the following conditions is sufficient to guarantee that integers $x$ , $y$ , and $z$ satisfy the equation \[x(x-y)+y(y-z)+z(z-x) = 1?\] $\textbf{(A)} \: x>y$ and $y=z$ $\textbf{(B)} \: x=y-1$ and $y=z-1$ $\textbf{(C)} \: x=z+1$ and $y=x+1$ $\textbf{(D)} \: x=z$ and $y-1=x$ $\textbf{(E)} \: x+y+z=1$

### 1.7 线性模型

- **2021 Fall AMC 12A Problem 3**
  - 考点：把速度、时间、数量或差值关系转化为线性等式。
  - 标签：速度;时间;线性模型
  - 题面：Mr. Lopez has a choice of two routes to get to work. Route A is $6$ miles long, and his average speed along this route is $30$ miles per hour. Route B is $5$ miles long, and his average speed along this route is $40$ miles per hour, except for a $\frac{1}{2}$ -mile stretch in a school zone where his average speed is $20$ miles per hour. By how many minutes is Route B quicker than Route A? $\textbf{(A)}\ 2 \frac{3}{4} \qquad\textbf{(B)}\ 3 \frac{3}{4} \qquad\textbf{(C)}\ 4 \frac{1}{2} \qquad\textbf{(D)}\ 5 \frac{1}{2} \qquad\textbf{(E)}\ 6 \frac{3}{4}$
- **2021 Fall AMC 12B Problem 3**
  - 考点：把速度、时间、数量或差值关系转化为线性等式。
  - 标签：温度;差值;线性模型
  - 题面：At noon on a certain day, Minneapolis is $N$ degrees warmer than St. Louis. At $4{:}00$ the temperature in Minneapolis has fallen by $5$ degrees while the temperature in St. Louis has risen by $3$ degrees, at which time the temperatures in the two cities differ by $2$ degrees. What is the product of all possible values of $N?$ $\textbf{(A)}\: 10\qquad\textbf{(B)} \: 30\qquad\textbf{(C)} \: 60\qquad\textbf{(D)} \: 100\qquad\textbf{(E)} \: 120$

### 1.8 运算与化简

- **2021 Fall AMC 12A Problem 1**
  - 考点：通过代数化简、配对或基本运算降低计算量。
  - 标签：代数;平方;化简
  - 题面：What is the value of $\frac{(2112-2021)^2}{169}$ ? $\textbf{(A) } 7 \qquad\textbf{(B) } 21 \qquad\textbf{(C) } 49 \qquad\textbf{(D) } 64 \qquad\textbf{(E) } 91$
- **2021 Fall AMC 12A Problem 2**
  - 考点：通过代数化简、配对或基本运算降低计算量。
  - 标签：矩形;面积;代数
  - 题面：Menkara has a $4 \times 6$ index card. If she shortens the length of one side of this card by $1$ inch, the card would have area $18$ square inches. What would the area of the card be in square inches if instead she shortens the length of the other side by $1$ inch? $\textbf{(A) }16\qquad\textbf{(B) }17\qquad\textbf{(C) }18\qquad\textbf{(D) }19\qquad\textbf{(E) }20$
- **2021 Fall AMC 12B Problem 1**
  - 考点：通过代数化简、配对或基本运算降低计算量。
  - 标签：数位;求和;化简
  - 题面：What is the value of $1234+2341+3412+4123?$ $\textbf{(A)}\: 10{,}000\qquad\textbf{(B)} \: 10{,}010\qquad\textbf{(C)} \: 10{,}110\qquad\textbf{(D)} \: 11{,}000\qquad\textbf{(E)} \: 11{,}110$

## 2. 几何

### 2.1 三角形

- **2021 Fall AMC 12A Problem 6**
  - 考点：运用三角形边角关系、三角函数或面积公式。
  - 标签：角度;平行线;三角形
  - 备注：题面包含图形
  - 题面：As shown in the figure below, point $E$ lies on the opposite half-plane determined by line $CD$ from point $A$ so that $\angle CDE = 110^\circ$ . Point $F$ lies on $\overline{AD}$ so that $DE=DF$ , and $ABCD$ is a square. What is the degree measure of $\angle AFE$ ? [Diagram] $\textbf{(A) }160\qquad\textbf{(B) }164\qquad\textbf{(C) }166\qquad\textbf{(D) }170\qquad\textbf{(E) }174$
- **2021 Fall AMC 12A Problem 24**
  - 考点：运用三角形边角关系、三角函数或面积公式。
  - 标签：四边形;等差数列;余弦定理
  - 题面：Convex quadrilateral $ABCD$ has $AB = 18, \angle{A} = 60^\circ,$ and $\overline{AB} \parallel \overline{CD}.$ In some order, the lengths of the four sides form an arithmetic progression, and side $\overline{AB}$ is a side of maximum length. The length of another side is $a.$ What is the sum of all possible values of $a$ ? $\textbf{(A) } 24 \qquad \textbf{(B) } 42 \qquad \textbf{(C) } 60 \qquad \textbf{(D) } 66 \qquad \textbf{(E) } 84$
- **2021 Fall AMC 12B Problem 8**
  - 考点：运用三角形边角关系、三角函数或面积公式。
  - 标签：等腰三角形;面积;三角函数
  - 题面：The product of the lengths of the two congruent sides of an obtuse isosceles triangle is equal to the product of the base and twice the triangle's height to the base. What is the measure, in degrees, of the vertex angle of this triangle? $\textbf{(A)} \: 105 \qquad\textbf{(B)} \: 120 \qquad\textbf{(C)} \: 135 \qquad\textbf{(D)} \: 150 \qquad\textbf{(E)} \: 165$

### 2.2 几何变换

- **2021 Fall AMC 12B Problem 15**
  - 考点：用旋转、反射或对称关系简化面积和长度。
  - 标签：旋转;正方形;面积
  - 备注：题面包含图形
  - 题面：Three identical square sheets of paper each with side length $6$ are stacked on top of each other. The middle sheet is rotated clockwise $30^\circ$ about its center and the top sheet is rotated clockwise $60^\circ$ about its center, resulting in the $24$ -sided polygon shown in the figure below. The area of this polygon can be expressed in the form $a-b\sqrt{c}$ , where $a$ , $b$ , and $c$ are positive integers, and $c$ is not divisible by the square of any prime. What is $a+b+c$ ? [Diagram] $(\textbf{A})\: 75\qquad(\textbf{B}) \: 93\qquad(\textbf{C}) \: 96\qquad(\textbf{D}) \: 129\qquad(\textbf{E}) \: 147$

### 2.3 圆与曲线

- **2021 Fall AMC 12A Problem 11**
  - 考点：利用圆、弦、切线、圆周角或曲线方程求关键量。
  - 标签：圆;弦;勾股定理
  - 题面：Consider two concentric circles of radius $17$ and $19.$ The larger circle has a chord, half of which lies inside the smaller circle. What is the length of the chord in the larger circle? $\textbf{(A)}\ 12\sqrt{2} \qquad\textbf{(B)}\ 10\sqrt{3} \qquad\textbf{(C)}\ \sqrt{17 \cdot 19} \qquad\textbf{(D)}\ 18 \qquad\textbf{(E)}\ 8\sqrt{6}$
- **2021 Fall AMC 12B Problem 9**
  - 考点：利用圆、弦、切线、圆周角或曲线方程求关键量。
  - 标签：等边三角形;内心;外接圆
  - 题面：Triangle $ABC$ is equilateral with side length $6$ . Suppose that $O$ is the center of the inscribed circle of this triangle. What is the area of the circle passing through $A$ , $O$ , and $C$ ? $\textbf{(A)} \: 9\pi \qquad\textbf{(B)} \: 12\pi \qquad\textbf{(C)} \: 18\pi \qquad\textbf{(D)} \: 24\pi \qquad\textbf{(E)} \: 27\pi$
- **2021 Fall AMC 12B Problem 22**
  - 考点：利用圆、弦、切线、圆周角或曲线方程求关键量。
  - 标签：直角三角形;相切圆;相似
  - 题面：Right triangle $ABC$ has side lengths $BC=6$ , $AC=8$ , and $AB=10$ . A circle centered at $O$ is tangent to line $BC$ at $B$ and passes through $A$ . A circle centered at $P$ is tangent to line $AC$ at $A$ and passes through $B$ . What is $OP$ ? $\textbf{(A)}\ \frac{23}{8} \qquad\textbf{(B)}\ \frac{29}{10} \qquad\textbf{(C)}\ \frac{35}{12} \qquad\textbf{(D)}\ \frac{73}{25} \qquad\textbf{(E)}\ 3$
- **2021 Fall AMC 12B Problem 24**
  - 考点：利用圆、弦、切线、圆周角或曲线方程求关键量。
  - 标签：角平分线;圆;相似三角形
  - 题面：Triangle $ABC$ has side lengths $AB = 11, BC=24$ , and $CA = 20$ . The bisector of $\angle{BAC}$ intersects $\overline{BC}$ in point $D$ , and intersects the circumcircle of $\triangle{ABC}$ in point $E \ne A$ . The circumcircle of $\triangle{BED}$ intersects the line $AB$ in points $B$ and $F \ne B$ . What is $CF$ ? $\textbf{(A) } 28 \qquad \textbf{(B) } 20\sqrt{2} \qquad \textbf{(C) } 30 \qquad \textbf{(D) } 32 \qquad \textbf{(E) } 20\sqrt{3}$

### 2.4 坐标几何

- **2021 Fall AMC 12A Problem 13**
  - 考点：建立坐标或利用斜率、距离与单位圆关系求解。
  - 标签：角平分线;斜率;坐标
  - 题面：The angle bisector of the acute angle formed at the origin by the graphs of the lines $y = x$ and $y=3x$ has equation $y=kx.$ What is $k?$ $\textbf{(A)} \ \frac{1+\sqrt{5}}{2} \qquad \textbf{(B)} \ \frac{1+\sqrt{7}}{2} \qquad \textbf{(C)} \ \frac{2+\sqrt{3}}{2} \qquad \textbf{(D)} \ 2\qquad \textbf{(E)} \ \frac{2+\sqrt{5}}{2}$
- **2021 Fall AMC 12B Problem 10**
  - 考点：建立坐标或利用斜率、距离与单位圆关系求解。
  - 标签：单位圆;等腰三角形;坐标
  - 题面：What is the sum of all possible values of $t$ between $0$ and $360$ such that the triangle in the coordinate plane whose vertices are \[(\cos 40^\circ,\sin 40^\circ), (\cos 60^\circ,\sin 60^\circ), \text{ and } (\cos t^\circ,\sin t^\circ)\] is isosceles? $\textbf{(A)} \: 100 \qquad\textbf{(B)} \: 150 \qquad\textbf{(C)} \: 330 \qquad\textbf{(D)} \: 360 \qquad\textbf{(E)} \: 380$

### 2.5 面积与相似

- **2021 Fall AMC 12A Problem 14**
  - 考点：抓住面积分割、相似关系或比例约束建立方程。
  - 标签：六边形;面积;周长
  - 备注：题面包含图形
  - 题面：In the figure, equilateral hexagon $ABCDEF$ has three nonadjacent acute interior angles that each measure $30^\circ$ . The enclosed area of the hexagon is $6\sqrt{3}$ . What is the perimeter of the hexagon? [Diagram] $\textbf{(A)} \: 4 \qquad \textbf{(B)} \: 4\sqrt3 \qquad \textbf{(C)} \: 12 \qquad \textbf{(D)} \: 18 \qquad \textbf{(E)} \: 12\sqrt3$
- **2021 Fall AMC 12A Problem 21**
  - 考点：抓住面积分割、相似关系或比例约束建立方程。
  - 标签：梯形;对角线;面积
  - 备注：题面包含图形
  - 题面：Let $ABCD$ be an isosceles trapezoid with $\overline{BC} \parallel \overline{AD}$ and $AB=CD$ . Points $X$ and $Y$ lie on diagonal $\overline{AC}$ with $X$ between $A$ and $Y$ , as shown in the figure. Suppose $\angle AXD = \angle BYC = 90^\circ$ , $AX = 3$ , $XY = 1$ , and $YC = 2$ . What is the area of $ABCD$ ? [Diagram] $\textbf{(A)}\: 15\qquad\textbf{(B)} \: 5\sqrt{11}\qquad\textbf{(C)} \: 3\sqrt{35}\qquad\textbf{(D)} \: 18\qquad\textbf{(E)} \: 7\sqrt{7}$
- **2021 Fall AMC 12B Problem 2**
  - 考点：抓住面积分割、相似关系或比例约束建立方程。
  - 标签：面积;分割;坐标网格
  - 备注：题面包含图形
  - 题面：What is the area of the shaded figure shown below? [Diagram] $\textbf{(A)}\: 4\qquad\textbf{(B)} \: 6\qquad\textbf{(C)} \: 8\qquad\textbf{(D)} \: 10\qquad\textbf{(E)} \: 12$

## 3. 数论

### 3.1 整数构造

- **2021 Fall AMC 12B Problem 5**
  - 考点：利用整数范围、构造和极值条件筛选可能值。
  - 标签：分数;整数;构造
  - 题面：Call a fraction $\frac{a}{b}$ , not necessarily in the simplest form, special if $a$ and $b$ are positive integers whose sum is $15$ . How many distinct integers can be written as the sum of two, not necessarily different, special fractions? $\textbf{(A)}\ 9 \qquad\textbf{(B)}\ 10 \qquad\textbf{(C)}\ 11 \qquad\textbf{(D)}\ 12 \qquad\textbf{(E)}\ 13$

### 3.2 整除与同余

- **2021 Fall AMC 12A Problem 25**
  - 考点：把条件转化为同余、余数或整除分类讨论。
  - 标签：同余;多项式;计数
  - 题面：Let $m\ge 5$ be an odd integer, and let $D(m)$ denote the number of quadruples $(a_1, a_2, a_3, a_4)$ of distinct integers with $1\le a_i \le m$ for all $i$ such that $m$ divides $a_1+a_2+a_3+a_4$ . There is a polynomial \[q(x) = c_3x^3+c_2x^2+c_1x+c_0\] such that $D(m) = q(m)$ for all odd integers $m\ge 5$ . What is $c_1?$ $\textbf{(A)}\ {-}6\qquad\textbf{(B)}\ {-}1\qquad\textbf{(C)}\ 4\qquad\textbf{(D)}\ 6\qquad\textbf{(E)}\ 11$
- **2021 Fall AMC 12B Problem 25**
  - 考点：把条件转化为同余、余数或整除分类讨论。
  - 标签：余数和;整除;分类计数
  - 题面：For $n$ a positive integer, let $R(n)$ be the sum of the remainders when $n$ is divided by $2$ , $3$ , $4$ , $5$ , $6$ , $7$ , $8$ , $9$ , and $10$ . For example, $R(15) = 1+0+3+0+3+1+7+6+5=26$ . How many two-digit positive integers $n$ satisfy $R(n) = R(n+1)\,?$ $\textbf{(A) }0\qquad\textbf{(B) }1\qquad\textbf{(C) }2\qquad\textbf{(D) }3\qquad\textbf{(E) }4$

### 3.3 质因数与整除

- **2021 Fall AMC 12A Problem 5**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：最小公倍数;步长;整数
  - 题面：Elmer the emu takes $44$ equal strides to walk between consecutive telephone poles on a rural road. Oscar the ostrich can cover the same distance in $12$ equal leaps. The telephone poles are evenly spaced, and the $41$ st pole along this road is exactly one mile ( $5280$ feet) from the first pole. How much longer, in feet, is Oscar's leap than Elmer's stride? $\textbf{(A) }6\qquad\textbf{(B) }8\qquad\textbf{(C) }10\qquad\textbf{(D) }11\qquad\textbf{(E) }15$
- **2021 Fall AMC 12A Problem 8**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：最小公倍数;质因数;整除
  - 题面：Let $M$ be the least common multiple of all the integers $10$ through $30,$ inclusive. Let $N$ be the least common multiple of $M,32,33,34,35,36,37,38,39,$ and $40.$ What is the value of $\frac{N}{M}?$ $\textbf{(A)}\ 1 \qquad\textbf{(B)}\ 2 \qquad\textbf{(C)}\ 37 \qquad\textbf{(D)}\ 74 \qquad\textbf{(E)}\ 2886$
- **2021 Fall AMC 12A Problem 20**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：约数函数;迭代;质因数
  - 题面：For each positive integer $n$ , let $f_1(n)$ be twice the number of positive integer divisors of $n$ , and for $j \ge 2$ , let $f_j(n) = f_1(f_{j-1}(n))$ . For how many values of $n \le 50$ is $f_{50}(n) = 12?$ $\textbf{(A) }7\qquad\textbf{(B) }8\qquad\textbf{(C) }9\qquad\textbf{(D) }10\qquad\textbf{(E) }11$
- **2021 Fall AMC 12B Problem 6**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：质因数分解;数字和;整除
  - 题面：The greatest prime number that is a divisor of $16{,}384$ is $2$ because $16{,}384 = 2^{14}$ . What is the sum of the digits of the greatest prime number that is a divisor of $16{,}383$ ? $\textbf{(A)} \: 3\qquad\textbf{(B)} \: 7\qquad\textbf{(C)} \: 10\qquad\textbf{(D)} \: 16\qquad\textbf{(E)} \: 22$
- **2021 Fall AMC 12B Problem 12**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：约数和;质因数分解;函数
  - 题面：For $n$ a positive integer, let $f(n)$ be the quotient obtained when the sum of all positive divisors of $n$ is divided by $n.$ For example, \[f(14)=(1+2+7+14)\div 14=\frac{12}{7}\] What is $f(768)-f(384)?$ $\textbf{(A)}\ \frac{1}{768} \qquad\textbf{(B)}\ \frac{1}{192} \qquad\textbf{(C)}\ 1 \qquad\textbf{(D)}\ \frac{4}{3} \qquad\textbf{(E)}\ \frac{8}{3}$
- **2021 Fall AMC 12B Problem 16**
  - 考点：分解质因数并检查整除、最大公因数或最小公倍数条件。
  - 标签：最大公因数;奇偶性;枚举
  - 题面：Suppose $a$ , $b$ , $c$ are positive integers such that \[a+b+c=23\] and \[\gcd(a,b)+\gcd(b,c)+\gcd(c,a)=9.\] What is the sum of all possible distinct values of $a^2+b^2+c^2$ ? $\textbf{(A)}\: 259\qquad\textbf{(B)} \: 438\qquad\textbf{(C)} \: 516\qquad\textbf{(D)} \: 625\qquad\textbf{(E)} \: 687$

### 3.4 进制与数字

- **2021 Fall AMC 12A Problem 4**
  - 考点：分析数字、位值或进制表示带来的整数约束。
  - 标签：数字;质数;整除
  - 题面：The six-digit number $\underline{2}\,\underline{0}\,\underline{2}\,\underline{1}\,\underline{0}\,\underline{A}$ is prime for only one digit $A.$ What is $A?$ $(\textbf{A})\: 1\qquad(\textbf{B}) \: 3\qquad(\textbf{C}) \: 5 \qquad(\textbf{D}) \: 7\qquad(\textbf{E}) \: 9$
- **2021 Fall AMC 12A Problem 10**
  - 考点：分析数字、位值或进制表示带来的整数约束。
  - 标签：九进制;余数;位值
  - 题面：The base-nine representation of the number $N$ is $27{,}006{,}000{,}052_{\text{nine}}.$ What is the remainder when $N$ is divided by $5?$ $\textbf{(A) } 0\qquad\textbf{(B) } 1\qquad\textbf{(C) } 2\qquad\textbf{(D) } 3\qquad\textbf{(E) }4$

## 4. 组合数学

### 4.1 图形计数

- **2021 Fall AMC 12B Problem 19**
  - 考点：把交点或图形结构转化为组合计数。
  - 标签：正多边形;交点;组合计数
  - 备注：按交点数量的主要思想归入图形计数。
  - 题面：Regular polygons with $5,6,7,$ and $8$ sides are inscribed in the same circle. No two of the polygons share a vertex, and no three of their sides intersect at a common point. At how many points inside the circle do two of their sides intersect? $(\textbf{A})\: 52\qquad(\textbf{B}) \: 56\qquad(\textbf{C}) \: 60\qquad(\textbf{D}) \: 64\qquad(\textbf{E}) \: 68$

### 4.2 图论与网络

- **2021 Fall AMC 12A Problem 16**
  - 考点：把连接限制表示成图，利用连通性和极值结构计数。
  - 标签：图论;连通性;极值
  - 备注：按计算机连接网络的主要思想归入图论与网络。
  - 题面：An organization has $30$ employees, $20$ of whom have a brand A computer while the other $10$ have a brand B computer. For security, the computers can only be connected to each other and only by cables. The cables can only connect a brand A computer to a brand B computer. Employees can communicate with each other if their computers are directly connected by a cable or by relaying messages through a series of connected computers. Initially, no computer is connected to any other. A technician arbitrarily selects one computer of each brand and installs a cable between them, provided there is not already a cable between that pair. The technician stops once every employee can communicate with each other. What is the maximum possible number of cables used? $\textbf{(A)}\ 190 \qquad\textbf{(B)}\ 191 \qquad\textbf{(C)}\ 192 \qquad\textbf{(D)}\ 195 \qquad\textbf{(E)}\ 196$

### 4.3 染色与构造

- **2021 Fall AMC 12B Problem 20**
  - 考点：按颜色和对称类型分类，并用构造或轨道计数。
  - 标签：立方体;旋转;染色
  - 题面：A cube is constructed from $4$ white unit cubes and $4$ blue unit cubes. How many different ways are there to construct the $2 \times 2 \times 2$ cube using these smaller cubes? (Two constructions are considered the same if one can be rotated to match the other.) $(\textbf{A})\: 7\qquad(\textbf{B}) \: 8\qquad(\textbf{C}) \: 9\qquad(\textbf{D}) \: 10\qquad(\textbf{E}) \: 11$

## 5. 概率与统计

### 5.1 平均数与数据集

- **2021 Fall AMC 12A Problem 7**
  - 考点：把平均数、总和或数据条件转化为代数约束。
  - 标签：平均数;总和;数据
  - 题面：A school has $100$ students and $5$ teachers. In the first period, each student is taking one class, and each teacher is teaching one class. The enrollments in the classes are $50, 20, 20, 5,$ and $5$ . Let $t$ be the average value obtained if a teacher is picked at random and the number of students in their class is noted. Let $s$ be the average value obtained if a student was picked at random and the number of students in their class, including the student, is noted. What is $t-s$ ? $\textbf{(A)}\ {-}18.5 \qquad\textbf{(B)}\ {-}13.5 \qquad\textbf{(C)}\ 0 \qquad\textbf{(D)}\ 13.5 \qquad\textbf{(E)}\ 18.5$

### 5.2 组合概率

- **2021 Fall AMC 12A Problem 18**
  - 考点：分别计数有利情形与总情形，或使用期望的线性性。
  - 标签：多项分布;组合计数;概率
  - 题面：Each of $20$ balls is tossed independently and at random into one of $5$ bins. Let $p$ be the probability that some bin ends up with $3$ balls, another with $5$ balls, and the other three with $4$ balls each. Let $q$ be the probability that every bin ends up with $4$ balls. What is $\frac{p}{q}$ ? $\textbf{(A)}\ 1 \qquad\textbf{(B)}\ 4 \qquad\textbf{(C)}\ 8 \qquad\textbf{(D)}\ 12 \qquad\textbf{(E)}\ 16$
- **2021 Fall AMC 12A Problem 22**
  - 考点：分别计数有利情形与总情形，或使用期望的线性性。
  - 标签：井字棋;条件计数;概率
  - 题面：Azar and Carl play a game of tic-tac-toe. Azar places an $X$ in one of the boxes in a $3$ -by- $3$ array of boxes, then Carl places an $O$ in one of the remaining boxes. After that, Azar places an $X$ in one of the remaining boxes, and so on until all 9 boxes are filled or one of the players has 3 of their symbols in a row - horizontal, vertical, or diagonal - whichever comes first, in which case that player wins the game. Suppose the players make their moves at random, rather than trying to follow a rational strategy, and that Carl wins the game when he places his third $O$ . How many ways can the board look after the game is over? $\textbf{(A) } 36 \qquad\textbf{(B) } 112 \qquad\textbf{(C) } 120 \qquad\textbf{(D) } 148 \qquad\textbf{(E) } 160$
- **2021 Fall AMC 12B Problem 11**
  - 考点：分别计数有利情形与总情形，或使用期望的线性性。
  - 标签：骰子;整除;补集概率
  - 题面：Una rolls $6$ standard $6$ -sided dice simultaneously and calculates the product of the $6{ }$ numbers obtained. What is the probability that the product is divisible by $4?$ $\textbf{(A)}\: \frac34\qquad\textbf{(B)} \: \frac{57}{64}\qquad\textbf{(C)} \: \frac{59}{64}\qquad\textbf{(D)} \: \frac{187}{192}\qquad\textbf{(E)} \: \frac{63}{64}$
- **2021 Fall AMC 12B Problem 17**
  - 考点：分别计数有利情形与总情形，或使用期望的线性性。
  - 标签：随机游走;三角网格;概率
  - 题面：A bug starts at a vertex of a grid made of equilateral triangles of side length $1$ . At each step the bug moves in one of the $6$ possible directions along the grid lines randomly and independently with equal probability. What is the probability that after $5$ moves the bug never will have been more than $1$ unit away from the starting position? $\textbf{(A)}\ \frac{13}{108} \qquad\textbf{(B)}\ \frac{7}{54} \qquad\textbf{(C)}\ \frac{29}{216} \qquad\textbf{(D)}\ \frac{4}{27} \qquad\textbf{(E)}\ \frac{1}{16}$
- **2021 Fall AMC 12B Problem 23**
  - 考点：分别计数有利情形与总情形，或使用期望的线性性。
  - 标签：期望;连续整数;线性性
  - 题面：What is the average number of pairs of consecutive integers in a randomly selected subset of $5$ distinct integers chosen from the set $\{ 1, 2, 3, …, 30\}$ ? (For example the set $\{1, 17, 18, 19, 30\}$ has $2$ pairs of consecutive integers.) $\textbf{(A)}\ \frac{2}{3} \qquad\textbf{(B)}\ \frac{29}{36} \qquad\textbf{(C)}\ \frac{5}{6} \qquad\textbf{(D)}\ \frac{29}{30} \qquad\textbf{(E)}\ 1$
