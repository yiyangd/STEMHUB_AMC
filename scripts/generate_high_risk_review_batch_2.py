import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 2"
base.BATCH_NUMBER = 286
base.REVIEW_SKIPPED = [
    "2021 Fall AMC 12A Problem 18: local CSV statement does not match the AoPS Fall problem statement; skipped for data repair before page generation.",
    "2021 Fall AMC 12A Problem 19: local CSV statement does not match the AoPS Fall problem statement; skipped for data repair before page generation.",
]

base.PROBLEMS = {
    "2016 AMC 12A Problem 14": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2016_AMC_12A_Answer_Key",
        "answer": ("C", "6"),
        "statement": "Each vertex of a cube is to be labeled with an integer $1$ through $8$, with each integer being used once, in such a way that the sum of the four numbers on the vertices of a face is the same for each face. Arrangements that can be obtained from each other through rotations of the cube are considered to be the same. How many different arrangements are possible?",
        "choices": [("A", "1"), ("B", "3"), ("C", "6"), ("D", "12"), ("E", "24")],
        "key_idea": "First force the common face sum to be 18, then count valid labeled cubes and divide by the 24 rotations of a cube.",
        "solution": [
            ("Find the common face sum",
             "The labels add to\n\n\\[1+2+\\cdots+8=36.\\]\n\nOpposite faces together contain all eight vertices. If every face has the same sum $S$, then two opposite faces have total $2S=36$, so\n\n\\[S=18.\\]\n\nThus every face must have vertex-label sum $18$."),
            ("Set up a reproducible finite count",
             "Fix one face of the cube, say the face $x=0$. The four labels on that face must be a $4$-element subset of $\\{1,2,\\ldots,8\\}$ with sum $18$.\n\nThe possible sets are\n\n\\[(1,2,7,8),(1,3,6,8),(1,4,5,8),(1,4,6,7),\\]\n\\[(2,3,5,8),(2,3,6,7),(2,4,5,7),(3,4,5,6).\\]"),
            ("Check the opposite face using side-face equations",
             "After the labels on the fixed face are ordered, the remaining four labels go on the opposite face. We only need to check two independent adjacent side-face sums, because the opposite pairs of faces already total $36$.\n\nFor each ordered fixed face, there are at most $4!=24$ possible orders for the opposite face, so this is a small exact count, not an estimate."),
            ("Use the count table",
             "Carrying out that check gives the following numbers of labeled cubes for the eight possible fixed-face sets:\n\n\\[16,16,16,24,24,16,16,16.\\]\n\nTherefore the total number of labeled arrangements with a specified face position is\n\n\\[16+16+16+24+24+16+16+16=144.\\]"),
            ("Account for rotations",
             "Because all labels are distinct, no nontrivial rotation can leave a labeled cube unchanged. Each rotational equivalence class therefore contains exactly $24$ labeled arrangements.\n\nSo the number of arrangements up to rotation is\n\n\\[\\frac{144}{24}=6.\\]\n\nThe answer is $6$."),
        ],
    },
    "2016 AMC 12B Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2016_AMC_12B_Answer_Key",
        "answer": ("B", "[201,400]"),
        "statement": "For a certain positive integer $n<1000$, the decimal equivalent of $\\frac1n$ is $0.\\overline{abcdef}$, a repeating decimal of period $6$, and the decimal equivalent of $\\frac1{n+6}$ is $0.\\overline{wxyz}$, a repeating decimal of period $4$. In which interval does $n$ lie?",
        "choices": [("A", "$[1,200]$"), ("B", "$[201,400]$"), ("C", "$[401,600]$"), ("D", "$[601,800]$"), ("E", "$[801,999]$")],
        "key_idea": "A period condition means the denominator divides a repunit of that length but not a shorter one.",
        "solution": [
            ("Translate repeating periods into divisibility",
             "If $\\frac1d$ has repeating period $r$, then $d$ divides\n\n\\[10^r-1.\\]\n\nThe period is exactly $r$ only if $d$ does not divide any $10^k-1$ for a smaller positive $k$."),
            ("Use the period 4 condition first",
             "The denominator $n+6$ has period $4$, so it divides\n\n\\[10^4-1=9999.\\]\n\nIt must not have a smaller period. Since $n<1000$, we only need divisors $n+6<1006$."),
            ("List the possible values of n+6",
             "The divisors of $9999$ below $1006$ that have exact period $4$ are\n\n\\[101,303,909.\\]\n\nTherefore the possible values of $n$ are\n\n\\[95,297,903.\\]"),
            ("Check the period 6 condition for n",
             "Now $\\frac1n$ must have exact period $6$. The value $n=95$ is impossible because it is divisible by $5$, so its decimal does not have a purely repeating period of $6$.\n\nFor $n=903$, the period is $42$, not $6$. For $n=297$, the period is exactly $6$."),
            ("Choose the interval",
             "Thus\n\n\\[n=297.\\]\n\nThis lies in the interval $[201,400]$, so the answer is $[201,400]$."),
        ],
    },
    "2021 Spring AMC 12B Problem 13": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12B_Answer_Key",
        "answer": ("D", "6"),
        "statement": "How many values of $\\theta$ in the interval $0<\\theta\\le2\\pi$ satisfy\n\n\\[1-3\\sin\\theta+5\\cos3\\theta=0?\\]",
        "choices": [("A", "2"), ("B", "4"), ("C", "5"), ("D", "6"), ("E", "8")],
        "key_idea": "Use the tangent half-angle substitution to turn the trigonometric equation into a polynomial root count.",
        "solution": [
            ("Use a substitution that avoids graph guessing",
             "The expression contains both $\\sin\\theta$ and $\\cos3\\theta$, so direct factoring is not obvious. A reliable way to count roots is the tangent half-angle substitution\n\n\\[t=\\tan\\frac{\\theta}{2}.\\]\n\nThis gives a one-to-one correspondence from $0<\\theta<\\pi$ to $t>0$ and from $\\pi<\\theta<2\\pi$ to $t<0$."),
            ("Convert the equation to a polynomial",
             "Using\n\n\\[\\sin\\theta=\\frac{2t}{1+t^2},\\qquad \\cos\theta=\\frac{1-t^2}{1+t^2},\\]\n\nand $\\cos3\\theta=4\\cos^3\\theta-3\\cos\\theta$, the equation becomes\n\n\\[2t^6+3t^5-39t^4+6t^3+36t^2+3t-3=0.\\]\n\nSo the original problem has no more than $6$ solutions away from the endpoints."),
            ("Show that six real roots actually occur",
             "Let\n\n\\[P(t)=2t^6+3t^5-39t^4+6t^3+36t^2+3t-3.\\]\n\nA sign check gives changes of sign on the six disjoint intervals\n\n\\[(-6,-5),\\quad (-1,-\\tfrac12),\\quad (-\\tfrac25,-\\tfrac14),\\]\n\\[(0,\\tfrac12),\\quad (1,2),\\quad (3,4).\\]\n\nBy the Intermediate Value Theorem, $P(t)$ has at least one real root in each interval."),
            ("Use the degree to finish the count",
             "Because $P(t)$ is a degree-$6$ polynomial, it can have at most $6$ real roots. The six sign-change intervals already force at least $6$ real roots, so it has exactly $6$ real roots."),
            ("Check the endpoints and translate back",
             "The endpoints do not add extra solutions: at $\\theta=2\\pi$, the left side is $1+5=6$, and $\\theta=0$ is not included. Also $\\theta=\\pi$ gives $1+5\\cos3\\pi=-4$, so it is not a solution.\n\nThus the number of values of $\\theta$ is $6$."),
        ],
    },
}


if __name__ == "__main__":
    base.main()
