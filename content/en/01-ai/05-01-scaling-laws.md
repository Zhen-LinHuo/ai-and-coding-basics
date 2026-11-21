### Why scale works: scaling laws {#sec:scaling-laws}

#### The one-line intuition

In this field, "bigger" is not a mystical slogan but a **curve you can draw in advance**: make the model bigger (parameters, data and compute all growing together) and the loss falls along a smooth power law, with the amount of the fall predictable before training starts. This curve is the scaling law, and it is the ledger that lets the whole industry stake billions on it.

#### An analogy: economies of scale

Double a factory's output and unit cost falls by a fixed proportion — that is economies of scale in industry. Large models moved this onto "intelligence": **each time inputs (compute, data, parameters) multiply, the loss falls by a fixed proportion, and that proportion can be predicted in advance** [@kaplan2020]. It is not "bigger might be better" but "bigger is necessarily better along a curve" — and that curve is exactly what let the whole industry bet billions.

#### What the scaling law is saying

![The scaling line on log-log axes](figures/src/05-01-scaling.svg){#fig:scaling}

Plot both loss and compute on logarithmic axes and the measured points land almost on a straight line ([Figure 1-24](#fig:scaling)) — that is the **scaling law**. What it means in practice: **to test whether a bigger model is better, you don't have to build it; read the line and you can quote a price.**

#### The 2022 correction: invest on both sides

Compute gets spent in two places: **parameters** (brain capacity) and **data** (the textbooks). The 2022 Chinchilla work corrected the earlier imbalance — given a fixed compute budget, parameters and data should be **scaled up in proportion**, with roughly 20 words of text per parameter [@hoffmann2022] ([Figure 1-25](#fig:budget)). Earlier large models generally had "a huge brain and too little reading"; the same compute could have bought a lower loss.

![Three ways to split a fixed budget](figures/src/05-01-budget.svg){#fig:budget}

#### Built-in limitations: diminishing returns and the data wall

A power law is a curve that flattens (a straight line in log-log, increasingly flat in ordinary coordinates): **the loss is still falling, but each equal drop in loss costs several times the input** ([Figure 1-26](#fig:diminishing)). A harder constraint is **the data wall** — high-quality public text is close to exhausted, so the "feed it more data" leg stops first [@hoffmann2022].

![Diminishing returns and the data wall](figures/src/05-01-diminishing.svg){#fig:diminishing}

> **Common misconceptions**
>
> Two of them. One: "the scaling law is a law" — it is an empirical regularity, not a law of physics; change the data quality or the architecture and the curve moves. Two: "falling loss = capability rising in proportion" — loss is only a proxy, and some capabilities (reasoning, multi-step calculation) appear more abruptly and are harder to predict. That is called **emergence**, and it is itself contested.

#### Summary and self-check

Three sentences: loss against compute is close to a straight line on log-log axes, and that is what the industry dares to bet on; the budget has to be split in proportion between parameters and data; the flattening curve and the data wall show that "bigger" is no perpetual motion machine.

Two self-check questions:

1. A company doubles its compute. Under Chinchilla, should it double parameters, double data, or double only one?
2. Why does the data wall push the industry to research synthetic data and small models? (Hint: which of the two legs stops first?)
