import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 6"
base.BATCH_NUMBER = 290
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2017 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2017_AMC_12B_Answer_Key",
        "answer": ("D", "557"),
        "statement": r"""A set of $n$ people participate in an online video basketball tournament. Each person may be a member of any number of $5$-player teams, but no two teams may have exactly the same $5$ members. The site statistics show a curious fact: the average, over all subsets of size $9$ of the set of $n$ participants, of the number of complete teams whose members are among those $9$ people is equal to the reciprocal of the average, over all subsets of size $8$ of the set of $n$ participants, of the number of complete teams whose members are among those $8$ people. How many values $n$, $9\le n\le2017$, can be the number of participants?""",
        "choices": [("A", "477"), ("B", "482"), ("C", "487"), ("D", "557"), ("E", "562")],
        "key_idea": "Convert the average over subsets into a divisibility condition on a binomial coefficient.",
        "solution": [
            ("Count the contribution of one team",
             r"""Suppose there are $T$ complete $5$-player teams. A fixed team is contained in

\[\binom{n-5}{k-5}\]

subsets of size $k$. Since there are $\binom nk$ total subsets of size $k$, the average number of complete teams inside a random $k$-subset is

\[T\frac{\binom{n-5}{k-5}}{\binom nk}=T\frac{\binom k5}{\binom n5}.\]"""),
            ("Apply the condition for k = 8 and k = 9",
             r"""For $k=9$, the average is

\[T\frac{\binom95}{\binom n5}=T\frac{126}{\binom n5}.\]

For $k=8$, the average is

\[T\frac{\binom85}{\binom n5}=T\frac{56}{\binom n5}.\]

The first average is the reciprocal of the second, so their product is $1$."""),
            ("Turn the condition into an integer divisibility question",
             r"""Thus

\[\left(T\frac{126}{\binom n5}\right)\left(T\frac{56}{\binom n5}\right)=1.\]

Since $126\cdot56=7056=84^2$, we get

\[\left(\frac{84T}{\binom n5}\right)^2=1.\]

So a valid tournament exists exactly when

\[T=\frac{\binom n5}{84}\]

is an integer."""),
            ("Count when the binomial coefficient is divisible by 84",
             r"""We need $\binom n5$ divisible by

\[84=2^2\cdot3\cdot7.\]

Checking the five consecutive factors in $\binom n5=\frac{n(n-1)(n-2)(n-3)(n-4)}{120}$ gives these residue conditions:

\[
\begin{aligned}
n&\equiv0,1,2,3,4,8,10,12,16,17,18,19,20,24,26,28\pmod{32},\\
n&\not\equiv5,8\pmod9,\\
n&\not\equiv5,6\pmod7.
\end{aligned}
\]

The moduli $32,9,7$ are relatively prime, so one full period has $16\cdot7\cdot5=560$ good residue classes modulo $2016$."""),
            ("Adjust for the actual range",
             r"""The range $9\le n\le2017$ contains all residue classes modulo $2016$ except $2,3,4,5,6,7,8$, while it includes residues $0$ and $1$. Among the missing residues, $2,3,$ and $4$ would have been counted. Therefore the number of valid $n$ is

\[560-3=557.\]

So the answer is $557$."""),
        ],
    },
    "2020 AMC 12B Problem 14": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12B_Answer_Key",
        "answer": ("A", "Bela will always win."),
        "statement": r"""Bela and Jenn play the following game on the closed interval $[0,n]$ of the real number line, where $n$ is a fixed integer greater than $4$. They take turns playing, with Bela going first. On his first turn, Bela chooses any real number in the interval $[0,n]$. Thereafter, the player whose turn it is chooses a real number that is more than one unit away from all numbers previously chosen by either player. A player unable to choose such a number loses. Using optimal strategy, which player will win the game?""",
        "choices": [
            ("A", "Bela will always win."),
            ("B", "Jenn will always win."),
            ("C", "Bela will win if and only if $n$ is odd."),
            ("D", "Jenn will win if and only if $n$ is odd."),
            ("E", "Jenn will win if and only if $n>8$."),
        ],
        "key_idea": "Bela takes the midpoint first, then mirrors every move Jenn makes.",
        "solution": [
            ("Look for symmetry",
             r"""The interval $[0,n]$ is symmetric about its midpoint $\frac n2$. In games on symmetric boards, a common first-player strategy is to take the center and then mirror the opponent."""),
            ("Choose Bela's first move",
             r"""Bela chooses

\[\frac n2\]

on his first turn. This point is now unavailable, and every other point has a distinct mirror image across the midpoint."""),
            ("Describe the mirror response",
             r"""Whenever Jenn chooses a point $x$, Bela responds with

\[n-x.\]

This point is not equal to $x$ unless $x=\frac n2$, which Jenn cannot choose because Bela already chose it."""),
            ("Check that the mirror response is legal",
             r"""The previously chosen points come in mirror pairs, together with the midpoint. If Jenn's point $x$ is more than one unit away from all previously chosen points, then its mirror $n-x$ is also more than one unit away from all mirror images of those points. It is also more than one unit from the midpoint because $x$ was legal."""),
            ("Conclude who gets stuck first",
             r"""So every legal Jenn move gives Bela a legal response. Since only finitely many points can be chosen with mutual distances more than $1$ in a bounded interval, the game must eventually end. Jenn is the first player who can fail to move. Therefore Bela always wins."""),
        ],
    },
    "2020 AMC 12B Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12B_Answer_Key",
        "answer": ("B", "2"),
        "statement": r"""How many integers $n\ge2$ are there such that whenever $z_1,z_2,\ldots,z_n$ are complex numbers satisfying

\[|z_1|=|z_2|=\cdots=|z_n|=1\]

and

\[z_1+z_2+\cdots+z_n=0,\]

then the numbers $z_1,z_2,\ldots,z_n$ are equally spaced on the unit circle in the complex plane?""",
        "choices": [("A", "1"), ("B", "2"), ("C", "3"), ("D", "4"), ("E", "5")],
        "key_idea": "Only $n=2$ and $n=3$ force a regular configuration; all larger n have simple counterexamples.",
        "solution": [
            ("Check n = 2",
             r"""If $z_1+z_2=0$, then $z_2=-z_1$. These two points are opposite endpoints of a diameter, so they are equally spaced on the unit circle."""),
            ("Check n = 3",
             r"""If three unit complex numbers add to $0$, their vector sum forms a closed equilateral triangle. Equivalently, after rotating the picture, the only possibility is

\[1,\omega,\omega^2,\]

where $\omega$ is a primitive cube root of unity. Thus the three points are equally spaced."""),
            ("Build counterexamples for even n at least 4",
             r"""If $n$ is even and $n\ge4$, take $\frac n2$ copies of $1$ and $\frac n2$ copies of $-1$. The sum is $0$, and every number has absolute value $1$. But because values are repeated, the points are not $n$ equally spaced points around the circle."""),
            ("Build counterexamples for odd n at least 5",
             r"""If $n$ is odd and $n\ge5$, use the three cube roots

\[1,\omega,\omega^2\]

whose sum is $0$, and then add $\frac{n-3}{2}$ pairs $1,-1$. The total sum is still $0$, but the resulting list has repeated points and is not equally spaced."""),
            ("Count the valid n-values",
             r"""The property holds for $n=2$ and $n=3$, and fails for every $n\ge4$. Therefore the number of integers $n\ge2$ with the stated property is

\[2.\]"""),
        ],
    },
    "2020 AMC 12B Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12B_Answer_Key",
        "answer": ("B", "$2-\\sqrt2$"),
        "statement": r"""For each real number $a$ with $0\le a\le1$, let numbers $x$ and $y$ be chosen independently at random from the intervals $[0,a]$ and $[0,1]$, respectively, and let $P(a)$ be the probability that

\[\sin^2(\pi x)+\sin^2(\pi y)>1.\]

What is the maximum value of $P(a)$?""",
        "choices": [
            ("A", "$\\frac7{12}$"),
            ("B", "$2-\\sqrt2$"),
            ("C", "$\\frac{1+\\sqrt2}{4}$"),
            ("D", "$\\frac{\\sqrt5-1}{2}$"),
            ("E", "$\\frac58$"),
        ],
        "key_idea": "Convert the trigonometric inequality into a diamond-shaped region in the unit square.",
        "solution": [
            ("Understand the probability geometrically",
             r"""The pair $(x,y)$ is uniformly distributed over the rectangle

\[0\le x\le a,\qquad 0\le y\le1.\]

So $P(a)$ is an area inside this rectangle divided by its total area $a$."""),
            ("Find the boundary of the inequality",
             r"""The inequality

\[\sin^2(\pi x)+\sin^2(\pi y)>1\]

is equivalent to

\[\sin^2(\pi x)>\cos^2(\pi y).\]

On the unit square, the boundary lines are

\[y=\frac12-x,\quad y=x-\frac12,\quad y=x+\frac12,\quad y=\frac32-x.\]

These form a diamond with vertices $(0,\frac12)$, $(\frac12,0)$, $(1,\frac12)$, and $(\frac12,1)$."""),
            ("Compute the area for a at most one-half",
             r"""For $0\le a\le\frac12$, the vertical slice of the diamond at position $x$ has length $2x$. Thus the favorable area is

\[\int_0^a 2x\,dx=a^2.\]

Since the rectangle area is $a$, we get

\[P(a)=a.\]"""),
            ("Compute the area for a at least one-half",
             r"""For $\frac12\le a\le1$, the area up to $x=\frac12$ is $\frac14$. From $x=\frac12$ to $x=a$, the vertical slice length is $2(1-x)$. Hence the favorable area is

\[\frac14+\int_{1/2}^a2(1-x)\,dx=2a-a^2-\frac12.\]

Therefore

\[P(a)=\frac{2a-a^2-\frac12}{a}=2-a-\frac1{2a}.\]"""),
            ("Maximize the expression",
             r"""For $a\le\frac12$, the maximum is at most $\frac12$. For $a\ge\frac12$, maximize

\[2-a-\frac1{2a}.\]

Its derivative is

\[-1+\frac1{2a^2},\]

which is $0$ when $a=\frac1{\sqrt2}$. The maximum value is

\[2-\frac1{\sqrt2}-\frac{\sqrt2}{2}=2-\sqrt2.\]"""),
        ],
    },
    "2021 Spring AMC 12A Problem 25": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("E", "9"),
        "statement": r"""Let $d(n)$ denote the number of positive integers that divide $n$, including $1$ and $n$. Let

\[f(n)=\frac{d(n)}{\sqrt[3]{n}}.\]

There is a unique positive integer $N$ such that $f(N)>f(n)$ for all positive integers $n\ne N$. What is the sum of the digits of $N$?""",
        "choices": [("A", "5"), ("B", "6"), ("C", "7"), ("D", "8"), ("E", "9")],
        "key_idea": "Factor n and maximize each prime's contribution independently.",
        "solution": [
            ("Write the function prime by prime",
             r"""If

\[n=\prod p^{e_p},\]

then

\[d(n)=\prod(e_p+1)\]

and

\[\sqrt[3]{n}=\prod p^{e_p/3}.\]

Therefore

\[f(n)=\prod_p \frac{e_p+1}{p^{e_p/3}}.\]"""),
            ("Maximize one prime at a time",
             r"""For each fixed prime $p$, we choose the exponent $e$ that maximizes

\[\frac{e+1}{p^{e/3}}.\]

This works because the full expression is a product of independent prime contributions."""),
            ("Check the small primes",
             r"""For $p=2$, the best exponent is $e=3$, giving contribution

\[\frac4{2}=2.\]

For $p=3$, the best exponent is $e=2$. For $p=5$ and $p=7$, the best exponent is $e=1$."""),
            ("Show larger primes should not appear",
             r"""For $p\ge11$, even using exponent $1$ gives

\[\frac2{\sqrt[3]{p}}<1.\]

Higher exponents only become worse after the peak. So no prime $p\ge11$ appears in the maximizing integer."""),
            ("Compute N and its digit sum",
             r"""Thus

\[N=2^3\cdot3^2\cdot5\cdot7=2520.\]

The sum of the digits of $2520$ is

\[2+5+2+0=9.\]

So the answer is $9$."""),
        ],
    },
    "2021 Spring AMC 12B Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("B", "$(6,2,1)$"),
        "statement": r"""Arjun and Beth play a game in which they take turns removing one brick or two adjacent bricks from one wall among a set of several walls of bricks, with gaps possibly creating new walls. The walls are one brick tall. Arjun plays first, and the player who removes the last brick wins. For which starting configuration is there a strategy that guarantees a win for Beth?""",
        "choices": [("A", "$(6,1,1)$"), ("B", "$(6,2,1)$"), ("C", "$(6,2,2)$"), ("D", "$(6,3,1)$"), ("E", "$(6,3,2)$")],
        "key_idea": "Use Sprague-Grundy values for single walls and xor the wall values.",
        "solution": [
            ("Turn each wall into a game value",
             r"""This is an impartial game: both players have the same moves, and the last move wins. For one wall of length $n$, let $g(n)$ be its Sprague-Grundy value. A position with several walls has value equal to the xor of the wall values."""),
            ("Compute the small wall values",
             r"""A move from a wall can remove one brick or two adjacent bricks, possibly splitting the wall into two smaller walls. Using mex values gives

\[
g(1)=1,\quad g(2)=2,\quad g(3)=3,\quad g(4)=1,\quad g(5)=4,\quad g(6)=3.
\]"""),
            ("Know what a zero xor means",
             r"""A position is losing for the player to move exactly when the xor of all wall values is $0$. Since Arjun moves first, Beth has a guaranteed win precisely for the answer choice whose xor is $0$."""),
            ("Evaluate the answer choices",
             r"""Using the values above,

\[
\begin{aligned}
(6,1,1)&: 3\oplus1\oplus1=3,\\
(6,2,1)&: 3\oplus2\oplus1=0,\\
(6,2,2)&: 3\oplus2\oplus2=3,\\
(6,3,1)&: 3\oplus3\oplus1=1,\\
(6,3,2)&: 3\oplus3\oplus2=2.
\end{aligned}
\]"""),
            ("Choose the losing position for Arjun",
             r"""Only $(6,2,1)$ has xor $0$. That means Arjun starts in a losing position if both players play optimally, so Beth has a strategy that guarantees a win."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
