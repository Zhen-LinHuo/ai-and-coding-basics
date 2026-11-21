# EN-GB translation guide (ai-and-coding-basics)

You are translating this book into **British English** for `content/en/`.
The Chinese edition is the source of truth for content and structure; you own tone as well as accuracy.
Voice: friendly, plain, second person ("you"), concrete analogies, no fluff, no hype, never condescending.

## Hard rules
1. **British English**: -ise/-isation, -our, -re, licence (noun) / license (verb), tokeniser, generalisation, behaviour, colour, centre, maths (not math).
2. **Preserve exactly, never translate:** heading anchors `{#sec:...}` and figure anchors `{#fig:...}` (byte-identical); citation keys `[@key]`; image paths `figures/src/....svg`; markdown structure (heading levels, tables, blockquotes, bold/italic, lists); numbers, units, formulas, code.
3. Translate figure alt text/captions (no "图" prefix).
4. Callout `> **常见误解**` -> `> **Common misconceptions**`; other callout labels translate naturally (e.g. `> **一句话记住**` -> `> **One line to remember**`).
5. **Beat headings are canonical — use exactly these:**
   - `### 一句话直觉` -> `### The one-line intuition`
   - `### 一个类比：X` -> `### An analogy: X`
   - `### 它解决什么问题：X` / `### 它解决什么问题` -> `### The problem it solves: X` / `### The problem it solves`
   - `### 天然短板：X` / `### 天然短板` -> `### Built-in limitations: X` / `### Built-in limitations`
   - `### 小结与自检` -> `### Summary and self-check`
   - `### 数学注解` -> `### Maths note`
   - Other `###` subheads: translate freely, keep short title-style (no full stops).
6. `## ` section titles: translate naturally, keep short.
7. **No CJK characters, no full-width punctuation, no 「」** in output. Use " " and ( ).
8. Keep the rhythm: short paragraphs, one idea each. Restructure sentences freely; never drop information or invent claims.
9. Model/product names (GPT, Claude, DeepSeek, Mamba, RWKV, ReLU...) stay as-is.

## Terminology (canonical; use these exact renderings)
| 泛化 | generalization |
| 反向传播 | backpropagation |
| 分布漂移 | distribution shift |
| 感知机 | perceptron |
| 哈希 | hash |
| 幻觉 | hallucination |
| 激活函数 | activation function |
| 交叉引用 | cross-reference |
| 进程 | process |
| 决策边界 | decision boundary |
| 可复现性 | reproducibility |
| 联想记忆 | associative memory |
| 流形 | manifold |
| 强化学习 | reinforcement learning |
| 检索增强 | retrieval-augmented generation |
| 数据泄漏 | data leakage |
| 数据墙 | data wall |
| 缩放定律 | scaling law |
| 损失函数 | loss function |
| 锁文件 | lock file |
| 提交 | commit |
| 暂存区 | staging area |
| 钻石依赖 | diamond dependency |
| 提示词 | prompt |
| 温度 | temperature |
| 采样策略 | sampling strategy |
| 预训练 | pretraining |
| 监督微调 | supervised fine-tuning |
| 对齐 | alignment |
| 对齐税 | alignment tax |
| 过拟合 | overfitting |
| 早停 | early stopping |
| 注意力机制 | attention |
| 多头注意力 | multi-head attention |
| 上下文窗口 | context window |
| 自监督 | self-supervised |
| 嵌入 | embedding |
| 量化 | quantization |
| KV 缓存 | KV cache |
| 声明式管理 | declarative management |
| 代际回滚 | generation rollback |
| 容器镜像 | container image |
| 语义化版本 | semantic versioning |
| 许可证 | license |
| 依赖 | dependency |
| 状态空间模型 | state space model |
| 编译器 | compiler |
| 解释器 | interpreter |
| 调用栈 | call stack |
| 越狱 | jailbreak |
| 扩散模型 | diffusion model |
| 微调 | fine-tuning |
| 学习率 | learning rate |
| 隐藏层 | hidden layer |
| 多模态 | multimodal |
| 训练/验证/测试 | train/val/test split |
| 三大流派 | the three schools |
| 符号主义 | symbolism (the symbolic school) |
| 连接主义 | connectionism |
| 行为主义 | behaviourism |
| 缩放定律 | scaling laws |
| 数据墙 | the data wall |
| KV 缓存 | the KV cache |
| 智能体 | agent |
| 技能 | skills |
| 上下文窗口 | the context window |
| 温度 | temperature |
| 第 1 部分 / 第 2 部分 | Part 1 / Part 2 |
