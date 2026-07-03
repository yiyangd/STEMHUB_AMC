import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 10"
base.BATCH_NUMBER = 294
base.REVIEW_SKIPPED = [
    "2015 AMC 12B Problem 19: skipped because the local CSV statement does not match the AoPS statement."
]

base.PROBLEMS = {
    "2011 AMC 12B Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12B_Answer_Key",
        "answer": ("C", r"$\frac{195}{8}$"),
        "statement": r"""Triangle $ABC$ has $AB=13$, $BC=14$, and $AC=15$. The points $D$, $E$, and $F$ are the midpoints of $\overline{AB}$, $\overline{BC}$, and $\overline{AC}$ respectively. Let $X\ne E$ be the intersection of the circumcircles of $\triangle BDE$ and $\triangle CEF$. What is $XA+XB+XC$?""",
        "choices": [
            ("A", "$24$"),
            ("B", "$14\\sqrt3$"),
            ("C", "$\\frac{195}{8}$"),
            ("D", "$\\frac{129\\sqrt7}{14}$"),
            ("E", "$\\frac{69\\sqrt2}{4}$"),
        ],
        "key_idea": "Recognize the second intersection as the circumcenter of the original triangle, then compute the circumradius.",
        "solution": [
            ("Look for a point shared by both smaller circumcircles",
             r"""When two circles are defined using midpoints of a triangle, a good first question is whether the circumcenter of the original triangle appears naturally. Let $O$ be the circumcenter of $\triangle ABC$.

Since $D$ is the midpoint of $\overline{AB}$, the line $OD$ is the perpendicular bisector of $\overline{AB}$. Similarly, $OE$ is the perpendicular bisector of $\overline{BC}$."""),
            ("Show that O lies on the first small circle",
             r"""Because $OD\perp AB$, we have $\angle BDO=90^\circ$. Because $OE\perp BC$, we have $\angle BEO=90^\circ$.

Thus both $D$ and $E$ lie on the circle with diameter $\overline{BO}$. Therefore $B,D,E,O$ are concyclic, so $O$ lies on the circumcircle of $\triangle BDE$."""),
            ("Show that O lies on the second small circle",
             r"""The same reasoning works with $\overline{BC}$ and $\overline{AC}$. We have $OE\perp BC$ and $OF\perp AC$, so

\[\angle CEO=\angle CFO=90^\circ.\]

Therefore $C,E,F,O$ are concyclic, and $O$ also lies on the circumcircle of $\triangle CEF$."""),
            ("Identify X and reduce the problem",
             r"""The two given circles already share $E$. Their other intersection is $X$, and we have just found that $O$ is on both circles.

So $X=O$. This means

\[XA=XB=XC=R,\]

where $R$ is the circumradius of $\triangle ABC$."""),
            ("Compute the circumradius",
             r"""The triangle has side lengths $13$, $14$, and $15$. Its semiperimeter is

\[s=\frac{13+14+15}{2}=21.\]

By Heron's formula, its area is

\[K=\sqrt{21\cdot8\cdot7\cdot6}=84.\]

The circumradius formula gives

\[R=\frac{abc}{4K}=\frac{13\cdot14\cdot15}{4\cdot84}=\frac{65}{8}.\]"""),
            ("Finish the requested sum",
             r"""Since all three distances from $X$ to the vertices are equal to $R$,

\[XA+XB+XC=3R=3\cdot\frac{65}{8}=\frac{195}{8}.\]

Therefore the answer is $\frac{195}{8}$."""),
        ],
    },
    "2012 AMC 12B Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("D", "$18$"),
        "statement": r"""Define the function $f_1$ on the positive integers by setting $f_1(1)=1$ and if $n=p_1^{e_1}p_2^{e_2}\cdots p_k^{e_k}$ is the prime factorization of $n>1$, then

\[f_1(n)=(p_1+1)^{e_1-1}(p_2+1)^{e_2-1}\cdots(p_k+1)^{e_k-1}.\]

For every $m\ge2$, let $f_m(n)=f_1(f_{m-1}(n))$. For how many $N$ in the range $1\le N\le400$ is the sequence $(f_1(N),f_2(N),f_3(N),\ldots)$ unbounded?""",
        "choices": [("A", "$15$"), ("B", "$16$"), ("C", "$17$"), ("D", "$18$"), ("E", "$19$")],
        "key_idea": "Track which prime-power exponents can grow under repeated application of the function.",
        "solution": [
            ("Focus on exponents, not on the whole number",
             r"""The function removes first powers: if a prime appears to the first power, it contributes exponent $0$ and disappears. So only repeated prime factors can help create long-term growth.

The dangerous growth happens when repeated application creates larger and larger powers of $2$ or $3$, because

\[f_1(2^a)=3^{a-1},\qquad f_1(3^b)=4^{b-1}=2^{2b-2}.\]"""),
            ("Find when powers of 2 grow",
             r"""Start with $2^a$. Applying the function twice gives

\[f_2(2^a)=f_1(3^{a-1})=4^{a-2}=2^{2a-4}.\]

This exponent is larger than $a$ exactly when $2a-4>a$, or $a\ge5$. Therefore every multiple of $2^5=32$ in the range works.

There are

\[\left\lfloor\frac{400}{32}\right\rfloor=12\]

such numbers."""),
            ("Find when powers of 3 grow",
             r"""Now start with $3^b$. Applying the function twice gives

\[f_2(3^b)=f_1(4^{b-1})=f_1(2^{2b-2})=3^{2b-3}.\]

This exponent grows when $2b-3>b$, or $b\ge4$. Therefore every multiple of $3^4=81$ works.

There are

\[\left\lfloor\frac{400}{81}\right\rfloor=4\]

such numbers."""),
            ("Check the remaining possible squareful cores",
             r"""After removing primes that occur only once, any remaining candidate at most $400$ has a small squareful core. The only additional prime-power core that creates a growing power of $2$ is

\[7^3=343,\]

because

\[f_1(7^3)=8^2=2^6.\]

There is only one multiple of $343$ up to $400$."""),
            ("Catch the mixed exceptional case",
             r"""There is one more mixed core:

\[2^4\cdot5^2=400.\]

It works because

\[f_1(400)=f_1(2^4\cdot5^2)=3^3\cdot6=2\cdot3^4,\]

and then the $3^4$ part enters the growing case from Step 3."""),
            ("Add without double-counting",
             r"""The counted sets do not overlap within $1\le N\le400$: a common multiple of $32$ and $81$ is already larger than $400$, and $343$ and $400$ are separate exceptional values.

So the total number of $N$ is

\[12+4+1+1=18.\]

Therefore the answer is $18$."""),
        ],
    },
    "2015 AMC 12A Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12A_Answer_Key",
        "answer": ("D", "$\\sqrt{15}+8$"),
        "statement": r"""A circle of radius $r$ passes through both foci of, and exactly four points on, the ellipse with equation $x^2+16y^2=16$. The set of all possible values of $r$ is an interval $[a,b)$. What is $a+b$?""",
        "choices": [
            ("A", "$5\\sqrt2+4$"),
            ("B", "$\\sqrt{17}+7$"),
            ("C", "$6\\sqrt2+3$"),
            ("D", "$\\sqrt{15}+8$"),
            ("E", "$12$"),
        ],
        "key_idea": "Use the foci of the ellipse and bound the circle radius by when it becomes tangent at a vertex of the ellipse.",
        "solution": [
            ("Put the ellipse in standard form",
             r"""Rewrite the ellipse as

\[\frac{x^2}{16}+y^2=1.\]

So its semimajor axis is $4$ and its semiminor axis is $1$. The foci lie on the $x$-axis at

\[(\pm\sqrt{4^2-1^2},0)=(\pm\sqrt{15},0).\]"""),
            ("Describe all circles through the two foci",
             r"""A circle passing through both foci must have its center on the perpendicular bisector of the segment joining them. That perpendicular bisector is the $y$-axis.

So write the circle center as $(0,t)$. Its radius is

\[r=\sqrt{15+t^2}.\]"""),
            ("Find the smallest possible radius",
             r"""The smallest circle through the two foci occurs when the segment between the foci is a diameter. This corresponds to $t=0$.

Then

\[r=\sqrt{15}.\]

This circle still intersects the ellipse in four points, so $a=\sqrt{15}$."""),
            ("Find where the four-intersection condition stops",
             r"""As $|t|$ increases, the circle grows and moves upward or downward. The transition from four intersections to fewer intersections happens when the circle becomes tangent to one endpoint of the minor axis, either $(0,1)$ or $(0,-1)$.

Use $(0,1)$. At the boundary, its distance to the center $(0,t)$ equals the distance from the center to a focus:

\[|1-t|=\sqrt{15+t^2}.\]"""),
            ("Compute the upper endpoint",
             r"""Taking the relevant boundary with $t<1$, square both sides:

\[(1-t)^2=15+t^2.\]

This gives

\[1-2t+t^2=15+t^2,\]

so $t=-7$. The corresponding radius is

\[r=\sqrt{15+49}=8.\]"""),
            ("Use the interval notation",
             r"""At the boundary radius $8$, the circle is tangent, so the problem no longer has exactly four intersection points. Thus the possible radii form

\[[\sqrt{15},8).\]

Therefore

\[a+b=\sqrt{15}+8.\]"""),
        ],
    },
    "2015 AMC 12B Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12B_Answer_Key",
        "answer": ("D", "$192$"),
        "statement": r"""Four circles, no two of which are congruent, have centers at $A$, $B$, $C$, and $D$, and points $P$ and $Q$ lie on all four circles. The radius of circle $A$ is $\frac58$ times the radius of circle $B$, and the radius of circle $C$ is $\frac58$ times the radius of circle $D$. Furthermore, $AB=CD=39$ and $PQ=48$. Let $R$ be the midpoint of $\overline{PQ}$. What is $AR+BR+CR+DR$?""",
        "choices": [("A", "$180$"), ("B", "$184$"), ("C", "$188$"), ("D", "$192$"), ("E", "$196$")],
        "key_idea": "All centers lie on the perpendicular bisector of the common chord, so the problem becomes one-dimensional.",
        "solution": [
            ("Use the common chord",
             r"""Every circle passes through $P$ and $Q$. Therefore each center lies on the perpendicular bisector of $\overline{PQ}$.

Since $R$ is the midpoint of $\overline{PQ}$ and $PQ=48$, each radius satisfies

\[r^2=(\text{distance from center to }R)^2+24^2.\]

So the problem reduces to distances along one line."""),
            ("Analyze one pair of circles",
             r"""Consider a pair whose center distance is $39$ and whose radii are in the ratio $5:8$. Let the larger-radius center be distance $x$ from $R$, and let the smaller-radius center be distance $y$ from $R$.

Then

\[y^2+24^2=\frac{25}{64}(x^2+24^2).\]"""),
            ("Solve the same-side case",
             r"""If the two centers are on the same side of $R$, then their distance apart is

\[x-y=39.\]

Substituting $x=y+39$ into the radius equation gives

\[y^2+576=\frac{25}{64}\big((y+39)^2+576\big).\]

This simplifies to

\[y^2-50y-399=0,\]

so the positive solution is $y=57$, and then $x=96$."""),
            ("Understand the opposite-side case",
             r"""If the two centers are on opposite sides of $R$, then the sum of their distances from $R$ is simply the distance between the centers:

\[x+y=39.\]

For such a pair, the contribution to the requested sum is therefore $39$."""),
            ("Use the noncongruent condition",
             r"""There are two pairs, $(A,B)$ and $(C,D)$, and no two circles may be congruent. If both pairs used the same configuration, the resulting distances from $R$ would repeat and the corresponding radii would repeat.

Thus one pair must contribute the same-side distances $57$ and $96$, while the other pair contributes $39$ in total."""),
            ("Finish the sum",
             r"""Therefore

\[AR+BR+CR+DR=57+96+39=192.\]

So the answer is $192$."""),
        ],
    },
    "2020 AMC 12A Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12A_Answer_Key",
        "answer": ("B", "$\\sqrt7$"),
        "statement": r"""Suppose that $\triangle ABC$ is an equilateral triangle of side length $s$, with the property that there is a unique point $P$ inside the triangle such that $AP=1$, $BP=\sqrt3$, and $CP=2$. What is $s$?""",
        "choices": [
            ("A", "$1+\\sqrt2$"),
            ("B", "$\\sqrt7$"),
            ("C", "$\\frac83$"),
            ("D", "$\\sqrt{5+\\sqrt5}$"),
            ("E", "$2\\sqrt2$"),
        ],
        "key_idea": "Rotate one segment by 60 degrees to create a 30-60-90 triangle and reveal the angle at P.",
        "solution": [
            ("Use the equilateral structure",
             r"""Because $\triangle ABC$ is equilateral, a $60^\circ$ rotation is natural. The goal is to learn the angle between $\overline{AP}$ and $\overline{CP}$, because then $\triangle APC$ contains the side $AC=s$."""),
            ("Rotate point P around A",
             r"""Rotate $P$ by $60^\circ$ about $A$ to a point $Q$, in the direction that sends $B$ toward $C$.

Then

\[AQ=AP=1,\qquad PQ=1,\]

because $\triangle APQ$ is equilateral. Also the rotation sends $\overline{BP}$ to a segment from $C$ to $Q$, so

\[CQ=BP=\sqrt3.\]"""),
            ("Identify a simple triangle",
             r"""Now look at $\triangle PCQ$. Its side lengths are

\[CP=2,\qquad CQ=\sqrt3,\qquad PQ=1.\]

These are the side lengths of a $30^\circ$-$60^\circ$-$90^\circ$ triangle. In particular, the angle opposite the side $\sqrt3$ is $60^\circ$, so

\[\angle CPQ=60^\circ.\]"""),
            ("Find the angle APC",
             r"""Since $\triangle APQ$ is equilateral,

\[\angle APQ=60^\circ.\]

The point $Q$ is created on the other side of $\overline{AP}$ from $C$ in the useful configuration, so the angle between $\overline{AP}$ and $\overline{CP}$ is

\[\angle APC=60^\circ+60^\circ=120^\circ.\]"""),
            ("Apply the Law of Cosines",
             r"""Now use $\triangle APC$, where $AP=1$, $CP=2$, and $\angle APC=120^\circ$. The side opposite this angle is $AC=s$.

\[s^2=1^2+2^2-2\cdot1\cdot2\cos120^\circ.\]

Since $\cos120^\circ=-\frac12$,

\[s^2=1+4+2=7.\]"""),
            ("Choose the positive side length",
             r"""A side length is positive, so

\[s=\sqrt7.\]

Therefore the answer is $\sqrt7$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
