### Data input: from real quantities to high-dimensional vectors {#sec:data-input}

#### The one-line intuition

The neuron from [Section 1.3.1](#sec:neural-networks) does one thing: it takes numbers and computes a weighted sum. It doesn't know red, it doesn't know Chinese characters, it doesn't know cats. So everything in the world — photos, speech, text, the way you're walking right now — has to settle one thing first before it can enter a neural network: **it has to become a column of numbers.**

This section is about the craft of that transformation. Once it's done, a thing is represented by its column of numbers, and however many cells that column has, we say the world has that many **dimensions**.

#### An analogy: a medical report

A medical report compresses "you as a person" into a few hundred numbers: height, weight, blood pressure, twenty blood markers… The doctor has never met you, but reading the numbers alone lets them make a reasonably reliable judgement. Compression necessarily loses things — your personality isn't in the report — but if the markers are chosen well, what gets lost is exactly the part that doesn't affect the judgement.

That's the kind of report a neural network eats. Choose its "tests" well and it learns fast and accurately; choose them badly and no amount of genius will save it.

#### Images: from colour to tensor

A digital photo is, on screen, already an array of numbers: three numbers per pixel, describing the intensity of red, green and blue light (0 to 255). So "feeding a photo to the network" isn't translation, it's **copying** — except you're copying three million numbers ([the figure below](#fig:rgb-tensor)).

![A colour photo becoming three arrays of numbers](figures/src/03-02-rgb-tensor.svg){#fig:rgb-tensor}

Greyscale is simpler: black-and-white handwritten digits are usually made into a 28×28 grid, each cell a number from 0 to 1. Straighten the 784 cells out row by row and you get a 784-dimensional vector ([the figure below](#fig:flatten)) — 784 is the "dimensionality" this world hands the network.

![A 28×28 handwritten digit straightened into a 784-dimensional vector](figures/src/03-02-flatten.svg){#fig:flatten}

Straightening loses no information but it does lose **relationships**: two pixels that sat next to each other on the paper are 28 positions apart in the vector, and the network has to relearn "next to each other" for itself. That's the starting point for a lot of later architecture inventions — file it away for now.

#### Text: from characters to chunks

Numbers and images are numbers by nature. Text isn't, so it has to be cut up first. The cutting method is a purely engineering trade-off ([the figure below](#fig:bpe)); the mainstream approach is called BPE (byte-pair encoding)[@sennrich2016]: start from single characters, repeatedly count which pair of partners occurs most often in the corpus, and merge them into a new symbol. After tens of thousands of rounds, common words have been merged into whole chunks and rare words have fallen back to characters — **one vocabulary serving both ends**.

![The BPE merging process](figures/src/03-02-bpe.svg){#fig:bpe}

![How many chunks the same sentence takes in different languages](figures/src/03-02-tokenize-compare.svg){#fig:tokenize-compare}

Each chunk that comes out is called a **token**. The model's eyes see no words, only tokens and their ids. Chinese has no spaces and its characters are all common, so BPE usually doesn't merge Chinese characters, and the same passage costs two or three times as many tokens in Chinese as in English — a ratio that turns into a hard cash constraint when we get to the context window in Section 1.5.

#### Where the data comes from

Vectors are the "shape"; data is the "material". The material has three sources: **naturally labelled** (the star rating when you order takeaway, the timestamp on a photo), **labelled with money and labour** (medical images need a doctor to draw the boxes), and **self-generated** (take text off the internet directly — "the next sentence" is a free ground truth, which is the single most important insight of the large language model era; Section 1.5 expands on it).

Dirty data makes a dirty model: an annotator's hand slips, a crawler drags in duplicate samples, a form gets one cell copied wrong — the network faithfully learns those errors too, and learns them just as eagerly.

#### Built-in limitations: dimension is a choice, and choices cost

Turning the world into vectors means making a decision at every step: using 784 cells to represent a digit is deciding "ignore stroke thickness and colour"; using three numbers for a pixel is deciding "the way hue and brightness combine doesn't matter". **Whatever the representation throws away, the network can never learn back.**

The subtler cost is dimension itself: the higher it goes, the less "nearby" means anything — in a 784-dimensional space two points are neither far nor close. The curse of dimensionality, put plainly, is this: the more cells there are, the more samples you need, or most cells will wait their whole lives for a single example.

> **Common misconceptions**
>
> That "AI sees" the photo. It doesn't. It reads a numerical spreadsheet whose format — dimensions, order, the value range of each cell — was all decided by people; two worlds with different formats are two different worlds to it. That's also why "show the AI what a human eye sees" always has a layer of representation in between — and the biases in that representation pass straight through to the model.

#### Summary and self-check

Three sentences: every input first becomes a fixed-length vector, and the dimensionality is just "how many numbers it took to describe a thing"; text gets cut into tokens, and vocabulary size is the dividing line between "how much to memorise" and "how much to assemble"; what the representation throws away can never be learned back, and dirty data gets learned just as eagerly.

Two self-check questions:

1. Rotate a 28×28 handwritten digit by 90 degrees and then straighten it — does the resulting vector have any relationship to the original? What does that say about the flattening representation?
2. An app needs to recognise handwritten Chinese characters. Should its vocabulary lean large or small? (Hint: whether Chinese characters are "characters" or "chunks" depends on whether you want the model to memorise or to assemble.)

**Maths note.** This section only introduces notation: the input vector is written in bold as $\mathbf{x} = (x_1, x_2, \dots, x_d)$, where $d$ is the dimensionality; the array formed by stacking an image's three colour layers is called a tensor, which is just the mathematical name for "a multi-dimensional table". The BPE merging rule involves no maths, only counting.
