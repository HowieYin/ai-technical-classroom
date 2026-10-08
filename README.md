# ai-technical-classroom

An evidence-gated, multi-role AI technical classroom Skill that turns papers, code, engineering topics, and debugging questions into auditable learning archives and publishable offline HTML reports.

## What It Provides

- A five-role workflow: Alex Tensor (instructor), Bob Prompt (learner/author), Leo (technical reviewer), Alice (HTML reviewer), and Nora (recorder/timing auditor).
- Paper-first research, technical teaching, original-figure interpretation, formula/shape explanations, and role-to-role mastery questioning.
- An offline `report.html` plus standalone accessible `components/*.html` interactions.
- A portable, PID-backed course timer that counts only active autonomous-runner sessions and evidence checkpoints.
- A delivery validator covering artifacts, reviews, timing eligibility, public-report leaks, HTML structure, interactions, and a reproducibility/submission package.

## Install

Copy or clone this repository into a Skill directory supported by your agent runtime. The repository root is the Skill folder and contains `SKILL.md`.

```sh
git clone git@github.com:HowieYin/ai-technical-classroom.git
```

The core scripts require Python 3.10+ and only use the standard library.

## Quick Start

Create a course archive in any workspace:

```sh
python3 scripts/init_course.py \
  --output /path/to/workspace \
  --topic "FlashAttention's IO model" \
  --source "https://arxiv.org/abs/2205.14135"
```

Read `SKILL.md` and `references/course-protocol.md` before running a course. Attach `scripts/course_timer.py` to a durable agent runner if you need auditable timed-course status; without a persistent runner, use the workflow as an untimed research-and-writing draft.

## Structure

```text
SKILL.md                       Skill trigger and workflow
agents/openai.yaml             Optional UI metadata
references/course-protocol.md  Portable operating contract
scripts/init_course.py         Course and submission-package initializer
scripts/course_timer.py        PID-backed active-time evidence gates
scripts/validate_delivery.py   Pre-delivery archive validator
```

## License

MIT. See `LICENSE`.
