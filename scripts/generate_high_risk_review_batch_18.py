import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 18"
base.BATCH_NUMBER = 302
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2019 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2019_AMC_12A_Answer_Key",
        "answer": ("E", "$15$"),
        "statement": r"""Let $\triangle A_0B_0C_0$ be a triangle whose angle measures are exactly $59.999^\circ$, $60^\circ$, and $60.001^\circ$. For each positive integer $n$, define $A_n$ to be the foot of the altitude from $A_{n-1}$ to line $B_{n-1}C_{n-1}$. Likewise, define $B_n$ to be the foot of the altitude from $B_{n-1}$ to line $A_{n-1}C_{n-1}$, and $C_n$ to be the foot of the altitude from $C_{n-1}$ to line $A_{n-1}B_{n-1}$. What is the least positive integer $n$ for which $\triangle A_nB_nC_n$ is obtuse?""",
        "choices": [("A", "$10$"), ("B", "$11$"), ("C", "$13$"), ("D", "$14$"), ("E", "$15$")],
        "key_idea": "The altitude-foot triangle transforms each angle x into 180 degrees minus 2x, so small deviations from 60 degrees double each step.",
        "solution": [
            ("Recognize the triangle being formed",
             r"""The points $A_n,B_n,C_n$ are the feet of the three altitudes of $\triangle A_{n-1}B_{n-1}C_{n-1}$. So $\triangle A_nB_nC_n$ is the orthic triangle of the previous triangle.

As long as the previous triangle is acute, the three feet lie on the sides, and the usual orthic-triangle angle relation applies."""),
            ("Find the angle transformation",
             r"""Suppose an acute triangle has an angle $x$ at one vertex. In its orthic triangle, the corresponding angle is

\[180^\circ-2x.\]

One way to see this is to use the two right angles created by the altitude feet. The relevant quadrilaterals are cyclic, and angle chasing gives two angles of size $90^\circ-x$, which add to $180^\circ-2x$."""),
            ("Measure angles by deviation from 60 degrees",
             r"""Write an angle as

\[60^\circ+d.\]

After one orthic-triangle step, it becomes

\[180^\circ-2(60^\circ+d)=60^\circ-2d.\]

So the deviation from $60^\circ$ is multiplied by $-2$ at each step."""),
            ("Track the initial deviations",
             r"""The original triangle has angle deviations

\[-0.001^\circ,\quad 0^\circ,\quad 0.001^\circ.\]

After $n$ steps, the deviations become

\[(-2)^n(-0.001^\circ),\quad 0^\circ,\quad (-2)^n(0.001^\circ).\]

Therefore the largest angle after $n$ steps is

\[60^\circ+0.001^\circ\cdot2^n.\]"""),
            ("Decide when the triangle first becomes obtuse",
             r"""The triangle becomes obtuse exactly when the largest angle is greater than $90^\circ$:

\[60^\circ+0.001^\circ\cdot2^n>90^\circ.\]

This simplifies to

\[2^n>30000.\]"""),
            ("Compare powers of 2",
             r"""Now

\[2^{14}=16384<30000,\]

but

\[2^{15}=32768>30000.\]

So the first time an angle becomes obtuse is at

\[n=15.\]

Therefore the answer is $15$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
