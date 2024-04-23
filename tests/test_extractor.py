import json
import shutil
from pathlib import Path
from typing import Any
from unittest import TestCase, mock

import pytest
from kubernetes import client

from kubedantic.extractor import K8sOpenAPIExtractor


@pytest.mark.usefixtures("data_path")
class K8sOpenAPIExtractorTestCase(TestCase):
    data_path: Path

    def setUp(self):
        self.output_path = self.data_path / "extractor" / "output"
        self.expected_path = self.data_path / "extractor" / "expected"
        self.extractor = K8sOpenAPIExtractor(output_path=self.output_path)

        self.mock_client = mock.MagicMock(spec=client.ApiClient)
        self.mock_client.configuration = mock.MagicMock(spec=client.Configuration)
        self.extractor._client = self.mock_client

        self.data_path = self.data_path / "extractor" / "openapi_v3"

    def tearDown(self):
        self.extractor._client = None
        shutil.rmtree(self.output_path, ignore_errors=True)

    def _load_json(self, path: Path) -> Any:
        with open(path) as f:
            return json.load(f)

    def test_extract(self):
        expected_specs = [
            self.data_path / "paths.json",
            self.data_path / "api" / "v1.json",
            self.data_path / "apis" / "apps" / "v1.json",
            self.data_path / "apis" / "batch" / "v1.json",
            self.data_path / "apis" / "security.istio.io" / "v1.json",
            self.data_path / "apis" / "security.istio.io" / "v1beta1.json",
        ]
        self.extractor._client.call_api.side_effect = [
            self._load_json(p) for p in expected_specs
        ]

        specs = list(self.extractor.extract())

        self.assertEqual(len(specs), 2)

        self.assertEqual(specs[0], self.output_path / "k8s.json")
        self.assertEqual(specs[1], self.output_path / "crd.json")

        self.assertTrue((self.output_path / "k8s.json").exists())
        self.assertTrue((self.output_path / "crd.json").exists())

        self.assertEqual(
            self._load_json(self.output_path / "k8s.json"),
            self._load_json(self.expected_path / "k8s.json"),
        )
        self.assertEqual(
            self._load_json(self.output_path / "crd.json"),
            self._load_json(self.expected_path / "crd.json"),
        )

    def test_extract_unsupported(self):
        self.extractor._client.call_api.side_effect = [
            {"paths": {"/openapi/v3": {"serverRelativeURL": "/apis/unsupported/v1"}}},
            self._load_json(self.data_path / "apis" / "unsupported" / "v1.json"),
        ]

        specs = list(self.extractor.extract())

        self.assertEqual(len(specs), 0)
        self.assertFalse(
            (self.output_path / "apis" / "unsupported" / "v1.json").exists()
        )

    def test_extract_cached(self):
        self.extractor.output_path = self.expected_path

        specs = list(self.extractor.extract())

        self.assertEqual(len(specs), 2)
        self.assertTrue((self.expected_path / "k8s.json").exists())
        self.assertTrue((self.expected_path / "crd.json").exists())
        self.assertFalse((self.output_path / "k8s.json").exists())
        self.assertFalse((self.output_path / "crd.json").exists())
