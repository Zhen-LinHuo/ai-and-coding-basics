## The fight over freedom: open source, licences and the currents in developer communities {#sec:licenses}

### The one-line intuition

A licence is not legal decoration but **an enforceable contract**: it decides what others may do with your code, and what you must give back. Choosing a licence is essentially choosing a point between "free to use" and "forced to share".

### Two idealisms: free software and open source

In 1983 Stallman started the GNU project, taking the position of **free software**: software freedom is the user's right — the freedom to run, study, modify and redistribute, none dispensable[@stallman1985]. In 1998 another group proposed **open source**: no morality, only effectiveness — the open development model produces better software[@raymond1999]. The two lists overlap heavily (the OSI's ten criteria for open source and the four freedoms are nearly equivalent); the disagreement is in **how the case is argued**: one side says "this is a right", the other "this is a method". The argument has never been adjudicated and does not need to be — it lets two sets of values collaborate on the same body of code.

### The licence spectrum

![The licence spectrum](figures/src/28-01-spectrum.svg){#fig:spectrum}

The two ends of the spectrum: **permissive licences** (MIT — keep a copyright notice, do as you like with the rest) through to **strong copyleft** (AGPL — use my code and your whole work must be open-sourced under the same licence). In between are gradations: Apache adds a patent grant; MPL requires only "the file you changed" to be open-sourced; GPL requires the whole derivative work to be open-sourced; AGPL brings "providing a service over the network" into scope too — closing the loophole of the SaaS era.

**The mechanism of copyleft** is called "infection": code released under the GPL, whichever project it enters, makes that project release under the GPL as well. This is not a punishment but a legal enforcement of the "share" clause — the baton of freedom.

### The compatibility matrix: check before you choose

![The compatibility matrix](figures/src/28-02-matrix.svg){#fig:matrix}

The practical tool for choosing is the **compatibility matrix** ([Figure 1-63](#fig:matrix)): rows are your project, columns are the code you want to bring in. An MIT project can swallow any code; a GPL project can swallow any code but the whole project must then be GPL; an MIT project that pulls in GPL code is forced to GPL; AGPL code constrains you even if you only call its network service. **Pulling in a dependency = signing its licence** — the same sentence as "a dependency is borrowed trust" from [Section 2.4](#sec:package-managers), seen from the legal side.

### This book's choice

The body text of this book is released under **CC BY-SA 4.0** (copyleft: adaptations must credit the author and be shared under the same licence — knowledge should pass hand to hand like GPL code), and the code under **Apache-2.0** (permissive: a tool is only valuable when it is used as widely as possible). **Copyleft for content, permissive for tools** — one licence per kind of asset, a common and self-consistent combination.

### Built-in limitations: licences protect code, not ideas

A licence constrains **the expression of code**, not **the idea itself** — after reading your open-source implementation, someone can rewrite it in another language without violating any licence (ideas are not protected by copyright; what is protected is the specific text you wrote). The AI era adds a new question: is a model trained on open code a "derivative work"? There is no settled answer yet, and it is one more unresolved argument beyond [Section 1.6](#sec:alignment-hallucination-safety).

> **Common misconceptions**
>
> Two of them. First, "open source = free of charge" — the open-source definition is about freedom, not price; selling open-source software for money is entirely legal. Second, "no licence = use it however you like" — the default is **all rights reserved**, and with code that has no licence there is legally nothing you may do with it.

### Summary and self-check

Three sentences: a licence is an enforceable contract, and the spectrum runs from permissive to strong copyleft; copyleft uses an infectious clause to make "sharing" legally mandatory; pulling in a dependency means signing its licence, so check the compatibility matrix before you choose.

Two questions to check yourself:

1. You want to ship a closed-source product that includes a GPL library — what compliant routes are there?
2. Why is this book's "copyleft for content, permissive for tools" self-consistent? (Hint: the two assets are used in different ways.)

**Maths note.** No formulas in this section. One fact about legal structure: the licence chain is a **transitive closure** — if A (GPL) depends on B (MIT), the combined result only has to satisfy the stronger of the two requirements; when several licences coexist, **the strictest one constrains the whole chain**.
