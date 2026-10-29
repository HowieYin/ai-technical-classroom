# AI Technical Classroom

[![Language: English](https://img.shields.io/badge/Language-English-1f6feb)](README.md)
[![语言：简体中文](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-dc4a22)](README.zh-CN.md)

> 一个可移植的 **Agent Skill**：把技术主题、论文、代码仓库、URL、本地文件或工程问题，转化为证据驱动的学习档案，以及可离线打开、具有发表级质量的 HTML 技术报告。

`ai-technical-classroom` **不是**聊天机器人、托管服务或 LLM SDK；它是一个以 **`SKILL.md` 为入口的工作流包**。把它安装到支持 Agent Skills 的编码 Agent（如 Claude Code、Codex、TraeX，或其他兼容运行时）后，再让该 Agent 执行技术课程。

Agent 宿主提供模型、工具调用、文件权限、浏览/检索能力；在严格计时模式下，还需要一个持续运行的 autonomous runner。本仓库提供的则是研究、教学、审稿、HTML 交付与审计工作流。

## 为什么需要它

很多“帮我总结这篇论文”的流程最终只会给出一份很薄的概览：缺少一手证据、公式跳步、图表不解释，或只做出一个好看的网页。本 Skill 强制完整技术闭环：

```text
用户给定的直接材料
        ↓
paper-first 调研与证据地图
        ↓
Alex / Bob 技术教学与对抗式掌握检查
        ↓
面向真实读者的文章 + 机制相关交互组件
        ↓
Alex / Leo / Alice 多轮审稿 + Nora 计时审计
        ↓
离线 HTML 报告 + 可复现/投稿准备材料
```

它适合 AI、ML 系统、硬件、数学、软件架构等主题：这些主题需要严肃处理一手论文、公式、源代码、实验、图表、设计权衡与失败模式。

## 这个 Skill 提供什么

| 能力 | 强制要求 |
| --- | --- |
| 五角色协作 | Alex Tensor 负责授课和事实核验；Bob Prompt 独立学习和写作；Leo 做论文级技术审稿；Alice 审查 HTML/可访问性；Nora 记录并审计计时。 |
| Paper-first 调研 | 先读取用户给定材料，再使用原始论文、官方实现、官方文档和可复现证据。 |
| 技术深度 | 覆盖机制、变量/shape/单位、数值例子、实现/数据流、复杂度、替代方案和失败模式。 |
| 可发表 HTML | 产出面向外部读者的离线 `report.html`，而非课堂 transcript 或作业页面。 |
| 有意义的交互 | 至少一个独立的 `components/*.html`；读者可调整真实技术变量，并观察某个机制的变化。 |
| 审稿门禁 | Alex、Leo、Alice 都至少经历两轮实质性的“审查 → 修改 → 验证”。 |
| 证据门禁 | 可选的 PID 活跃时间、checkpoint 与 Nora 资格结论。 |
| 研究/投稿包 | 编辑源、代码、数据、结果、选刊、模拟审稿、修订日志、诚信声明与 A/B/C 结论的骨架。 |

## 何时使用

当你希望 Agent 完成下面的任务时，使用本 Skill：

- 精读并讲解论文、调研技术方向，或解释一个真实实现；
- 将本地仓库、调试日志、系统设计转化为可长期复用的技术文章；
- 创建带论文图/表解读和机制交互组件的自包含 HTML 报告；
- 为调研过程、课堂对话、技术审稿与可复现边界留下可审计记录；
- 明确区分“快速研究草稿”和真正完成了证据计时门槛的自主课程。

不适合：一段话摘要、普通文案修改、泛营销网页，或无法提供来源/复现证据却声称有实验结论的任务。

## 依赖与前提

### 必需

- 一个能够加载含 `SKILL.md` 目录的 Agent 运行时；
- 具备技术推理与工具调用能力的模型；
- 对目标工作区拥有读写权限；
- Python **3.10+**。本仓库脚本仅使用 Python 标准库。

### 强烈建议

- 能访问一手来源和官方文档的联网/浏览器工具；
- 可用于桌面和窄屏审查的浏览器或 HTML 渲染器；
- 如果要获得严格计时资格，需有持久运行的 Agent runner。

### 必须理解：Skill 与模型/API 是两层

本仓库**不会自行向任何 LLM 发请求，也不会保存 API Key**。模型、API endpoint 与工具权限由 Agent 宿主配置：

```text
Agent 宿主配置       →  模型 / API Key / endpoint / 工具
ai-technical-classroom → 调研、课程、审稿与交付工作流
你的工作区            → course-records/<日期>-<主题>/
```

只要 Agent 运行时能调用该模型并执行本地工具，本 Skill 可以搭配本地模型、直连服务商 API、OpenAI-compatible 网关或 Anthropic-compatible 网关使用。

## 安装

### 更新已安装的 Skill

如果通过 `git clone` 安装，可在实际安装目录执行更新：

```sh
git -C /path/to/skills/ai-technical-classroom pull --ff-only
```

将路径替换为你的实际安装目录。更新后新开一个 Agent 会话，使其加载最新指令。如果 Git 提示本地修改或历史分叉，请先处理这些差异；不要用强制 reset 丢弃自己的定制。

克隆本仓库，然后将**含 `SKILL.md` 的仓库根目录**放进 Agent 的 Skill 搜索路径。

```sh
git clone https://github.com/HowieYin/ai-technical-classroom.git
```

不同 Agent 的 Skill 发现目录不同。下方是常见安装方式；如果你的 Agent 版本使用其它目录，请以它自身的官方配置为准。

### Claude Code

安装给当前用户：

```sh
mkdir -p ~/.claude/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  ~/.claude/skills/ai-technical-classroom
```

也可以把 Skill 跟随项目版本管理：

```sh
mkdir -p .claude/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .claude/skills/ai-technical-classroom
```

安装后重启 Claude Code 或新开一个会话。显式调用：

```text
Use $ai-technical-classroom to ...
```

### Codex CLI / Codex Agents

用户级安装：

```sh
mkdir -p ~/.codex/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  ~/.codex/skills/ai-technical-classroom
```

项目级安装：

```sh
mkdir -p .codex/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .codex/skills/ai-technical-classroom
```

新开 Codex 会话，然后显式调用：

```text
Use $ai-technical-classroom to teach and write a technical report about ...
```

### TraeX / TRAE CLI

全局安装：

```sh
mkdir -p "${TRAE_HOME:-$HOME/.trae}/skills"
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  "${TRAE_HOME:-$HOME/.trae}/skills/ai-technical-classroom"
```

仅安装给当前项目：

```sh
mkdir -p .trae/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .trae/skills/ai-technical-classroom
```

新开会话后，使用 `$ai-technical-classroom`。

### 其他 Agent 运行时

任何支持开放 `SKILL.md` 约定的运行时都可使用：

1. 将本仓库根目录放入该运行时配置的 Skills 目录；
2. 确认它可以读取该目录并运行 `python3`；
3. 新开 Agent 会话，使其重新扫描 Skills；
4. 如果不支持自动触发，就在 prompt 中显式写 `ai-technical-classroom` 或 `$ai-technical-classroom`。

如果你的运行时根本不支持 Skills，也可以将 `SKILL.md` 作为 system/developer instructions 加载，并保留 `references/`、`scripts/` 的相对路径可访问。

## 在 Agent 宿主中配置 LLM / API

请在 **Agent 宿主** 中配置，而不是在此仓库中。绝不要把 API Key 写进本仓库、`SKILL.md`、课程档案或 `manifest.md`。

### Claude Code

通过 Claude Code 正常的登录/API Key 流程鉴权；使用直接 API 时，常见方式是从含凭证的 shell 启动：

```sh
export ANTHROPIC_API_KEY="replace-with-your-secret"
claude
```

如果使用 Anthropic-compatible 企业网关或代理，按该网关与 Claude Code 的要求配置 URL/认证信息，并将它们保存在环境变量或宿主的私有配置中。

### Codex / OpenAI-Compatible 宿主

对于直连 OpenAI-compatible 服务的宿主，通常模式为：

```sh
export OPENAI_API_KEY="replace-with-your-secret"
# 仅当你的宿主/网关文档明确要求时设置：
export OPENAI_BASE_URL="https://your-gateway.example/v1"
```

然后依据所用 Codex 版本/宿主的官方文档选择 provider 和 model。不同 Codex 发行版、版本或企业网关的配置文件及字段可能不同；本仓库不会写死可能过期的 provider 配置。

### 通用 Agent 宿主

使用这种安全模式：

```sh
export PROVIDER_API_KEY="replace-with-your-secret"
export PROVIDER_BASE_URL="https://provider.example/v1"  # 如服务商需要
agent-cli --model "provider-model-name"
```

开始长课程前，确认四件事：

1. Agent 能成功完成一次模型调用；
2. Agent 对目标工作区有写权限；
3. 主题需要外部来源时，浏览器/检索工具可用；
4. 若要声明严格计时完成，有一个真正持久运行的 runner。

## 如何调用

最通用可靠的方式是显式调用：

```text
Use $ai-technical-classroom to turn [topic / paper / URL / repository / log]
into a rigorous technical course and offline HTML report.
```

请给出明确主题和可选范围。真实用户是 **Course Owner**，不是模拟学生：不需要回答 Alex/Bob 的问题，也不需要批准每一步。

### 示例 1：论文精读

```text
Use $ai-technical-classroom.

Topic: FlashAttention and the IO-aware view of exact attention.
Direct source: https://arxiv.org/abs/2205.14135
Scope: derive the IO model, explain the tiled forward algorithm, compare the
memory/computation trade-off with standard attention, and create an interactive
tile-size / memory-traffic explainer. Deliver an offline English HTML report.
```

### 示例 2：代码 / 系统分析

```text
Use $ai-technical-classroom.

Topic: Explain the scheduler and KV-cache lifecycle in this repository.
Direct material: ./path/to/repository
Scope: trace the real request path, identify data ownership and state
transitions, compare prefill and decode behavior, and write an offline HTML
architecture report with an interactive timeline. Do not invent benchmarks.
```

### 示例 3：非计时草稿

```text
Use $ai-technical-classroom to create an untimed, evidence-grounded research
and HTML draft about speculative decoding. Do not claim the 30m+30m+2h+1h
timed-course qualification unless a persistent runner is actually available.
```

## 端到端示例

这个例子包含 **Agent 调用** 与可选命令行工具。通常应该由 Agent 完成，不需要人手模拟五个角色。

### 1. 创建课程档案

```sh
git clone https://github.com/HowieYin/ai-technical-classroom.git
cd ai-technical-classroom

python3 scripts/init_course.py \
  --output ~/technical-courses \
  --topic "FlashAttention IO model" \
  --source "https://arxiv.org/abs/2205.14135"
```

该命令会输出类似目录：

```text
~/technical-courses/course-records/2026-10-09-flashattention-io-model
```

其中已包含资料地图、课程计划、审稿表、报告目标、组件目录、计时文件和投稿包骨架。

### 2. 让 Agent 执行课程

```text
Use $ai-technical-classroom and work in
~/technical-courses/course-records/2026-10-09-flashattention-io-model.

Read the direct source first. Complete the research map and paper lineage,
then conduct the course autonomously. Keep the classroom record internal;
write a reader-facing report.html and a standalone components/io-tile-explorer.html.
```

### 3. 可选：把持久 Runner 接入计时器

只有当运行时真的有持续产出内容的 persistent runner 时，才使用此部分。设它的 PID 是 `${RUNNER_PID}` 且它仍然存活：

```sh
COURSE=~/technical-courses/course-records/2026-10-09-flashattention-io-model

python3 scripts/course_timer.py init "$COURSE"
python3 scripts/course_timer.py start-session "$COURSE" "$RUNNER_PID" "alex-preparation"
# runner 将实质内容写进 $COURSE/alex-preparation.md
python3 scripts/course_timer.py end-session "$COURSE" "Alex prepared source map"
python3 scripts/course_timer.py checkpoint "$COURSE" alex_preparation \
  source-map alex-preparation.md "Primary sources and teaching path recorded"
```

对后续阶段重复“live session + 证据 checkpoint”模式。计时器会拒绝跳过阶段、死亡 PID、活跃时间不足和缺少证据的情况；它是完整性机制，不是可挂着不管的秒表。

### 4. 交付前验证

在所有产物、审稿与计时证据完成后：

```sh
python3 scripts/validate_delivery.py \
  ~/technical-courses/course-records/2026-10-09-flashattention-io-model
```

验证器会检查：

- 完整课程与 `submission-package` 产物；
- 完成且有效的计时器状态和 Nora 的 `eligible` 结论；
- 语义 HTML、来源/参考内容、无内部课堂痕迹和至少一个独立交互；
- 原生可键盘操作控件和 `prefers-reduced-motion`；
- Alex、Leo、Alice 各至少两轮审稿记录；
- 唯一明确的 A/B/C 投稿结论。

## 课程产物

```text
course-records/YYYY-MM-DD-topic/
├── preparation-brief.md       # 范围、直接材料和角色边界
├── research.md                # 证据地图和来源状态
├── papers.md                  # 论文谱系与原图计划
├── alex-preparation.md        # 内部备课记录
├── bob-preparation.md         # 独立预习记录
├── transcript.md              # 内部技术对话
├── nora-log.md                # 内部时间顺序审计记录
├── mastery.md                 # 内部 recall/transfer 证据
├── report.html                # 面向公开读者的离线技术文章
├── components/
│   └── *.html                 # 独立技术交互组件
├── reviews.md                 # 问题 → 修改 → 验证记录
├── manifest.md                # 产物和验证清单
├── timer.state / timer.log    # 活跃 session 的计时证据
└── submission-package/        # 编辑源、代码、数据、结果、审稿与结论
```

## 严格计时课程与非计时草稿

| 模式 | 允许做什么 | 可以如何表述 |
| --- | --- | --- |
| 非计时草稿 | 没有 persistent runner 时，也可完成调研、教学、HTML、审稿、组件和投稿材料骨架。 | “证据驱动草稿”或“非计时课程草稿”。 |
| 严格计时课程 | 有效 live runner session、证据文件增长、所有阶段时长/checkpoint、计时完成，以及 Nora 资格结论。 | 已完成完整的 30m + 30m + 2h + 1h 证据门禁课程。 |

不要使用 `sleep`、空闲墙钟时间、结束后的 CLI/model turn、伪造 transcript 时间戳或真实用户的后续消息来满足计时门槛。

## 仓库结构

```text
SKILL.md                       给 Agent 读取的 Skill 入口
README.md                      英文使用文档
README.zh-CN.md                简体中文使用文档
agents/openai.yaml             兼容宿主可用的 UI 元数据
references/course-protocol.md  可移植课程、产物与审稿协议
scripts/init_course.py         初始化课程档案与投稿包骨架
scripts/course_timer.py        PID 活跃时间与 checkpoint 门禁
scripts/validate_delivery.py   交付前验证器
```

## 安全与研究诚信

- 不要提交 API Key、session token、专有源代码、私有论文或敏感课程记录。
- 一手材料优先；论文图、表、实验与结论必须可归因。
- 不得伪造资料、实验结果、代码路径或定量性能。
- A/B/C 是投稿准备度结论，不代表论文已经被接收。
- Skill 可以约束流程，但不能让无证据的主张变成事实；发布前仍应人工审阅。

## 贡献

欢迎提升可移植性、来源严谨性、HTML 可访问性或确定性验证能力的贡献。请保持 runner-agnostic，不要提交凭证或私有内容；修改脚本时请补充测试/冒烟验证。

## 许可证

[MIT](LICENSE)。
