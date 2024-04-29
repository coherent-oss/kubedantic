import json
import shutil
from pathlib import Path
from typing import Any
from unittest import TestCase, mock

import pytest

from generator.extractor import K8sOpenAPIExtractor, NoSchemaFoundError


@pytest.mark.usefixtures("data_path")
class K8sOpenAPIExtractorTestCase(TestCase):
    data_path: Path

    def setUp(self):
        self.data_path = self.data_path / "extractor"
        self.output_path = self.data_path / "output"
        self.expected_path = self.data_path / "expected"
        self.extractor = K8sOpenAPIExtractor(output_path=self.output_path)
        self.extractor.client = mock.MagicMock()

    def tearDown(self):
        shutil.rmtree(self.output_path, ignore_errors=True)

    def _load_json(self, path: Path) -> Any:
        return json.loads(path.read_text())

    def _mock_response(self, payload: Path) -> mock.MagicMock:
        response = mock.MagicMock()
        response.json.return_value = self._load_json(payload)
        return response

    def test_extract(self):
        expected_payloads = [
            self.data_path / "specs.json",
            self.data_path / "apis__apps__v1_openapi.json",
            self.data_path / "apis__batch__v1_openapi.json",
            self.data_path / "releases.json",
        ]
        self.extractor.client.get.side_effect = [
            self._mock_response(payload) for payload in expected_payloads
        ]

        output_file = self.extractor.extract()

        self.assertEqual(output_file, self.output_path / "v1_30_0.json")
        self.assertTrue((self.output_path / "v1_30_0.json").exists())

        self.assertEqual(
            self._load_json(self.output_path / "v1_30_0.json"),
            self._load_json(self.expected_path / "v1_30_0.json"),
        )

    def test_extract_no_schema(self):
        mock_response = mock.MagicMock()
        mock_response.json.return_value = []
        self.extractor.client.get.return_value = mock_response

        with self.assertRaises(NoSchemaFoundError):
            self.extractor.extract()
