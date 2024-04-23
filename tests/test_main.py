import shutil
from pathlib import Path
from unittest import mock

import pytest

from kubedantic.main import run


@pytest.fixture
def output_path(data_path: Path):
    path = data_path / "main" / "output"
    yield path
    shutil.rmtree(path, ignore_errors=True)


@mock.patch("kubedantic.main.K8sOpenAPIExtractor.extract")
@mock.patch("kubedantic.main.K8sOpenAPIParser.parse")
def test_run(
    mock_parse: mock.MagicMock, mock_extract: mock.MagicMock, output_path: Path
):
    expected_output = "class Test: pass"

    mock_extract.return_value = [Path("path/to/spec")]
    mock_parse.return_value = {
        ("path", "to", "spec"): mock.MagicMock(body=expected_output)
    }

    run([
        "--output-path",
        str(output_path / "models"),
        "--specs-path",
        str(output_path / "specs"),
    ])

    assert (output_path / "models" / "to" / "spec.py").exists()

    with open(output_path / "models" / "to" / "spec.py") as f:
        assert f.read() == expected_output
