import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 7"
base.BATCH_NUMBER = 291
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2011 AMC 12B Problem 16": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12B_Answer_Key",
        "answer": ("C", "$\\frac{2\\sqrt3}{3}$"),
        "statement": r"""Rhombus $ABCD$ has side length $2$ and $\angle B=120^\circ$. Region $R$ consists of all points inside the rhombus that are closer to vertex $B$ than any of the other three vertices. What is the area of $R$?""",
        "choices": [
            ("A", "$\\frac{\\sqrt3}{3}$"),
            ("B", "$\\frac{\\sqrt3}{2}$"),
            ("C", "$\\frac{2\\sqrt3}{3}$"),
            ("D", "$1+\\frac{\\sqrt3}{3}$"),
            ("E", "$2$"),
        ],
        "key_idea": "Use perpendicular bisectors: points closer to B than another vertex lie on B's side of that vertex's perpendicular bisector.",
        "solution": [
            ("Put the rhombus in coordinates",
             r"""Let

\[B=(0,0),\quad A=(2,0),\quad C=(-1,\sqrt3),\quad D=(1,\sqrt3).\]

This gives side length $2$ and angle $120^\circ$ at $B$. Coordinates let us replace the distance comparisons with linear inequalities."""),
            ("Write the closer-to-B inequalities",
             r"""Being closer to $B$ than to $A$ means the point is on $B$'s side of the perpendicular bisector of $\overline{BA}$, so

\[x\le1.\]

Similarly, comparing with $C$ and $D$ gives

\[y\le \frac{x+2}{\sqrt3},\qquad y\le\frac{2-x}{\sqrt3}.\]"""),
            ("Find the polygon for region R",
             r"""Intersecting these three half-planes with the rhombus gives a pentagon with vertices

\[(0,0),\quad (1,0),\quad \left(1,\frac1{\sqrt3}\right),\quad \left(0,\frac2{\sqrt3}\right),\quad \left(-\frac12,\frac{\sqrt3}{2}\right).\]

These are exactly the points inside the rhombus that remain on $B$'s side of all three perpendicular bisectors."""),
            ("Compute the area",
             r"""Using the shoelace formula on these five vertices gives

\[\text{Area}(R)=\frac{2\sqrt3}{3}.\]

This is the desired region because every boundary line came from an equal-distance condition."""),
            ("Choose the answer",
             r"""Therefore the area of $R$ is

\[\boxed{\frac{2\sqrt3}{3}}.\]"""),
        ],
    },
    "2012 AMC 12B Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("A", "$\\frac{3\\sqrt2}{4}$"),
        "statement": r"""A unit cube has vertices $P_1,P_2,P_3,P_4,P_1',P_2',P_3',$ and $P_4'$. Vertices $P_2,P_3,$ and $P_4$ are adjacent to $P_1$, and for $1\le i\le4$, vertices $P_i$ and $P_i'$ are opposite to each other. A regular octahedron has one vertex in each of the segments $P_1P_2$, $P_1P_3$, $P_1P_4$, $P_1'P_2'$, $P_1'P_3'$, and $P_1'P_4'$. What is the octahedron's side length?""",
        "choices": [
            ("A", "$\\frac{3\\sqrt2}{4}$"),
            ("B", "$\\frac{7\\sqrt6}{16}$"),
            ("C", "$\\frac{\\sqrt5}{2}$"),
            ("D", "$\\frac{2\\sqrt3}{3}$"),
            ("E", "$\\frac{\\sqrt6}{2}$"),
        ],
        "key_idea": "Place the cube in coordinates and force the candidate octahedron edges to be equal.",
        "solution": [
            ("Choose symmetric coordinates",
             r"""Place $P_1=(0,0,0)$ and let the three adjacent vertices be on the coordinate axes. By symmetry, the three octahedron vertices near $P_1$ can be written as

\[(t,0,0),\quad (0,t,0),\quad (0,0,t).\]

The three opposite vertices are then

\[(1-t,1,1),\quad (1,1-t,1),\quad (1,1,1-t).\]"""),
            ("Compute one edge among the lower three vertices",
             r"""The distance between $(t,0,0)$ and $(0,t,0)$ is

\[\sqrt{t^2+t^2}=t\sqrt2.\]

This must be the side length of the regular octahedron."""),
            ("Compute a connecting edge",
             r"""A connecting edge, for example from $(t,0,0)$ to $(1,1-t,1)$, has squared length

\[(1-t)^2+(1-t)^2+1=2t^2-4t+3.\]

This must also equal the square of the side length, $2t^2$."""),
            ("Solve for t",
             r"""So

\[2t^2-4t+3=2t^2,\]

which gives

\[t=\frac34.\]"""),
            ("Find the side length",
             r"""The side length is

\[t\sqrt2=\frac34\sqrt2=\frac{3\sqrt2}{4}.\]

So the answer is $\frac{3\sqrt2}{4}$."""),
        ],
    },
    "2013 AMC 12A Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2013_AMC_12A_Answer_Key",
        "answer": ("E", "$\\frac{223}{286}$"),
        "statement": r"""Three distinct segments are chosen at random among the segments whose endpoints are the vertices of a regular $12$-gon. What is the probability that the lengths of these three segments are the three side lengths of a triangle with positive area?""",
        "choices": [
            ("A", "$\\frac{553}{715}$"),
            ("B", "$\\frac{443}{572}$"),
            ("C", "$\\frac{111}{143}$"),
            ("D", "$\\frac{81}{104}$"),
            ("E", "$\\frac{223}{286}$"),
        ],
        "key_idea": "Classify segments by length type, then count the triples that fail the triangle inequality.",
        "solution": [
            ("Classify the possible segment lengths",
             r"""In a regular $12$-gon, a segment can skip $k$ steps around the polygon, where $k=1,2,\ldots,6$. Let these lengths be

\[a_k=2\sin\left(\frac{k\pi}{12}\right).\]

For $k=1,2,3,4,5$, there are $12$ segments of length $a_k$. For $k=6$, there are $6$ diameters."""),
            ("Count all possible choices",
             r"""There are

\[\binom{12}{2}=66\]

segments total, so the number of ways to choose three distinct segments is

\[\binom{66}{3}=45760.\]"""),
            ("List the length-type triples that fail",
             r"""A triangle fails exactly when the two shorter lengths do not sum to more than the longest length. Checking the six length types gives these failing triples:

\[(1,1,3),(1,1,4),(1,1,5),(1,1,6),\]
\[(1,2,4),(1,2,5),(1,2,6),\]
\[(1,3,5),(1,3,6),(2,2,6).\]

Here $(1,2,4)$ means lengths $a_1,a_2,a_4$."""),
            ("Count the failing choices",
             r"""Weight each type by the number of actual segments of that type. Since types $1$ through $5$ each have $12$ segments and type $6$ has $6$, the failing triples contribute

\[10080\]

choices. This is a finite table count, not an estimate."""),
            ("Subtract from all choices",
             r"""Thus the number of successful triples is

\[45760-10080=35680.\]

The probability is

\[\frac{35680}{45760}=\frac{223}{286}.\]

So the answer is $\frac{223}{286}$."""),
        ],
    },
    "2018 AMC 12B Problem 16": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2018_AMC_12B_Answer_Key",
        "answer": ("B", "$\\frac{3\\sqrt2}{2}-\\frac32$"),
        "statement": r"""The solutions to the equation $(z+6)^8=81$ are connected in the complex plane to form a convex regular polygon, three of whose vertices are labeled $A,B,$ and $C$. What is the least possible area of $\triangle ABC$?""",
        "choices": [
            ("A", "$\\frac{\\sqrt6}{6}$"),
            ("B", "$\\frac{3\\sqrt2}{2}-\\frac32$"),
            ("C", "$2\\sqrt3-3\\sqrt2$"),
            ("D", "$\\frac{\\sqrt2}{2}$"),
            ("E", "$\\sqrt3-1$"),
        ],
        "key_idea": "The roots form a regular octagon; the least nonzero triangle uses three consecutive vertices.",
        "solution": [
            ("Identify the polygon",
             r"""The equation can be written as

\[(z+6)^8=81=3^4.\]

Thus the eight solutions for $z+6$ have magnitude

\[81^{1/8}=\sqrt3.\]

So the solutions form a regular octagon of radius $\sqrt3$, translated left by $6$. Translation does not change area."""),
            ("Choose the smallest triangle",
             r"""Among triangles formed by vertices of a regular octagon, the smallest nonzero area comes from three consecutive vertices. Any wider spacing increases either the base or the height."""),
            ("Use convenient consecutive vertices",
             r"""Take the vertices at angles $45^\circ$, $90^\circ$, and $135^\circ$. Their coordinates are

\[\left(\frac{\sqrt6}{2},\frac{\sqrt6}{2}\right),\quad (0,\sqrt3),\quad \left(-\frac{\sqrt6}{2},\frac{\sqrt6}{2}\right).\]"""),
            ("Compute base and height",
             r"""The base between the two lower points has length $\sqrt6$. The height from the middle point to that base is

\[\sqrt3-\frac{\sqrt6}{2}.\]

Therefore the area is

\[\frac12\sqrt6\left(\sqrt3-\frac{\sqrt6}{2}\right).\]"""),
            ("Simplify",
             r"""This becomes

\[\frac{3\sqrt2}{2}-\frac32.\]

So the least possible area is $\frac{3\sqrt2}{2}-\frac32$."""),
        ],
    },
    "2021 Spring AMC 12A Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("B", "$\\frac{40}{3}$"),
        "statement": r"""Suppose that on a parabola with vertex $V$ and focus $F$ there exists a point $A$ such that $AF=20$ and $AV=21$. What is the sum of all possible values of the length $FV$?""",
        "choices": [("A", "$13$"), ("B", "$\\frac{40}{3}$"), ("C", "$\\frac{41}{3}$"), ("D", "$14$"), ("E", "$\\frac{43}{3}$")],
        "key_idea": "Use the standard parabola model with vertex at the origin and focus distance d.",
        "solution": [
            ("Set up a standard parabola",
             r"""Put the vertex at the origin and the focus at $(0,d)$, where $d=FV$. Then the parabola has equation

\[x^2=4dy.\]"""),
            ("Use the distance to the directrix",
             r"""The directrix is the line $y=-d$. If $A=(u,v)$ is on the parabola, then its distance to the focus equals its distance to the directrix. Since $AF=20$,

\[v+d=20,\]

so

\[v=20-d.\]"""),
            ("Use the distance to the vertex",
             r"""The condition $AV=21$ gives

\[u^2+v^2=441.\]

Because $A$ is on the parabola, $u^2=4dv$. Substitute $v=20-d$:

\[4d(20-d)+(20-d)^2=441.\]"""),
            ("Solve for d",
             r"""Simplifying gives

\[3d^2-40d+41=0.\]

This quadratic has two positive roots, and both correspond to possible configurations of the point $A$."""),
            ("Use the sum of roots",
             r"""The sum of the two possible values of $d$ is

\[\frac{40}{3}\]

by Vieta's formula. Therefore the requested sum is $\frac{40}{3}$."""),
        ],
    },
    "2021 Spring AMC 12B Problem 14": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("A", "$24\\sqrt5$"),
        "statement": r"""Let $ABCD$ be a rectangle and let $\overline{DM}$ be a segment perpendicular to the plane of $ABCD$. Suppose that $\overline{DM}$ has integer length, and the lengths of $\overline{MA},\overline{MC},$ and $\overline{MB}$ are consecutive odd positive integers, in this order. What is the volume of pyramid $MABCD$?""",
        "choices": [("A", "$24\\sqrt5$"), ("B", "$60$"), ("C", "$28\\sqrt5$"), ("D", "$66$"), ("E", "$8\\sqrt{70}$")],
        "key_idea": "Use 3D coordinates from the perpendicular height and the rectangle side lengths.",
        "solution": [
            ("Assign coordinates",
             r"""Let $D=(0,0,0)$ and $M=(0,0,h)$, where $h=DM$ is an integer. Let

\[A=(a,0,0),\quad C=(0,b,0),\quad B=(a,b,0).\]"""),
            ("Translate the three distances",
             r"""Suppose

\[MA=k,\quad MC=k+2,\quad MB=k+4,\]

where $k$ is an odd positive integer. Then

\[
a^2+h^2=k^2,\quad b^2+h^2=(k+2)^2,\quad a^2+b^2+h^2=(k+4)^2.
\]"""),
            ("Eliminate a and b",
             r"""From the first two equations,

\[a^2=k^2-h^2,\qquad b^2=(k+2)^2-h^2.\]

Substitute these into the third equation:

\[k^2+(k+2)^2-h^2=(k+4)^2.\]"""),
            ("Find the integer height",
             r"""Simplifying gives

\[h^2=8k-12.\]

Trying odd positive $k$ with integer $h$ gives $k=7$ and $h=3$. Then

\[a^2=49-9=40,\qquad b^2=81-9=72.\]"""),
            ("Compute the volume",
             r"""The base area of rectangle $ABCD$ is

\[ab=\sqrt{40\cdot72}=24\sqrt5.\]

The pyramid volume is

\[\frac13\cdot h\cdot ab=\frac13\cdot3\cdot24\sqrt5=24\sqrt5.\]"""),
        ],
    },
    "2023 AMC 12B Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2023_AMC_12B_Answer_Key",
        "answer": ("E", "$6\\sqrt3+\\pi$"),
        "statement": r"""A lampshade is made in the form of the lateral surface of the frustum of a right circular cone. The height of the frustum is $3\sqrt3$ inches, its top diameter is $6$ inches, and its bottom diameter is $12$ inches. A bug is at the bottom of the lampshade, and there is a glob of honey on the top edge of the lampshade at the spot farthest from the bug. The bug wants to crawl to the honey, but it must stay on the surface of the lampshade. What is the length in inches of its shortest path to the honey?""",
        "choices": [("A", "$6+3\\pi$"), ("B", "$6+6\\pi$"), ("C", "$6\\sqrt3$"), ("D", "$6\\sqrt5$"), ("E", "$6\\sqrt3+\\pi$")],
        "key_idea": "Unroll the frustum as an annular sector; the shortest path must be tangent to the removed inner circle.",
        "solution": [
            ("Find the slant lengths of the full cone",
             r"""The bottom radius is $6$, the top radius is $3$, and the vertical height between them is $3\sqrt3$. The frustum's slant height is

\[\sqrt{3^2+(3\sqrt3)^2}=6.\]

By similarity, the slant distance from the cone apex to the top circle is $6$, and to the bottom circle is $12$."""),
            ("Unroll the cone",
             r"""When the cone is unrolled, the lateral surface becomes a sector. The outer radius is $12$, and the outer arc length is the bottom circumference $12\pi$. Therefore the sector angle is

\[\frac{12\pi}{12}=\pi.\]"""),
            ("Locate the two points in the sector",
             r"""The honey is opposite the bug around the circular frustum. A half-turn around the original cone becomes half of the sector angle, so the angular separation in the unrolled picture is

\[\frac{\pi}{2}.\]

Thus the bug is at radius $12$, and the honey is on the inner circle of radius $6$, separated by angle $\frac\pi2$."""),
            ("Notice why the straight line is not allowed",
             r"""The straight segment between these two points would pass inside the removed inner disk of radius $6$. That part of the cone is not part of the frustum, so the valid shortest path must touch the inner circle tangentially and then follow the inner circle to the honey."""),
            ("Compute tangent plus arc",
             r"""From the outer point at radius $12$, the tangent length to the inner circle of radius $6$ is

\[\sqrt{12^2-6^2}=6\sqrt3.\]

The tangent point is $60^\circ$ from the bug's radius, while the honey is $90^\circ$ away, leaving an arc angle of $30^\circ=\frac\pi6$. The arc length is

\[6\cdot\frac\pi6=\pi.\]"""),
            ("Add the two pieces",
             r"""Therefore the shortest surface path has length

\[6\sqrt3+\pi.\]

So the answer is $6\sqrt3+\pi$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
