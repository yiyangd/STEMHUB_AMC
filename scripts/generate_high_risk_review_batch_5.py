import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 5"
base.BATCH_NUMBER = 289
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2012 AMC 12B Problem 18": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("B", "512"),
        "statement": r"""Let $(a_1,a_2,\ldots,a_{10})$ be a list of the first $10$ positive integers such that for each $2\le i\le10$, either $a_i+1$ or $a_i-1$ or both appear somewhere before $a_i$ in the list. How many such lists are there?""",
        "choices": [("A", "120"), ("B", "512"), ("C", "1024"), ("D", "181,440"), ("E", "362,880")],
        "key_idea": "At every stage the chosen numbers must form one contiguous interval of integers.",
        "solution": [
            ("Understand what the condition means",
             r"""When a number is placed after the first position, it must be next to a number that has already appeared. So if the numbers already chosen form a block such as

\[4,5,6,7,\]

then the next number can only extend that block to the left or to the right, becoming $3$ or $8$."""),
            ("Observe the interval structure",
             r"""After the first number is chosen, the set of chosen numbers is always a contiguous interval. This is true at the start, and each new legal number can only be one less than the current smallest chosen number or one greater than the current largest chosen number."""),
            ("Choose the first number",
             r"""Suppose the first number is $s$. Then eventually the numbers

\[1,2,\ldots,s-1\]

must be added on the left, and the numbers

\[s+1,s+2,\ldots,10\]

must be added on the right. The left additions must occur in the order $s-1,s-2,\ldots,1$, and the right additions must occur in the order $s+1,s+2,\ldots,10$."""),
            ("Count the ways after fixing the first number",
             r"""Once $s$ is fixed, the only freedom is how to interlace the $s-1$ left moves with the $10-s$ right moves. There are $9$ moves after the first number, and we choose which $s-1$ of them are left moves:

\[\binom{9}{s-1}.\]"""),
            ("Sum over all possible starting numbers",
             r"""Therefore the total number of lists is

\[\sum_{s=1}^{10}\binom{9}{s-1}=\sum_{j=0}^{9}\binom9j=2^9=512.\]

So the answer is $512$."""),
        ],
    },
    "2012 AMC 12B Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12B_Answer_Key",
        "answer": ("B", "92"),
        "statement": r"""Consider all polynomials of a complex variable

\[P(z)=4z^4+az^3+bz^2+cz+d,\]

where $a,b,c,$ and $d$ are integers, $0\le d\le c\le b\le a\le4$, and the polynomial has a zero $z_0$ with $|z_0|=1$. What is the sum of all values $P(1)$ over all the polynomials with these properties?""",
        "choices": [("A", "84"), ("B", "92"), ("C", "100"), ("D", "108"), ("E", "120")],
        "key_idea": "Use the triangle inequality on the unit circle to force only a short list of coefficient patterns.",
        "solution": [
            ("Use the unit-circle condition",
             r"""If $|z_0|=1$ and $P(z_0)=0$, then

\[4z_0^4=-(az_0^3+bz_0^2+cz_0+d).\]

Taking absolute values gives

\[4=|az_0^3+bz_0^2+cz_0+d|.\]

But the triangle inequality gives

\[|az_0^3+bz_0^2+cz_0+d|\le a+b+c+d.\]"""),
            ("Use the coefficient restrictions",
             r"""The coefficients are ordered:

\[0\le d\le c\le b\le a\le4.\]

This makes the search small. The only way a unit-circle zero can occur is when the vector sum of the lower-degree terms has length exactly $4$, matching the leading term. This forces the lower coefficients to align in special cyclotomic patterns."""),
            ("List the possible patterns",
             r"""Checking the allowed ordered coefficient patterns gives exactly seven polynomials:

\[4z^4+4z^3,\]
\[4z^4+4z^3+z^2+z,\]
\[4z^4+4z^3+2z^2+2z,\]
\[4z^4+4z^3+3z^2+3z,\]
\[4z^4+4z^3+4z^2,\]
\[4z^4+4z^3+4z^2+4z,\]
\[4z^4+4z^3+4z^2+4z+4.\]"""),
            ("Explain why this list is reliable",
             r"""Each polynomial in the list has a visible unit-circle zero: several have $z=-1$ as a zero, $4z^4+4z^3+4z^2$ has primitive cube roots, and $4(z^4+z^3+z^2+z+1)$ has fifth roots of unity. The coefficient restrictions exclude all other cases."""),
            ("Add the corresponding values of P(1)",
             r"""The seven values of $P(1)$ are

\[8,10,12,14,12,16,20.\]

Their sum is

\[8+10+12+14+12+16+20=92.\]

So the answer is $92$."""),
        ],
    },
    "2014 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("B", "40"),
        "statement": r"""The parabola $\mathcal P$ has focus $(0,0)$ and goes through the points $(4,3)$ and $(-4,-3)$. For how many points $(x,y)\in\mathcal P$ with integer coordinates is it true that

\[|4x+3y|\le1000?\]""",
        "choices": [("A", "38"), ("B", "40"), ("C", "42"), ("D", "44"), ("E", "46")],
        "key_idea": "Rotate coordinates using $4x+3y$ and $3x-4y$, then count a simple congruence.",
        "solution": [
            ("Find the direction of the directrix",
             r"""The points $(4,3)$ and $(-4,-3)$ are both distance $5$ from the focus $(0,0)$. Since both lie on the parabola, each must also be distance $5$ from the directrix. This forces the directrix to be parallel to the line through those two points, so a useful perpendicular coordinate is

\[3x-4y.\]"""),
            ("Write the parabola equation",
             r"""One valid directrix is

\[3x-4y=25.\]

Using the focus-directrix definition,

\[\sqrt{x^2+y^2}=\frac{|3x-4y-25|}{5}.\]

Squaring and simplifying gives

\[(4x+3y)^2+50(3x-4y)-625=0.\]"""),
            ("Introduce the key integer parameter",
             r"""Let

\[w=4x+3y.\]

The condition in the problem is $|w|\le1000$. From the parabola equation,

\[3x-4y=\frac{625-w^2}{50}.\]

Since $x$ and $y$ are integers, $w$ is an integer, and this expression must be compatible with integer $x,y$."""),
            ("Reduce to a congruence",
             r"""Write $w=5r$. Then

\[3x-4y=\frac{25-r^2}{2}.\]

Solving the two linear equations for $x$ and $y$ shows that $x$ and $y$ are integers exactly when

\[r\equiv5\pmod{10}.\]"""),
            ("Count the possible r-values",
             r"""The inequality $|w|\le1000$ becomes

\[|5r|\le1000,\]

so $|r|\le200$. The integers $r$ satisfying $r\equiv5\pmod{10}$ in this range are

\[-195,-185,\ldots,185,195.\]

There are $40$ such values. Hence there are $40$ integer-coordinate points."""),
        ],
    },
    "2017 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2017_AMC_12A_Answer_Key",
        "answer": ("E", "39"),
        "statement": r"""A square is drawn in the coordinate plane with vertices at $(2,2)$, $(-2,2)$, $(-2,-2)$, and $(2,-2)$. A particle starts at $(0,0)$. Every second it moves with equal probability to one of the eight nearest lattice points. The particle eventually hits the square for the first time, either at one of the $4$ corners or one of the $12$ lattice points in the interior of a side. The probability that it hits a corner rather than an interior point of a side is $\frac mn$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?""",
        "choices": [("A", "4"), ("B", "5"), ("C", "7"), ("D", "15"), ("E", "39")],
        "key_idea": "Use symmetry to reduce the random walk to three interior states.",
        "solution": [
            ("Use symmetry to name the states",
             r"""Before the particle hits the square, it is inside the $3\times3$ lattice of points with coordinates $-1,0,1$. By symmetry, there are only three kinds of interior states:

\[C=(0,0),\quad A=(1,0)\text{ type},\quad B=(1,1)\text{ type}.\]

Let their probabilities of eventually hitting a corner be $C,A,$ and $B$ respectively."""),
            ("Write the equation from the center",
             r"""From the center, the particle moves to four $A$-type points and four $B$-type points. Therefore

\[C=\frac{4A+4B}{8}=\frac{A+B}{2}.\]"""),
            ("Write the equation from an A-type point",
             r"""From a point like $(1,0)$, three moves hit side-interior boundary points, two moves go to $A$-type points, two moves go to $B$-type points, and one move goes to $C$. Side-interior boundary points contribute probability $0$. Thus

\[A=\frac{2A+2B+C}{8}.\]"""),
            ("Write the equation from a B-type point",
             r"""From a point like $(1,1)$, one move hits a corner, four moves hit side-interior boundary points, two moves go to $A$-type points, and one move goes to $C$. Hence

\[B=\frac{1+2A+C}{8}.\]"""),
            ("Solve the small system",
             r"""Solving

\[C=\frac{A+B}{2},\qquad A=\frac{2A+2B+C}{8},\qquad B=\frac{1+2A+C}{8}\]

gives

\[C=\frac4{35}.\]

The particle starts at the center, so the desired probability is $\frac4{35}$. Therefore $m+n=4+35=39$."""),
        ],
    },
    "2018 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2018_AMC_12A_Answer_Key",
        "answer": ("D", "18"),
        "statement": r"""For a positive integer $n$ and nonzero digits $a,b,$ and $c$, let $A_n$ be the $n$-digit integer each of whose digits is $a$, let $B_n$ be the $n$-digit integer each of whose digits is $b$, and let $C_n$ be the $2n$-digit integer each of whose digits is $c$. What is the greatest possible value of $a+b+c$ for which there are at least two values of $n$ such that

\[C_n-B_n=A_n^2?\]""",
        "choices": [("A", "12"), ("B", "14"), ("C", "16"), ("D", "18"), ("E", "20")],
        "key_idea": "Write all repeated-digit numbers using the repunit $R_n=(10^n-1)/9$.",
        "solution": [
            ("Represent the repeated digits",
             r"""Let

\[R_n=\frac{10^n-1}{9}.\]

Then

\[A_n=aR_n,\qquad B_n=bR_n,\qquad C_n=cR_{2n}=c(10^n+1)R_n.\]"""),
            ("Substitute into the equation",
             r"""The equation $C_n-B_n=A_n^2$ becomes

\[c(10^n+1)R_n-bR_n=a^2R_n^2.\]

Dividing by $R_n$ gives

\[c(10^n+1)-b=a^2R_n.\]"""),
            ("Use 10^n = 9R_n + 1",
             r"""Since $10^n=9R_n+1$, the left side becomes

\[c(9R_n+2)-b=9cR_n+2c-b.\]

So

\[(a^2-9c)R_n=2c-b.\]"""),
            ("Use the condition that two n-values work",
             r"""The right side $2c-b$ is fixed, while $R_n$ changes with $n$. If the equation holds for at least two different values of $n$, the coefficient of $R_n$ must be $0$. Thus

\[a^2=9c\quad\text{and}\quad b=2c.\]"""),
            ("Maximize the digit sum",
             r"""Because $a$ is a nonzero digit and $a^2=9c$, the possible values are

\[(a,c)=(3,1),(6,4),(9,9).\]

The corresponding $b=2c$ values are $2,8,18$. The last is not a digit, so the largest valid sum is

\[6+8+4=18.\]"""),
        ],
    },
    "2020 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12A_Answer_Key",
        "answer": ("C", "929"),
        "statement": r"""The number $a=\frac pq$, where $p$ and $q$ are relatively prime positive integers, has the property that the sum of all real numbers $x$ satisfying

\[\lfloor x\rfloor\{x\}=a x^2\]

is $420$, where $\lfloor x\rfloor$ denotes the greatest integer less than or equal to $x$ and $\{x\}=x-\lfloor x\rfloor$ denotes the fractional part of $x$. What is $p+q$?""",
        "choices": [("A", "245"), ("B", "593"), ("C", "929"), ("D", "1331"), ("E", "1332")],
        "key_idea": "Write $x=n+r$ and observe that the ratio $r/n$ is constant for all positive solutions.",
        "solution": [
            ("Separate integer and fractional parts",
             r"""Let

\[x=n+r,\]

where $n=\lfloor x\rfloor$ and $0\le r<1$. If $n<0$, then $nr\le0$ while $ax^2\ge0$, so no negative interval gives useful positive solutions. The solution $x=0$ contributes nothing to the sum."""),
            ("Scale the fractional part",
             r"""For $n>0$, write

\[r=nt.\]

Then the equation becomes

\[n(nt)=a(n+nt)^2.\]

After canceling $n^2$, we get

\[t=a(1+t)^2.\]

So the same value of $t$ works for every positive integer part $n$ that is allowed."""),
            ("Find how many integer parts occur",
             r"""The condition $0\le r<1$ becomes

\[0\le nt<1,\]

so the positive integer parts are $n=1,2,\ldots,M$ for some $M$, where

\[\frac1{M+1}\le t<\frac1M.\]"""),
            ("Use the given sum of solutions",
             r"""The positive solutions are

\[x=n(1+t)\quad(n=1,2,\ldots,M).\]

Their sum is

\[(1+t)\frac{M(M+1)}2=420.\]

So

\[t=\frac{840}{M(M+1)}-1.\]"""),
            ("Locate M and compute a",
             r"""The value of $t$ must also satisfy $\frac1{M+1}\le t<\frac1M$. Testing this narrow condition gives

\[M=28,\qquad t=\frac1{29}.\]

Then

\[a=\frac{t}{(1+t)^2}=\frac{1/29}{(30/29)^2}=\frac{29}{900}.\]

Thus $p+q=29+900=929$."""),
        ],
    },
    "2021 Spring AMC 12B Problem 18": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("A", "$-2$"),
        "statement": r"""Let $z$ be a complex number satisfying

\[12|z|^2=2|z+2|^2+|z^2+1|^2+31.\]

What is the value of

\[z+\frac6z?\]""",
        "choices": [("A", "$-2$"), ("B", "$-1$"), ("C", "$\\frac12$"), ("D", "$1$"), ("E", "$4$")],
        "key_idea": "Rewrite the condition as a sum of squares to force $|z|^2=6$ and $\operatorname{Re}(z)=-1$.",
        "solution": [
            ("Write z in terms of size and real part",
             r"""Let $|z|=r$ and let $x=\operatorname{Re}(z)$. Then

\[|z+2|^2=r^2+4x+4.\]

Also,

\[|z^2+1|^2=r^4+2\operatorname{Re}(z^2)+1.\]"""),
            ("Simplify the equation",
             r"""Using $\operatorname{Re}(z^2)=x^2-y^2$ and $r^2=x^2+y^2$, the given equation simplifies to

\[12r^2=r^4+4x^2+8x+40.\]"""),
            ("Complete squares",
             r"""Move everything to one side:

\[0=r^4-12r^2+4x^2+8x+40.\]

This factors as a sum of squares:

\[(r^2-6)^2+4(x+1)^2=0.\]"""),
            ("Use the fact that a sum of squares is zero",
             r"""Both terms are nonnegative, so both must be zero. Therefore

\[r^2=6,\qquad x=-1.\]

That is, $|z|^2=6$ and $\operatorname{Re}(z)=-1$."""),
            ("Evaluate the requested expression",
             r"""Since $|z|^2=6$, we have

\[\frac6z=\frac{|z|^2}{z}=\overline z.\]

Thus

\[z+\frac6z=z+\overline z=2\operatorname{Re}(z)=2(-1)=-2.\]"""),
        ],
    },
    "2021 Spring AMC 12B Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("B", "17"),
        "statement": r"""Two fair dice, each with at least $6$ faces, are rolled. On each face of each die is printed a distinct integer from $1$ to the number of faces on that die, inclusive. The probability of rolling a sum of $7$ is $\frac34$ of the probability of rolling a sum of $10$, and the probability of rolling a sum of $12$ is $\frac1{12}$. What is the least possible number of faces on the two dice combined?""",
        "choices": [("A", "16"), ("B", "17"), ("C", "18"), ("D", "19"), ("E", "20")],
        "key_idea": "Convert probabilities into counts of ordered pairs on an $m$ by $n$ grid.",
        "solution": [
            ("Name the dice sizes",
             r"""Let the dice have $m$ and $n$ faces, with $6\le m\le n$. Each ordered roll is equally likely, so there are $mn$ possible outcomes."""),
            ("Count the sum-7 outcomes",
             r"""Because both dice have at least $6$ faces, the sum $7$ can occur in exactly the usual six ways:

\[(1,6),(2,5),(3,4),(4,3),(5,2),(6,1).\]

So $N_7=6$."""),
            ("Use the relation between sums 7 and 10",
             r"""The probability for sum $7$ is $\frac34$ of the probability for sum $10$, so the counts satisfy

\[N_7=\frac34N_{10}.\]

Since $N_7=6$, we get

\[N_{10}=8.\]"""),
            ("Force the smaller die to have 8 faces",
             r"""With $m\le n$, the number of ways to roll $10$ increases as the smaller die grows. If $m=6$ or $7$, there are only $6$ or $7$ ways. If both dice have at least $9$ faces, there are $9$ ways. Therefore $N_{10}=8$ forces

\[m=8.\]"""),
            ("Use the sum-12 probability",
             r"""Now $m=8$. If the larger die has $n$ faces, the probability of sum $12$ is

\[\frac{N_{12}}{8n}=\frac1{12},\]

so

\[8n=12N_{12}.\]

For $n=9$, the pairs summing to $12$ are $(3,9),(4,8),(5,7),(6,6),(7,5),(8,4)$, so $N_{12}=6$ and $8n=72=12\cdot6$. Thus $n=9$ works, and the least total number of faces is $8+9=17$."""),
        ],
    },
    "2021 Spring AMC 12B Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("D", "$2\\le S<6$"),
        "statement": r"""Let $S$ be the sum of all positive real numbers $x$ for which

\[x^{2^{\sqrt2}}=(\sqrt2)^{2^x}.\]

Which of the following statements is true?""",
        "choices": [("A", "$S<\\sqrt2$"), ("B", "$S=\\sqrt2$"), ("C", "$\\sqrt2<S<2$"), ("D", "$2\\le S<6$"), ("E", "$S\\ge6$")],
        "key_idea": "Take logarithms and compare a concave logarithmic curve with an exponential curve.",
        "solution": [
            ("Take logarithms carefully",
             r"""Taking $\log_2$ of both sides gives

\[2^{\sqrt2}\log_2 x=2^x\log_2(\sqrt2).\]

Since $\log_2(\sqrt2)=\frac12$, this becomes

\[2^{\sqrt2}\log_2 x=2^{x-1}.\]"""),
            ("Notice the domain restriction",
             r"""The right side is positive, so $\log_2 x$ must be positive. Therefore all solutions have

\[x>1.\]

This already helps us reason about the graphs without worrying about small positive $x$."""),
            ("Find one exact solution",
             r"""Try $x=\sqrt2$. Then

\[\log_2(\sqrt2)=\frac12,\]

so the left side is

\[2^{\sqrt2}\cdot\frac12=2^{\sqrt2-1},\]

which equals the right side $2^{\sqrt2-1}$. Thus $x=\sqrt2$ is one solution."""),
            ("Locate the other solution",
             r"""Let

\[F(x)=2^{\sqrt2}\log_2x,\qquad G(x)=2^{x-1}.\]

At $x=2$, $F(2)=2^{\sqrt2}>2=G(2)$. At $x=4$, $F(4)=2\cdot2^{\sqrt2}<8=G(4)$. By continuity, there is another solution between $2$ and $4$."""),
            ("Explain why there are no more solutions",
             r"""The function $F(x)$ is concave, while $G(x)$ is convex and increasing. Their difference can cross the axis at most twice in this setting. We have already found one solution at $\sqrt2$ and one solution between $2$ and $4$, so these are all the positive solutions."""),
            ("Bound the sum",
             r"""Therefore

\[S=\sqrt2+t\]

for some $2<t<4$. Hence

\[2<S<\sqrt2+4<6.\]

So the true statement is $2\le S<6$."""),
        ],
    },
    "2023 AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2023_AMC_12A_Answer_Key",
        "answer": ("C", "$-1$"),
        "statement": r"""There is a unique sequence of integers $a_1,a_2,\ldots,a_{2023}$ such that

\[\tan 2023x=\frac{a_1\tan x+a_3\tan^3x+a_5\tan^5x+\cdots+a_{2023}\tan^{2023}x}{1+a_2\tan^2x+a_4\tan^4x+\cdots+a_{2022}\tan^{2022}x}\]

whenever $\tan 2023x$ is defined. What is $a_{2023}$?""",
        "choices": [("A", "$-2023$"), ("B", "$-2022$"), ("C", "$-1$"), ("D", "$1$"), ("E", "$2023$")],
        "key_idea": "Use $(1+it)^{2023}$ to read off the numerator of $\tan(2023\arctan t)$.",
        "solution": [
            ("Replace tan x with a variable",
             r"""Let

\[t=\tan x.\]

Then $2023x=2023\arctan t$, so the problem is asking about the rational expression for $\tan(2023\arctan t)$."""),
            ("Use a complex-number representation",
             r"""If $x=\arctan t$, then a complex number with argument $x$ is $1+it$. Therefore

\[(1+it)^{2023}\]

has argument $2023x$. The tangent of that argument is

\[\frac{\operatorname{Im}(1+it)^{2023}}{\operatorname{Re}(1+it)^{2023}}.\]"""),
            ("Identify the numerator coefficients",
             r"""The imaginary part contains the odd powers of $t$:

\[\operatorname{Im}(1+it)^{2023}=\binom{2023}{1}t-\binom{2023}{3}t^3+\binom{2023}{5}t^5-\cdots+a_{2023}t^{2023}.\]

The signs alternate because $i^{2k+1}$ alternates between $i$ and $-i$."""),
            ("Read the final coefficient",
             r"""The coefficient of $t^{2023}$ comes from the term

\[\binom{2023}{2023}i^{2023}t^{2023}.\]

Since $2023=4\cdot505+3$, we have

\[i^{2023}=i^3=-i.\]

Thus the imaginary coefficient is $-1$."""),
            ("Match the requested notation",
             r"""The denominator has constant term $1$, so there is no scaling change to the numerator. Therefore

\[a_{2023}=-1.\]

The answer is $-1$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
