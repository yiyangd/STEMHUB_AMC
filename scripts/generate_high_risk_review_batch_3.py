import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 3"
base.BATCH_NUMBER = 287
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2014 AMC 12A Problem 21": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("A", "1"),
        "statement": "For every real number $x$, let $\\lfloor x\\rfloor$ denote the greatest integer not exceeding $x$, and let\n\n\\[f(x)=\\lfloor x\\rfloor(2014^{x-\\lfloor x\\rfloor}-1).\\]\n\nThe set of all numbers $x$ such that $1\\le x<2014$ and $f(x)\\le1$ is a union of disjoint intervals. What is the sum of the lengths of those intervals?",
        "choices": [
            ("A", "1"),
            ("B", "$\\dfrac{\\log 2015}{\\log 2014}$"),
            ("C", "$\\dfrac{\\log 2014}{\\log 2013}$"),
            ("D", "$\\dfrac{2014}{2013}$"),
            ("E", "$2014^{1/2014}$"),
        ],
        "key_idea": "Write $x$ as an integer part plus a fractional part, then use a telescoping logarithm sum.",
        "solution": [
            ("Separate the integer and fractional parts",
             "The floor function tells us to look at one interval at a time. Let\n\n\\[k=\\lfloor x\\rfloor.\\]\n\nBecause $1\\le x<2014$, the integer $k$ can be any value from $1$ through $2013$. On the interval $k\\le x<k+1$, the floor value is fixed, so the expression becomes easier to handle."),
            ("Rewrite the inequality on one fixed interval",
             "For a fixed $k$, we have\n\n\\[f(x)=k(2014^{x-k}-1).\\]\n\nThe condition $f(x)\\le1$ is therefore\n\n\\[k(2014^{x-k}-1)\\le1.\\]\n\nSince $k>0$, this is equivalent to\n\n\\[2014^{x-k}\\le1+\\frac1k=\\frac{k+1}{k}.\\]"),
            ("Turn the exponential inequality into an interval length",
             "Taking logarithms base $2014$ gives\n\n\\[x-k\\le \\log_{2014}\\left(\\frac{k+1}{k}\\right).\\]\n\nSo the allowed values of $x$ in the $k$th interval run from $k$ to\n\n\\[k+\\log_{2014}\\left(\\frac{k+1}{k}\\right).\\]\n\nThus the length contributed by this $k$ is exactly $\\log_{2014}\\left(\\frac{k+1}{k}\\right)$."),
            ("Add the lengths and look for cancellation",
             "The total length is\n\n\\[\\sum_{k=1}^{2013}\\log_{2014}\\left(\\frac{k+1}{k}\\right).\\]\n\nA natural reason to use logarithms here is that a sum of logs becomes the log of a product. Therefore\n\n\\[\\sum_{k=1}^{2013}\\log_{2014}\\left(\\frac{k+1}{k}\\right)=\\log_{2014}\\left(\\prod_{k=1}^{2013}\\frac{k+1}{k}\\right).\\]"),
            ("Finish the telescoping product",
             "The product cancels almost completely:\n\n\\[\\prod_{k=1}^{2013}\\frac{k+1}{k}=\\frac21\\cdot\\frac32\\cdot\\frac43\\cdots\\frac{2014}{2013}=2014.\\]\n\nSo the total length is\n\n\\[\\log_{2014}(2014)=1.\\]\n\nThe answer is $1$."),
        ],
    },
    "2014 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("B", "279"),
        "statement": "The number $5^{867}$ is between $2^{2013}$ and $2^{2014}$. How many pairs of integers $(m,n)$ are there such that $1\\le m\\le2012$ and\n\n\\[5^n<2^m<2^{m+2}<5^{n+1}?\\]",
        "choices": [("A", "278"), ("B", "279"), ("C", "280"), ("D", "281"), ("E", "282")],
        "key_idea": "Count how often three consecutive powers of 2 fit between two consecutive powers of 5.",
        "solution": [
            ("Interpret the inequality visually on a number line",
             "The inequality\n\n\\[5^n<2^m<2^{m+2}<5^{n+1}\\]\n\nmeans that the three consecutive powers $2^m,2^{m+1},2^{m+2}$ all lie strictly between two consecutive powers of $5$. So each valid pair corresponds to an interval $(5^n,5^{n+1})$ that contains three powers of $2$."),
            ("Notice that each interval contains only two or three powers of 2",
             "Between $5^n$ and $5^{n+1}$, the ratio of the endpoints is $5$. Since\n\n\\[2^2=4<5<8=2^3,\\]\n\nthere are at least two powers of $2$ in such intervals often, but there can never be four consecutive powers of $2$ inside one interval. Thus each interval contributes either two or three powers of $2$."),
            ("Count all powers of 2 before $5^{867}$",
             "We are told\n\n\\[2^{2013}<5^{867}<2^{2014}.\\]\n\nTherefore the powers $2^1,2^2,\\ldots,2^{2013}$ are exactly the positive powers of $2$ below $5^{867}$. There are $2013$ such powers."),
            ("Set up a total-count equation",
             "There are $867$ intervals from $5^0$ to $5^{867}$:\n\n\\[(5^0,5^1),(5^1,5^2),\\ldots,(5^{866},5^{867}).\\]\n\nLet $T$ be the number of these intervals that contain three powers of $2$. The other $867-T$ intervals contain two powers of $2$. Since the total number of powers counted is $2013$,\n\n\\[3T+2(867-T)=2013.\\]"),
            ("Solve and connect back to pairs",
             "Solving gives\n\n\\[3T+1734-2T=2013,\\]\n\nso\n\n\\[T=279.\\]\n\nEach interval with three powers of $2$ determines exactly one starting exponent $m$, namely the first of those three exponents. Therefore the number of valid pairs $(m,n)$ is $279$."),
        ],
    },
    "2014 AMC 12A Problem 23": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("B", "883"),
        "statement": "The fraction\n\n\\[\\frac1{99^2}=0.\\overline{b_{n-1}b_{n-2}\\ldots b_2b_1b_0},\\]\n\nwhere $n$ is the length of the period of the repeating decimal expansion. What is the sum $b_0+b_1+\\cdots+b_{n-1}$?",
        "choices": [("A", "874"), ("B", "883"), ("C", "887"), ("D", "891"), ("E", "892")],
        "key_idea": "Recognize the repeating block of $1/99^2$ as two-digit blocks and then sum their digits.",
        "solution": [
            ("Use the special role of 99",
             "The denominator $99$ is useful because\n\n\\[\\frac1{99}=0.\\overline{01}.\\]\n\nSquaring the denominator suggests that the decimal for $\\frac1{99^2}$ should have a pattern organized in two-digit blocks rather than single digits."),
            ("Find the repeating block pattern",
             "A short long-division pattern gives\n\n\\[\\frac1{99^2}=0.\\overline{000102030405\\ldots 969799}.\\]\n\nThe block is made of two-digit entries. It goes from $00$ through $97$, then ends with $99$. The two-digit block $98$ is skipped because the carrying at the end of the period changes the final blocks."),
            ("Translate the question into a digit sum",
             "The problem asks for the sum of all digits in one full repeating period. Since the period consists of two-digit blocks, we can compare it with the easier list\n\n\\[00,01,02,\\ldots,98,99.\\]\n\nThat full list contains every two-digit number from $00$ to $99$."),
            ("Sum the digits in the full two-digit list",
             "In the ones place, each digit $0$ through $9$ appears $10$ times. In the tens place, each digit $0$ through $9$ also appears $10$ times. Therefore the total digit sum for $00$ through $99$ is\n\n\\[2\\cdot10(0+1+\\cdots+9)=20\\cdot45=900.\\]"),
            ("Subtract the missing block",
             "The actual repeating block skips $98$. The digit sum of $98$ is\n\n\\[9+8=17.\\]\n\nTherefore the desired digit sum is\n\n\\[900-17=883.\\]\n\nThe answer is $883$."),
        ],
    },
    "2014 AMC 12A Problem 24": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2014_AMC_12A_Answer_Key",
        "answer": ("C", "301"),
        "statement": "Let $f_0(x)=x+|x-100|-|x+100|$, and for $n\\ge1$, let\n\n\\[f_n(x)=|f_{n-1}(x)|-1.\\]\n\nFor how many values of $x$ is $f_{100}(x)=0$?",
        "choices": [("A", "299"), ("B", "300"), ("C", "301"), ("D", "302"), ("E", "303")],
        "key_idea": "Work backward through the map $y\\mapsto |y|-1$, then count how many $x$ values give each starting value under $f_0$.",
        "solution": [
            ("Separate the two layers of the problem",
             "The function $f_0$ first turns $x$ into some value $y$. After that, every step applies the same rule\n\n\\[g(y)=|y|-1.\\]\n\nSo the problem becomes: which starting values $y=f_0(x)$ satisfy $g^{100}(y)=0$, and how many $x$ values produce those $y$ values?"),
            ("Work backward from 0 through the repeated rule",
             "If $g(y)=a$, then\n\n\\[|y|-1=a,\\]\n\nso\n\n\\[|y|=a+1.\\]\n\nThis has solutions $y=\\pm(a+1)$ whenever $a\\ge -1$. Starting from $0$ and working backward repeatedly produces a clear pattern: after $100$ steps, the possible starting values are\n\n\\[-100,-98,-96,\\ldots,96,98,100.\\]\n\nThere are $101$ such values."),
            ("Understand how many x-values give one y-value",
             "Now analyze\n\n\\[f_0(x)=x+|x-100|-|x+100|.\\]\n\nBreak the real line at $x=-100$ and $x=100$. This gives\n\n\\[f_0(x)=\\begin{cases}x+200,&x<-100,\\\\-x,&-100\\le x<100,\\\\x-200,&x\\ge100.\\end{cases}\\]\n\nThis piecewise form lets us count preimages without drawing a complicated graph."),
            ("Count preimages for interior and endpoint y-values",
             "For $-100<y<100$, each of the three pieces can produce that $y$, so there are $3$ corresponding values of $x$. For $y=100$ and $y=-100$, only two pieces produce the value because of the endpoint conditions."),
            ("Finish the count",
             "Among the $101$ possible $y$-values, the two endpoint values $-100$ and $100$ each have $2$ preimages. The remaining $99$ values each have $3$ preimages. Therefore the number of solutions is\n\n\\[2+2+99\\cdot3=301.\\]\n\nThe answer is $301$."),
        ],
    },
    "2015 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12A_Answer_Key",
        "answer": ("D", "8"),
        "statement": "For each positive integer $n$, let $S(n)$ be the number of sequences of length $n$ consisting solely of the letters $A$ and $B$, with no more than three $A$s in a row and no more than three $B$s in a row. What is the remainder when $S(2015)$ is divided by $12$?",
        "choices": [("A", "0"), ("B", "4"), ("C", "6"), ("D", "8"), ("E", "10")],
        "key_idea": "Group valid sequences by their final run and compute a short recurrence modulo small numbers.",
        "solution": [
            ("Model the last run instead of the whole sequence",
             "The condition only cares about consecutive equal letters, so a natural approach is to build sequences by runs. Let $A(n)$ be the number of valid length-$n$ sequences ending in $A$. By symmetry, the same number end in $B$, so\n\n\\[S(n)=2A(n).\\]\n\nThis means we only need to understand $A(n)$."),
            ("Derive the recurrence",
             "A valid sequence ending in $A$ can end with exactly one, two, or three $A$s. Immediately before that final run, the sequence must either end in $B$ or be empty. By symmetry, this gives\n\n\\[A(n)=A(n-1)+A(n-2)+A(n-3)\\]\n\nfor the modular pattern we need, with initial values\n\n\\[A(0)=1,\\quad A(1)=1,\\quad A(2)=2.\\]"),
            ("Reduce the target modulus",
             "We want $S(2015)\\pmod{12}$. Since $S(n)=2A(n)$, it is enough to know $A(2015)\\pmod6$. To find a residue modulo $6$, we can combine information modulo $2$ and modulo $3$."),
            ("Find the pattern modulo 2",
             "Using the recurrence modulo $2$, the values of $A(n)$ begin\n\n\\[1,1,0,0,1,1,0,0,\\ldots\\]\n\nwith period $4$. Since\n\n\\[2015\\equiv3\\pmod4,\\]\n\nwe get\n\n\\[A(2015)\\equiv0\\pmod2.\\]"),
            ("Find the pattern modulo 3",
             "Using the same recurrence modulo $3$, the sequence has period $13$, and it begins\n\n\\[1,1,2,1,1,1,0,2,0,2,1,0,0,\\ldots\\]\n\nSince\n\n\\[2015=13\\cdot155,\\]\n\nwe have\n\n\\[A(2015)\\equiv A(0)\equiv1\\pmod3.\\]"),
            ("Combine the residues and answer the question",
             "The number congruent to $0$ modulo $2$ and $1$ modulo $3$ is\n\n\\[A(2015)\equiv4\\pmod6.\\]\n\nTherefore\n\n\\[S(2015)=2A(2015)\equiv 2\\cdot4=8\\pmod{12}.\\]\n\nThe answer is $8$."),
        ],
    },
}


if __name__ == "__main__":
    base.main()
