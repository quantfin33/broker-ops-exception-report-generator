from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class BrokerOpsCliTests(unittest.TestCase):
    def run_module(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        return subprocess.run(
            [sys.executable, "-m", "broker_ops_report", *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_imports(self) -> None:
        import broker_ops_report

        self.assertEqual(
            broker_ops_report.PROJECT_NAME,
            "Broker Operations Exception Report Generator",
        )

    def test_root_help_works(self) -> None:
        result = self.run_module("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validate-inputs", result.stdout)
        self.assertIn("generate-reports", result.stdout)
        self.assertIn("run-demo", result.stdout)

    def test_command_help_works(self) -> None:
        for command in ("validate-inputs", "generate-reports", "run-demo"):
            with self.subTest(command=command):
                result = self.run_module(command, "--help")

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(command, result.stdout)

    def test_validate_inputs_command_succeeds_for_current_fixtures(self) -> None:
        result = self.run_module("validate-inputs")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validation successful.", result.stdout)
        self.assertIn("Order events rows:", result.stdout)
        self.assertIn("Market events rows:", result.stdout)

    def test_report_commands_remain_placeholders(self) -> None:
        for command in ("generate-reports", "run-demo"):
            with self.subTest(command=command):
                result = self.run_module(command)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Phase 1 scaffold only", result.stdout)
                self.assertIn("No data was read", result.stdout)
                self.assertIn("no live broker", result.stdout)

    def test_no_network_or_live_dependencies_are_required(self) -> None:
        from broker_ops_report import config

        self.assertFalse(config.LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(config.NETWORK_DEPENDENCIES, ())
        self.assertIn("no live broker", config.NO_LIVE_INTEGRATIONS_MESSAGE)


if __name__ == "__main__":
    unittest.main()
