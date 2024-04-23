from pathlib import Path
from typing import Tuple
from unittest import TestCase

import pytest

from kubedantic.extractor import K8sOpenAPIExtractor
from kubedantic.parser import K8sOpenAPIParser


@pytest.mark.usefixtures("data_path")
class K8sOpenAPIParserTestCase(TestCase):
    data_path: Path

    def setUp(self):
        self.specs_path = self.data_path / "extractor" / "expected"
        self.expected_path = self.data_path / "parser" / "expected"

        self.parser = K8sOpenAPIParser(
            K8sOpenAPIExtractor(output_path=self.specs_path).extract()
        )

    def _compare_with_expected(self, name: Tuple[str, ...], result: str):
        expected_file = self.expected_path.joinpath(*name[4:]).with_suffix(".py")

        with open(expected_file, "r") as f:
            expected = f.read()

        self.assertEqual(expected, result, f"File {expected_file} does not match")

    def test_parse(self):
        results = self.parser.parse()

        for name, result in results.items():
            self._compare_with_expected(name, result.body)
