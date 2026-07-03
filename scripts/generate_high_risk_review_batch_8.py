import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 8"
base.BATCH_NUMBER = 292
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2012 AMC 12B Problem 17": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("C", "$\\frac{32}{5}$"),
        "statement": r"""Square $PQRS$ lies in the first quadrant. Points $(3,0),(5,0),(7,0),$ and $(13,0)$ lie on lines $SP,RQ,PQ,$ and $SR$, respectively. What is the sum of the coordinates of the center of square $PQRS$?""",
        "choices": [
            ("A", "$6$"),
            ("B", "$\\frac{31}{5}$"),
            ("C", "$\\frac{32}{5}$"),
            ("D", "$\\frac{33}{5}$"),
            ("E", "$\\frac{34}{5}$"),
        ],
        "key_idea": "Use slopes of the square's sides and the midlines between opposite parallel sides.",
        "solution": [
            ("Represent the four side lines by slopes",
             r"""Let the lines through $(3,0)$ and $(5,0)$ be the two opposite sides $SP$ and $RQ$. Since the square is in the first quadrant, write their common positive slope as $m$:

\[y=m(x-3),\qquad y=m(x-5).\]

The other two sides are perpendicular, so their slope is $-\frac1m$:

\[y=-\frac1m(x-7),\qquad y=-\frac1m(x-13).\]"""),
            ("Use equal distances between opposite sides",
             r"""The distance between the two lines of slope $m$ is

\[\frac{2m}{\sqrt{m^2+1}}.\]

The distance between the two perpendicular side lines is

\[\frac{6}{\sqrt{m^2+1}}.\]

In a square, these two distances are both the side length, so

\[\frac{2m}{\sqrt{m^2+1}}=\frac{6}{\sqrt{m^2+1}},\]

which gives $m=3$."""),
            ("Find the two center lines",
             r"""The center of a square lies halfway between each pair of opposite sides. The midline between the lines through $(3,0)$ and $(5,0)$ has the same slope $3$ and passes through $(4,0)$:

\[y=3(x-4).\]

The midline between the lines through $(7,0)$ and $(13,0)$ has slope $-\frac13$ and passes through $(10,0)$:

\[y=-\frac13(x-10).\]"""),
            ("Intersect the midlines",
             r"""Solve

\[3(x-4)=-\frac13(x-10).\]

Multiplying by $3$ gives

\[9x-36=-x+10,\]

so $x=\frac{23}{5}$. Then

\[y=3\left(\frac{23}{5}-4\right)=\frac95.\]"""),
            ("Add the coordinates",
             r"""The center is

\[\left(\frac{23}{5},\frac95\right),\]

so the requested sum is

\[\frac{23}{5}+\frac95=\frac{32}{5}.\]"""),
        ],
    },
    "2012 AMC 12A Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12A_Answer_Key",
        "answer": ("C", "$\\frac{4}{25}$"),
        "statement": r"""Let $S$ be the square one of whose diagonals has endpoints $\left(\frac{1}{10},\frac{7}{10}\right)$ and $\left(-\frac{1}{10},-\frac{7}{10}\right)$. A point $v=(x,y)$ is chosen uniformly at random over all pairs of real numbers $x$ and $y$ such that $0\le x\le 2012$ and $0\le y\le 2012$. Let $T(v)$ be a translated copy of $S$ centered at $v$. What is the probability that the square region determined by $T(v)$ contains exactly two points with integer coordinates in its interior?""",
        "choices": [
            ("A", "$\\frac18$"),
            ("B", "$\\frac{7}{50}$"),
            ("C", "$\\frac{4}{25}$"),
            ("D", "$\\frac14$"),
            ("E", "$\\frac{8}{25}$"),
        ],
        "key_idea": "Use periodicity modulo the integer lattice and compute one overlap area in a unit cell.",
        "solution": [
            ("Reduce the probability to one unit cell",
             r"""The square $[0,2012]\times[0,2012]$ is made of an integer number of unit cells. Because integer lattice points repeat with period $1$ in both directions, it is enough to study the center $v$ inside one unit cell

\[U=[0,1]\times[0,1].\]

Boundary cases have probability $0$, so we can count areas inside $U$."""),
            ("Understand which two lattice points can appear",
             r"""The diagonal of $S$ has length

\[\sqrt{\left(\frac15\right)^2+\left(\frac75\right)^2}=\sqrt2,\]

so $S$ has side length $1$. A tilted unit square can contain two integer points only when those integer points are adjacent lattice points, not diagonal lattice points."""),
            ("Compute one adjacent-pair region",
             r"""First count centers for which $T(v)$ contains both $(0,0)$ and $(1,0)$. This means $v$ must lie in the intersection of two congruent squares: one centered at $(0,0)$ and one centered at $(1,0)$.

Inside $U$, that overlap is the quadrilateral with vertices

\[\left(\frac38,0\right),\quad \left(\frac58,0\right),\quad \left(\frac{23}{50},\frac{11}{50}\right),\quad \left(\frac3{10},\frac1{10}\right).\]"""),
            ("Find the area of that region",
             r"""Using the shoelace formula on those four vertices gives area

\[\frac1{25}.\]

This is the probability contribution for one specific adjacent pair of integer points, such as $(0,0)$ and $(1,0)$."""),
            ("Use symmetry for the four adjacent pairs",
             r"""In each unit cell, there are four possible adjacent pairs around the cell: horizontal lower, horizontal upper, vertical left, and vertical right. By symmetry, each has the same area $\frac1{25}$.

Therefore the desired probability is

\[4\cdot\frac1{25}=\frac4{25}.\]"""),
        ],
    },
    "2014 AMC 12A Problem 17": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("A", "$2+2\\sqrt7$"),
        "statement": r"""A $4\times4\times h$ rectangular box contains a sphere of radius $2$ and eight smaller spheres of radius $1$. The smaller spheres are each tangent to three sides of the box, and the larger sphere is tangent to each of the smaller spheres. What is $h$?""",
        "choices": [
            ("A", "$2+2\\sqrt7$"),
            ("B", "$3+2\\sqrt5$"),
            ("C", "$4+2\\sqrt7$"),
            ("D", "$4\\sqrt5$"),
            ("E", "$4\\sqrt7$"),
        ],
        "key_idea": "Place sphere centers in 3D coordinates and use the tangency distance between centers.",
        "solution": [
            ("Place the box in coordinates",
             r"""Let the box be

\[0\le x\le4,\qquad 0\le y\le4,\qquad 0\le z\le h.\]

A small sphere tangent to the three coordinate-side faces has center $(1,1,1)$."""),
            ("Locate the large sphere by symmetry",
             r"""The eight small spheres sit symmetrically near the eight corners of the box. Therefore the large sphere's center must lie on the center line of the box:

\[\left(2,2,\frac h2\right).\]

This avoids needing a diagram; the symmetry forces the horizontal coordinates to be $2$ and $2$."""),
            ("Translate tangency into a distance equation",
             r"""A sphere of radius $2$ tangent to a sphere of radius $1$ has center-to-center distance

\[2+1=3.\]

So the distance from $(1,1,1)$ to $\left(2,2,\frac h2\right)$ must be $3$:

\[\sqrt{(2-1)^2+(2-1)^2+\left(\frac h2-1\right)^2}=3.\]"""),
            ("Solve for h",
             r"""Squaring gives

\[1+1+\left(\frac h2-1\right)^2=9,\]

so

\[\left(\frac h2-1\right)^2=7.\]

Since the height is greater than $2$, we take the positive value:

\[\frac h2-1=\sqrt7.\]"""),
            ("Finish",
             r"""Thus

\[h=2+2\sqrt7.\]

The answer is $2+2\sqrt7$."""),
        ],
    },
    "2014 AMC 12A Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("D", "$14$"),
        "statement": r"""In $\triangle BAC$, $\angle BAC=40^\circ$, $AB=10$, and $AC=6$. Points $D$ and $E$ lie on $\overline{AB}$ and $\overline{AC}$ respectively. What is the minimum possible value of $BE+DE+CD$?""",
        "choices": [
            ("A", "$6\\sqrt3+3$"),
            ("B", "$\\frac{27}{2}$"),
            ("C", "$8\\sqrt3$"),
            ("D", "$14$"),
            ("E", "$3\\sqrt3+9$"),
        ],
        "key_idea": "Unfold the broken path by reflecting across the two sides of the angle.",
        "solution": [
            ("Recognize the broken-path structure",
             r"""The expression

\[BE+DE+CD\]

is the length of a path from $B$ to $C$ that touches side $AC$ at $E$ and side $AB$ at $D$. When a shortest path reflects off lines, a standard way to handle it is to unfold the reflections into one straight segment."""),
            ("Reflect one endpoint across each side",
             r"""Reflect $B$ across line $AC$ to a point $B'$, and reflect $C$ across line $AB$ to a point $C'$. Then

\[BE=B'E,\qquad CD=C'D.\]

So minimizing $BE+DE+CD$ is the same as minimizing the broken path

\[B'E+ED+DC'.\]"""),
            ("Turn the minimum into a straight line",
             r"""The shortest route from $B'$ to $C'$ through points $E$ and $D$ on the two sides occurs when $B',E,D,C'$ are collinear. Therefore the minimum value is simply

\[B'C'.\]

This is the key idea: reflection changes the path length but removes the bends."""),
            ("Find the angle between the reflected rays",
             r"""Reflection preserves distance from $A$, so

\[AB'=AB=10,\qquad AC'=AC=6.\]

The original angle at $A$ is $40^\circ$. After the two reflections, the angle between rays $AB'$ and $AC'$ is

\[40^\circ+40^\circ+40^\circ=120^\circ.\]"""),
            ("Use the Law of Cosines",
             r"""Now apply the Law of Cosines in triangle $AB'C'$:

\[(B'C')^2=10^2+6^2-2(10)(6)\cos120^\circ.\]

Since $\cos120^\circ=-\frac12$,

\[(B'C')^2=100+36+60=196.\]"""),
            ("Finish",
             r"""Thus

\[B'C'=14.\]

So the minimum possible value of $BE+DE+CD$ is $14$."""),
        ],
    },
    "2021 Spring AMC 12A Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("A", "$7$"),
        "statement": r"""The five solutions to the equation $(z-1)(z^2+2z+4)(z^2+4z+6)=0$ may be written in the form $x_k+y_ki$ for $1\le k\le5$, where $x_k$ and $y_k$ are real. Let $\mathcal E$ be the unique ellipse that passes through the points $(x_1,y_1),(x_2,y_2),(x_3,y_3),(x_4,y_4),$ and $(x_5,y_5)$. The eccentricity of $\mathcal E$ can be written in the form $\sqrt{\frac mn}$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?""",
        "choices": [("A", "$7$"), ("B", "$9$"), ("C", "$11$"), ("D", "$13$"), ("E", "$15$")],
        "key_idea": "Find the ellipse equation from the five complex roots, then compute its eccentricity.",
        "solution": [
            ("Convert roots into points",
             r"""The roots are

\[1,\qquad -1\pm i\sqrt3,\qquad -2\pm i\sqrt2.\]

So the five points are

\[(1,0),\quad (-1,\pm\sqrt3),\quad (-2,\pm\sqrt2).\]"""),
            ("Use symmetry to simplify the ellipse equation",
             r"""The points are symmetric about the $x$-axis, so the ellipse is also symmetric about the $x$-axis. Thus its equation can be written in the form

\[Ax^2+Cy^2+Dx+F=0.\]

There is no $xy$ term and no $y$ term because of the symmetry."""),
            ("Plug in the three independent point types",
             r"""Using $(1,0)$ gives

\[A+D+F=0.\]

Using $(-1,\sqrt3)$ gives

\[A+3C-D+F=0.\]

Using $(-2,\sqrt2)$ gives

\[4A+2C-2D+F=0.\]"""),
            ("Solve the relative coefficients",
             r"""Subtracting the first equation from the second gives

\[3C-2D=0,\]

so $D=\frac32C$. Subtracting the first equation from the third gives

\[3A+2C-3D=0.\]

Substitute $D=\frac32C$ to get $A=\frac56C$."""),
            ("Write the ellipse in standard form",
             r"""Scale by choosing $C=6$. Then one equation for the ellipse is

\[5x^2+6y^2+9x-14=0.\]

Completing the square gives

\[\frac{\left(x+\frac9{10}\right)^2}{\frac{361}{100}}+\frac{y^2}{\frac{361}{120}}=1.\]

So $a^2=\frac{361}{100}$ and $b^2=\frac{361}{120}$."""),
            ("Compute the eccentricity",
             r"""The eccentricity is

\[\frac ca=\sqrt{1-\frac{b^2}{a^2}}.\]

Here

\[\frac{b^2}{a^2}=\frac{361/120}{361/100}=\frac56,\]

so

\[\frac ca=\sqrt{\frac16}.\]

Thus $m+n=1+6=7$."""),
        ],
    },
    "2021 Spring AMC 12B Problem 11": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("D", "$12\\sqrt2$"),
        "statement": r"""Triangle $ABC$ has $AB=13$, $BC=14$, and $AC=15$. Let $P$ be the point on $\overline{AC}$ such that $PC=10$. There are exactly two points $D$ and $E$ on line $BP$ such that quadrilaterals $ABCD$ and $ABCE$ are trapezoids. What is the distance $DE$?""",
        "choices": [
            ("A", "$\\frac{42}{5}$"),
            ("B", "$6\\sqrt2$"),
            ("C", "$\\frac{84}{5}$"),
            ("D", "$12\\sqrt2$"),
            ("E", "$18$"),
        ],
        "key_idea": "Place the 13-14-15 triangle in coordinates and intersect line BP with the two parallel lines forced by the trapezoid condition.",
        "solution": [
            ("Choose friendly coordinates",
             r"""A $13$-$14$-$15$ triangle has area $84$, so one convenient placement is

\[B=(0,0),\qquad C=(14,0),\qquad A=(5,12).\]

This gives $AB=13$, $BC=14$, and $AC=15$."""),
            ("Locate point P",
             r"""Since $PC=10$ and $AC=15$, point $P$ is $\frac{10}{15}=\frac23$ of the way from $C$ to $A$. Therefore

\[P=C+\frac23(A-C)=(14,0)+\frac23(-9,12)=(8,8).\]

So line $BP$ is simply $y=x$."""),
            ("Find one trapezoid point",
             r"""For one trapezoid, side $AD$ is parallel to $BC$. Since $BC$ is horizontal, $AD$ is horizontal. Thus $D$ lies on the horizontal line through $A$, namely $y=12$.

Because $D$ is also on $BP$, where $y=x$, we get

\[D=(12,12).\]"""),
            ("Find the other trapezoid point",
             r"""For the other trapezoid, side $CE$ is parallel to $AB$. The slope of $AB$ is

\[\frac{12-0}{5-0}=\frac{12}{5}.\]

The line through $C=(14,0)$ with this slope is

\[y=\frac{12}{5}(x-14).\]

Intersecting with $y=x$ gives $x=24$, so

\[E=(24,24).\]"""),
            ("Compute DE",
             r"""Now

\[DE=\sqrt{(24-12)^2+(24-12)^2}=12\sqrt2.\]

So the answer is $12\sqrt2$."""),
        ],
    },
    "2022 AMC 12A Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2022_AMC_12A_Answer_Key",
        "answer": ("B", "$\\frac13$"),
        "statement": r"""Isosceles trapezoid $ABCD$ has parallel sides $AD$ and $BC$, with $BC<AD$ and $AB=CD$. There is a point $P$ in the plane such that $PA=1$, $PB=2$, $PC=3$, and $PD=4$. What is $\frac{BC}{AD}$?""",
        "choices": [
            ("A", "$\\frac14$"),
            ("B", "$\\frac13$"),
            ("C", "$\\frac12$"),
            ("D", "$\\frac23$"),
            ("E", "$\\frac34$"),
        ],
        "key_idea": "Use symmetric coordinates for the isosceles trapezoid and subtract squared distance equations.",
        "solution": [
            ("Put the trapezoid in symmetric coordinates",
             r"""Because the trapezoid is isosceles, it has a line of symmetry perpendicular to the bases. Place the longer base $AD$ horizontally with

\[A=(-a,0),\qquad D=(a,0),\]

and the shorter base with

\[B=(-b,h),\qquad C=(b,h),\]

where $a>b>0$. Then

\[AD=2a,\qquad BC=2b.\]"""),
            ("Let P be arbitrary",
             r"""The point $P$ does not need to lie on the symmetry axis, so write

\[P=(x,y).\]

The distances to $A$ and $D$ are

\[(x+a)^2+y^2=1^2,\]

\[(x-a)^2+y^2=4^2.\]"""),
            ("Subtract the equations for A and D",
             r"""Subtracting the two equations removes $y^2$:

\[(x-a)^2-(x+a)^2=16-1.\]

The left side is $-4ax$, so

\[-4ax=15.\]"""),
            ("Use the same idea for B and C",
             r"""Similarly, the distances to $B$ and $C$ give

\[(x+b)^2+(y-h)^2=2^2,\]

\[(x-b)^2+(y-h)^2=3^2.\]

Subtracting gives

\[(x-b)^2-(x+b)^2=9-4,\]

so

\[-4bx=5.\]"""),
            ("Compare the two results",
             r"""We have

\[-4ax=15,\qquad -4bx=5.\]

Since the same point $P$ has the same $x$-coordinate in both equations,

\[\frac{a}{b}=\frac{15}{5}=3.\]

Therefore $a=3b$."""),
            ("Find the ratio of bases",
             r"""Finally,

\[\frac{BC}{AD}=\frac{2b}{2a}=\frac ba=\frac13.\]

So the answer is $\frac13$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
