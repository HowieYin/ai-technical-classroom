# AI Technical Classroom

> A portable **Agent Skill** for turning a technical topic, research paper, codebase, URL, local artifact, or engineering question into an evidence-grounded learning archive and a publication-quality, offline HTML technical report.

`ai-technical-classroom` is not a chatbot, a hosted service, or an LLM SDK. It is a **`SKILL.md`-based workflow package**: install it into a capable coding agent (Claude Code, Codex, TraeX, or another agent runtime that loads Agent Skills), then ask that agent to run a technical course. The agent supplies the model, tool use, file access, browser/research ability, and—in strict timed mode—a durable runner.

## Why This Exists

Most “summarize this paper” workflows produce a thin overview, leak unsupported claims, or stop at an attractive web page. This Skill enforces a deeper technical loop:

```text
direct material
      ↓
paper-first research and evidence map
      ↓
Alex / Bob technical teaching and adversarial mastery checks
      ↓
reader-facing article + mechanism-specific interactive component
      ↓
Alex / Leo / Alice reviews + Nora timing audit
      ↓
offline HTML report + reproducibility / submission package
```

It is designed for AI, ML systems, hardware, mathematics, software architecture, and similar technical subjects where primary sources, equations, source code, experiments, figures, trade-offs, and failure modes matter.

## What You Get

| Capability | What it enforces |
| --- | --- |
| Five-role workflow | Alex Tensor teaches and fact-checks; Bob Prompt learns and writes; Leo performs paper-style technical review; Alice reviews HTML/accessibility; Nora records and audits timing. |
| Paper-first research | Direct user material first; then primary papers, official implementations, official docs, and reproducible evidence. |
| Technical depth | Mechanism, variables/shapes/units, numerical examples, implementation/data flow, complexity, alternatives, and failure modes. |
| Publishable HTML | A reader-facing offline `report.html`, not a transcript or classroom homework page. |
| Meaningful interaction | At least one separate `components/*.html` tool that teaches a real mechanism through an adjustable technical variable. |
| Review gate | Two substantive review/revision/verification rounds for Alex, Leo, and Alice. |
| Evidence gate | Optional PID-backed active-time accounting, checkpoints, and Nora's eligibility verdict. |
| Research package | Editable-paper, code, data, results, venue, mock-review, revision, integrity, and A/B/C verdict scaffolding. |

## When to Use It

Use this Skill when you want an agent to:

- deeply read and teach a paper, survey a field, or explain an implementation;
- transform a local repository, debugging artifact, or system design into a durable technical article;
- create a self-contained HTML report with source figures/tables and a mechanism-specific interactive explainer;
- create an audit trail for research, classroom dialogue, technical review, and reproducibility boundaries;
- distinguish a quick research draft from a genuinely timed, evidence-gated autonomous course.

Do **not** use it for a one-paragraph summary, ordinary prose editing, generic marketing pages, or a claim of experimental evidence that you cannot reproduce or source.

## Requirements

### Required

- An agent runtime that can load a directory containing `SKILL.md`.
- A model capable of technical reasoning and tool use.
- Read/write access to a workspace.
- Python **3.10+** for the bundled helpers. They use only the standard library.

### Strongly Recommended

- Web or browser tools for accessing primary sources and official documentation.
- A browser or HTML renderer for desktop and narrow-screen review.
- A persistent agent runner if you want the strict, timed-course qualification.

### Important: Skill vs. Model/API

This repository does **not** send requests to an LLM by itself and it never stores an API key. Your **agent host** owns LLM configuration:

```text
Agent host configuration  →  model / API key / endpoint / tools
ai-technical-classroom    →  research, course, review, and deliverable workflow
your workspace            →  course-records/<date>-<topic>/
```

The Skill remains useful with a local model, a direct provider API, an OpenAI-compatible gateway, or an Anthropic-compatible gateway—as long as the chosen agent runtime can use that model and call local tools.

## Installation

Clone once, then install the repository root—the directory containing `SKILL.md`—into your agent's Skill search path.

```sh
git clone https://github.com/HowieYin/ai-technical-classroom.git
```

The exact discovery path is host-specific. Common layouts are below; check your installed agent version if it uses a different configured Skills directory.

### Claude Code

Install for one user:

```sh
mkdir -p ~/.claude/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  ~/.claude/skills/ai-technical-classroom
```

Or make it repository-local so a team can version the workflow with the project:

```sh
mkdir -p .claude/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .claude/skills/ai-technical-classroom
```

Restart Claude Code or start a new session after installation. Invoke it explicitly with `$ai-technical-classroom`, or describe a task that matches the Skill metadata.

### Codex CLI / Codex Agents

Install for one user:

