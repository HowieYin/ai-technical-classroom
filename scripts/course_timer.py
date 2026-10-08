#!/usr/bin/env python3
"""Evidence-gated active-time tracker for an autonomous technical course."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path


PHASES = ("alex_preparation", "bob_preparation", "teaching", "discussion")
TARGET_SECONDS = {
    "alex_preparation": 1800,
    "bob_preparation": 1800,
    "teaching": 7200,
    "discussion": 3600,
}
REQUIRED_CHECKPOINTS = {
    "alex_preparation": 2,
    "bob_preparation": 2,
    "teaching": 4,
    "discussion": 2,
}


@dataclass
class State:
    phase: str = "alex_preparation"
    validity: str = "valid"
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    active_seconds: dict[str, float] = field(
        default_factory=lambda: {phase: 0.0 for phase in PHASES}
    )
    checkpoints: dict[str, list[dict[str, object]]] = field(
        default_factory=lambda: {phase: [] for phase in PHASES}
    )
    teaching_target_seconds: int = TARGET_SECONDS["teaching"]
    session: dict[str, object] | None = None
    nora_verdict: str = "pending"


def state_path(course_dir: Path) -> Path:
    return course_dir / "timer.state"


def log_path(course_dir: Path) -> Path:
    return course_dir / "timer.log"


def load(course_dir: Path) -> State:
    path = state_path(course_dir)
    if not path.exists():
        raise ValueError(f"timer not initialized: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return State(**payload)


def save(course_dir: Path, state: State) -> None:
    state_path(course_dir).write_text(
        json.dumps(asdict(state), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def log(course_dir: Path, action: str, **fields: object) -> None:
    payload = {"at": time.time(), "action": action, **fields}
    with log_path(course_dir).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def process_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def ensure_valid(state: State) -> None:
    if state.validity != "valid":
        raise ValueError(f"course timing is invalid: {state.validity}")


def ensure_no_open_session(state: State) -> None:
    if state.session is not None:
        raise ValueError("a timer session is already open")


def phase_ready(state: State, phase: str) -> bool:
    return (
        state.active_seconds[phase] >= target_for(state, phase)
        and len(state.checkpoints[phase]) >= REQUIRED_CHECKPOINTS[phase]
    )


def target_for(state: State, phase: str) -> int:
    return state.teaching_target_seconds if phase == "teaching" else TARGET_SECONDS[phase]


def required_evidence(course_dir: Path, evidence: str) -> Path:
    candidate = (course_dir / evidence).resolve()
    if course_dir.resolve() not in candidate.parents:
        raise ValueError("evidence path must remain inside the course directory")
    if not candidate.is_file() or candidate.stat().st_size == 0:
        raise ValueError(f"missing or empty evidence file: {evidence}")
    return candidate


def command_init(args: argparse.Namespace) -> None:
    args.course_dir.mkdir(parents=True, exist_ok=True)
    if state_path(args.course_dir).exists():
        raise ValueError(f"timer already initialized: {state_path(args.course_dir)}")
    state = State()
    save(args.course_dir, state)
    log(args.course_dir, "initialized", standard="30m+30m+2h+1h")
    print(f"initialized {args.course_dir}")


def command_start_session(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    ensure_no_open_session(state)
    if state.phase not in PHASES:
        raise ValueError(f"cannot start a session in phase {state.phase}")
    if args.pid <= 0 or not process_is_alive(args.pid):
        raise ValueError(f"runner PID is not alive: {args.pid}")
    state.session = {
        "pid": args.pid,
        "label": args.label,
        "phase": state.phase,
        "started_at": time.time(),
    }
    save(args.course_dir, state)
    log(args.course_dir, "session_started", pid=args.pid, label=args.label, phase=state.phase)
    print(f"started {state.phase} session for PID {args.pid}")


def command_end_session(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    if state.session is None:
        raise ValueError("no timer session is open")
    session = state.session
    pid = int(session["pid"])
    if not process_is_alive(pid):
        state.validity = "invalid:runner_died_before_session_close"
        state.session = None
        save(args.course_dir, state)
        log(args.course_dir, "invalidated", reason=state.validity)
        raise ValueError(state.validity)
    elapsed = time.time() - float(session["started_at"])
    phase = str(session["phase"])
    state.active_seconds[phase] += elapsed
    state.session = None
    save(args.course_dir, state)
    log(args.course_dir, "session_closed", phase=phase, elapsed_seconds=elapsed, summary=args.summary)
    print(f"credited {elapsed:.1f}s to {phase}")


def command_checkpoint(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    if args.phase != state.phase:
        raise ValueError(f"checkpoint phase {args.phase} does not match current phase {state.phase}")
    evidence = required_evidence(args.course_dir, args.evidence)
    item = {
        "id": args.activity_id,
        "evidence": str(evidence.relative_to(args.course_dir.resolve())),
        "summary": args.summary,
        "at": time.time(),
        "bytes": evidence.stat().st_size,
    }
    state.checkpoints[args.phase].append(item)
    save(args.course_dir, state)
    log(args.course_dir, "checkpoint", phase=args.phase, **item)
    print(f"recorded {args.phase} checkpoint {args.activity_id}")


def command_next_phase(args: argparse.Namespace, expected: str, next_phase: str) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    ensure_no_open_session(state)
    if state.phase != expected:
        raise ValueError(f"expected {expected}, current phase is {state.phase}")
    if not phase_ready(state, expected):
        raise ValueError(
            f"{expected} gate not met: {state.active_seconds[expected]:.1f}/"
            f"{target_for(state, expected)} seconds, {len(state.checkpoints[expected])}/"
            f"{REQUIRED_CHECKPOINTS[expected]} checkpoints"
        )
    state.phase = next_phase
    save(args.course_dir, state)
    log(args.course_dir, "phase_changed", previous=expected, current=next_phase)
    print(f"entered {next_phase}")


def command_extend_teaching(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    if state.phase != "teaching":
        raise ValueError("teaching can only be extended while in the teaching phase")
    if args.seconds <= 0 or state.teaching_target_seconds + args.seconds > 14400:
        raise ValueError("teaching total must remain between 2 and 4 hours")
    state.teaching_target_seconds += args.seconds
    save(args.course_dir, state)
    log(args.course_dir, "teaching_extended", seconds=args.seconds, reason=args.reason)
    print(f"teaching target extended by {args.seconds}s")


def command_finish(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    ensure_valid(state)
    ensure_no_open_session(state)
    if state.phase != "discussion" or not phase_ready(state, "discussion"):
        raise ValueError("discussion gate is not met")
    state.phase = "complete"
    state.finished_at = time.time()
    save(args.course_dir, state)
    log(args.course_dir, "completed")
    print("course timing complete; Nora attestation still required")


def command_attest(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    if args.verdict == "eligible":
        if state.phase != "complete" or state.validity != "valid":
            raise ValueError("cannot attest eligible before valid timer completion")
        missing = [phase for phase in PHASES if not phase_ready(state, phase)]
        if missing:
            raise ValueError(f"cannot attest eligible; gates missing for {', '.join(missing)}")
    state.nora_verdict = args.verdict
    save(args.course_dir, state)
    log(args.course_dir, "nora_attested", verdict=args.verdict)
    print(f"Nora timing verdict: {args.verdict}")


def command_invalidate(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    state.validity = f"invalid:{args.reason}"
    state.session = None
    save(args.course_dir, state)
    log(args.course_dir, "invalidated", reason=args.reason)
    print(state.validity)


def command_status(args: argparse.Namespace) -> None:
    state = load(args.course_dir)
    payload = asdict(state)
    payload["targets"] = {**TARGET_SECONDS, "teaching": state.teaching_target_seconds}
    payload["required_checkpoints"] = REQUIRED_CHECKPOINTS
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("course_dir", type=Path)
    init.set_defaults(func=command_init)

    start = commands.add_parser("start-session")
    start.add_argument("course_dir", type=Path)
    start.add_argument("pid", type=int)
    start.add_argument("label")
    start.set_defaults(func=command_start_session)

    end = commands.add_parser("end-session")
    end.add_argument("course_dir", type=Path)
    end.add_argument("summary")
    end.set_defaults(func=command_end_session)

    checkpoint = commands.add_parser("checkpoint")
    checkpoint.add_argument("course_dir", type=Path)
    checkpoint.add_argument("phase", choices=PHASES)
    checkpoint.add_argument("activity_id")
    checkpoint.add_argument("evidence")
    checkpoint.add_argument("summary")
    checkpoint.set_defaults(func=command_checkpoint)

    for name, expected, next_phase in (
        ("begin-bob-preparation", "alex_preparation", "bob_preparation"),
        ("begin-teaching", "bob_preparation", "teaching"),
        ("begin-discussion", "teaching", "discussion"),
    ):
        subparser = commands.add_parser(name)
        subparser.add_argument("course_dir", type=Path)
        subparser.set_defaults(
            func=lambda args, expected=expected, next_phase=next_phase: command_next_phase(
                args, expected, next_phase
            )
        )

    extend = commands.add_parser("extend-teaching")
    extend.add_argument("course_dir", type=Path)
    extend.add_argument("seconds", type=int)
    extend.add_argument("reason")
    extend.set_defaults(func=command_extend_teaching)

    finish = commands.add_parser("finish")
    finish.add_argument("course_dir", type=Path)
    finish.set_defaults(func=command_finish)

    attest = commands.add_parser("nora-attest")
    attest.add_argument("course_dir", type=Path)
    attest.add_argument("verdict", choices=("eligible", "ineligible"))
    attest.set_defaults(func=command_attest)

    invalidate = commands.add_parser("invalidate")
    invalidate.add_argument("course_dir", type=Path)
    invalidate.add_argument("reason")
    invalidate.set_defaults(func=command_invalidate)

    status = commands.add_parser("status")
    status.add_argument("course_dir", type=Path)
    status.set_defaults(func=command_status)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.func(args)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
