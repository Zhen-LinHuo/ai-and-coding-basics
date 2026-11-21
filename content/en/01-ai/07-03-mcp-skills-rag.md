### Extending the agent: MCP, skills, embeddings and knowledge bases {#sec:mcp-skills-rag}

#### The one-line intuition

The harness fitted the model with hands; this section is about **how far those hands can reach**: connecting to tools (MCP, a common protocol), to methods (skills, instruction sheets loaded on demand), and to knowledge (embeddings and retrieval). All three answer one question: **how does the world outside the model get plugged in cheaply.**

#### MCP: turning M×N wiring into M+N

![The host-server structure of MCP](figures/src/07-03-mcp.svg){#fig:mcp}

Without a common protocol, connecting M assistants to N tools means writing M×N pieces of bespoke glue — every vendor inventing its own interface. MCP (Model Context Protocol) standardises the interface: the assistant implements a client once, the tool implements a server once, and in between they speak the same protocol[@anthropic2024].

**M+N replaces M×N** — and the value of a standard interface is far greater than the interface itself: adding a new tool goes from "start a development project" to "change one line of config". Structurally the same as the history of USB: before the standard, every peripheral had its own port.

#### Skills: instruction sheets borrowed on demand

![How skills differ from prompts](figures/src/07-03-skills.svg){#fig:skills}

Cram every operating instruction into the context and you soon burn through the budget of [Section 1.7.1](#sec:harness), and most of it has nothing to do with the current task. The **skills** answer: keep only a one-line catalogue resident in the context ("skills A/B/C exist, here's what each covers"), fetch the full text only when the matching job comes up, and drop it again afterwards.

Which makes the difference from a prompt clear: **a prompt is the speech you carry every time; a skill is a book borrowed from the library when needed**. "Load on demand" is the crux — it lets an agent command a hundred methods without having to carry a hundred methods at once.

#### Retrieval augmentation: look it up first, then answer

![The retrieval-augmented pipeline](figures/src/07-03-rag.svg){#fig:rag}

The mechanistic root of hallucination ([Section 1.6](#sec:alignment-hallucination-safety)) is "making it up from parameter memory". Retrieval-augmented generation (RAG) takes another route: **encode the question as a vector, fetch the few passages in the knowledge base that are closest in meaning, and hand both the material and the question to the model** — so it speaks from the material rather than from memory[@lewis2020].

"Closest in meaning" works thanks to **embeddings**: the "everything is a list of numbers" planted in [Section 1.3.2](#sec:data-input) unfolds here — training brings texts with similar meaning close together in vector space ([Figure 1-52](#fig:vectors)), so retrieval collapses into the simple geometry of "find the nearest neighbours".

![The geometric intuition of vector space](figures/src/07-03-vectors.svg){#fig:vectors}

#### Built-in limitations: retrieval eases hallucination, it does not cure it

Three residual risks: **if the material isn't there, it still makes things up** (when retrieval comes back empty, the model falls back to memory mode); **if retrieval is wrong, the answer is wrong** ("similar meaning" can fetch an irrelevant passage); **the material itself can be wrong** (RAG is faithful to its sources, not a guarantee that they are true). RAG pushes hallucination from "uncontrollable" to "auditable" — a change of kind, but not down to zero.

> **Common misconceptions**
>
> That "once you add RAG, the model learns from the live internet". The knowledge base is a **static snapshot**; it does not update with model training. RAG changes "what it looks at when answering", not "what the model knows". The distinction was settled long ago in the training/inference framing of [Section 1.3.4](#sec:train-and-infer).

#### Summary and self-check

Three sentences: MCP turns M×N wiring into M+N with a common protocol; skills solve the context budget with "catalogue resident, body on demand"; RAG eases hallucination with "look it up first, then speak" but does not cure it.

Two self-check questions:

1. Why is "the value of a standard interface far greater than the interface itself"? Give a structurally similar example from outside this book.
2. An enterprise knowledge base updates every three days. What happens when the RAG system is asked "what was concluded in today's meeting"?

**Maths note.** Embedding retrieval: the document and the question are each encoded as vectors $\mathbf{d}_i, \mathbf{q}$, and you take the k with the largest cosine similarity $\cos(\mathbf{q},\mathbf{d}_i)=\frac{\mathbf{q}\cdot\mathbf{d}_i}{\|\mathbf{q}\|\|\mathbf{d}_i\|}$. An approximate nearest-neighbour index (such as HNSW) brings a query down from "compare against every document" to "compare against a small subset".
