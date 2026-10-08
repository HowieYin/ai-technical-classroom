---
name: ai-technical-classroom
description: Run a rigorous, evidence-gated technical learning workflow that turns an AI, systems, mathematics, or engineering topic, paper, URL, repository, local files, or debugging question into a publishable offline HTML technical report. Use when an agent must independently research and teach a topic through the Alex Tensor, Bob Prompt, Leo, Alice, and Nora roles; produce paper-first analysis, original-figure interpretation, meaningful interactive HTML components, review records, reproducibility materials, and an auditable course archive.
---

# AI Technical Classroom

Create a durable course workspace, then run a paper-first technical course without making the course owner act as a simulated student or reviewer. Deliver a reader-facing `report.html`, never a classroom transcript masquerading as an article.

This skill works with any capable agent runner. Its bundled scripts are runner-agnostic: they initialize course artifacts, enforce active-session timing evidence, and validate delivery. A long-running autonomous agent process is required before claiming timed-course completion.

## Start

1. Read `references/course-protocol.md` before planning or creating course files.
2. Initialize an empty output directory:

   ```sh
   python3 <skill-dir>/scripts/init_course.py \
     --output <workspace> --topic "<topic>" --source "<paper, URL, or local path>"
   ```

   The script creates `<workspace>/course-records/<date>-<slug>/`. Do not overwrite an existing course.
3. Read the initialized `preparation-brief.md`, `plan.md`, and `research.md`; resolve the topic boundary and primary sources before any teaching segment.
4. Use `scripts/course_timer.py` only around live, content-producing autonomous runner sessions. It rejects wall-clock idling, missing evidence, phase skips, and dead runner PIDs.
5. Produce the final report and run `scripts/validate_delivery.py <course-dir>`. Fix every failure before reporting completion.

## Roles

- **Alex Tensor — instructor and factual reviewer:** research first, define the central technical question, teach mechanism and evidence, and reject unsupported claims.
- **Bob Prompt — learner and author:** prepare independently, ask concrete questions, pass recall/transfer checks, write the public-facing HTML, and resolve reviews.
- **Leo — technical peer reviewer:** assess novelty positioning, evidence, comparisons, reproducibility, figure claims, and conclusion strength.
- **Alice — HTML and information-design reviewer:** assess reading hierarchy, responsive rendering, accessibility, and whether every interaction serves a technical question.
- **Nora — recorder and timing auditor:** record the process in internal files and attest only when all timed phases have live-session and evidence support.

Never ask the real course owner to answer questions intended for Bob or to approve stage transitions. Simulate role-to-role dialogue internally and keep it in `transcript.md` / `nora-log.md`, not in `report.html`.

## Workflow

### 1. Prepare

Create and fill `preparation-brief.md`, `research.md`, `papers.md`, and `plan.md`.

- Read user-supplied papers, URLs, code, logs, and local files directly before extending research.
- Prefer primary papers, author pages, official documentation, official implementations, and reproducible measurements.
- Build a 5–10 paper lineage and deeply read at least three core papers when the topic has a sufficient literature.
- Record each source, claim, evidence type, limitations, and planned report location.
- Do not invent citations, measurements, figure contents, benchmarks, code paths, or publication venues.

### 2. Teach and Test

Run separate Alex preparation, Bob preparation, teaching, and discussion phases. The normal minimum is 30 minutes + 30 minutes + 2 hours + 1 hour of **active, PID-backed** work. Teaching may be extended to four hours when documented.

- Start a timer session only while a durable runner PID is alive.
- Add phase checkpoints only after their cited evidence file grew with substantive work.
- Use the `grill-me` / `grilling` approach whenever a role exposes an ambiguity, weak causal explanation, unsupported claim, or merely fluent recall.
- Teach each important mechanism through: problem → intuition → concrete example → formal variables/shapes/units → algorithm/dataflow → engineering consequence → failure mode → recall or transfer test.
- Treat formula explanation as incomplete until it states symbols, source, shape/unit, operations, numerical example, costs, alternatives, and failure boundary.

If no persistent runner exists, create research and draft artifacts but state clearly that the course is an untimed draft. Never manufacture elapsed time, use sleep/polling, or treat an ended agent turn as a live course.

### 3. Write the Technical Article

Write `report.html` for external technical readers, not for the classroom. It must:

- lead with the central question, scope, conclusion, and direction map;
- connect background, prior work, mechanism, source evidence, implementation, comparisons, limits, and conclusion as one argument;
- distinguish sourced facts from explicitly bounded analysis in normal academic prose, without internal classroom labels;
- place source figures/tables next to their first full explanation; identify source, figure/table number, and what the graphic does and does not establish;
- include at least one standalone `components/*.html` interaction tied to the actual mechanism, with native keyboard controls, no-JS core fallback, visible focus, and reduced-motion behavior;
- stay usable offline through local relative assets or self-contained markup.

Do not leak role names, teaching stages, mastery colors, internal evidence labels, transcript language, or unresolved course logistics into the public report.

### 4. Review and Publish

Run at least two substantive `review → revision → verification` rounds for Alex, Leo, and Alice. Keep the issue-to-fix trail in `reviews.md`; do not claim approval with any open blocker or major issue.

Before final delivery:

- render `report.html` and each component at desktop and narrow widths;
- verify all claimed figures load and no empty media columns squeeze text;
- write the submission package: editable source, code/environment notes, data provenance, results/plotting notes, related-work comparison, venue rationale, mock review, revision log, academic-integrity declaration, and exactly one A/B/C verdict;
- have Nora write `nora-timing-attestation.md` only after the timer reports a valid complete course;
- run the validator and record its result in `manifest.md`.

## Bundled Resources

- `references/course-protocol.md`: portable operating contract and artifact specification.
- `scripts/init_course.py`: create a self-contained course skeleton.
- `scripts/course_timer.py`: enforce live-session active-time and evidence gates.
- `scripts/validate_delivery.py`: check a course archive before delivery.
- `assets/`: intentionally empty; place reusable, license-compatible HTML/CSS assets here only when needed.
