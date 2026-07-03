import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 11"
base.BATCH_NUMBER = 295
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2010 AMC 12B Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2010_AMC_12B_Answer_Key",
        "answer": ("D", r"$\sqrt{\frac{425}{2}}$"),
        "statement": r"""Let $ABCD$ be a cyclic quadrilateral. The side lengths of $ABCD$ are distinct integers less than $15$ such that $BC\cdot CD=AB\cdot DA$. What is the largest possible value of $BD$?""",
        "choices": [
            ("A", "$\\sqrt{\\frac{325}{2}}$"),
            ("B", "$\\sqrt{185}$"),
            ("C", "$\\sqrt{\\frac{389}{2}}$"),
            ("D", "$\\sqrt{\\frac{425}{2}}$"),
            ("E", "$\\sqrt{\\frac{533}{2}}$"),
        ],
        "key_idea": "Use supplementary angles in a cyclic quadrilateral to express the diagonal in terms of the four sides.",
        "solution": [
            ("Name the sides and use the cyclic condition",
             r"""Let

\[AB=a,\quad BC=b,\quad CD=c,\quad DA=d.\]

The condition in the problem is

\[bc=ad.\]

Because $ABCD$ is cyclic, opposite angles are supplementary, so

\[\cos\angle BAD=-\cos\angle BCD.\]"""),
            ("Apply the Law of Cosines in two triangles",
             r"""Use diagonal $\overline{BD}$ to split the quadrilateral into $\triangle ABD$ and $\triangle BCD$.

In $\triangle ABD$,

\[BD^2=a^2+d^2-2ad\cos\angle BAD.\]

In $\triangle BCD$,

\[BD^2=b^2+c^2-2bc\cos\angle BCD.\]"""),
            ("Add the two equations",
             r"""Since $ad=bc$ and the cosines have opposite signs, the cosine terms cancel when the two equations are added.

Thus

\[2BD^2=a^2+b^2+c^2+d^2.\]

So maximizing $BD$ is the same as maximizing the sum of the squares of the four side lengths, subject to $ad=bc$ and the sides being distinct integers less than $15$."""),
            ("Do an organized factor check",
             r"""The largest side should be included if possible, so test side length $14$. With $a=14$, the equation becomes

\[14d=bc.\]

The largest valid distinct factor choice under $15$ is

\[d=6,\qquad b=7,\qquad c=12,\]

because $14\cdot6=7\cdot12=84$. A finite check of the other factor pairs with side lengths below $15$ gives a smaller square-sum."""),
            ("Compute the diagonal",
             r"""For the side lengths $14,7,12,6$ in cyclic order satisfying the product condition,

\[2BD^2=14^2+7^2+12^2+6^2.\]

Therefore

\[2BD^2=196+49+144+36=425.\]

So

\[BD^2=\frac{425}{2}.\]"""),
            ("Finish",
             r"""The largest possible value of the diagonal is

\[BD=\sqrt{\frac{425}{2}}.\]

Therefore the answer is $\sqrt{\frac{425}{2}}$."""),
        ],
    },
    "2012 AMC 12B Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("D", "$63$"),
        "statement": r"""A trapezoid has side lengths $3$, $5$, $7$, and $11$. The sum of all the possible areas of the trapezoid can be written in the form $r_1\sqrt{n_1}+r_2\sqrt{n_2}+r_3$, where $r_1$, $r_2$, and $r_3$ are rational numbers and $n_1$ and $n_2$ are positive integers not divisible by the square of a prime. What is the greatest integer less than or equal to $r_1+r_2+r_3+n_1+n_2$?""",
        "choices": [("A", "$57$"), ("B", "$59$"), ("C", "$61$"), ("D", "$63$"), ("E", "$65$")],
        "key_idea": "Treat each possible pair of bases separately; the difference of the bases and the two legs form a triangle that determines the height.",
        "solution": [
            ("Decide which side lengths can be bases",
             r"""In a trapezoid, if the bases have lengths $B$ and $b$ with $B>b$, then the horizontal offset between the legs has total length $B-b$.

The two non-base sides, together with this offset $B-b$, must form a triangle. Checking the possible base pairs, the only valid pairs are

\[(11,3),\qquad (11,5),\qquad (11,7).\]"""),
            ("Use a triangle to find the height",
             r"""For each valid base pair, the two legs and the base difference determine a triangle. The height of that triangle is exactly the height of the trapezoid.

If that triangle has area $K$ and the base difference is $d$, then

\[K=\frac12dh,\]

so

\[h=\frac{2K}{d}.\]"""),
            ("Compute the area when the bases are 11 and 3",
             r"""Here the base difference is $8$, and the legs are $5$ and $7$. The triangle with sides $5,7,8$ has area

\[K=\sqrt{10\cdot5\cdot3\cdot2}=10\sqrt3.\]

Thus

\[h=\frac{2K}{8}=\frac{5\sqrt3}{2}.\]

The trapezoid area is

\[\frac12(11+3)h=\frac{35\sqrt3}{2}.\]"""),
            ("Compute the area when the bases are 11 and 5",
             r"""Here the base difference is $6$, and the legs are $3$ and $7$. The triangle with sides $3,6,7$ has area

\[K=\sqrt{8\cdot5\cdot2\cdot1}=4\sqrt5.\]

So

\[h=\frac{2K}{6}=\frac{4\sqrt5}{3}.\]

The trapezoid area is

\[\frac12(11+5)h=\frac{32\sqrt5}{3}.\]"""),
            ("Compute the area when the bases are 11 and 7",
             r"""Here the base difference is $4$, and the legs are $3$ and $5$. This is a $3$-$4$-$5$ triangle, so the trapezoid height is $3$.

The area is

\[\frac12(11+7)\cdot3=27.\]"""),
            ("Add the possible areas and answer the question",
             r"""The sum of all possible areas is

\[\frac{35}{2}\sqrt3+\frac{32}{3}\sqrt5+27.\]

Thus

\[r_1=\frac{35}{2},\quad n_1=3,\quad r_2=\frac{32}{3},\quad n_2=5,\quad r_3=27.\]

Then

\[r_1+r_2+r_3+n_1+n_2=\frac{35}{2}+\frac{32}{3}+27+3+5=63+\frac16.\]

The greatest integer less than or equal to this is $63$."""),
        ],
    },
    "2018 AMC 12A Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2018_AMC_12A_Answer_Key",
        "answer": ("D", "$12$"),
        "statement": r"""Triangle $ABC$ is an isosceles right triangle with $AB=AC=3$. Let $M$ be the midpoint of hypotenuse $\overline{BC}$. Points $I$ and $E$ lie on sides $\overline{AC}$ and $\overline{AB}$, respectively, so that $AI>AE$ and $AIME$ is a cyclic quadrilateral. Given that triangle $EMI$ has area $2$, the length $CI$ can be written as $\frac{a-\sqrt b}{c}$, where $a$, $b$, and $c$ are positive integers and $b$ is not divisible by the square of any prime. What is the value of $a+b+c$?""",
        "choices": [("A", "$9$"), ("B", "$10$"), ("C", "$11$"), ("D", "$12$"), ("E", "$13$")],
        "key_idea": "Use coordinates and the cyclic condition to relate AE and AI, then use the area condition.",
        "solution": [
            ("Set up coordinates that match the right triangle",
             r"""Place

\[A=(0,0),\quad B=(3,0),\quad C=(0,3).\]

Then the midpoint of the hypotenuse is

\[M=\left(\frac32,\frac32\right).\]

Let

\[E=(e,0),\qquad I=(0,i).\]

The condition $AI>AE$ means $i>e$."""),
            ("Use the cyclic condition",
             r"""The circle through $A$, $E$, and $I$ has equation

\[x^2+y^2-ex-iy=0.\]

Since $M$ is also on this circle,

\[\left(\frac32\right)^2+\left(\frac32\right)^2-\frac32e-\frac32i=0.\]

This simplifies to

\[e+i=3.\]"""),
            ("Use the area of triangle EMI",
             r"""The area of $\triangle EMI$ can be computed from coordinates:

\[\text{Area}=\frac12\left(\frac32(e+i)-ei\right).\]

Since $e+i=3$ and the area is $2$,

\[2=\frac12\left(\frac92-ei\right).\]

Thus

\[ei=\frac12.\]"""),
            ("Solve for e and i",
             r"""Now $e$ and $i$ are the two roots of

\[t^2-3t+\frac12=0.\]

Using the quadratic formula,

\[t=\frac{3\pm\sqrt7}{2}.\]

Because $i>e$, we have

\[i=\frac{3+\sqrt7}{2}.\]"""),
            ("Find CI",
             r"""The length $CI$ is the distance from $C=(0,3)$ to $I=(0,i)$, so

\[CI=3-i.\]

Therefore

\[CI=3-\frac{3+\sqrt7}{2}=\frac{3-\sqrt7}{2}.\]"""),
            ("Read off the requested sum",
             r"""The expression has the form

\[\frac{a-\sqrt b}{c}=\frac{3-\sqrt7}{2}.\]

So $a=3$, $b=7$, and $c=2$, giving

\[a+b+c=3+7+2=12.\]"""),
        ],
    },
    "2018 AMC 12A Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2018_AMC_12A_Answer_Key",
        "answer": ("E", "$80$"),
        "statement": r"""In $\triangle PAT$, $\angle P=36^\circ$, $\angle A=56^\circ$, and $PA=10$. Points $U$ and $G$ lie on sides $\overline{TP}$ and $\overline{TA}$, respectively, so that $PU=AG=1$. Let $M$ and $N$ be the midpoints of segments $\overline{PA}$ and $\overline{UG}$, respectively. What is the degree measure of the acute angle formed by lines $MN$ and $PA$?""",
        "choices": [("A", "$76$"), ("B", "$77$"), ("C", "$78$"), ("D", "$79$"), ("E", "$80$")],
        "key_idea": "Use vectors: the midpoint of two unit vectors points in the average direction.",
        "solution": [
            ("Put PA on the x-axis",
             r"""Place

\[P=(0,0),\qquad A=(10,0).\]

Then $M=(5,0)$, and line $PA$ is horizontal. So the desired angle is the angle that line $MN$ makes with the horizontal."""),
            ("Write coordinates for U and G",
             r"""Since $PU=1$ and $\angle P=36^\circ$,

\[U=(\cos36^\circ,\sin36^\circ).\]

At $A$, the side $AT$ points at angle $180^\circ-56^\circ=124^\circ$ from the positive $x$-axis. Because $AG=1$,

\[G=(10+\cos124^\circ,\sin124^\circ)=(10-\cos56^\circ,\sin56^\circ).\]"""),
            ("Use the midpoint N",
             r"""Since $N$ is the midpoint of $\overline{UG}$,

\[N=\left(\frac{10+\cos36^\circ-\cos56^\circ}{2},\frac{\sin36^\circ+\sin56^\circ}{2}\right).\]

Subtracting $M=(5,0)$, the direction vector of $\overline{MN}$ is proportional to

\[(\cos36^\circ-\cos56^\circ,\ \sin36^\circ+\sin56^\circ).\]"""),
            ("Find the slope of MN",
             r"""Therefore the tangent of the angle $\theta$ between $MN$ and the horizontal is

\[\tan\theta=\frac{\sin36^\circ+\sin56^\circ}{\cos36^\circ-\cos56^\circ}.\]

Now use sum-to-product identities:

\[\sin36^\circ+\sin56^\circ=2\sin46^\circ\cos10^\circ,\]

and

\[\cos36^\circ-\cos56^\circ=2\sin46^\circ\sin10^\circ.\]"""),
            ("Simplify the angle",
             r"""The common factor $2\sin46^\circ$ cancels, so

\[\tan\theta=\frac{\cos10^\circ}{\sin10^\circ}=\cot10^\circ=\tan80^\circ.\]

Thus the line $MN$ makes an angle of $80^\circ$ with $PA$."""),
            ("Finish",
             r"""The problem asks for the acute angle between the lines, and $80^\circ$ is acute.

Therefore the answer is $80^\circ$."""),
        ],
    },
    "2021 Spring AMC 12A Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("D", "$122$"),
        "statement": r"""Semicircle $\Gamma$ has diameter $AB$ of length $14$. Circle $\Omega$ lies tangent to $AB$ at a point $P$ and intersects $\Gamma$ at points $Q$ and $R$. If $QR=3\sqrt3$ and $\angle QPR=60^\circ$, then the area of $\triangle PQR$ is $\frac{a\sqrt b}{c}$, where $a$ and $c$ are relatively prime positive integers, and $b$ is a positive integer not divisible by the square of any prime. What is $a+b+c$?""",
        "choices": [("A", "$110$"), ("B", "$114$"), ("C", "$118$"), ("D", "$122$"), ("E", "$126$")],
        "key_idea": "Use the chord length in circle Omega to find its radius, then locate the common chord of the two circles.",
        "solution": [
            ("Find the radius of circle Omega",
             r"""The points $P,Q,R$ all lie on circle $\Omega$, and $\angle QPR=60^\circ$ subtends chord $\overline{QR}$.

If the radius of $\Omega$ is $r$, then

\[QR=2r\sin60^\circ=r\sqrt3.\]

Since $QR=3\sqrt3$, we get

\[r=3.\]"""),
            ("Set up coordinates",
             r"""Put the center of the semicircle at $C=(0,0)$ and let $AB$ be the $x$-axis. The semicircle has radius $7$.

Since $\Omega$ is tangent to $AB$ at $P$, write

\[P=(p,0),\qquad O=(p,3),\]

where $O$ is the center of $\Omega$."""),
            ("Use the common chord distance",
             r"""The common chord $QR$ has length $3\sqrt3$. In circle $\Omega$, the distance from $O$ to the chord is

\[\sqrt{3^2-\left(\frac{3\sqrt3}{2}\right)^2}=\frac32.\]

In the larger circle $\Gamma$, the distance from $C$ to the same chord is

\[\sqrt{7^2-\left(\frac{3\sqrt3}{2}\right)^2}=\frac{13}{2}.\]"""),
            ("Find the distance between the centers",
             r"""The chord lies on the far side of $O$ from $C$, so the distance between the centers is

\[CO=\frac{13}{2}-\frac32=5.\]

But

\[CO=\sqrt{p^2+3^2},\]

so

\[p^2+9=25,\qquad p=4\]

up to symmetry."""),
            ("Find the distance from P to QR",
             r"""The line $CO$ has direction vector $(4,3)$, so the common chord $QR$ is perpendicular to that direction. Its foot from $C$ is $\frac{13}{2}$ units along the direction from $C$ to $O$, giving the chord line

\[4x+3y=\frac{65}{2}.\]

The distance from $P=(4,0)$ to this line is

\[\frac{|4\cdot4+3\cdot0-\frac{65}{2}|}{\sqrt{4^2+3^2}}=\frac{33}{10}.\]"""),
            ("Compute the area",
             r"""Now use base $QR=3\sqrt3$ and height $\frac{33}{10}$:

\[\text{Area}=\frac12\cdot3\sqrt3\cdot\frac{33}{10}=\frac{99\sqrt3}{20}.\]

Thus $a=99$, $b=3$, and $c=20$, so

\[a+b+c=99+3+20=122.\]"""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
