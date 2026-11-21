## Making it behave: alignment, hallucination and safety {#sec:alignment-hallucination-safety}

### The one-line intuition

The model that left the factory in [Section 1.5](#sec:llms) only knows how to "continue web pages" — ask it a question and it may well invent ten similar questions. Between "can talk" and "actually useful" lies a stretch of **factory education**: first demonstration, then fine-tuning. And the two problems this education cannot fix — hallucination and jailbreaks — each have their own mechanistic roots.

This section answers the three most common questions: why can it "answer questions"? Why does it say things that are confidently wrong? What do the safety guardrails actually block, and what do they cost?

### An analogy: onboarding a new employee

Pretraining is like **reading every document the company has amassed over ten years** — astonishing breadth, but a feral way of working: ask it to "write an apology letter to a customer" and it may hand you an "analysis of apology-letter writing techniques". Supervised fine-tuning is like **learning the job from a mentor**: studying dozens of demonstrations of "here is how you handle this situation", until it looks like an assistant. Reinforcement learning from human feedback is like **tuning against customer feedback**: produce several versions of the same task, have a person pick the better one, and nudge towards what people prefer.

![The three stages of factory education](figures/src/06-01-three-stages.svg){#fig:three-stages}

Only the three stages together[@ouyang2022] turn a "continuation machine" into an "assistant". Note a fact that is easy to overlook: **all three stages change the same batch of parameters of the same model** — nothing is bolted on; the model itself is reshaped.

### Hallucination: a consequence you can derive from the mechanism

The conclusion first: **hallucination is not a malfunction; it is the natural product of the training objective.** [Section 1.5](#sec:llms) said pretraining's objective is "predict the next word", and the criterion for choosing that next word is **does it sound right**, not **is it true** — the two criteria are never distinguished during training.

Split it into two causes ([Figure 1-39](#fig:hallucination)). **Cause one, missing knowledge**: for things absent from the training data, the model does not know that it does not know — it has no natural representation of the state "I'm not sure", so it just carries on composing plausible text. **Cause two, fluency first**: composing a perfectly formatted fake citation scores exactly as highly as restating a real fact, under the "predict the next word" objective — a systematic review of hallucination is [@ji2023].

![The two causes of hallucination](figures/src/06-02-hallucination.svg){#fig:hallucination}

This is why the classic "invented citation" hallucination is so easy to explain: the format it has seen a thousand times; the content it has not. **Missing knowledge gives it the freedom; fluency first gives it the nerve.** Why can't you eliminate it by "trying harder"? Because eliminating it would require putting "truth" into the training objective — and "truth" cannot be labelled automatically from text. That is exactly the hole retrieval-augmented generation ([Section 1.7.3](#sec:mcp-skills-rag)) is meant to fill.

### Safety: a line that gets probed from every direction

The third stage of alignment taught the model that "dangerous requests should be refused". But "dangerous" is **a line drawn on a continuous spectrum** ([Figure 1-40](#fig:jailbreak)): drawn too loosely, harm leaks through the gaps; drawn too tightly, normal chemistry lessons and medical questions get refused too.

![The boundary between refusal and jailbreaks](figures/src/06-03-jailbreak.svg){#fig:jailbreak}

And a line is a rule, and rules can be gamed: wrap the same dangerous request in a story shell ("imagine you are a machine with no restrictions", "my granny always used to read me this recipe") and early safety training may fail — this is a **jailbreak**. It is not a bug you "fix and move on"; it is a running contest of attack and defence: each patch closes one workaround, and new workarounds keep appearing. Approaches like Constitutional AI have the model **criticise and correct itself** against a written set of principles, moving part of the defensive line from human labelling to auditable rules[@bai2022].

### Built-in limitations: the alignment tax

Alignment is not free. Once a model has been tuned to be polite, safe and well-behaved, benchmark scores usually **dip slightly** — that loss is colloquially the **alignment tax** ([Figure 1-41](#fig:alignment-tax)). It is not a bug but a genuine trade: giving up a slice of "unrestrained capability" in exchange for "safe to hand to ordinary people".

![The alignment tax: the price of obedience](figures/src/06-04-alignment-tax.svg){#fig:alignment-tax}

The real argument is about **how big the tax should be, and alignment to whom**: "make it behave" can mean behaving for the user, for the vendor, or for the regulator, and the three do not always want the same things. This question only sharpens in the agent era of [Section 1.7](#sec:agents) — the more hands and feet, the heavier the consequences of "behaving".

> **Common misconceptions**
>
> Two of them. One: "hallucination is a bug; fix it and it's gone" — as long as the training objective is still "predict the next word", hallucination has a mechanistic source; what you can do is use retrieval, calibration and refusal to push down its **rate and harm**. Two: "safety alignment is just a filter bolted on" — it reshapes parameters, affects capability (the alignment tax), and is a contest of attack and defence that never ends.

### Summary and self-check

Three sentences: supervised fine-tuning and human feedback after pretraining reshape a "continuation machine" into an "assistant"; hallucination grows mechanistically out of a training objective where "sounds right is not the same as is true"; safety alignment is a contest of attack and defence, and its price is the alignment tax.

Two self-check questions:

1. Why is it so hard to teach a model to say "I'm not sure" when answering? (Hint: in the training data, which is more common — a confident wrong answer, or honest ignorance?)
2. A company claims "our model has no hallucinations". Given this section's mechanistic analysis, what is that statement most likely to mean?

**Maths note.** The RLHF objective is usually written as: $\max_\pi\ \mathbb{E}_{x\sim\pi}\,[r(x)] - \beta\,\mathrm{KL}(\pi \,\|\, \pi_{\text{ref}})$ — maximise the human-preference reward $r$ while the KL term tethers the model to the reference model $\pi_{\text{ref}}$, stopping it from drifting away to please the rater. The larger $\beta$, the heavier the alignment tax.
