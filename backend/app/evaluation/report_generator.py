"""
Utilities for generating benchmark reports.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from app.evaluation.evaluation_models import BenchmarkReport

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates benchmark reports in different formats.
    """

    def __init__(
        self,
        output_directory: str | Path,
    ) -> None:

        self._output_directory = Path(
            output_directory
        )

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # Console
    # ---------------------------------------------------------

    def generate_console_report(
        self,
        report: BenchmarkReport,
    ) -> None:
        """
        Print a formatted benchmark report.
        """

        print()
        print("=" * 50)
        print(" Retrieval Benchmark Report")
        print("=" * 50)
        print()

        print(
            f"Questions Evaluated : "
            f"{report.total_questions}"
        )

        print(
            f"Recall@1            : "
            f"{report.recall_at_1:.3f}"
        )

        print(
            f"Recall@5            : "
            f"{report.recall_at_5:.3f}"
        )

        print(
            f"Precision@5         : "
            f"{report.precision_at_5:.3f}"
        )

        print(
            f"MRR                 : "
            f"{report.mrr:.3f}"
        )

        print(
            f"Hit Rate            : "
            f"{report.hit_rate:.3f}"
        )

        print(
            f"Average Latency     : "
            f"{report.average_latency_ms:.2f} ms"
        )

        print()

        logger.info(
            "Console report generated."
        )

    # ---------------------------------------------------------
    # JSON
    # ---------------------------------------------------------

    def generate_json_report(
        self,
        report: BenchmarkReport,
    ) -> Path:
        """
        Save the benchmark report as JSON.

        Returns:
            Path to the generated report.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_path = (
            self._output_directory
            / f"benchmark_{timestamp}.json"
        )

        output_path.write_text(
            report.model_dump_json(
                indent=4,
            ),
            encoding="utf-8",
        )

        logger.info(
            "Benchmark report saved to '%s'.",
            output_path,
        )

        return output_path