```sh
mkdir -p ~/.codex/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  ~/.codex/skills/ai-technical-classroom
```

For a project-local setup:

```sh
mkdir -p .codex/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .codex/skills/ai-technical-classroom
```

Start a fresh Codex session and invoke:

```text
Use $ai-technical-classroom to teach and write a technical report about ...
```

### TraeX / TRAE CLI

Install globally:

```sh
mkdir -p "${TRAE_HOME:-$HOME/.trae}/skills"
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  "${TRAE_HOME:-$HOME/.trae}/skills/ai-technical-classroom"
```

Or install it only for the current workspace:

```sh
mkdir -p .trae/skills
git clone https://github.com/HowieYin/ai-technical-classroom.git \
  .trae/skills/ai-technical-classroom
```

Open a fresh session, then use `$ai-technical-classroom`.

### Other Agent Runtimes

Use any runtime that supports the open `SKILL.md` convention:

1. Place this repository root in its configured Skill directory.
2. Ensure the runtime can read the Skill directory and execute `python3`.
3. Start a new agent session so it rescans Skills.
4. Ask the agent to use `ai-technical-classroom`, explicitly naming the Skill if implicit discovery is unavailable.

If your runtime does not natively support Skills, attach the contents of `SKILL.md` to its system/developer instructions and keep `references/` and `scripts/` accessible at their relative paths.

## Configure the LLM/API in the Agent Host

Do this in the **host**, not in this repository. Never commit an API key to a Skill repository, `SKILL.md`, course archive, or `manifest.md`.

### Claude Code

Authenticate or configure your Claude Code provider using its normal login/API-key mechanism, then launch Claude Code from a shell where the provider credential is available:

```sh
export ANTHROPIC_API_KEY="replace-with-your-secret"
claude
```

If you use an Anthropic-compatible proxy or enterprise gateway, follow that gateway's Claude Code configuration requirements and keep its URL/key in environment variables or the host's private configuration—not in this repository.

### Codex / OpenAI-Compatible Hosts

For a direct OpenAI-compatible host, the common pattern is:

```sh
export OPENAI_API_KEY="replace-with-your-secret"
# Optional only if your host/provider documents a compatible endpoint:
export OPENAI_BASE_URL="https://your-gateway.example/v1"
```

Then configure the host's selected model/provider according to its documentation. Different Codex distributions and versions use different configuration files and provider names, so this repository intentionally does not hard-code a potentially stale config snippet.

### Generic Agent Host

Use this secure pattern:

```sh
export PROVIDER_API_KEY="replace-with-your-secret"
export PROVIDER_BASE_URL="https://provider.example/v1"  # if required
agent-cli --model "provider-model-name"
```

Verify four things before a long course:

1. the agent can make one successful model call;
2. the agent has file-write permission in the target workspace;
3. browser/research tools are available if the topic needs external sources;
4. a durable runner exists if you need verified active-time completion.

## Invoke the Skill

Explicit invocation is the most portable option:

```text
Use $ai-technical-classroom to turn [topic / paper / URL / repository / log] into a rigorous technical course and offline HTML report.
```

Give the agent a clear topic and optional scope. The human is the **course owner**, not the simulated student: do not answer Alex/Bob questions or approve individual stages.

### Prompt: Paper Deep Read

```text
Use $ai-technical-classroom.

Topic: FlashAttention and the IO-aware view of exact attention.
Direct source: https://arxiv.org/abs/2205.14135
Scope: derive the IO model, explain the tiled forward algorithm, compare the
memory/computation trade-off with standard attention, and create an interactive
tile-size / memory-traffic explainer. Deliver an offline English HTML report.
```

### Prompt: Code / Systems Analysis

```text
Use $ai-technical-classroom.

Topic: Explain the scheduler and KV-cache lifecycle in this repository.
Direct material: ./path/to/repository
Scope: trace the real request path, identify data ownership and state
transitions, compare prefill and decode behavior, and write an offline HTML
architecture report with an interactive timeline. Do not invent benchmarks.
```

### Prompt: Untimed Draft

```text
Use $ai-technical-classroom to create an untimed, evidence-grounded research
and HTML draft about speculative decoding. Do not claim the 30m+30m+2h+1h
timed-course qualification unless a persistent runner is actually available.
```

## End-to-End Example

This example shows the **agent-facing** workflow and the optional command-line helpers. The agent should normally run these steps; you do not have to manually simulate the five roles.

### 1. Initialize an Archive

```sh
git clone https://github.com/HowieYin/ai-technical-classroom.git
cd ai-technical-classroom

python3 scripts/init_course.py \
  --output ~/technical-courses \
  --topic "FlashAttention IO model" \
  --source "https://arxiv.org/abs/2205.14135"
```

