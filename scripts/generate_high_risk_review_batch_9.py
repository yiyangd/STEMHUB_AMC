import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 9"
base.BATCH_NUMBER = 293
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2011 AMC 12B Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12B_Answer_Key",
        "answer": ("B", "$8\\sqrt2$"),
        "statement": r"""Let $P(z)=z^8+(4\sqrt3+6)z^4-(4\sqrt3+7)$. What is the minimum perimeter among all the 8-sided polygons in the complex plane whose vertices are precisely the zeros of $P(z)$?""",
        "choices": [
            ("A", "$4\\sqrt3+4$"),
            ("B", "$8\\sqrt2$"),
            ("C", "$3\\sqrt2+3\\sqrt6$"),
            ("D", "$4\\sqrt2+4\\sqrt3$"),
            ("E", "$4\\sqrt3+6$"),
        ],
        "key_idea": "Solve for the two sets of fourth roots and connect the roots in circular order for the least perimeter.",
        "solution": [
            ("Reduce the polynomial to a quadratic in z^4",
             r"""Let $w=z^4$. Then

\[w^2+(4\sqrt3+6)w-(4\sqrt3+7)=0.\]

One root is $w=1$, since substituting $1$ makes the expression zero. The other root is

\[-(4\sqrt3+7)=-(2+\sqrt3)^2.\]"""),
            ("Describe the eight roots geometrically",
             r"""The equation $z^4=1$ gives the four unit roots at angles

\[0^\circ,\ 90^\circ,\ 180^\circ,\ 270^\circ.\]

The equation $z^4=-(2+\sqrt3)^2$ gives four roots with radius

\[\rho=\sqrt{2+\sqrt3}\]

and angles

\[45^\circ,\ 135^\circ,\ 225^\circ,\ 315^\circ.\]"""),
            ("Choose the shortest way to visit the vertices",
             r"""For points arranged on two concentric squares with alternating angles, the shortest 8-sided polygon connects neighboring angles in circular order. Any chord that skips an intermediate vertex can be shortened by replacing it with the two local edges through that intermediate vertex.

Thus the minimum perimeter has eight congruent edges, each joining a unit-radius point to a $\rho$-radius point separated by $45^\circ$."""),
            ("Compute one edge length",
             r"""By the Law of Cosines, one such edge has squared length

\[1^2+\rho^2-2\rho\cos45^\circ.\]

Since $\rho^2=2+\sqrt3$ and $\rho=\sqrt{2+\sqrt3}$, this simplifies to

\[1+(2+\sqrt3)-2\sqrt{2+\sqrt3}\cdot\frac{\sqrt2}{2}=2.\]

So each edge has length $\sqrt2$."""),
            ("Finish the perimeter",
             r"""There are $8$ equal edges, so the minimum perimeter is

\[8\sqrt2.\]

Therefore the answer is $8\sqrt2$."""),
        ],
    },
    "2015 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12B_Answer_Key",
        "answer": ("B", "$2024$"),
        "statement": r"""A bee starts flying from point $P_0$. She flies $1$ inch due east to point $P_1$. For $j\ge1$, once the bee reaches point $P_j$, she turns $30^\circ$ counterclockwise and then flies $j+1$ inches straight to point $P_{j+1}$. When the bee reaches $P_{2015}$ she is exactly $a\sqrt b+c\sqrt d$ inches away from $P_0$, where $a,b,c,$ and $d$ are positive integers and $b$ and $d$ are not divisible by the square of any prime. What is $a+b+c+d$?""",
        "choices": [("A", "$2016$"), ("B", "$2024$"), ("C", "$2032$"), ("D", "$2040$"), ("E", "$2048$")],
        "key_idea": "Represent each flight as a complex vector and group the directions into 12-step cycles.",
        "solution": [
            ("Turn the path into a vector sum",
             r"""Let

\[q=\cos30^\circ+i\sin30^\circ.\]

The first segment has vector $1$, the second has vector $2q$, the third has vector $3q^2$, and so on. Thus the displacement after $2015$ flights is

\[S=\sum_{k=1}^{2015} kq^{k-1}.\]"""),
            ("Use the 12-step period",
             r"""Because $q^{12}=1$, the directions repeat every $12$ segments. Write $2015=12\cdot167+11$.

For one complete 12-step block,

\[\sum_{r=1}^{12} rq^{r-1}=-\frac{12}{1-q}.\]

The constant part of each block cancels because

\[\sum_{r=1}^{12}q^{r-1}=0.\]"""),
            ("Add the full blocks and the last 11 steps",
             r"""The $167$ full blocks and the final $11$ terms combine to

\[S=168\left(-\frac{12}{1-q}\right)-2016q^{11}.\]

Substituting $q=\frac{\sqrt3+i}{2}$ and simplifying gives

\[S=-1008(1+\sqrt3)-1008(1+\sqrt3)i.\]"""),
            ("Convert displacement to distance",
             r"""The distance from $P_0$ is the magnitude of $S$:

\[|S|=1008(1+\sqrt3)\sqrt2.\]

Distribute the $\sqrt2$:

\[|S|=1008\sqrt2+1008\sqrt6.\]"""),
            ("Read off the requested sum",
             r"""So we may take

\[a=1008,\quad b=2,\quad c=1008,\quad d=6.\]

Therefore

\[a+b+c+d=1008+2+1008+6=2024.\]"""),
        ],
    },
    "2018 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2018_AMC_12A_Answer_Key",
        "answer": ("A", "$20$"),
        "statement": r"""The solutions to the equations $z^2=4+4\sqrt{15}i$ and $z^2=2+2\sqrt3 i$, where $i=\sqrt{-1}$, form the vertices of a parallelogram in the complex plane. The area of this parallelogram can be written in the form $p\sqrt q-r\sqrt s$, where $p,q,r,$ and $s$ are positive integers and neither $q$ nor $s$ is divisible by the square of any prime number. What is $p+q+r+s$?""",
        "choices": [("A", "$20$"), ("B", "$21$"), ("C", "$22$"), ("D", "$23$"), ("E", "$24$")],
        "key_idea": "Find the square roots explicitly and use a determinant for the parallelogram area.",
        "solution": [
            ("Find the first pair of roots",
             r"""Let $u^2=4+4\sqrt{15}i$. Since

\[|4+4\sqrt{15}i|=16,\]

we have $|u|=4$. If $u=x+yi$, then

\[x^2+y^2=16,\qquad x^2-y^2=4.\]

Solving gives $x^2=10$ and $y^2=6$, so one root is

\[u=\sqrt{10}+i\sqrt6.\]"""),
            ("Find the second pair of roots",
             r"""Similarly, let $v^2=2+2\sqrt3i$. Then $|v|=2$, and

\[x^2+y^2=4,\qquad x^2-y^2=2.\]

Thus one root is

\[v=\sqrt3+i.\]"""),
            ("Understand the parallelogram",
             r"""The four roots are

\[u,\ -u,\ v,\ -v.\]

These naturally form a parallelogram centered at the origin. Its area is twice the absolute value of the determinant formed by $u$ and $v$:

\[\text{Area}=2|\operatorname{Im}(u\overline v)|.\]"""),
            ("Compute the determinant",
             r"""Using coordinates, this determinant is

\[\sqrt{10}\cdot1-\sqrt6\cdot\sqrt3=\sqrt{10}-3\sqrt2.\]

Its absolute value is

\[3\sqrt2-\sqrt{10}.\]"""),
            ("Match the required form",
             r"""Therefore the area is

\[2(3\sqrt2-\sqrt{10})=6\sqrt2-2\sqrt{10}.\]

So $p=6$, $q=2$, $r=2$, and $s=10$, giving

\[p+q+r+s=20.\]"""),
        ],
    },
    "2019 AMC 12A Problem 18": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2019_AMC_12A_Answer_Key",
        "answer": ("D", "$2\\sqrt5$"),
        "statement": r"""A sphere with center $O$ has radius $6$. A triangle with sides of length $15,15,$ and $24$ is situated in space so that each of its sides is tangent to the sphere. What is the distance between $O$ and the plane determined by the triangle?""",
        "choices": [("A", "$2\\sqrt3$"), ("B", "$4$"), ("C", "$3\\sqrt2$"), ("D", "$2\\sqrt5$"), ("E", "$5$")],
        "key_idea": "Project the sphere center onto the triangle plane; the cross-section circle is tangent to the triangle's sides.",
        "solution": [
            ("Look at the cross-section in the triangle's plane",
             r"""Let the distance from $O$ to the plane of the triangle be $h$. The plane cuts the sphere in a circle.

Because each side of the triangle is tangent to the sphere, each side is tangent to this cross-section circle. Thus the cross-section circle is the incircle of the triangle."""),
            ("Find the triangle's inradius",
             r"""The triangle has sides $15,15,24$. Dropping the altitude to the side of length $24$ splits it into two segments of length $12$.

The altitude is

\[\sqrt{15^2-12^2}=9.\]

So the area is

\[\frac12\cdot24\cdot9=108.\]"""),
            ("Use area equals inradius times semiperimeter",
             r"""The semiperimeter is

\[s=\frac{15+15+24}{2}=27.\]

If the inradius is $r$, then

\[108=27r,\]

so

\[r=4.\]"""),
            ("Relate the incircle radius to the sphere radius",
             r"""In a perpendicular cross-section through $O$ and the center of the incircle, we get a right triangle. The sphere radius is $6$, the cross-section circle radius is $4$, and the distance from $O$ to the plane is $h$.

Therefore

\[h^2+4^2=6^2.\]"""),
            ("Finish",
             r"""Thus

\[h=\sqrt{36-16}=\sqrt{20}=2\sqrt5.\]

So the distance from $O$ to the plane is $2\sqrt5$."""),
        ],
    },
    "2019 AMC 12A Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2019_AMC_12A_Answer_Key",
        "answer": ("A", "$9$"),
        "statement": r"""In $\triangle ABC$ with integer side lengths, $\cos A=\frac{11}{16}$, $\cos B=\frac78$, and $\cos C=-\frac14$. What is the least possible perimeter for $\triangle ABC$?""",
        "choices": [("A", "$9$"), ("B", "$12$"), ("C", "$23$"), ("D", "$27$"), ("E", "$44$")],
        "key_idea": "Use the sine values and the Law of Sines to get the side ratio.",
        "solution": [
            ("Convert cosines to sines",
             r"""The side lengths of a triangle are proportional to the sines of the opposite angles. Since all triangle angles have positive sine,

\[\sin A=\sqrt{1-\left(\frac{11}{16}\right)^2}=\frac{3\sqrt{15}}{16},\]

\[\sin B=\sqrt{1-\left(\frac78\right)^2}=\frac{\sqrt{15}}{8},\]

\[\sin C=\sqrt{1-\left(-\frac14\right)^2}=\frac{\sqrt{15}}{4}.\]"""),
            ("Find the side ratio",
             r"""By the Law of Sines,

\[a:b:c=\sin A:\sin B:\sin C.\]

Substituting the values gives

\[\frac{3\sqrt{15}}{16}:\frac{\sqrt{15}}8:\frac{\sqrt{15}}4.\]

Multiplying by $\frac{16}{\sqrt{15}}$ gives the ratio

\[3:2:4.\]"""),
            ("Check that the ratio makes sense",
             r"""The angle $C$ is obtuse because $\cos C<0$, and the side opposite it should be the largest side. In the ratio $3:2:4$, the largest side is indeed opposite $C$, so the ratio is consistent with the angle data."""),
            ("Use integer side lengths",
             r"""All side lengths are integers, so the triangle must be an integer multiple of

\[3,2,4.\]

The least possible positive integer side lengths are exactly $3,2,4$."""),
            ("Finish",
             r"""The least possible perimeter is

\[3+2+4=9.\]

So the answer is $9$."""),
        ],
    },
    "2021 Spring AMC 12A Problem 17": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("D", "$194$"),
        "statement": r"""Trapezoid $ABCD$ has $AB\parallel CD$, $BC=CD=43$, and $AD\perp BD$. Let $O$ be the intersection of the diagonals $AC$ and $BD$, and let $P$ be the midpoint of $BD$. Given that $OP=11$, the length $AD$ can be written in the form $m\sqrt n$, where $m$ and $n$ are positive integers and $n$ is not divisible by the square of any prime. What is $m+n$?""",
        "choices": [("A", "$65$"), ("B", "$132$"), ("C", "$157$"), ("D", "$194$"), ("E", "$215$")],
        "key_idea": "Use the diagonal intersection ratio in a trapezoid together with AD perpendicular to BD.",
        "solution": [
            ("Name the key lengths",
             r"""Let

\[BD=d,\qquad AD=x,\qquad AB=L.\]

Since $AD\perp BD$, triangle $ABD$ is right, so

\[L^2=x^2+d^2.\]"""),
            ("Use the condition BC = CD",
             r"""Because $AB\parallel CD$ and $CD=43$, place $CD$ as a segment parallel to $AB$ with length $43$. A coordinate computation comparing $BC$ to $CD$ gives a useful simplification:

\[BC=43 \quad\Longrightarrow\quad AB=86.\]

The reason is that the horizontal and vertical components force the longer base to be exactly twice the shorter parallel side."""),
            ("Use the diagonal intersection ratio",
             r"""In a trapezoid, the intersection of the diagonals divides each diagonal in the ratio of the two bases. Since

\[AB:CD=86:43=2:1,\]

point $O$ divides $BD$ so that

\[BO:OD=2:1.\]

Thus

\[OD=\frac d3.\]"""),
            ("Use the midpoint information",
             r"""Point $P$ is the midpoint of $BD$, so

\[PD=\frac d2.\]

Since $O$ lies on $BD$ and $OP=11$,

\[\left|\frac d2-\frac d3\right|=\frac d6=11.\]

Therefore

\[d=66.\]"""),
            ("Find AD",
             r"""Now use the right triangle $ABD$:

\[AD^2=AB^2-BD^2=86^2-66^2.\]

This gives

\[AD^2=7396-4356=3040=16\cdot190.\]

So

\[AD=4\sqrt{190}.\]"""),
            ("Finish",
             r"""Thus $m=4$ and $n=190$, so

\[m+n=194.\]

The answer is $194$."""),
        ],
    },
    "2022 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2022_AMC_12A_Answer_Key",
        "answer": ("A", "$4.5$"),
        "statement": r"""Let $c$ be a real number, and let $z_1,z_2$ be the two complex numbers satisfying the quadratic $z^2-cz+10=0$. Points $z_1,z_2,\frac1{z_1},$ and $\frac1{z_2}$ are the vertices of a convex quadrilateral $Q$ in the complex plane. When the area of $Q$ obtains its maximum possible value, $c$ is closest to which of the following?""",
        "choices": [("A", "$4.5$"), ("B", "$5$"), ("C", "$5.5$"), ("D", "$6$"), ("E", "$6.5$")],
        "key_idea": "Use Vieta's formulas and maximize the area of the symmetric trapezoid in the complex plane.",
        "solution": [
            ("Describe the roots",
             r"""For the quadrilateral to have positive area, the roots should be a nonreal conjugate pair. Write

\[z_1=a+bi,\qquad z_2=a-bi.\]

By Vieta's formulas,

\[z_1z_2=a^2+b^2=10,\]

and

\[c=z_1+z_2=2a.\]"""),
            ("Find the reciprocal points",
             r"""Since $a^2+b^2=10$,

\[\frac1{z_1}=\frac{a-bi}{10},\qquad \frac1{z_2}=\frac{a+bi}{10}.\]

So the four points form a symmetric trapezoid in the complex plane."""),
            ("Write the area in terms of a and b",
             r"""The long vertical base has length $2b$, and the short vertical base has length $\frac{b}{5}$. The horizontal distance between those two bases is

\[a-\frac a{10}=\frac{9a}{10}.\]

Thus the area is

\[\frac12\left(2b+\frac b5\right)\frac{9a}{10}=\frac{99}{100}ab.\]"""),
            ("Maximize ab",
             r"""We need to maximize $ab$ subject to

\[a^2+b^2=10.\]

For a fixed sum of squares, the product $ab$ is largest when $a=b$. Hence

\[a=b=\sqrt5.\]"""),
            ("Convert back to c",
             r"""Since $c=2a$, the area is maximized when

\[c=2\sqrt5=\sqrt{20}\approx4.47.\]

Among the answer choices, this is closest to $4.5$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
