# Glossary {.unnumbered}

Sorted alphabetically. Each entry gives the English term, the Chinese term, a one-line definition, and the section where it first appears.

| Term | 中文 | Definition | See |
|:--|:--|:--|:--|
| activation function | 激活函数 | The non-linearity applied after a neuron's weighted sum (such as "clamp negatives to zero") | 1.4.1 |
| alignment | 对齐 | Shaping a model's behaviour to match human expectations and values | 1.6 |
| alignment tax | 对齐税 | The capability lost in exchange for safety alignment | 1.6 |
| associative memory | 联想记忆 | Storing and retrieving patterns directly in the weights of neurons connected within a layer | 1.3.1 |
| attention | 注意力机制 | A computation that weights and sums the context by relevance | 1.5.2 |
| backpropagation | 反向传播 | Distributing the output error back through the network, layer by layer, onto every weight | 1.3.3 |
| call stack | 调用栈 | The record area where nested function calls stack up layer by layer | 2.1 |
| commit | 提交 | An immutable snapshot in version control | 2.2 |
| compiler | 编译器 | A tool that translates source code into machine instructions in one go | 2.1 |
| container image | 容器镜像 | An immutable distribution package of an application together with its environment (the OCI specification) | 2.5 |
| context window | 上下文窗口 | The upper limit on all the input a model can see at once | 1.7.1 |
| copyleft | copyleft | A licence whose terms require derivative works to carry the same licence | 2.8 |
| cross-reference | 交叉引用 | A reference to a section or figure number, generated automatically | 2.7 |
| data leakage | 数据泄漏 | Exam questions leaking into the question bank, inflating evaluation scores | 1.4.3 |
| data wall | 数据墙 | The constraint that high-quality training text is close to running out | 1.5.1 |
| decision boundary | 决策边界 | The geometric boundary a model draws between "output 1" and "output 0" | 1.3.1 |
| declarative management | 声明式管理 | Declare the desired state and let the tooling converge the system onto it | 2.5 |
| dependency | 依赖 | A piece of software another piece of software needs in order to run | 2.4 |
| diamond dependency | 钻石依赖 | Two dependencies demanding different versions of the same library | 2.4 |
| diffusion model | 扩散模型 | A model that generates data by learning to undo noise | 1.5.4 |
| distribution shift | 分布漂移 | The distribution of real-world data drifting away from the training distribution over time | 1.4.3 |
| early stopping | 早停 | Halting training where the validation loss starts to rise again | 1.4.3 |
| embedding | 嵌入 | Encoding text or images into vectors whose distances can be compared | 1.7.3 |
| fine-tuning | 微调 | Continuing to train after pretraining to adapt to a particular task | 1.7.1 |
| generalization | 泛化 | The ability to still perform well on data never seen before | 1.4.3 |
| generation rollback | 代际回滚 | Every system change becomes a new generation, which can be rolled back atomically | 2.6 |
| hallucination | 幻觉 | Fluent output that is factually wrong | 1.6 |
| hash | 哈希 | Squeezing arbitrary content into a fixed-length fingerprint that changes if even one byte differs | 2.5 |
| hidden layer | 隐藏层 | A layer of neurons sandwiched between input and output | 1.4.1 |
| interpreter | 解释器 | A program that reads and executes source code statement by statement | 2.1 |
| jailbreak | 越狱 | A prompting technique for getting around safety alignment | 1.6 |
| KV cache | KV 缓存 | The historical keys and values kept during inference, growing linearly with the context | 1.8 |
| learning rate | 学习率 | How far gradient descent steps downhill on each step | 1.3.3 |
| license | 许可证 | An executable contract declaring how code may be used | 2.8 |
| lock file | 锁文件 | A record that pins the exact version of the whole dependency tree with hashes | 2.4 |
| loss function | 损失函数 | A function that quantifies "how badly wrong" as a single number | 1.3.3 |
| manifold | 流形 | The low-dimensional surface where data actually clusters inside a high-dimensional space | 1.3.3 |
| multi-head attention | 多头注意力 | Several attention mechanisms in parallel, each attending to different relationships | 1.5.2 |
| multimodal | 多模态 | A model where text, images and audio share one representation space | 1.5.0 |
| overfitting | 过拟合 | Performing well on the training data but poorly on new data | 1.4.3 |
| perceptron | 感知机 | A linear classifier made of a single neuron | 1.3.1 |
| pretraining | 预训练 | The stage of self-supervised training on vast amounts of unlabelled text | 1.6 |
| process | 进程 | A running program: its memory, state and flow of execution as a whole | 2.1 |
| prompt | 提示词 | The input a user gives the model; the steering signal for conditional generation | 1.5.4 |
| quantization | 量化 | Storing parameters in fewer bits, trading memory for speed | 1.8 |
| reinforcement learning | 强化学习 | Learning from the environment's score alone, with no standard answers | 1.4.2 |
| reproducibility | 可复现性 | The same input giving the same result on any machine, at any time | 2.5 |
| retrieval-augmented generation | 检索增强 | Looking things up before answering, to mitigate hallucination | 1.7.3 |
| sampling strategy | 采样策略 | The rule for picking the next token from a probability table | 1.5.0 |
| scaling law | 缩放定律 | The power-law relationship between loss and growth in compute, data and parameters | 1.5.1 |
| self-supervised | 自监督 | A pretraining approach that constructs its own questions and answers from the data itself | 1.4.2 |
| semantic versioning | 语义化版本 | A convention that uses three number segments to declare how badly an interface breaks | 2.4 |
| staging area | 暂存区 | The buffer where you pick which changes to archive | 2.2 |
| state space model | 状态空间模型 | A sequence model that compresses history into a fixed-size state | 1.5.3 |
| supervised fine-tuning | 监督微调 | The stage of teaching a model "how to be an assistant" with human-written demonstrations | 1.6 |
| temperature | 温度 | The parameter that dials randomness up or down when drawing tokens | 1.5.4 |
| token | token | The smallest unit of input a tokeniser produces; it is all the model ever sees | 1.3.2 |
| train/val/test split | 训练/验证/测试 | Splitting data three ways: tuning, choosing, final exam | 1.4.3 |
