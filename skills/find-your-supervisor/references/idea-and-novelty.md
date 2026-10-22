# Idea formation, prior-art search and originality gates

## The right output is a falsifiable scientific claim

1. Start with failure case and task consequence, not an attractive architecture name.
2. Translate research DNA into **design hypotheses** (e.g., structured memory helps long occlusion at fixed tokens). Do not assert copied ideas are novel.
3. Search the latest 3–8 closest works using multiple author-independent queries, venue archives, arXiv, code search and citations. Specify date; if live lookup unavailable, mark novelty unverified.
4. Produce overlap table: idea component, nearest paper, what exactly overlaps, what is materially different, new test to decide, novelty confidence.
5. Find two **killer baselines**: no new module and strongest low-compute nearest competitor. Matched parameters / data / latency where relevant.
6. Build the cheapest **counterexample** likely to falsify the core mechanism. If simple 2D saliency, FIFO cache or larger encoder matches gains, the proposed 3D mechanism is not validated.
7. Predeclare stop/go/pivot conditions. Avoid retrofitting the hypothesis after looking at test data.

## Research-grade novelty checklist

- Is change representational, optimization-based, data-based, evaluation-based or a mere module assembly?
- Is the claim scientifically interesting beyond one benchmark and is mechanism measurable?
- Does improvement survive matched training resources and data splits?
- What would a skeptical reviewer say? Write rejection points before coding.
- Does the proposed first paper create reusable data/tooling for next projects?

Output no more than three candidate hypotheses per request and only one recommended pilot until evidence warrants expansion.
