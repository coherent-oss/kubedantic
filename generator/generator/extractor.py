import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)


LATEST_K8S_VERSION = "master"

# Internal or unnecessary specs
SKIP_SPECS = {
    "version_openapi.json",
    "apis__resource.k8s.io__v1alpha2_openapi.json",
    "apis__internal.apiserver.k8s.io__v1alpha1_openapi.json",
    "apis__storagemigration.k8s.io__v1alpha1_openapi.json",
}


class Schema(BaseModel):
    openapi: str
    info: Dict[str, Any]
    schemas: Dict[str, Any]

    @classmethod
    def from_spec(cls, spec: Dict[str, Any]) -> "Schema":
        return cls(
            openapi=spec["openapi"],
            info=spec["info"],
            schemas=spec["components"]["schemas"],
        )

    def to_openapi(self) -> Dict[str, Any]:
        return {
            "openapi": self.openapi,
            "info": self.info,
            "components": {"schemas": self.schemas},
        }


class OpenAPIPath(BaseModel):
    name: str
    path: Path
    url: str
    download_url: str

    @property
    def should_skip(self) -> bool:
        return (
            not self.path.stem.split("__")[-1].startswith("v")
            or self.name in SKIP_SPECS
            or self.path.suffix != ".json"
        )


class K8sOpenAPIExtractor:
    schema: Optional[Schema] = None
    k8s_version: Optional[str] = None

    def __init__(
        self,
        output_path: Union[str, Path],
        api_url: str = "https://api.github.com/",
        repo_owner: str = "kubernetes",
        repo_name: str = "kubernetes",
        version: str = LATEST_K8S_VERSION,
    ):
        self.output_path = Path(output_path)
        self.api_url = api_url if api_url.endswith("/") else f"{api_url}/"
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.version = version
        self.client = requests.Session()

    def _fetch(
        self,
        url: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Tuple[int, int] = (3, 30),
    ) -> Any:
        url = url or f"{self.api_url}{path}"
        response = self.client.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def _fetch_openapi_specs(self) -> List[OpenAPIPath]:
        response = self._fetch(
            path=f"repos/{self.repo_owner}/{self.repo_name}/contents/api/openapi-spec/v3",
            params={"ref": self.version},
        )
        return [
            OpenAPIPath(
                name=content["name"],
                path=Path(content["path"]),
                url=content["url"],
                download_url=content["download_url"],
            )
            for content in response
            if content["type"] == "file"
        ]

    def _write_schema(self) -> Path:
        assert self.schema is not None, "Schema is not loaded yet."
        assert self.k8s_version is not None, "K8s version is not resolved yet."

        out_path = self.output_path / Path(
            self.k8s_version.replace(".", "_")
        ).with_suffix(".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Writing spec to %s", out_path)

        with open(out_path, "w") as f:
            f.write(json.dumps(self.schema.to_openapi(), indent=4, default=str))

        return out_path

    def _add_to_schema(self, spec: Dict[str, Any]):
        if self.schema is None:
            self.schema = Schema.from_spec(spec)
        else:
            self.schema.schemas.update(spec["components"]["schemas"])

    def _load_schema_by_path(self) -> Path:
        paths = self._fetch_openapi_specs()
        for path in paths:
            if path.should_skip:
                continue

            logger.info("Fetching specs for %s", path.download_url)
            spec = self._fetch(url=path.download_url)
            self._add_to_schema(spec)

        return self._write_schema()

    def _resolve_k8s_version(self) -> None:
        tag = "latest" if self.version == LATEST_K8S_VERSION else self.version

        logger.info("Fetching release %s", tag)
        release = self._fetch(
            path=f"repos/{self.repo_owner}/{self.repo_name}/releases/{tag}"
        )
        self.k8s_version = release["tag_name"]
        logger.info("Resolved k8s version: %s", self.k8s_version)

    def extract(self) -> Path:
        self._resolve_k8s_version()
        return self._load_schema_by_path().absolute()
