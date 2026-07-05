import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 14"
base.BATCH_NUMBER = 298
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2011 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2011_AMC_12A_Answer_Key",
        "answer": ("D", "$80^\\circ$"),
        "statement": r"""Triangle $ABC$ has $\angle BAC=60^\circ$, $\angle CBA\le90^\circ$, $BC=1$, and $AC\ge AB$. Let $H$, $I$, and $O$ be the orthocenter, incenter, and circumcenter of $\triangle ABC$, respectively. Assume that the area of pentagon $BCOIH$ is the maximum possible. What is $\angle CBA$?""",
        "choices": [
            ("A", "$60^\\circ$"),
            ("B", "$72^\\circ$"),
            ("C", "$75^\\circ$"),
            ("D", "$80^\\circ$"),
            ("E", "$90^\\circ$"),
        ],
        "key_idea": "Show that B, C, O, I, and H are cyclic, then maximize an inscribed quadrilateral by spacing key chords evenly.",
        "solution": [
            ("Start with the fixed angle information",
             r"""Let

\[\angle ABC=B,\qquad \angle ACB=C.\]

Since $\angle A=60^\circ$, we have

\[B+C=120^\circ.\]

The condition $AC\ge AB$ means the side opposite $B$ is at least the side opposite $C$, so $B\ge C$. Thus $B\ge60^\circ$ and $C\le60^\circ$."""),
            ("Put O, I, and H on one circle",
             r"""Three standard angle facts are useful here:

\[\angle BOC=2\angle BAC=120^\circ,\]

\[\angle BIC=90^\circ+\frac12\angle BAC=120^\circ,\]

and

\[\angle BHC=180^\circ-\angle BAC=120^\circ.\]

Thus the points $B,C,O,I,H$ all see chord $\overline{BC}$ under the same angle, so they are concyclic."""),
            ("Reduce the area problem",
             r"""The triangle $BCO$ is fixed because $BC=1$ and $\angle BOC=120^\circ$. Therefore its area is fixed.

So maximizing the area of pentagon $BCOIH$ is the same as maximizing the area of quadrilateral $BOIH$ on this fixed circle."""),
            ("Find a built-in equality of chords",
             r"""In $\triangle BOC$, we have $OB=OC$, so

\[\angle OCB=30^\circ.\]

Because $CI$ bisects $\angle C$, and because the altitude $CH$ makes a $30^\circ$ angle with $CA$, angle chasing gives

\[\angle OCI=30^\circ-\frac C2,\]

and

\[\angle ICH=30^\circ-\frac C2.\]

These equal inscribed angles subtend equal chords, so

\[OI=IH.\]"""),
            ("Use the maximum-area idea on a fixed circle",
             r"""On a fixed circle with endpoints $B$ and $O$ fixed, the quadrilateral $BOIH$ has the most area when the moving points divide the relevant arc as evenly as their constraints allow.

Since we already know $OI=IH$, the maximum occurs when the third chord is equal too:

\[OI=IH=HB.\]

This is the same principle that an inscribed polygon with fixed endpoints gains area when its intermediate vertices are spread evenly rather than clustered."""),
            ("Convert equal chords into the requested angle",
             r"""Equal chords give equal arcs, so the corresponding angles at $C$ are equal:

\[\angle OCI=\angle ICH=\angle HCB.\]

But together these three angles make

\[\angle OCB=30^\circ.\]

Therefore each is $10^\circ$. In particular,

\[\angle ICH=30^\circ-\frac C2=10^\circ,\]

so $C=40^\circ$. Hence

\[B=120^\circ-C=80^\circ.\]

Therefore $\angle CBA=80^\circ$."""),
        ],
    },
    "2019 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2019_AMC_12B_Answer_Key",
        "answer": ("C", "$12+10\\sqrt3$"),
        "statement": r"""Let $ABCD$ be a convex quadrilateral with $BC=2$ and $CD=6$. Suppose that the centroids of $\triangle ABC$, $\triangle BCD$, and $\triangle ACD$ form the vertices of an equilateral triangle. What is the maximum possible value of the area of $ABCD$?""",
        "choices": [
            ("A", "$27$"),
            ("B", "$16\\sqrt3$"),
            ("C", "$12+10\\sqrt3$"),
            ("D", "$9+12\\sqrt3$"),
            ("E", "$30$"),
        ],
        "key_idea": "Use vectors to turn the centroid condition into the statement that triangle ABD is equilateral.",
        "solution": [
            ("Use vectors for the centroid condition",
             r"""Place $A$ at the origin. Let the position vectors of $B$ and $D$ be $\vec p$ and $\vec q$.

Write the position vector of $C$ as

\[m\vec p+n\vec q.\]

This is natural because the condition involves centroids, and centroids are averages of position vectors."""),
            ("Compute the three centroid differences",
             r"""The centroids of $\triangle ABC$, $\triangle BCD$, and $\triangle ACD$ are

\[G_1=\frac{(m+1)\vec p+n\vec q}{3},\]

\[G_2=\frac{(m+1)\vec p+(n+1)\vec q}{3},\]

and

\[G_3=\frac{m\vec p+(n+1)\vec q}{3}.\]

Therefore

\[\overrightarrow{G_1G_2}=\frac{\vec q}{3},\quad
\overrightarrow{G_2G_3}=-\frac{\vec p}{3},\quad
\overrightarrow{G_3G_1}=\frac{\vec p-\vec q}{3}.\]"""),
            ("Translate equilateral centroids back to triangle ABD",
             r"""Since $G_1G_2G_3$ is equilateral, these three vectors have equal lengths. Thus

\[|\vec p|=|\vec q|=|\vec p-\vec q|.\]

But these are exactly the lengths

\[AB,\ AD,\ BD.\]

So $\triangle ABD$ must be equilateral."""),
            ("Express the quadrilateral area using angle BCD",
             r"""Let

\[\theta=\angle BCD.\]

Because $BC=2$ and $CD=6$, the Law of Cosines gives

\[BD^2=2^2+6^2-2\cdot2\cdot6\cos\theta=40-24\cos\theta.\]

Since $\triangle ABD$ is equilateral, its area is

\[\frac{\sqrt3}{4}BD^2=10\sqrt3-6\sqrt3\cos\theta.\]"""),
            ("Add the area of triangle BCD",
             r"""The area of $\triangle BCD$ is

\[\frac12\cdot2\cdot6\sin\theta=6\sin\theta.\]

So the total area is

\[10\sqrt3+6\sin\theta-6\sqrt3\cos\theta.\]

Rewrite the variable part as

\[6(\sin\theta-\sqrt3\cos\theta)=12\sin(\theta-60^\circ).\]"""),
            ("Maximize the expression",
             r"""The largest possible value of $\sin(\theta-60^\circ)$ is $1$, and this occurs when

\[\theta=150^\circ,\]

which is a valid angle for the triangle with sides $2$, $6$, and $BD$.

Therefore the maximum area is

\[10\sqrt3+12.\]

So the answer is $12+10\sqrt3$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
