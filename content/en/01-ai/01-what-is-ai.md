## What artificial intelligence is {#sec:what-is-ai}

### The one-line intuition

Artificial intelligence is not a product and not a technology: it is a **goal** — getting machines to do "the things that need intelligence". When that goal was written down in 1955 [@mccarthy1955], the authors themselves could not say clearly what it covered. Seventy years on, its boundary is still moving.

This section does not try to define AI. Its job is to give you a **map**: from now on, whenever you hear a new word — large model, agent, deep learning — you can put it in the right place on that map and say how it relates to the layer next to it.

### An analogy: three generations of spam filtering

Think of one concrete task: deciding whether an email is spam.

**First generation: people write the rules.** "Block anything containing the word 'prize'." The machine only executes; all the intelligence sits in the head of the person writing the rules. Systems like this are still everywhere today, but their name is not AI, it is **automation**.

**Second generation: the machine learns the rules.** Give it ten thousand emails already labelled "spam / not spam" by humans and let it find the pattern itself. People no longer write rules; they supply two things only — the **raw material** (data) and the **marking scheme** (right or wrong). That is machine learning.

**Third generation: the machine does the job itself.** No labels at all; the machine discovers for itself that emails fall naturally into a few categories. Today's large language models mostly live on top of this layer — they do not just judge, they **generate** things that did not exist before.

![Three ways of tackling the same task](figures/src/01-01-ladder.svg)

The difference between these three generations is a difference in where the intelligence sits: in the first, in rules written by people; in the second, in parameters tuned from examples; in the third, in structure the machine finds for itself. Later chapters will come back to this ladder again and again.

### Four words, one map

Four words that the news mixes up freely are in fact nested inside one another ([the figure below](#fig:ai-nested)):

**Artificial intelligence** is the outermost goal. **Machine learning** is currently the main means of reaching it — tuning parameters from data. **Deep learning** is one branch of machine learning, using neural networks with many layers. **Large language models** are one product of deep learning. Almost everything called "AI" in the news today lives in the innermost ring; but the outer rings have not vanished — the robot arms in a factory, the route planning in a maps app, all of that is artificial intelligence too, just not the star of the news.

![How artificial intelligence, machine learning, deep learning and large language models nest](figures/src/01-01-nested.svg){#fig:ai-nested}

The point of the concentric circles is **positioning**. When you hear a new term, ask which layer it sits in, then ask how it relates to the neighbouring layer, and you will usually know which chapter's tools to reach for.

### Built-in limitations: the hard things are easy, the easy things are hard

The definition "the things that need intelligence" hides a trap: **the word "intelligence" overrates the difficulty of some problems and underrates others.**

Getting a machine to play Go beat the world champion back in 1997; getting a machine to cross a living room without hitting the furniture is still an open problem for the robotics industry. Getting a machine to recite the whole encyclopaedia is trivial; getting a machine to recognise the same cat in two photographs took decades to do properly. The psychologist Moravec summed up this contrast in one line: it is comparatively easy to make computers exhibit adult-level performance on intelligence tests or checkers, and difficult or impossible to give them the perceptual and mobility skills of a one-year-old [@moravec1988].

![The Moravec paradox](figures/src/01-01-moravec.svg){#fig:ai-moravec}

The reason is not the machine, it is **evolution**: walking, recognising cats, hearing tone of voice are instincts polished over hundreds of millions of years. They feel effortless to us because evolution has hidden the computation behind them. Chess and arithmetic are only a few thousand years old; we have to work hard to learn them, and every rule sits out in the open — **what sits out in the open, a machine can copy**. This asymmetry is one of the base colours of the whole book: what a machine is good at never depends on how hard the task is for a person, but on whether the task's regularity can be expressed in data.

> **Common misconceptions**
>
> Thinking "AI is a thing", which is why questions like "when will AI take over the world" get asked. In reality AI is a set of goals whose boundary has been redrawn continuously for seventy years: today's AI and the AI of 1990 share only a name. A misconception of the same kind is "it can play chess, so it can think" — playing chess only shows that one particular datafied task is done well; see the green region in [the figure above](#fig:ai-moravec).

### Summary and self-check

Three sentences: AI is a goal, not a product; machine learning replaces "people write the rules" with "data plus a marking scheme"; and how strong a machine is does not follow how hard the task is for people, but whether the task's regularity can be expressed in data.

Two questions to check yourself:

1. A meeting-scheduling system that "reads" emails and replies automatically — which generation does it belong to? And if its reading ability comes from a large language model?
2. Why does "machines will never walk the way people do" need reassessing after the 2010s? (Hint: computation that evolution has hidden does not have to stay hidden forever.)
