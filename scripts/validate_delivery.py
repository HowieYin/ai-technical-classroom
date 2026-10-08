#!/usr/bin/env python3
"""Validate the portable AI Technical Classroom delivery contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


COURSE_FILES = (
    "preparation-brief.md",
    "alex-preparation.md",
    "bob-preparation.md",
    "research.md",
    "plan.md",
    "papers.md",
    "transcript.md",
    "nora-log.md",
    "mastery.md",
    "reviews.md",
    "course-retrospective.md",
    "manifest.md",
    "nora-timing-attestation.md",
    "report.html",
)
SUBMISSION_FILES = (
    "paper-source/README.md",
    "code/README.md",
    "data/README.md",
    "results/README.md",
    "related-work-comparison.md",
    "venue-selection.md",
    "mock-review.md",
    "revision-log.md",
    "academic-integrity.md",
    "submission-verdict.md",
)
PUBLIC_LEAKS = (
    r"\bAlex Tensor\b",
    r"\bBob Prompt\b",
    r"\bLeo\b",
    r"\bAlice\b",
    r"\bNora\b",
    r"\bTeaching\s+\d+\b",
    r"\bgrill(?:ing)?\b",
    r"学习债务",
    r"停车场",
)


def contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), flags=re.IGNORECASE) is not None


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <course-dir>", file=sys.stderr)
        return 2

    course_dir = Path(sys.argv[1]).expanduser().resolve()
    failures: list[str] = []

    if not course_dir.is_dir():
        print(f"FAIL: missing course directory: {course_dir}", file=sys.stderr)
        return 2

    for relative in COURSE_FILES:
        path = course_dir / relative
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty required artifact: {relative}")

    for relative in SUBMISSION_FILES:
        path = course_dir / "submission-package" / relative
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty submission artifact: {relative}")

    report = course_dir / "report.html"
    if report.is_file() and report.stat().st_size:
        for pattern, description in (
            (r"<!doctype html|<html[\s>]", "HTML root"),
            (r"<main[\s>]", "semantic main"),
            (r"<(?:h1|title)[\s>]", "title"),
            (r"reference|source|来源|参考", "reference section"),
            (r"component|组件|交互", "interaction explanation"),
        ):
            if not contains(report, pattern):
                failures.append(f"report lacks {description}")
        for pattern in PUBLIC_LEAKS:
            if contains(report, pattern):
                failures.append(f"public report leaks internal classroom text: {pattern}")

    components = sorted((course_dir / "components").glob("*.html"))
    if not components:
        failures.append("no standalone HTML component")
    for component in components:
        if not contains(component, r"<!doctype html|<html[\s>]"):
            failures.append(f"component is not HTML: {component.name}")
        if not contains(component, r"<(?:button|input|select|textarea)[\s>]"):
            failures.append(f"component lacks a native keyboard control: {component.name}")
        if not contains(component, r"prefers-reduced-motion"):
            failures.append(f"component lacks reduced-motion handling: {component.name}")

    reviews = course_dir / "reviews.md"
    if reviews.is_file() and reviews.stat().st_size:
        for reviewer in ("Alex", "Leo", "Alice"):
            if len(re.findall(reviewer, reviews.read_text(encoding="utf-8"), flags=re.IGNORECASE)) < 2:
                failures.append(f"reviews lack two recorded rounds for {reviewer}")
        if not contains(reviews, r"blocker|major|closed|关闭"):
            failures.append("reviews do not show disposition of major issues")

    timer_file = course_dir / "timer.state"
    if not timer_file.is_file():
        failures.append("missing timer.state")
    else:
        try:
            timer = json.loads(timer_file.read_text(encoding="utf-8"))
            if timer.get("phase") != "complete":
                failures.append("timer does not report phase=complete")
            if timer.get("validity") != "valid":
                failures.append("timer validity is not valid")
            if timer.get("nora_verdict") != "eligible":
                failures.append("Nora has not marked timing eligible")
            targets = {
                "alex_preparation": 1800,
                "bob_preparation": 1800,
                "teaching": int(timer.get("teaching_target_seconds", 7200)),
                "discussion": 3600,
            }
            checkpoints = {
                "alex_preparation": 2,
                "bob_preparation": 2,
                "teaching": 4,
                "discussion": 2,
            }
            active_seconds = timer.get("active_seconds", {})
            recorded_checkpoints = timer.get("checkpoints", {})
            for phase, target in targets.items():
                if float(active_seconds.get(phase, 0)) < target:
                    failures.append(f"timer active time is below threshold for {phase}")
                if len(recorded_checkpoints.get(phase, [])) < checkpoints[phase]:
                    failures.append(f"timer checkpoints are below threshold for {phase}")
        except json.JSONDecodeError:
            failures.append("timer.state is not valid JSON")

    verdict = course_dir / "submission-package" / "submission-verdict.md"
    if verdict.is_file() and verdict.stat().st_size:
        matches = re.findall(r"(?m)^\s*([ABC])[\.:、]", verdict.read_text(encoding="utf-8"))
        if len(matches) != 1:
            failures.append("submission verdict must state exactly one A/B/C conclusion")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print(f"Delivery validation failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    print(f"Delivery validation passed: {report} ({len(components)} component(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
