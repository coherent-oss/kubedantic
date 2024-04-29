import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests  # type: ignore
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


class NoSchemaFoundError(Exception):
    pass


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
    _k8s_version: Optional[str] = None

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

    @property
    def k8s_version(self) -> str:
        if self._k8s_version is None:
            self._k8s_version = self._fetch_k8s_version()
        return self._k8s_version

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

    def _fetch_k8s_version(self) -> str:
        tag = "latest" if self.version == LATEST_K8S_VERSION else self.version

        logger.info("Fetching release %s", tag)
        version = self._fetch(
            path=f"repos/{self.repo_owner}/{self.repo_name}/releases/{tag}"
        )["tag_name"]
        logger.info("Found k8s version %s", version)
        return version

    def _write_schema(self, schema: Schema) -> Path:
        out_path = self.output_path / Path(
            self.k8s_version.replace(".", "_")
        ).with_suffix(".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Writing spec to %s", out_path)
        out_path.write_text(json.dumps(schema.to_openapi(), indent=4, default=str))
        return out_path

    def _build_schema(self) -> Optional[Schema]:
        schema = None

        for path in self._fetch_openapi_specs():
            if path.should_skip:
                continue

            logger.info("Fetching specs for %s", path.download_url)
            spec = self._fetch(url=path.download_url)

            if schema is None:
                schema = Schema.from_spec(spec)
            else:
                schema.schemas.update(spec["components"]["schemas"])

        return schema

    def extract(self) -> Path:
        schema = self._build_schema()

        if schema is None:
            raise NoSchemaFoundError("Unable to find any schema")

        return self._write_schema(schema)
