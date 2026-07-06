import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 16"
base.BATCH_NUMBER = 300
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2012 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("B", r"$\frac{625}{144}$"),
        "statement": r"""Let

\[S=\{(x,y):x\in\{0,1,2,3,4\},\ y\in\{0,1,2,3,4,5\},\ (x,y)\ne(0,0)\}.\]

Let $T$ be the set of all right triangles whose vertices are in $S$. For every right triangle $t=\triangle ABC$ with vertices $A$, $B$, and $C$ in counter-clockwise order and right angle at $A$, let

\[f(t)=\tan(\angle CBA).\]

What is

\[\prod_{t\in T} f(t)?\]""",
        "choices": [
            ("A", "$1$"),
            ("B", "$\\frac{625}{144}$"),
            ("C", "$\\frac{125}{24}$"),
            ("D", "$6$"),
            ("E", "$\\frac{625}{24}$"),
        ],
        "key_idea": "Pair most triangles by reflections so their tangent factors multiply to 1, then enumerate the few unpaired boundary cases.",
        "solution": [
            ("Look for cancellation instead of listing every triangle",
             r"""There are many right triangles in the grid, so direct enumeration would be painful. The product suggests pairing triangles whose tangent factors are reciprocals.

For a right triangle with right angle at $A$,

\[\tan(\angle CBA)=\frac{AC}{AB}.\]

If a symmetry swaps the two legs from $A$, then the new tangent is the reciprocal, and the two factors multiply to $1$."""),
            ("Use reflection across the horizontal middle line",
             r"""Reflect the grid across the line

\[y=\frac52.\]

This maps the rectangle of grid points to itself, except that the excluded point $(0,0)$ would pair with $(0,5)$. Therefore every right triangle not involving $(0,5)$ can be paired with a reflected triangle, and each pair contributes product $1$."""),
            ("Use a second reflection for triangles involving (0,5)",
             r"""Now focus only on triangles that do involve $(0,5)$. Reflect across the line

\[x+y=5.\]

This line fixes $(0,5)$. Most of the remaining triangles again pair off with reciprocal tangent values. The only ones that fail to pair are those that also have a vertex on the bottom edge $y=0$."""),
            ("Enumerate the remaining boundary triangles",
             r"""After the two reflection cancellations, the only factors left come from a short list of boundary triangles with $B=(0,5)$ and one vertex on $y=0$.

The nontrivial tangent values are

\[5,\quad \frac52,\quad \frac53,\quad \frac54,\quad \frac23,\quad \frac14.\]

There are also two remaining triangles with tangent value $1$, so they do not change the product."""),
            ("Compute the product of the remaining factors",
             r"""Thus the full product over all right triangles equals

\[5\cdot\frac52\cdot\frac53\cdot\frac54\cdot\frac23\cdot\frac14.\]

Multiplying the numerator and denominator gives

\[\frac{5^4\cdot2}{2\cdot3\cdot4\cdot3\cdot4}
=\frac{625}{144}.\]"""),
            ("Finish",
             r"""All other triangles were paired by reflections and contributed $1$, so the complete product is

\[\frac{625}{144}.\]

Therefore the answer is $\frac{625}{144}$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
