import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 15"
base.BATCH_NUMBER = 299
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2022 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2022_AMC_12A_Answer_Key",
        "answer": ("E", "$17$"),
        "statement": r"""A circle with integer radius $r$ is centered at $(r,r)$. Distinct line segments of length $c_i$ connect points $(0,a_i)$ to $(b_i,0)$ for $1\le i\le14$ and are tangent to the circle, where $a_i$, $b_i$, and $c_i$ are all positive integers and $c_1\le c_2\le\cdots\le c_{14}$. What is the ratio $\frac{c_{14}}{c_1}$ for the least possible value of $r$?""",
        "choices": [
            ("A", "$\\frac{21}{5}$"),
            ("B", "$\\frac{85}{13}$"),
            ("C", "$7$"),
            ("D", "$\\frac{39}{5}$"),
            ("E", "$17$"),
        ],
        "key_idea": "Convert the tangent condition for an integer intercept segment into a divisor equation involving r.",
        "solution": [
            ("Turn each segment into a line equation",
             r"""The segment from $(0,a)$ to $(b,0)$ lies on the intercept-form line

\[ax+by=ab.\]

Its length is

\[c=\sqrt{a^2+b^2}.\]

Since the segment is tangent to the circle centered at $(r,r)$ with radius $r$, the distance from $(r,r)$ to this line must be $r$."""),
            ("Use the point-to-line distance formula",
             r"""The distance from $(r,r)$ to $ax+by=ab$ is

\[\frac{|ar+br-ab|}{\sqrt{a^2+b^2}}.\]

Because this distance equals $r$ and $\sqrt{a^2+b^2}=c$, we have

\[|r(a+b)-ab|=rc.\]

Squaring and using $c^2=a^2+b^2$ gives

\[(r(a+b)-ab)^2=r^2(a^2+b^2).\]"""),
            ("Simplify to a divisor equation",
             r"""Expanding the equation and simplifying gives

\[ab-2r(a+b)+2r^2=0.\]

This factors neatly as

\[(a-2r)(b-2r)=2r^2.\]

So for a fixed $r$, integer tangent segments correspond to integer factor pairs of $2r^2$."""),
            ("Find the smallest possible radius",
             r"""We need at least $14$ distinct ordered pairs $(a,b)$. Try small integer values of $r$.

For $r<6$, the number $2r^2$ has too few divisor pairs to produce $14$ valid positive pairs $(a,b)$. For example, when $r=5$, $2r^2=50$ has only $6$ positive divisors, and the negative-factor cases do not add enough positive intercepts.

For $r=6$,

\[2r^2=72=2^3\cdot3^2,\]

which has

\[(3+1)(2+1)=12\]

positive divisors, giving $12$ ordered positive-factor solutions."""),
            ("Account for the remaining two segments",
             r"""Negative factors can also work if both intercepts remain positive. With $r=6$, we have $2r=12$, and

\[(-8)(-9)=72.\]

These give

\[(a,b)=(12-8,12-9)=(4,3)\]

and the reversed pair $(3,4)$. Thus $r=6$ gives the required $14$ distinct segments, and no smaller radius does."""),
            ("Find the smallest and largest segment lengths",
             r"""For the negative pair $(a,b)=(3,4)$ or $(4,3)$, the segment length is

\[c_1=\sqrt{3^2+4^2}=5.\]

The largest segment comes from the most unequal positive factor pair of $72$, namely $(1,72)$ or $(72,1)$. This gives

\[(a,b)=(13,84)\quad\text{or}\quad(84,13),\]

so

\[c_{14}=\sqrt{13^2+84^2}=85.\]

Therefore

\[\frac{c_{14}}{c_1}=\frac{85}{5}=17.\]"""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
