### Attention: letting every word look back for answers {#sec:attention}

#### The one-line intuition

A word's meaning depends on the other words in the sentence. Attention lets every word **question all the words and retrieve information by relevance** — it turns "context" from a vague notion into a weighted average you can compute in parallel.

#### An analogy: a meeting

Reading "Xiaoming left his homework in the classroom", when you hear "it" you look back for what it refers to, and when you hear "left" you ask what was left — **every word questions the other words and retrieves information by relevance**. Attention turns this moment of mental activity into an arithmetic problem: query (what am I looking for), key (the label by which I can be found), value (the content I carry) [@vaswani2017].

#### One attention step: take values by degree of match

![One step of attention](figures/src/05-02-qkv.svg){#fig:qkv}

[Figure 1-27](#fig:qkv) is one step end to end: the current word issues a **query**, each word shows its **key**, a dot product gives the degree of match, softmax normalises it into percentages, and the **values** of all words are **summed with those weights**. The output is "the new representation this word should have under these conditions". The idea was born for translation — letting each word of the translation look back at the relevant part of the source [@bahdanau2015].

#### Multi-head: several pairs of eyes, each looking at its own thing

![Multi-head attention](figures/src/05-02-heads.svg){#fig:heads}

There are many kinds of relation between one word and another: grammatical collocation, reference, modification... **Multi-head** means running several independent attentions side by side, each watching its own relations, with outputs concatenated ([Figure 1-28](#fig:heads)). The division of labour between heads is not assigned by hand; it grows by itself during training.

#### Compared with recurrent networks: Chinese whispers vs a round table

![RNN and attention](figures/src/05-02-rnn-vs-attn.svg){#fig:rnn-vs-attn}

The champion before attention was the recurrent network (RNN): read word by word, each step getting only a summary compressed from the previous word, so **distant information wears away along the way**, and a hundred steps must be computed in order. Attention lets any two words connect directly ([Figure 1-29](#fig:rnn-vs-attn)): information doesn't wear away, and computation can be parallel — exactly the promise in the title of that 2017 paper, "Attention Is All You Need" [@vaswani2017].

#### Built-in limitations: quadratic complexity

A hundred words connected pairwise is 100×100 relations; **double the context and the computation quadruples**. This is both why long contexts are expensive and the problem that [Section 1.5.3](#sec:ssm-and-linear-attention) (compressing history into a fixed state) and [Section 1.8](#sec:compute-and-deployment) (the KV cache) set out to solve.

> **Common misconceptions**
>
> The belief that "attention = human attention". It is just the name of an arithmetic operation, "take a weighted sum of values by degree of match"; the seemingly "focused" patterns on a heatmap are a by-product of optimisation, unrelated to the physiology of human attention [@vaswani2017].

#### Summary and self-check

Three sentences: attention = every word questions the other words and retrieves information weighted by match; multi-head lets different relations be watched separately; against recurrent networks it wins on both undamaged information and parallelism, at the price of quadratic complexity.

Two self-check questions:

1. Context doubles from 4,000 tokens to 8,000 — how many times does the attention computation grow?
2. Why does attention "solve the information wear of recurrent networks"? (Hint: the connections in [Figure 1-29](#fig:rnn-vs-attn).)

**Maths note.** One attention step: $\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d}}\right)V$. $Q$, $K$ and $V$ are the query, key and value matrices; $\sqrt{d}$ is a scaling factor (it stops large dot products from pushing softmax into extreme distributions). Multi-head means doing this $h$ times in parallel and concatenating.
