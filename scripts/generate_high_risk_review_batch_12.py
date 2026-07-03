import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 12"
base.BATCH_NUMBER = 296
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2011 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12A_Answer_Key",
        "answer": ("C", "$2320$"),
        "statement": r"""Let $R$ be a unit square region and $n\ge4$ an integer. A point $X$ in the interior of $R$ is called $n$-ray partitional if there are $n$ rays emanating from $X$ that divide $R$ into $n$ triangles of equal area. How many points are $100$-ray partitional but not $60$-ray partitional?""",
        "choices": [("A", "$1500$"), ("B", "$1560$"), ("C", "$2320$"), ("D", "$2480$"), ("E", "$2500$")],
        "key_idea": "Turn the equal-area ray condition into a grid condition inside the square.",
        "solution": [
            ("Translate the geometry into coordinates",
             r"""Use a unit square with corners $(0,0)$, $(1,0)$, $(1,1)$, and $(0,1)$. Let

\[X=(r,q),\qquad 0<r,q<1.\]

The four rays through the four vertices split the square into four larger triangular sectors. Their areas are proportional to

\[q,\quad 1-r,\quad 1-q,\quad r.\]"""),
            ("Represent how many small triangles lie in each sector",
             r"""If $X$ is $n$-ray partitional, the $n$ equal-area triangles must be grouped among those four sectors. Let the numbers of equal triangles in the four sectors be positive integers

\[a,b,c,d.\]

Then

\[a+b+c+d=n.\]

Equal area in each sector means

\[\frac{q}{a}=\frac{1-r}{b}=\frac{1-q}{c}=\frac{r}{d}.\]"""),
            ("Find the coordinate form of an n-ray point",
             r"""From

\[\frac{q}{a}=\frac{1-q}{c},\]

we get

\[q=\frac{a}{a+c}.\]

Similarly, from

\[\frac{1-r}{b}=\frac{r}{d},\]

we get

\[r=\frac{d}{b+d}.\]

The remaining equality forces $a+c=b+d$, so since $a+b+c+d=n$, each of these sums must be $\frac n2$."""),
            ("Count the 100-ray partitional points",
             r"""For $n=100$, we have

\[a+c=b+d=50.\]

Therefore

\[X=\left(\frac{d}{50},\frac{a}{50}\right),\]

where $a$ and $d$ can each be any integer from $1$ to $49$. So there are

\[49\cdot49=2401\]

$100$-ray partitional points."""),
            ("Subtract the points that are also 60-ray partitional",
             r"""For $n=60$, the same reasoning gives points of the form

\[\left(\frac{m}{30},\frac{\ell}{30}\right),\]

with $m,\ell$ from $1$ to $29$.

A $100$-ray point

\[\left(\frac{d}{50},\frac{a}{50}\right)\]

is also a $60$-ray point exactly when both coordinates can be written with denominator $30$. This requires $a$ and $d$ to be divisible by $5$."""),
            ("Finish the count",
             r"""Among the integers $1,2,\ldots,49$, exactly $9$ are divisible by $5$:

\[5,10,\ldots,45.\]

So the overlap has

\[9\cdot9=81\]

points. The number requested is

\[2401-81=2320.\]"""),
        ],
    },
    "2014 AMC 12B Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12B_Answer_Key",
        "answer": ("D", "$391$"),
        "statement": r"""Let $ABCDE$ be a pentagon inscribed in a circle such that $AB=CD=3$, $BC=DE=10$, and $AE=14$. The sum of the lengths of all diagonals of $ABCDE$ is equal to $\frac mn$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?""",
        "choices": [("A", "$129$"), ("B", "$247$"), ("C", "$353$"), ("D", "$391$"), ("E", "$421$")],
        "key_idea": "Use symmetry and Ptolemy's theorem on several cyclic quadrilaterals to solve for the diagonals.",
        "solution": [
            ("Name the diagonal lengths",
             r"""Because the side pattern is symmetric,

\[AB=CD=3,\qquad BC=DE=10,\qquad AE=14.\]

The corresponding diagonals satisfy

\[AC=BD=CE.\]

Let this common length be $x$. Let

\[BE=y,\qquad AD=z.\]"""),
            ("Use Ptolemy on quadrilateral ABCE",
             r"""In cyclic quadrilateral $ABCE$, Ptolemy's theorem gives

\[AB\cdot CE+BC\cdot AE=AC\cdot BE.\]

Substitute the known lengths:

\[3x+10\cdot14=xy.\]

So

\[xy=3x+140.\]"""),
            ("Use Ptolemy on quadrilateral BCDE",
             r"""In cyclic quadrilateral $BCDE$, Ptolemy's theorem gives

\[BC\cdot DE+CD\cdot BE=BD\cdot CE.\]

Therefore

\[10\cdot10+3y=x^2,\]

or

\[x^2=100+3y.\]"""),
            ("Solve for the common diagonal",
             r"""From $xy=3x+140$, we have

\[y=3+\frac{140}{x}.\]

Substitute this into $x^2=100+3y$:

\[x^2=100+3\left(3+\frac{140}{x}\right).\]

Multiplying by $x$ gives

\[x^3=109x+420,\]

or

\[x^3-109x-420=0.\]"""),
            ("Factor and find y",
             r"""The cubic factors as

\[(x-12)(x+7)(x+5)=0.\]

Since $x$ is a length, $x=12$. Then

\[y=3+\frac{140}{12}=3+\frac{35}{3}=\frac{44}{3}.\]"""),
            ("Find the remaining diagonal and sum",
             r"""Use Ptolemy on cyclic quadrilateral $ABDE$:

\[AB\cdot DE+AE\cdot BD=AD\cdot BE.\]

Thus

\[3\cdot10+14\cdot12=z\cdot\frac{44}{3}.\]

So

\[z=\frac{198}{44/3}=\frac{27}{2}.\]

The sum of all five diagonals is

\[3x+y+z=3\cdot12+\frac{44}{3}+\frac{27}{2}=\frac{385}{6}.\]

Therefore $m+n=385+6=391$."""),
        ],
    },
    "2023 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2023_AMC_12B_Answer_Key",
        "answer": ("B", "$\\sqrt5-1$"),
        "statement": r"""A regular pentagon with area $\sqrt5+1$ is printed on paper and cut out. The five vertices of the pentagon are folded into the center of the pentagon, creating a smaller pentagon. What is the area of the new pentagon?""",
        "choices": [
            ("A", "$4-\\sqrt5$"),
            ("B", "$\\sqrt5-1$"),
            ("C", "$8-3\\sqrt5$"),
            ("D", "$\\frac{\\sqrt5+1}{2}$"),
            ("E", "$\\frac{2+\sqrt5}{3}$"),
        ],
        "key_idea": "Each fold crease is a perpendicular bisector from a vertex to the center, so the new pentagon is similar to the original.",
        "solution": [
            ("Recognize what each fold line is",
             r"""Let $O$ be the center of the original regular pentagon, and let $A$ be one vertex. Folding $A$ to $O$ means the crease is the perpendicular bisector of $\overline{AO}$.

So the crease is perpendicular to $\overline{AO}$ and passes through the midpoint of $\overline{AO}$."""),
            ("Describe the smaller pentagon",
             r"""Doing this for all five vertices creates five congruent crease lines. By rotational symmetry, the region left in the middle is also a regular pentagon.

Thus the new pentagon is similar to the original pentagon. We only need the linear scale factor."""),
            ("Compare apothems",
             r"""Let $R$ be the circumradius of the original pentagon. The apothem of the original pentagon is

\[R\cos36^\circ.\]

Each crease line is halfway from $O$ to a vertex, so the apothem of the new pentagon is

\[\frac R2.\]"""),
            ("Find the scale factor",
             r"""Therefore the linear scale factor from the original pentagon to the new pentagon is

\[\frac{R/2}{R\cos36^\circ}=\frac{1}{2\cos36^\circ}.\]

For a regular pentagon,

\[\cos36^\circ=\frac{1+\sqrt5}{4}.\]

So the scale factor is

\[\frac{1}{2\cdot\frac{1+\sqrt5}{4}}=\frac{2}{1+\sqrt5}=\frac{\sqrt5-1}{2}.\]"""),
            ("Convert the linear scale to an area scale",
             r"""Areas scale by the square of the linear factor. Hence the new area is

\[(\sqrt5+1)\left(\frac{\sqrt5-1}{2}\right)^2.\]

Now

\[\left(\frac{\sqrt5-1}{2}\right)^2=\frac{3-\sqrt5}{2}.\]"""),
            ("Finish the computation",
             r"""Thus the area is

\[(\sqrt5+1)\cdot\frac{3-\sqrt5}{2}.\]

Multiplying,

\[\frac{3\sqrt5+3-5-\sqrt5}{2}=\frac{2\sqrt5-2}{2}=\sqrt5-1.\]

Therefore the answer is $\sqrt5-1$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