The command prints a new directory like:

```text
~/technical-courses/course-records/2026-10-08-flashattention-io-model
```

It includes source maps, plans, review tables, a report target, a component directory, timer files, and a submission-package scaffold.

### 2. Ask the Agent to Run It

```text
Use $ai-technical-classroom and work in
~/technical-courses/course-records/2026-10-08-flashattention-io-model.

Read the direct source first. Complete the research map and paper lineage,
then conduct the course autonomously. Keep the classroom record internal;
write a reader-facing report.html and a standalone components/io-tile-explorer.html.
```

### 3. Optional: Attach a Durable Runner to the Timer

Only use this when your runtime has a genuinely persistent, content-producing runner. Assume its PID is `${RUNNER_PID}` and it is still alive:

```sh
COURSE=~/technical-courses/course-records/2026-10-08-flashattention-io-model

python3 scripts/course_timer.py init "$COURSE"
python3 scripts/course_timer.py start-session "$COURSE" "$RUNNER_PID" "alex-preparation"
# The runner writes substantive material to $COURSE/alex-preparation.md.
python3 scripts/course_timer.py end-session "$COURSE" "Alex prepared source map"
python3 scripts/course_timer.py checkpoint "$COURSE" alex_preparation \
  source-map alex-preparation.md "Primary sources and teaching path recorded"
```

Repeat the live-session/checkpoint pattern for the remaining gates. The timer intentionally rejects skipped phases, dead PIDs, insufficient active time, and missing evidence. It is an integrity mechanism, not a stopwatch to leave running.

### 4. Validate Before Delivery

After all artifacts, reviews, and timing evidence are complete:

```sh
python3 scripts/validate_delivery.py \
  ~/technical-courses/course-records/2026-10-08-flashattention-io-model
```

The validator checks for:

- the full course and submission-package inventory;
- a valid completed timer plus Nora's `eligible` verdict;
- semantic HTML, source/reference content, no internal classroom leakage, and at least one standalone interaction;
- accessible native controls and reduced-motion handling;
- two recorded review rounds for Alex, Leo, and Alice;
- one explicit A/B/C submission verdict.

## Course Output

```text
course-records/YYYY-MM-DD-topic/
├── preparation-brief.md       # scope, direct materials, and role boundary
├── research.md                # evidence map and source status
├── papers.md                  # lineage and source-figure plan
├── alex-preparation.md        # internal preparation record
├── bob-preparation.md         # independent learner preparation
├── transcript.md              # internal technical dialogue
├── nora-log.md                # internal chronological audit record
├── mastery.md                 # internal recall/transfer evidence
├── report.html                # public, offline technical article
├── components/
│   └── *.html                 # standalone technical interactions
├── reviews.md                 # issue → change → verification record
├── manifest.md                # artifact and validation inventory
├── timer.state / timer.log    # active-session timing evidence
└── submission-package/        # editable source, code, data, results, review, verdict
```

## Strict Timed Course vs. Untimed Draft

| Mode | What is allowed | What you may claim |
| --- | --- | --- |
| Untimed draft | Research, instruction, HTML, review, components, and submission scaffolding without a persistent runner. | “Evidence-grounded draft” or “untimed course draft.” |
| Timed course | Valid live runner sessions, evidence-file growth, all phase durations/checkpoints, timer completion, and Nora eligibility. | The full 30m + 30m + 2h + 1h evidence-gated course. |

Do not use sleep, idle wall time, a terminated CLI/model turn, fabricated transcript timestamps, or human follow-up messages to satisfy timing gates.

## Repository Layout

```text
SKILL.md                       The machine-facing Skill entry point
README.md                      This human-facing guide
agents/openai.yaml             Optional UI metadata for compatible hosts
references/course-protocol.md  Portable course, artifact, and review contract
scripts/init_course.py         Create a course archive and submission scaffold
scripts/course_timer.py        Enforce PID-backed active-time and checkpoint gates
scripts/validate_delivery.py   Validate the finished archive
```

## Security and Research Integrity

- Never commit API keys, session tokens, proprietary source code, private papers, or sensitive course records.
- Use direct/primary sources before secondary explanations.
- Attribute figures, tables, experiments, and claims; do not fabricate source material or quantitative results.
- A/B/C is a readiness verdict, not a claim that a paper has been accepted.
- Review output before publishing it: the Skill supports rigorous work but cannot make an unsupported claim true.

## Contributing

Contributions are welcome when they improve portability, source-grounded rigor, HTML accessibility, or deterministic validation. Keep changes runner-agnostic, avoid bundling credentials or private content, and add tests/smoke checks for helper-script changes.

## License

[MIT](LICENSE).
