import json
import logging
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union

from kubernetes import client, config
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


API_PATH_BY_TITLE: Dict[str, Path] = {
    "Kubernetes": Path("k8s"),  # Kubernetes API
    "Kubernetes CRD Swagger": Path("crd"),  # CustomResourceDefinition API
}


class SchemaMetadata(BaseModel):
    openapi: str
    title: str
    version: str

    @property
    def is_supported(self) -> bool:
        return self.openapi.startswith("3.") and self.title in API_PATH_BY_TITLE

    @property
    def path(self) -> Path:
        return API_PATH_BY_TITLE.get(self.title, Path(""))

    @classmethod
    def from_spec(cls, spec: Dict[str, Any]) -> "SchemaMetadata":
        return cls(
            openapi=spec["openapi"],
            title=spec["info"]["title"],
            version=spec["info"]["version"],
        )


class Schema(BaseModel):
    openapi_schema: Dict[str, Any] = Field(default_factory=dict)
    metadata: SchemaMetadata

    def to_openapi(self) -> Dict[str, Any]:
        return {
            "openapi": self.metadata.openapi,
            "info": {"title": self.metadata.title, "version": self.metadata.version},
            "components": {"schemas": self.openapi_schema},
        }


class K8sOpenAPIExtractor:
    _client: Optional[client.ApiClient] = None

    def __init__(self, output_path: Union[str, Path]):
        self.output_path = Path(output_path)
        self.schema_by_path: dict[Path, Schema] = {}

    @property
    def client(self) -> client.ApiClient:
        if self._client is None:
            self._client = config.new_client_from_config()  # pragma: no cover
        return self._client

    def _should_skip_path(self, path: str) -> bool:
        stem = Path(path.split("?")[0]).stem
        return not stem.startswith("v") or stem == "version"

    def _add_to_schema_by_path(self, spec: Dict[str, Any]):
        spec_metadata = SchemaMetadata.from_spec(spec)

        if not spec_metadata.is_supported:
            logger.warning("Skipping unsupported spec %s", spec_metadata.title)
            return

        schema_path = spec_metadata.path

        for name, schema in spec["components"].get("schemas", {}).items():
            current_schema = self.schema_by_path.get(
                schema_path, Schema(metadata=spec_metadata)
            )
            current_schema.openapi_schema[name] = schema
            self.schema_by_path[schema_path] = current_schema

    def call_api(self, resource_path: str, method: str = "GET", **kwargs: Any) -> Any:
        return self.client.call_api(
            resource_path=resource_path,
            method=method,
            response_type="object",
            auth_settings=self.client.configuration.auth_settings(),
            _return_http_data_only=True,
            **kwargs,
        )

    def _load_schema_by_path(self):
        paths = self.call_api(resource_path="/openapi/v3")["paths"]

        for name, value in paths.items():
            relative_path = value["serverRelativeURL"]

            if self._should_skip_path(relative_path):
                continue

            logger.info("Fetching specs for %s", name)
            spec = self.call_api(resource_path=relative_path)

            self._add_to_schema_by_path(spec)

    def _write_schema(self, path: Path, schemas: Schema) -> Path:
        out_path = self.output_path / path.with_suffix(".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Writing spec %s to %s", path, out_path)

        with open(out_path, "w") as f:
            f.write(json.dumps(schemas.to_openapi(), indent=4, default=str))

        return out_path

    def _load_specs(self) -> Generator[Path, None, None]:
        if self.output_path.exists():
            logger.info("Using existing specs")
            return self.output_path.glob("**/*.json")

        self._load_schema_by_path()

        return (
            self._write_schema(path, schemas)
            for path, schemas in self.schema_by_path.items()
        )

    def extract(self) -> List[Path]:
        """
        Extracts the Kubernetes OpenAPI specs and writes them to the output path.

        :return: The list of paths where the specs were written to.
        """
        return [path.absolute() for path in self._load_specs()]
