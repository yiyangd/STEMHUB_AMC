import generate_high_risk_review_batch as base


base.BATCH_LABEL = "High-risk reviewed problem pages batch 17"
base.BATCH_NUMBER = 301
base.REVIEW_SKIPPED = []

base.PROBLEMS = {
    "2012 AMC 12A Problem 22": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2012_AMC_12A_Answer_Key",
        "answer": ("C", "$20$"),
        "statement": r"""Distinct planes $p_1,p_2,\ldots,p_k$ intersect the interior of a cube $Q$. Let $S$ be the union of the faces of $Q$ and let

\[P=\bigcup_{j=1}^k p_j.\]

The intersection of $P$ and $S$ consists of the union of all segments joining the midpoints of every pair of edges belonging to the same face of $Q$. What is the difference between the maximum and minimum possible values of $k$?""",
        "choices": [("A", "$8$"), ("B", "$12$"), ("C", "$20$"), ("D", "$23$"), ("E", "$24$")],
        "key_idea": "Classify the possible plane sections of the cube whose boundary traces are midpoint-to-midpoint segments on faces.",
        "solution": [
            ("Understand what must appear on each face",
             r"""On each square face of the cube there are $4$ edge midpoints. The problem wants every segment joining two of these midpoints.

Each face therefore contributes

\[\binom42=6\]

segments. Across the $6$ faces of the cube, there are

\[6\cdot6=36\]

face-segments, which we will call traces."""),
            ("Separate the traces into two types",
             r"""On a square face, a segment joining midpoints of adjacent edges is a short trace. There are $4$ such traces per face, so the cube has

\[6\cdot4=24\]

short traces.

A segment joining midpoints of opposite edges is a long trace. There are $2$ such traces per face, so the cube has

\[6\cdot2=12\]

long traces."""),
            ("Classify the possible plane sections",
             r"""A plane cutting a cube can meet at most $6$ faces, so its section with the cube can have at most $6$ boundary traces.

If all boundary traces are allowed midpoint-to-midpoint traces, the possible sections are:

- $8$ triangular sections, one near each vertex, using $3$ short traces.
- $12$ rectangular sections, using a mix of allowed traces.
- $4$ central hexagonal sections, each using $6$ short traces.
- $3$ central square sections, each using $4$ long traces.

These are the only possibilities because once a plane contains one allowed trace on a face, the trace on each adjacent face is forced by coplanarity."""),
            ("Find the maximum possible k",
             r"""For the maximum, we may include every distinct plane whose traces are all allowed traces. Adding such a plane creates no forbidden segment on the surface of the cube.

So the largest possible value is the total number of possible planes:

\[8+12+4+3=27.\]"""),
            ("Find a lower bound for the minimum",
             r"""To cover all $36$ traces, each plane can contribute at most $6$ traces. If $k\le6$, then every plane would need to contribute exactly $6$ new traces with no overlap.

But a $6$-trace section of this kind is one of the central hexagons, and those contain only short traces. They cannot cover the $12$ long traces.

Therefore

\[k\ge7.\]"""),
            ("Show that seven planes are enough",
             r"""Now use the $4$ central hexagonal planes and the $3$ central square planes.

The $4$ hexagonal planes cover all $24$ short traces. The $3$ square planes cover all $12$ long traces.

Together they cover exactly the required $36$ traces, so the minimum possible value is

\[k=7.\]"""),
            ("Finish",
             r"""The difference between the maximum and minimum possible values of $k$ is

\[27-7=20.\]

Therefore the answer is $20$."""),
        ],
    },
}


if __name__ == "__main__":
    base.main()
