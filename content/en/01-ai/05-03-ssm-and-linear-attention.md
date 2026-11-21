### Linear attention and state space models: the RNN strikes back {#sec:ssm-and-linear-attention}

#### The one-line intuition

The quadratic complexity left by [the previous section](#sec:attention) has a surprising solution: **bring the old champion, the RNN, back**. Take the softmax out of attention and the same network can be rewritten as an RNN that "carries a fixed state and recurs word by word" — constant cache, linear speed. This is the shared idea of linear attention and state space models (SSMs) [@katharopoulos2020][@gu2023].

#### An analogy: meeting minutes

After a two-hour meeting you need to quote a sentence. You have two options: **go through the whole recording** (attention: exact, but you must play it all back); **carry a single page of minutes** (state: one page in your pocket, but details are compressed away).

Attention chooses to keep everything, with a cache that grows with the length of the meeting; RNNs/SSMs choose to keep only a summary, with a constant pocket. This section is about **how to take the minutes so that less is lost.**

#### The problem it solves: one formula, two algorithms

![Pair up first, or accumulate state first](figures/src/05-03-linear-attn.svg){#fig:linear-attn}

Attention outputs a "weighted sum". Mathematically, once the softmax is removed, the expression "(QKᵀ)V" can be computed in a different order using **associativity**: first accumulate a state matrix from K and V, then query it with Q ([Figure 1-31](#fig:linear-attn)). The result is identical, but the second order can **recur step by step** — a word arrives, the state is updated once, no need to look back over all history.

The recurrent version is an RNN: fixed state size, constant memory, linear speed. **It trains like attention (parallel) and infers like an RNN (thrifty with memory)** — one network, two forms.

![Recurrence: fixed-state word-by-word updates](figures/src/05-03-recurrence.svg){#fig:recurrence}

#### State space models: making "what to remember" learnable

![Full cache vs fixed state](figures/src/05-03-state-compare.svg){#fig:state-compare}

SSMs write the recurrence in a more general form: new state = decay of the old state + injection of the new input, **with how much to decay and how much to inject learned by the network itself**. RWKV rewrites attention into a purely recurrent form [@peng2023]; Mamba adds "selectivity" to the state — **the current input decides what gets written into the state and what is discarded** [@gu2023], which is exactly how you learn "which line belongs in the minutes".

#### Built-in limitations: exact recall is the weak spot

A fixed state is one sheet of paper: **write a hundred thousand words of history into it and the sheet is still that size**. Ask it to "find a particular sentence verbatim in a long document" and a pure SSM often fails — the detail has been compressed away. Attention, which looks back over the full history, is strong at finding details.

So the mainstream after 2025 is not replacement but **hybrids**: most layers use cheap linear/SSM layers for long-range continuity, a few layers use attention for exact recall ([Figure 1-32](#fig:mix)).

![Hybrids between the two extremes](figures/src/05-03-mix.svg){#fig:mix}

> **Common misconceptions**
>
> The belief that "SSMs will replace attention". The popularity of hybrid architectures shows precisely that the two are complements: one handles cheap long-range memory, the other expensive exact recall. Replacement theories appear every few months, yet the hybrid share keeps growing.

#### Summary and self-check

Three sentences: remove the softmax and attention can be rewritten as a recurrence with a fixed state; SSMs make "what to remember" learnable; pure SSMs lose on exact recall, and the mainstream answer is hybrid architecture.

Two self-check questions:

1. At a context of 100k tokens, roughly how many times larger is the pure-attention cache than a fixed state? (An order-of-magnitude estimate is enough.)
2. Why is a hybrid architecture more reliable than a pure SSM at tasks like "find a particular clause verbatim in a contract"?

**Maths note.** Recurrence: $h_t = A\,h_{t-1} + B\,x_t$, output $y_t = C\,h_t$; $A$ is the decay (learnable), $B$ the injection. Linear attention (no softmax) satisfies $y_t = Q_t \sum_{i\le t} K_i^\top V_i = Q_t\, S_t$, where $S_t = S_{t-1} + K_t^\top V_t$ — that is the "state accumulation" form.
