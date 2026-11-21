# 术语表 {.unnumbered}

按中文拼音排序。每条给出中文名、英文原词、一句话定义，以及首次出现的章节。

| 中文 | 英文 | 一句话定义 | 见 |
|:--|:--|:--|:--|
| copyleft | copyleft | 要求衍生作品沿用同一许可证的条款 | 2.8 |
| 泛化 | generalization | 在没见过的数据上依然表现好的能力 | 1.4.3 |
| 反向传播 | backpropagation | 把输出误差沿网络逐层分摊回每个权重 | 1.3.3 |
| 分布漂移 | distribution shift | 真实数据的分布随时间偏离训练数据的分布 | 1.4.3 |
| 感知机 | perceptron | 单个神经元构成的线性分类器 | 1.3.1 |
| 哈希 | hash | 把任意内容压成固定长度指纹，内容差一字节指纹即变 | 2.5 |
| 幻觉 | hallucination | 流畅但事实错误的生成结果 | 1.6 |
| 激活函数 | activation function | 神经元加权求和之后的非线性（如"负数归零"） | 1.4.1 |
| 交叉引用 | cross-reference | 指向章节或图表编号的引用，编号自动生成 | 2.7 |
| 进程 | process | 运行中的程序：内存、状态与执行流的整体 | 2.1 |
| 决策边界 | decision boundary | 模型划分"输出 1 / 输出 0"的几何边界 | 1.3.1 |
| 可复现性 | reproducibility | 同样的输入在任何机器、任何时间得到相同结果 | 2.5 |
| 联想记忆 | associative memory | 用层内互连神经元的权重直接存取图案 | 1.3.1 |
| 流形 | manifold | 高维空间中数据实际聚居的低维曲面 | 1.3.3 |
| 强化学习 | reinforcement learning | 只凭环境的分数而非标准答案进行学习 | 1.4.2 |
| 检索增强 | retrieval-augmented generation | 先查资料再作答，以缓解幻觉 | 1.7.3 |
| 数据泄漏 | data leakage | 考题混进题库，导致评估虚高 | 1.4.3 |
| 数据墙 | data wall | 高质量训练文本接近用尽的约束 | 1.5.1 |
| 缩放定律 | scaling law | 损失随算力、数据、参数增长的幂律关系 | 1.5.1 |
| 损失函数 | loss function | 把"错得离谱"量化成一个数的函数 | 1.3.3 |
| 锁文件 | lock file | 用哈希钉住整棵依赖树精确版本的记录 | 2.4 |
| 提交 | commit | 版本控制中的一次不可变快照 | 2.2 |
| 暂存区 | staging area | 从改动中挑选待存档内容的缓冲区 | 2.2 |
| 钻石依赖 | diamond dependency | 两个依赖要求同一库的不同版本 | 2.4 |
| 提示词 | prompt | 用户给模型的输入；条件生成的引导信号 | 1.5.4 |
| 温度 | temperature | 抽取 token 时调节随机程度的参数 | 1.5.4 |
| 采样策略 | sampling strategy | 从概率表中选出下一个 token 的规则 | 1.5.0 |
| 预训练 | pretraining | 在海量无标注文本上自监督训练的阶段 | 1.6 |
| 监督微调 | supervised fine-tuning | 用人写好的示范教模型"当助手"的阶段 | 1.6 |
| 对齐 | alignment | 让模型行为符合人类期望与价值观的调教 | 1.6 |
| 对齐税 | alignment tax | 安全对齐带来的能力下降 | 1.6 |
| 过拟合 | overfitting | 在训练数据上表现好、在新数据上表现差 | 1.4.3 |
| 早停 | early stopping | 在验证损失开始回升处停止训练 | 1.4.3 |
| 注意力机制 | attention | 按相关性对上下文加权求和的计算 | 1.5.2 |
| 多头注意力 | multi-head attention | 并行多套注意力，各自关注不同关系 | 1.5.2 |
| 上下文窗口 | context window | 模型一次能看到的全部输入上限 | 1.7.1 |
| 自监督 | self-supervised | 从数据自身构造题目与答案的预训练方式 | 1.4.2 |
| 嵌入 | embedding | 把文字/图像编码成可比较距离的向量 | 1.7.3 |
| 量化 | quantization | 用更少的位数存储参数，换显存与速度 | 1.8 |
| KV 缓存 | KV cache | 推理时保留的历史键值，随上下文线性增长 | 1.8 |
| 声明式管理 | declarative management | 声明期望状态，由工具收敛到该状态 | 2.5 |
| 代际回滚 | generation rollback | 系统每次变更成新一代，可原子回退 | 2.6 |
| 容器镜像 | container image | 应用连同环境的不可变分发包（OCI 规范） | 2.5 |
| 语义化版本 | semantic versioning | 用三段数字声明接口破坏程度的公约 | 2.4 |
| 许可证 | license | 声明代码可被如何使用的可执行合同 | 2.8 |
| 依赖 | dependency | 一个软件运行所需的另一个软件 | 2.4 |
| 状态空间模型 | state space model | 用固定大小状态压缩历史的序列模型 | 1.5.3 |
| 编译器 | compiler | 把源代码整体翻译成机器指令的工具 | 2.1 |
| 解释器 | interpreter | 逐句读取并执行源代码的程序 | 2.1 |
| 调用栈 | call stack | 函数嵌套调用时逐层叠放的记录区 | 2.1 |
| 越狱 | jailbreak | 绕过安全对齐的提示词手法 | 1.6 |
| 扩散模型 | diffusion model | 通过学习去噪过程来生成数据的模型 | 1.5.4 |
| 微调 | fine-tuning | 在预训练之后继续训练以适配特定任务 | 1.7.1 |
| 学习率 | learning rate | 梯度下降每步沿下坡方向走多远 | 1.3.3 |
| 隐藏层 | hidden layer | 夹在输入与输出之间的神经元层 | 1.4.1 |
| 多模态 | multimodal | 文本、图像、音频共用同一表示空间的模型 | 1.5.0 |
| 训练/验证/测试 | train/val/test split | 数据三分：调参、选型、终考 | 1.4.3 |
| token | token | 分词器产出的最小输入单位；模型只见到它 | 1.3.2 |
