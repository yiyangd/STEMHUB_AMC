import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 13"
base.BATCH_NUMBER = 297
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2011 AMC 12A Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12A_Answer_Key",
        "answer": ("C", "$2\\sqrt6$"),
        "statement": r"""Consider all quadrilaterals $ABCD$ such that $AB=14$, $BC=9$, $CD=7$, and $DA=12$. What is the radius of the largest possible circle that fits inside or on the boundary of such a quadrilateral?""",
        "choices": [
            ("A", "$\\sqrt{15}$"),
            ("B", "$\\sqrt{21}$"),
            ("C", "$2\\sqrt6$"),
            ("D", "$5$"),
            ("E", "$2\\sqrt7$"),
        ],
        "key_idea": "Use area bounds: a circle of radius r inside the quadrilateral forces area at least r times the semiperimeter, and Brahmagupta gives the maximum possible area.",
        "solution": [
            ("Relate a fitted circle to area",
             r"""Suppose a circle of radius $r$ fits inside a quadrilateral with side lengths $14,9,7,12$. If the circle center has perpendicular distances $d_1,d_2,d_3,d_4$ to the four sides, then each $d_i\ge r$.

Splitting the quadrilateral into four triangles from the circle center to the sides gives

\[K=\frac12(14d_1+9d_2+7d_3+12d_4).\]

Since every $d_i\ge r$,

\[K\ge \frac12(14+9+7+12)r=21r.\]"""),
            ("Turn this into an upper bound for r",
             r"""The previous inequality means

\[r\le \frac{K}{21}.\]

So to make $r$ as large as possible, we need the largest possible area $K$ for a quadrilateral with the given side lengths."""),
            ("Maximize the quadrilateral area",
             r"""For fixed side lengths, the maximum area occurs when the quadrilateral is cyclic. Then Brahmagupta's formula applies.

The semiperimeter is

\[s=\frac{14+9+7+12}{2}=21.\]

Thus the maximum area is

\[K_{\max}=\sqrt{(21-14)(21-9)(21-7)(21-12)}.\]"""),
            ("Compute the maximum area",
             r"""Substitute:

\[K_{\max}=\sqrt{7\cdot12\cdot14\cdot9}.\]

This simplifies to

\[K_{\max}=\sqrt{42^2\cdot6}=42\sqrt6.\]"""),
            ("Check that the bound is attainable",
             r"""We also need to know that this upper bound can actually be reached by a circle. The side lengths satisfy Pitot's condition:

\[14+7=9+12=21.\]

This is exactly the side-sum condition for a tangential quadrilateral. So there is a quadrilateral with these side lengths that has an incircle, and the circle can be tangent to all four sides at the maximum-area configuration."""),
            ("Finish the radius",
             r"""At the maximum,

\[21r=42\sqrt6.\]

Therefore

\[r=2\sqrt6.\]

So the largest possible radius is $2\sqrt6$."""),
        ],
    },
    "2015 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12A_Answer_Key",
        "answer": ("D", "$\\frac{143}{14}$"),
        "statement": r"""A collection of circles in the upper half-plane, all tangent to the $x$-axis, is constructed in layers as follows. Layer $L_0$ consists of two circles of radii $70^2$ and $73^2$ that are externally tangent. For $k\ge1$, the circles in $\bigcup_{j=0}^{k-1}L_j$ are ordered according to their points of tangency with the $x$-axis. For every pair of consecutive circles in this order, a new circle is constructed externally tangent to each of the two circles in the pair. Layer $L_k$ consists of the $2^{k-1}$ circles constructed in this way. Let $S=\bigcup_{j=0}^{6}L_j$, and for every circle $C$ denote by $r(C)$ its radius. What is

\[\sum_{C\in S}\frac{1}{\sqrt{r(C)}}?\]""",
        "choices": [
            ("A", "$\\frac{286}{35}$"),
            ("B", "$\\frac{583}{70}$"),
            ("C", "$\\frac{715}{73}$"),
            ("D", "$\\frac{143}{14}$"),
            ("E", "$\\frac{1573}{146}$"),
        ],
        "key_idea": "For circles tangent to the same line, the reciprocal square roots of the radii add when a new circle is inserted between two tangent circles.",
        "solution": [
            ("Find the key relation between three tangent circles",
             r"""Suppose two circles tangent to the $x$-axis have radii $x$ and $y$, and a new circle of radius $z$ is inserted between them, tangent to both and to the $x$-axis.

The horizontal distance between centers of tangent circles with radii $u$ and $v$ is

\[\sqrt{(u+v)^2-(u-v)^2}=2\sqrt{uv}.\]"""),
            ("Apply that distance relation",
             r"""For the new circle between the two older ones, the total horizontal distance satisfies

\[2\sqrt{xz}+2\sqrt{yz}=2\sqrt{xy}.\]

Divide by $2\sqrt{xyz}$:

\[\frac{1}{\sqrt{x}}+\frac{1}{\sqrt{y}}=\frac{1}{\sqrt{z}}.\]

So the quantity $1/\sqrt r$ behaves additively when a new circle is inserted."""),
            ("Translate the first layer into simple numbers",
             r"""The two starting radii are $70^2$ and $73^2$. Therefore their reciprocal square roots are

\[\frac1{70}\quad\text{and}\quad \frac1{73}.\]

Let

\[S_0=\frac1{70}+\frac1{73}.\]

The single circle in $L_1$ has reciprocal square root equal to the sum of these two, so $L_1$ also contributes $S_0$."""),
            ("See the layer pattern",
             r"""Each new layer is formed by inserting circles between consecutive existing circles. Because the new value equals the sum of its two neighbors, the total contribution of the layers grows by a factor of $3$ after $L_1$:

\[L_0:S_0,\qquad L_1:S_0,\qquad L_2:3S_0,\qquad L_3:9S_0,\]

and so on up to $L_6$."""),
            ("Add the seven layers",
             r"""Thus the requested total is

\[(1+1+3+9+27+81+243)S_0.\]

The coefficient is

\[1+1+3+9+27+81+243=365.\]"""),
            ("Finish the arithmetic",
             r"""Now

\[S_0=\frac1{70}+\frac1{73}=\frac{143}{70\cdot73}.\]

So the total is

\[365\cdot\frac{143}{70\cdot73}.\]

Since $365=5\cdot73$, this simplifies to

\[\frac{143}{14}.\]

Therefore the answer is $\frac{143}{14}$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
