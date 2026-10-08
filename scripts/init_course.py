#!/usr/bin/env python3
"""Initialize a portable AI Technical Classroom course archive."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FILES = {
    "preparation-brief.md": """# Preparation Brief

## Topic
{topic}

## Central Technical Question
<!-- State one answerable question. -->

## Scope and Non-goals
<!-- Bound the course. -->

## Direct Materials
{sources}

## Roles and Expected Outputs
- Alex: research and teaching plan
- Bob: independent preparation and technical HTML article
- Leo: technical peer review
- Alice: HTML and interaction review
- Nora: chronological record and timing audit
""",
    "research.md": """# Research Map

| Source | Type | Date/version | Claim to verify | Evidence level | Limitation | Planned use |
| --- | --- | --- | --- | --- | --- | --- |
{source_rows}
""",
    "papers.md": """# Paper Lineage

Build a 5–10 work lineage where the topic has sufficient literature. Select at least three core papers for deep reading.

| Work | Year | Primary link | Position in lineage | Core reading | Figures/tables to interpret |
| --- | ---: | --- | --- | --- | --- |
""",
    "plan.md": """# Course Plan

## Topic
{topic}

## Timed Standard
- Alex preparation: 30 minutes, 2 checkpoints
- Bob preparation: 30 minutes, 2 checkpoints
- Teaching: 2 hours, 4 checkpoints; extend to 4 hours only with a written reason
- Discussion: 1 hour, 2 checkpoints

## Central Question, Reader, and Article Thesis
<!-- Fill after direct-source research. -->

## Teaching Modules
1. Problem, lineage, and intuition
2. Formal mechanism and numerical example
3. Implementation, evidence, comparison, and failure modes
4. Recall, transfer, debate, and writing plan

## Interaction Plan
<!-- Name one technical variable the reader can alter and the observation it teaches. -->
""",
    "alex-preparation.md": "# Alex Preparation\n\n<!-- Sources, teaching dependencies, examples, risks, and checkpoints. -->\n",
    "bob-preparation.md": "# Bob Preparation\n\n<!-- Independent map, confusions, initial explanation, and test cases. -->\n",
    "transcript.md": "# Course Transcript\n\n<!-- Alex/Bob technical dialogue and active-session evidence. -->\n",
    "nora-log.md": "# Nora Chronological Record\n\n<!-- Chronological audit record. Add all four phase headings before attestation. -->\n",
    "mastery.md": "# Mastery Record\n\n## Green\n\n## Yellow\n\n## Red / Learning Debts\n\n## Transfer Tests\n",
    "reviews.md": """# Reviews

| Round | Reviewer | ID | Location | Severity | Evidence | Bob revision | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
""",
    "course-retrospective.md": "# Course Retrospective\n\n## Problem and Root Cause\n\n## Strong Moment and Reuse Rule\n\n## Role Improvements\n",
    "manifest.md": """# Manifest

## Course
- Topic: {topic}
- Course standard: portable 30m + 30m + 2h + 1h active-time workflow
- Status: initialized; not yet timed or delivered

## Artifact Inventory
<!-- Fill paths, sources, validation command/result, and review status. -->
""",
    "nora-timing-attestation.md": "# Nora Timing Attestation\n\nStatus: pending\n\n<!-- Mark eligible only after timer completion and all evidence gates. -->\n",
}

SUBMISSION_FILES = {
    "paper-source/README.md": "# Editable Paper Source\n\nDescribe editable source files and build steps.\n",
    "code/README.md": "# Code and Environment\n\nDescribe code, environment, commands, and reproducibility limits.\n",
    "data/README.md": "# Data Provenance\n\nDescribe data source, license/access conditions, preprocessing, or why no data applies.\n",
    "results/README.md": "# Results and Plotting\n\nDescribe raw results, plotting steps, and correspondence between figures and claims.\n",
    "related-work-comparison.md": "# Related Work Comparison\n\n| Work | Method | Data/setting | Metric/evidence | Strength | Limitation |\n| --- | --- | --- | --- | --- | --- |\n",
    "venue-selection.md": "# Venue Selection\n\nRecord three scope-matched candidate venues, their dated classification/source, and selection rationale.\n",
    "mock-review.md": "# Mock Review\n\n## Strengths\n\n## Major Concerns\n\n## Required Revisions\n",
    "revision-log.md": "# Revision Log\n\n| Review ID | Change | Files/sections | Verification |\n| --- | --- | --- | --- |\n",
    "academic-integrity.md": "# Academic Integrity\n\nDisclose AI assistance, source verification, authorship, and any unavailable materials.\n",
    "submission-verdict.md": "# Submission Verdict\n\nB: Not yet ready. State the concrete missing experiments, revisions, or verification needed.\n",
}


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (normalized or "technical-course")[:48].rstrip("-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Workspace root for course-records/")
    parser.add_argument("--topic", required=True, help="Course topic")
    parser.add_argument("--source", action="append", default=[], help="Direct paper, URL, or local path; repeatable")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.output.expanduser().resolve()
    course_root = workspace / "course-records"
    base = course_root / f"{date.today():%F}-{slugify(args.topic)}"
    course_dir = base
    index = 2
    while course_dir.exists():
        course_dir = Path(f"{base}-{index:02d}")
        index += 1

    course_dir.mkdir(parents=True)
    (course_dir / "components").mkdir()
    (course_dir / "figures").mkdir()
    submission_dir = course_dir / "submission-package"
    submission_dir.mkdir()

    sources = args.source or ["<!-- Add direct materials before research begins. -->"]
    source_lines = "\n".join(f"- {source}" for source in sources)
    source_rows = "\n".join(
        f"| {source} | direct material | unknown | <!-- verify --> | pending | <!-- add --> | <!-- add --> |"
        for source in sources
    )
    replacements = {"topic": args.topic, "sources": source_lines, "source_rows": source_rows}

    for relative_path, template in REQUIRED_FILES.items():
        (course_dir / relative_path).write_text(template.format(**replacements), encoding="utf-8")
    for relative_path, content in SUBMISSION_FILES.items():
        target = submission_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    print(course_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
