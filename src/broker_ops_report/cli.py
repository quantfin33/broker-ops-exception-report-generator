"""Command-line interface for the broker operations reporting demo."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .config import (
    DEFAULT_MARKET_EVENTS_PATH,
    DEFAULT_ORDER_EVENTS_PATH,
    DEFAULT_OUTPUT_DIR,
    NO_LIVE_INTEGRATIONS_MESSAGE,
    PROJECT_NAME,
    __version__,
)
from .validation import validate_inputs


PLACEHOLDER_MESSAGE = (
    "Phase 1 scaffold only: {command} is not implemented yet. "
    "No data was read, no reports were generated, and no live integrations were used."
)


def _add_common_input_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--orders",
        default=DEFAULT_ORDER_EVENTS_PATH,
        help="Path to broker-style order events CSV.",
    )
    parser.add_argument(
        "--market-events",
        default=DEFAULT_MARKET_EVENTS_PATH,
        help="Path to market events CSV.",
    )


def _placeholder_command(command_name: str) -> int:
    print(PLACEHOLDER_MESSAGE.format(command=command_name))
    print(NO_LIVE_INTEGRATIONS_MESSAGE)
    return 0


def _run_validate_inputs(args: argparse.Namespace) -> int:
    result = validate_inputs(args.orders, args.market_events)
    if result.ok:
        print("Validation successful.")
        print(f"Order events rows: {result.order_rows}")
        print(f"Market events rows: {result.market_event_rows}")
        print(NO_LIVE_INTEGRATIONS_MESSAGE)
        return 0

    print("Validation failed.")
    for issue in result.issues:
        print(f"- {issue.format()}")
    print(NO_LIVE_INTEGRATIONS_MESSAGE)
    return 1


def _run_generate_reports(_args: argparse.Namespace) -> int:
    return _placeholder_command("generate-reports")


def _run_demo(_args: argparse.Namespace) -> int:
    return _placeholder_command("run-demo")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="broker_ops_report",
        description=(
            "Static broker operations exception report generator demo. "
            "Includes CSV schema validation and placeholder report/demo commands."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{PROJECT_NAME} {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    validate_inputs = subparsers.add_parser(
        "validate-inputs",
        help="Validate broker-style input file schemas.",
        description="Validate static broker-style CSV schemas without generating reports.",
    )
    _add_common_input_options(validate_inputs)
    validate_inputs.set_defaults(handler=_run_validate_inputs)

    generate_reports = subparsers.add_parser(
        "generate-reports",
        help="Generate broker operations report outputs. Placeholder only in Phase 1.",
        description="Generate broker operations report outputs. Placeholder only in Phase 1.",
    )
    _add_common_input_options(generate_reports)
    generate_reports.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated report artifacts. Placeholder only in Phase 1.",
    )
    generate_reports.set_defaults(handler=_run_generate_reports)

    run_demo = subparsers.add_parser(
        "run-demo",
        help="Run the static demo workflow. Placeholder only in Phase 1.",
        description="Run the static demo workflow. Placeholder only in Phase 1.",
    )
    run_demo.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated report artifacts. Placeholder only in Phase 1.",
    )
    run_demo.set_defaults(handler=_run_demo)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))
