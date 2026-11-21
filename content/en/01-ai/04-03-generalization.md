### Has it actually learned? Generalisation, overfitting and evaluation {#sec:generalization}

#### The one-line intuition

A model that performs well on its training data has told you almost nothing. **The real skill is generalizing — still performing well on data it has never seen.** This section is about how to know it has managed that, and how it pretends to have.

This is the second turning point in the book. So far we have discussed "how it learns"; from here on we discuss "how you know it has learned" — and that second question is the line between treating AI as engineering and treating it as a faith.

#### An analogy: memorising the workbook versus solving the paper

Two students both score 95 on the same paper. One understood the method and scores 90 on a fresh paper; the other memorised every answer in the workbook and fails outright on a fresh paper.

**Same score, different skill.** Models are the same: if the "kinks" of [Section 1.3.3](#sec:learning) simply pass exactly through every training point, what it learned is not the pattern, it is this workbook ([Figure 1-19](#fig:fit-three)).

![Underfitting, just right, overfitting](figures/src/04-03-fit-three.svg){#fig:fit-three}

#### Three ways of "learning"

**Underfitting**: it has not even learned the training data, and misses the trend — too few kinks, too few parameters.

**Overfitting**: it knows the training data inside out, noise included, and draws wobbles that do not exist in the data — too many parameters, trained too long.

**Just right**: it catches the trend and tolerates the odd deviation. There is no natural boundary between the three, only a continuous spectrum from "fitting a bit more" to "memorising a bit more".

Curiously, look at the three training scores: underfitting is lowest, just right is in the middle, overfitting scores **100**. **Training score and real skill run in opposite directions on the overfitting side** — which is why "just watch the training loss" tells you nothing.

#### What to examine it with

So hold data back as an exam paper. Ten thousand records split three ways ([Figure 1-20](#fig:split)): the **training set** adjusts the weights; the **validation set** picks the model, sets the hyperparameters and decides when to stop; the **test set** is sat exactly once, at the end.

![Training set, validation set and test set](figures/src/04-03-split.svg){#fig:split}

Validation and test sets are both "data it has not seen"; the difference is **what you do with it, and how many times you use it**.

The validation set is a **mock exam**: you can review the paper afterwards, you can sit it again and again — you use its score to pick the model, tune the learning rate, decide when to stop. It is part of your decision loop. The test set is the **final exam**: sat once, after everything is fixed, and its score goes into what you promise the outside world.

Why can the test set only be sat once, when it is "just inference mode"? The model genuinely does not learn at inference time, but **you** do: every time you look at a test score you make a decision from it — pick this version, run another round, change the architecture. Decision information leaks back to the training side through your hands. The more times you sit it, the more leaks, and the more the score resembles a validation score rather than a final exam. Hence the engineering rule: **a test score is read once, fixed once, and then left alone.**

#### The most useful diagnostic: two loss curves

Training loss falls all the way down; validation loss falls and then rises — at the moment it turns up, the model has started memorising the workbook ([Figure 1-21](#fig:loss-curves)). That fork is the most important reading in training: **stop too early and you underfit, stop too late and you overfit, and "when to stop" is itself a decision** (known in engineering as early stopping).

![Where training loss and validation loss fork](figures/src/04-03-loss-curves.svg){#fig:loss-curves}

#### Why evaluation lies

Even with the process perfectly correct, the numbers are often dishonest. Three of the commonest cheats ([Figure 1-22](#fig:leakage)):

**Data leakage** — exam questions got into the question bank. Randomly splitting a time series (using the future to predict the past), two scans of the same patient landing on opposite sides of the split, the answer hiding in the inputs (predicting "will this be refunded" while using "refund amount" as a feature). The symptom is always the same: **offline scores that are suspiciously high**.

**Distribution shift** — the paper and the era moved on. A model scoring 95 on last year's data quietly slides to 70 as this year's users change habits; if the evaluation set is never refreshed, the metric becomes a placebo.

**The metric itself being gamed** — this is Goodhart's law: once a measure becomes a target, it stops being a good measure. Models that grind the leaderboard, models that write answers in the style of the evaluation set, are footnotes to that law [@recht2019].

![Three common kinds of data leakage](figures/src/04-03-leakage.svg){#fig:leakage}

#### Built-in limitations: a guarantee of generalisation does not exist

Geometrically you can think of it like this: the model "draws lines" between training points, and however smoothly it draws them, they are still only **guesses**; the real pattern may bend somewhere you hold no data. The manifold hypothesis ([Section 1.3.3](#sec:learning)) tells us the data lives on a low-dimensional sheet, but nobody guarantees that sheet stays smooth where you did not sample.

**In other words: generalisation is induction, and induction always needs assumptions.** All evaluation can do is expose where the assumptions fail; it cannot remove them. This is the bedrock of every discussion about "interpretability" and "trustworthy AI", and one of the roots of the hallucination problem in [Section 1.6](#sec:alignment-hallucination-safety).

> **Common misconceptions**
>
> People assume "99% accuracy" means a good model. Under class imbalance, 99% may just be another way of saying "it gets every single minority case wrong" (with 990 of 1,000 samples being normal email, always answering "normal" is 99%). So before reading any metric, ask three things: **how are the classes distributed, where did the test set come from, and how many times has this score been tuned?**

#### Summary and self-check

In three sentences: a training score says nothing about skill, only unseen data does; overfitting is memorising the workbook, and there training score and real skill run in opposite directions; evaluation is fooled by leakage, drift and gameable metrics — a guarantee of generalisation does not exist, so design can only expose failure.

Two self-check questions:

1. A model scores 99% on the training set, 62% on validation and 61% on test. Is the problem the model or the process? What do you look at first?
2. Why is "random splitting" itself a form of data leakage in tasks like predicting share prices or disease risk?

**Maths note.** Write the training loss as $L_{\text{train}}$ and the validation loss as $L_{\text{val}}$. In the overfitting region $L_{\text{train}}$ keeps falling while $L_{\text{val}}$ rises; early stopping takes the minimum of $L_{\text{val}}$. Generalisation error decomposes roughly as $L_{\text{val}} \approx \text{bias}^2 + \text{variance} + \text{noise}$: underfitting is high bias, overfitting is high variance, and just right is the compromise [@hastie2009].
