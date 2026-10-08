# Portable Course Protocol

## Contract

Turn one technical topic into an auditable learning process and a publication-quality, offline technical HTML report. The course owner provides the topic or materials only; all classroom roles act autonomously.

The public report is not a learning diary. Keep role dialogue, timing evidence, mastery checks, source uncertainty notes, and review logistics in the course archive.

## Required Roles

| Role | Responsibility | May approve |
| --- | --- | --- |
| Alex Tensor | research, instruction, technical correctness | technical content |
| Bob Prompt | independent preparation, questions, article writing | no self-approval |
| Leo | peer-review rigor, literature, experiments, claims | technical review |
| Alice | HTML engineering, accessibility, information design | presentation review |
| Nora | chronological record and timing qualification | timing eligibility only |

## Timed Course Standard

The normal standard is:

| Phase | Minimum active time | Checkpoints | Primary evidence |
| --- | ---: | ---: | --- |
| Alex preparation | 30 min | 2 | `alex-preparation.md` |
| Bob preparation | 30 min | 2 | `bob-preparation.md` |
| Teaching | 2 h | 4 | `transcript.md` |
| Discussion | 1 h | 2 | `transcript.md` |

Teaching may extend to a total of four hours only with a reason in `plan.md`.

Count time only while a durable autonomous runner is alive, a timer session is open, and the cited evidence grows. Do not count an ended CLI turn, `sleep`, polling, waiting, repeated filler, fabricated timestamps, or an owner response. Mark a course as an untimed draft if this evidence cannot be collected.

## Preparation

1. Create `preparation-brief.md` with the central question, scope, audience, sources, expected artifacts, and non-goals.
2. Build `research.md` from direct user material first, then primary sources. Record source URL/path, date/version, claim, evidence level, limitations, and planned use.
3. Create a 5–10 work lineage and select at least three core papers where the literature supports it. Explain inheritance, disagreement, and trade-offs.
4. Have Alex and Bob independently prepare. Preparation artifacts must not appear in the final article.

## Teaching and Discussion

For each mechanism, cover:

1. problem and prior limitation;
2. intuitive model plus where the analogy fails;
3. minimal concrete example;
4. variables, shapes or units, assumptions, and algorithm;
5. numerical example or code/data flow;
6. implementation, complexity, system consequence, and observable behavior;
7. alternatives, failure modes, and counterexamples;
8. recall, derivation, diagnosis, or transfer test.

Use adversarial role-to-role questioning whenever a claim is vague, a derivation skips a step, a causal explanation lacks evidence, or a learner only repeats fluent text. Close each branch with evidence or record it as an unresolved limitation.

## Course Archive

Create these files under one unique course directory:

```text
preparation-brief.md      alex-preparation.md      bob-preparation.md
research.md               plan.md                  papers.md
transcript.md             nora-log.md              mastery.md
report.html               components/*.html        reviews.md
course-retrospective.md   manifest.md              timer.state
timer.log                 nora-timing-attestation.md
submission-package/
```

The submission package contains:

```text
paper-source/README.md  code/README.md  data/README.md  results/README.md
related-work-comparison.md  venue-selection.md  mock-review.md
revision-log.md  academic-integrity.md  submission-verdict.md
```

## Public HTML Requirements

`report.html` must have a title, semantic `<main>`, a source section, and a coherent chain:

1. central question, scope, and conclusion;
2. direction map and prior work;
3. core mechanism, formula/algorithm, and concrete example;
4. source-material interpretation, including original figures/tables where available;
5. evidence, implementation, comparisons, limitations, and reproducibility boundary;
6. conclusion and references.

For each source figure/table: state the source, identifier, and placement; describe axes, legends, symbols, modules, reading order, the supported conclusion, and what it cannot prove. Do not substitute Mermaid for source evidence.

At least one standalone `components/*.html` page must answer a technical learning question. Use native controls, keyboard access, visible focus, reduced-motion support, a no-JS fallback, and explicit toy-model labels when appropriate.

Do not include Alex, Bob, Leo, Alice, Nora, lesson stage labels, mastery colors, transcript dialogue, timer metadata, internal evidence labels, or unresolved course administration in the public article.

## Review and Verdict

Record at least two substantive review/revision/verification rounds for Alex, Leo, and Alice. Every issue must include its location, severity, evidence, change, and final status. Render the report and components at desktop and narrow widths; reject missing figures, empty media columns, narrow squeezed text, horizontal overflow, inaccessible controls, or decorative-only interaction.

Select exactly one submission verdict:

- **A:** ready for the stated target, with auditable novelty, data, baselines, ablations or mechanism evidence, reproducibility, and format checks.
- **B:** potentially suitable but missing specified experiments, revisions, or verification.
- **C:** the question or contribution must be redesigned.

Nora may mark timing `eligible` only after every timed phase meets its active-time and checkpoint gates with valid evidence. Otherwise record `ineligible`; do not claim the course completed on the timed standard.
