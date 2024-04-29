from pathlib import Path

import pytest


@pytest.fixture
def data_path(request: pytest.FixtureRequest):
    path = Path(__file__).parent / "data"

    if request.cls:
        request.cls.data_path = path

    return path
