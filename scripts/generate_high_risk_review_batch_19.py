import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 19"
base.BATCH_NUMBER = 303
base.REVIEW_SKIPPED = [
    "2015 AMC 12B Problem 19: skipped because the local CSV statement still does not match the AoPS statement."
]

base.PROBLEMS = {
    "2012 AMC 12B Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("A", "$29\\sqrt3$"),
        "statement": r"""Square $AXYZ$ is inscribed in equiangular hexagon $ABCDEF$ with $X$ on $\overline{BC}$, $Y$ on $\overline{DE}$, and $Z$ on $\overline{EF}$. Suppose that $AB=40$, and $EF=41(\sqrt3-1)$. What is the side length of the square?""",
        "choices": [
            ("A", "$29\\sqrt3$"),
            ("B", "$\\frac{21}{2}\\sqrt2+\\frac{41}{2}\\sqrt3$"),
            ("C", "$20\\sqrt3+16$"),
            ("D", "$20\\sqrt2+13\\sqrt3$"),
            ("E", "$21\\sqrt6$"),
        ],
        "key_idea": "Use the 60-degree directions of an equiangular hexagon and the square's perpendicular sides to turn the diagram into length equations.",
        "solution": [
            ("Use the parallel directions in an equiangular hexagon",
             r"""An equiangular hexagon has exterior turns of $60^\circ$. Therefore

\[AB\parallel DE,\qquad BC\parallel EF,\qquad CD\parallel FA.\]

Since $Y$ lies on $\overline{DE}$, we have $YE\parallel AB$. Since $X$ lies on $\overline{BC}$ and $Z$ lies on $\overline{EF}$, we have $BX\parallel EZ$."""),
            ("Find one side length attached to Y",
             r"""Because $AXYZ$ is a square,

\[AX\parallel YZ,\qquad AX=YZ.\]

Using the parallel pairs

\[AB\parallel YE,\quad BX\parallel EZ,\quad AX\parallel YZ,\]

triangles $\triangle ABX$ and $\triangle YEZ$ have the same angles, and the corresponding square sides $AX$ and $YZ$ are equal. Thus the triangles are congruent.

So

\[YE=AB=40.\]"""),
            ("Introduce the remaining outside length",
             r"""Extend the lines $AF$ and $DE$ until they meet at a point $G$. Because the hexagon is equiangular, triangle $EFG$ is equilateral.

Hence

\[EG=FG=EF=41(\sqrt3-1).\]

Let

\[AF=t.\]"""),
            ("Use projections onto EF",
             r"""The lines $AF$ and $YE$ each make a $60^\circ$ angle with $EF$. Projecting the square geometry onto the line $EF$ gives

\[\frac{\sqrt3}{2}(AF+YE)=EF+\frac12(AF+YE).\]

This equation is just the statement that the total perpendicular-to-$EF$ contribution from the two slanted outer pieces matches the same square side, while their horizontal half-components and the gap $EF$ fill the direction along $EF$."""),
            ("Solve for AF",
             r"""Substitute $YE=40$ and $EF=41(\sqrt3-1)$:

\[\frac{\sqrt3}{2}(t+40)=41(\sqrt3-1)+\frac12(t+40).\]

Move the half-term to the left:

\[\frac{\sqrt3-1}{2}(t+40)=41(\sqrt3-1).\]

Thus

\[t+40=82,\qquad t=42.\]"""),
            ("Use triangle AGY to find the square side",
             r"""Now

\[AG=AF+FG=42+41(\sqrt3-1)=41\sqrt3+1,\]

and

\[YG=YE+EG=40+41(\sqrt3-1)=41\sqrt3-1.\]

The angle $\angle AGY$ is $60^\circ$, so by the Law of Cosines,

\[AY^2=(41\sqrt3+1)^2+(41\sqrt3-1)^2-(41\sqrt3+1)(41\sqrt3-1).\]"""),
            ("Convert the diagonal to the side of the square",
             r"""Simplifying the expression gives

\[AY^2=5046.\]

But $AY$ is a diagonal of the square, so if the side length is $s$, then

\[AY=s\sqrt2.\]

Therefore

\[2s^2=5046,\qquad s^2=2523=29^2\cdot3.\]

So

\[s=29\sqrt3.\]

The side length of the square is $29\sqrt3$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
