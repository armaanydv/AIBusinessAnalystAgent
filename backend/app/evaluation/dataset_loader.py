"""
Utilities for loading benchmark datasets used for retrieval evaluation.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.evaluation.evaluation_models import BenchmarkQuestion


class DatasetLoader:
    """
    Loads and validates benchmark datasets.
    """

    @staticmethod
    def load_dataset(dataset_path: str | Path) -> list[BenchmarkQuestion]:
        """
        Load and validate a benchmark dataset.

        Args:
            dataset_path:
                Path to the benchmark dataset JSON file.

        Returns:
            List of validated BenchmarkQuestion objects.

        Raises:
            FileNotFoundError:
                If the dataset file does not exist.

            ValueError:
                If the dataset is not a JSON array.

            ValidationError:
                If any benchmark question is invalid.
        """

        dataset_path = Path(dataset_path)

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {dataset_path}"
            )

        with dataset_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            raw_data = json.load(file)

        if not isinstance(raw_data, list):
            raise ValueError(
                "Benchmark dataset must be a JSON array."
            )

        return [
            BenchmarkQuestion.model_validate(item)
            for item in raw_data
        ]