### From images to language: diffusion models {#sec:diffusion}

#### The one-line intuition

Autoregressive models write one word at a time going forward; diffusion models take another road: **start with a blob of noise, then remove the noise step by step**, and after a few dozen steps the content appears ([Figure 1-33](#fig:noise)). They were originally the mainstay of image generation, and since 2025 they have broken into language generation too — because "parallel" is too tempting a word.

#### An analogy: developing a photograph

Diffusion works like developing film: the image is not drawn in one stroke but **emerges gradually** in the developer. Each step does one small thing — "take a little of this layer of fog away". During training every step of the reverse process has a known answer (because the model added the fog itself), so practice questions are endless and automatically generated [@ho2020].

#### The problem it solves: breaking "get it right in one go" into "fix a little each time"

![Adding noise and removing it](figures/src/05-04-noise.svg){#fig:noise}

Training takes the left path: add noise to a clear image step by step until it is pure noise — **what was added at each step is fully known**, and the network's job is to learn "subtract that bit". Generation takes the right path: start from pure noise, use the learned "denoising craft" in reverse, and after a few dozen steps the image appears.

**Break one big task into hundreds of small ones, each easy to learn** — that is the core reason diffusion can draw detail.

#### Conditioning: glance at the prompt at every step

![Text-guided conditional generation](figures/src/05-04-guided.svg){#fig:guided}

"What to draw" is decided by the prompt: every step of the denoising network receives the prompt's vector [@nichol2021]. During training the prompt is randomly blanked out, so the network learns both "draw unconditionally" and "draw under a condition", and the difference between the two is used to **amplify** the prompt's influence — one of the key tricks behind text-to-image quality.

#### From images to language: parallel decoding

![How autoregressive and diffusion models produce output](figures/src/05-04-parallel.svg){#fig:parallel}

Language diffusion (LLaDA [@nie2025], Mercury [@lou2025]) moves the same game to text: the whole sentence starts as placeholders, the model changes several positions at once each step, and after a few steps it converges on the complete text ([Figure 1-34](#fig:parallel)). **Autoregressive generation of n characters needs at least n steps; diffusion can produce a whole passage in a few dozen** — which is why the selling point of diffusion language models is "twice the tokens per second".

#### Built-in limitations: coherence and step count

Parallel rewriting saves steps but also loses one natural advantage of autoregression: **writing left to right, earlier text naturally constrains later text**. Diffusion needs more steps and better training to match the coherence of long passages; cut the steps too far and quality drops at once — the trade-off between steps and latency is its own "scaling law".

> **Common misconceptions**
>
> The belief that "diffusion models can only draw pictures". It is a **generative paradigm**, and images, audio, video, protein structures and text all have diffusion implementations. Paradigm and modality are two different things.

#### Summary and self-check

Three sentences: diffusion splits generation into a few hundred steps of "remove a bit of noise", with training examples generated automatically; conditional generation looks at the prompt at every step; moved to language, parallel decoding buys speed at the cost of harder long-text coherence.

Two self-check questions:

1. Why can diffusion's training data be "generated automatically without limit", while labels for supervised learning cannot?
2. For an application that must "quote a contract clause exactly, word for word", what risk does autoregression carry, and what risk does diffusion?

**Maths note.** Forward noising: $q(x_t \mid x_{t-1}) = \mathcal{N}\!\left(\sqrt{1-\beta_t}\,x_{t-1},\ \beta_t I\right)$, where $\beta_t$ is the noise strength at step $t$. The reverse process $p_\theta(x_{t-1}\mid x_t)$ that the network learns uses the same $\beta_t$, so the training objective (predict the noise added at each step) has an analytic answer.
