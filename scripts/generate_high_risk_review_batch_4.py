import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 4"
base.BATCH_NUMBER = 288
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2010 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2010_AMC_12B_Answer_Key",
        "answer": ("D", "77"),
        "statement": r"""For every integer $n\ge2$, let $\operatorname{pow}(n)$ be the largest power of the largest prime that divides $n$. For example,

\[\operatorname{pow}(144)=\operatorname{pow}(2^4\cdot3^2)=3^2.\]

What is the largest integer $m$ such that $2010^m$ divides

\[\prod_{n=2}^{5300}\operatorname{pow}(n)?\]""",
        "choices": [("A", "74"), ("B", "75"), ("C", "76"), ("D", "77"), ("E", "78")],
        "key_idea": "The limiting prime factor of 2010 is 67, so count how often 67 appears as the largest-prime-power contribution.",
        "solution": [
            ("Identify what m is measuring",
             r"""Since

\[2010=2\cdot3\cdot5\cdot67,\]

the largest possible $m$ is the smallest exponent among $2,3,5,$ and $67$ in the prime factorization of the large product. So we do not need the whole product; we only need to know which of these four primes is the bottleneck."""),
            ("Understand when a factor of 67 appears",
             r"""A number $n$ contributes a factor of $67$ to $\operatorname{pow}(n)$ only when $67$ is the largest prime factor of $n$. Write

\[n=67b.\]

Since $n\le5300$, we have $b\le79$. Also, every prime factor of $b$ must be at most $67$, otherwise the largest prime factor of $n$ would be larger than $67$."""),
            ("Count the allowed b-values",
             r"""The possible values are $b=1,2,\ldots,79$, except for the primes larger than $67$ in this range:

\[71,\quad 73,\quad 79.\]

That gives $79-3=76$ values of $b$. Each gives at least one factor of $67$ in the product."""),
            ("Remember the extra factor from 67 squared",
             r"""One of those values is $b=67$, giving

\[n=67^2.\]

For this particular $n$, the contribution is $\operatorname{pow}(n)=67^2$, so it contributes one extra factor of $67$. Therefore the total exponent of $67$ is

\[76+1=77.\]"""),
            ("Check that no smaller prime gives a smaller exponent",
             r"""We should still make sure that $2,3,$ or $5$ does not give a smaller exponent. The power of $2$ comes only from $n=2,2^2,\ldots,2^{12}$, so its exponent is

\[1+2+\cdots+12=78.\]

Counting similarly gives exponents $140$ for $3$ and $162$ for $5$. Thus the limiting exponent is $77$, coming from the prime $67$. Hence the largest possible $m$ is $77$."""),
        ],
    },
    "2013 AMC 12A Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2013_AMC_12A_Answer_Key",
        "answer": ("A", r"$(\log 2016,\log 2017)$"),
        "statement": r"""Consider

\[A=\log(2013+\log(2012+\log(2011+\log(\cdots+\log(3+\log2)\cdots)))).\]

Which of the following intervals contains $A$?""",
        "choices": [
            ("A", r"$(\log 2016,\log 2017)$"),
            ("B", r"$(\log 2017,\log 2018)$"),
            ("C", r"$(\log 2018,\log 2019)$"),
            ("D", r"$(\log 2019,\log 2020)$"),
            ("E", r"$(\log 2020,\log 2021)$"),
        ],
        "key_idea": "Bound the inner nested logarithm between 3 and 4, then use monotonicity of log.",
        "solution": [
            ("Name the nested expression",
             r"""A long nested expression is easier to control if we name its pieces. Define

\[f(2)=\log2,\qquad f(n)=\log(n+f(n-1))\quad(n\ge3).\]

Then the expression in the problem is $A=f(2013)$. We want to locate $f(2013)$ between two nearby logarithms."""),
            ("Reduce the goal to bounding f(2012)",
             r"""By the definition,

\[A=f(2013)=\log(2013+f(2012)).\]

So if we can show

\[3<f(2012)<4,\]

then

\[2016<2013+f(2012)<2017,\]

which would place $A$ in $(\log2016,\log2017)$."""),
            ("Get the lower bound",
             r"""The lower bound is direct. Since the inner logarithm values are positive, we have

\[f(2012)=\log(2012+f(2011))>\log2012.\]

Because $1000<2012$, it follows that $\log2012>3$. Therefore $f(2012)>3$."""),
            ("Get a safe upper bound",
             r"""For the upper bound, it is enough to know that $f(2011)<2011$. This follows by induction: $f(2)<2$, and if $f(n-1)<n-1$, then

\[f(n)=\log(n+f(n-1))<\log(2n-1)<n\]

for the values here. Thus

\[f(2012)=\log(2012+f(2011))<\log(2012+2011)=\log4023<4.\]"""),
            ("Conclude the interval",
             r"""We have shown

\[3<f(2012)<4.\]

Therefore

\[2016<2013+f(2012)<2017,\]

and applying the increasing function $\log$ gives

\[\log2016<A<\log2017.\]

The correct interval is $(\log2016,\log2017)$."""),
        ],
    },
    "2014 AMC 12A Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("E", "78"),
        "statement": r"""There are exactly $N$ distinct rational numbers $k$ such that $|k|<200$ and

\[5x^2+kx+12=0\]

has at least one integer solution for $x$. What is $N$?""",
        "choices": [("A", "6"), ("B", "12"), ("C", "24"), ("D", "48"), ("E", "78")],
        "key_idea": "Choose the integer root first, then solve for the rational parameter k.",
        "solution": [
            ("Let the integer root drive the problem",
             r"""Instead of trying to guess $k$, suppose the equation has an integer root $x$. Since the constant term is $12\ne0$, the root cannot be $0$. Now solve the equation for $k$:

\[5x^2+kx+12=0\quad\Rightarrow\quad k=-5x-\frac{12}{x}.\]

Every nonzero integer $x$ gives a rational value of $k$."""),
            ("Turn the condition on k into a condition on x",
             r"""For $x>0$, the value $k=-5x-\frac{12}{x}$ is negative, and

\[|k|=5x+\frac{12}{x}.\]

We need

\[5x+\frac{12}{x}<200.\]

This is clearly true for $1\le x\le39$, because at $x=39$ the value is $195+\frac{12}{39}<200$."""),
            ("Show where the positive x-values stop",
             r"""For $x\ge40$, we have

\[5x+\frac{12}{x}>5x\ge200.\]

So no positive integer $x\ge40$ works. Therefore the positive integer roots that work are exactly

\[x=1,2,\ldots,39.\]"""),
            ("Use symmetry for negative roots",
             r"""If $x<0$, write $x=-t$ with $t>0$. Then

\[k=5t+\frac{12}{t},\]

so the same inequality gives $t=1,2,\ldots,39$. Thus there are another $39$ possible roots from the negative side."""),
            ("Check that distinct roots give distinct k-values",
             r"""We still need distinct rational numbers $k$, not just roots. If two positive values $x$ and $y$ give the same magnitude, then

\[5x+\frac{12}{x}=5y+\frac{12}{y}.\]

Multiplying by $xy$ gives $(x-y)(5xy-12)=0$. Since $5xy=12$ is impossible for positive integers, we must have $x=y$. The negative side gives opposite signs of $k$, so there is no overlap. Hence

\[N=39+39=78.\]"""),
        ],
    },
    "2015 AMC 12A Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12A_Answer_Key",
        "answer": ("A", "59"),
        "statement": r"""Let $S$ be a square of side length $1$. Two points are chosen independently at random on the sides of $S$. The probability that the straight-line distance between the points is at least $\frac12$ is

\[\frac{a-b\pi}{c},\]

where $a,b,$ and $c$ are positive integers and $\gcd(a,b,c)=1$. What is $a+b+c$?""",
        "choices": [("A", "59"), ("B", "60"), ("C", "61"), ("D", "62"), ("E", "63")],
        "key_idea": "Condition on whether the second point lies on the same side, an adjacent side, or the opposite side.",
        "solution": [
            ("Fix the first point by symmetry",
             r"""Because all four sides of the square are symmetric, we may imagine that the first point is on one chosen side. The second point is equally likely to lie on the same side, either adjacent side, or the opposite side. The probabilities of these side cases are

\[\frac14,\quad \frac12,\quad \frac14.\]"""),
            ("Handle the opposite side",
             r"""If the second point is on the opposite side, then the vertical or horizontal separation is already $1$. Therefore the distance between the two points is certainly at least $\frac12$.

So the success probability in this case is $1$."""),
            ("Handle the same side",
             r"""If both points are on the same side, model their positions by two independent numbers $X,Y$ in $[0,1]$. We need

\[|X-Y|\ge\frac12.\]

In the unit square of possible pairs $(X,Y)$, this region consists of two right triangles of side length $\frac12$, with total area

\[2\cdot\frac12\cdot\frac12\cdot\frac12=\frac14.\]

So the success probability on the same side is $\frac14$."""),
            ("Handle adjacent sides",
             r"""If the points are on adjacent sides meeting at a corner, use coordinates $(x,0)$ and $(0,y)$ with $0\le x,y\le1$. The distance condition is

\[x^2+y^2\ge\frac14.\]

The failure region is the quarter circle of radius $\frac12$ near the shared corner, whose area is

\[\frac14\pi\left(\frac12\right)^2=\frac{\pi}{16}.\]

Therefore the success probability for adjacent sides is $1-\frac{\pi}{16}$."""),
            ("Average the three cases",
             r"""Now combine the cases:

\[P=\frac14\cdot\frac14+\frac12\left(1-\frac{\pi}{16}\right)+\frac14\cdot1.\]

This simplifies to

\[P=\frac1{16}+\frac12-\frac{\pi}{32}+\frac14=\frac{26-\pi}{32}.\]

Thus $a=26$, $b=1$, and $c=32$, so

\[a+b+c=26+1+32=59.\]"""),
        ],
    },
    "2017 AMC 12B Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2017_AMC_12B_Answer_Key",
        "answer": ("B", r"$\frac{5}{192}$"),
        "statement": r"""Abby, Bernardo, Carl, and Debra play a game in which each of them starts with four coins. The game consists of four rounds. In each round, four balls are placed in an urn: one green, one red, and two white. The players each draw a ball at random without replacement. Whoever gets the green ball gives one coin to whoever gets the red ball. What is the probability that, at the end of the fourth round, each of the players has four coins?""",
        "choices": [
            ("A", r"$\frac{7}{576}$"),
            ("B", r"$\frac{5}{192}$"),
            ("C", r"$\frac{1}{36}$"),
            ("D", r"$\frac{5}{144}$"),
            ("E", r"$\frac{7}{48}$"),
        ],
        "key_idea": "View each round as a directed transfer and count balanced directed multigraphs with four edges.",
        "solution": [
            ("Translate each round into a directed edge",
             r"""In one round, the green-ball player gives a coin to the red-ball player. So one round is an ordered pair

\[\text{giver}\to\text{receiver}.\]

There are $4$ choices for the giver and then $3$ choices for the receiver, so each round has $12$ equally likely outcomes. Across four rounds, there are

\[12^4\]

total ordered sequences of transfers."""),
            ("State the balance condition",
             r"""A player ends with four coins exactly when the number of coins they give equals the number of coins they receive. In graph language, each player must have

\[\text{outdegree}=\text{indegree}.\]

So we must count ordered sequences of four directed edges on four labeled vertices, with no loops, for which every vertex is balanced."""),
            ("Recognize the possible cycle structures",
             r"""A balanced directed graph decomposes into directed cycles. With exactly four edges and no loops, the only possible structures are:

1. two directed $2$-cycles, possibly using the same pair twice;
2. one directed $4$-cycle.

A directed $3$-cycle would leave one extra edge, which could not balance by itself."""),
            ("Count the two-cycle cases",
             r"""First, suppose two different unordered pairs form $2$-cycles. There are $\binom{6}{2}=15$ ways to choose the two pairs of players, and then the four directed edges can appear in any order, giving

\[15\cdot4!=360\]

ordered sequences.

If the same pair forms both $2$-cycles, there are $\binom42=6$ choices of the pair. The four transfers are two in each direction, so there are

\[\frac{4!}{2!2!}=6\]

orders for each pair, giving $6\cdot6=36$ sequences."""),
            ("Count the four-cycle cases",
             r"""Now count directed $4$-cycles. On four labeled players, the number of directed cycles up to rotation is

\[(4-1)!=6.\]

Once the four directed edges of the cycle are chosen, they may occur in any of the four rounds, so there are $4!$ orders. This gives

\[6\cdot4!=144\]

ordered sequences."""),
            ("Divide by all possible outcomes",
             r"""The number of favorable ordered sequences is

\[360+36+144=540.\]

Therefore the probability is

\[\frac{540}{12^4}=\frac{540}{20736}=\frac{5}{192}.\]

So the answer is $\frac{5}{192}$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
