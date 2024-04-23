import logging
import sys
from pathlib import Path
from typing import Any, Optional, Union
from urllib.parse import ParseResult

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model import pydantic_v2
from datamodel_code_generator.parser.jsonschema import JsonSchemaObject
from datamodel_code_generator.parser.openapi import OpenAPIParser
from pydantic import model_validator

logger = logging.getLogger(__name__)


def _get_python_version() -> PythonVersion:
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    logger.info("Detected Python version: %s", version)
    return PythonVersion(version)


class K8sSchemaObject(JsonSchemaObject):
    def _get_group_version_kind(self) -> tuple[str, str, str]:
        """
        Returns the group, version and kind of the object, if available.

        :return: Tuple with group, version and kind, in this order.
        """
        extra_k8s_properties = self.extras.get("x-kubernetes-group-version-kind")
        if not extra_k8s_properties:
            return "", "", ""

        if isinstance(extra_k8s_properties, list):
            if len(extra_k8s_properties) > 1:
                return "", "", ""
            extra_k8s_properties = extra_k8s_properties[0]

        group = extra_k8s_properties.get("group")
        version = extra_k8s_properties.get("version")
        kind = extra_k8s_properties.get("kind")

        return group, version, kind

    def _get_property_object(self, name: str) -> Optional[JsonSchemaObject]:
        if self.properties is None:
            return None

        property_object = self.properties.get(name)

        if not isinstance(property_object, JsonSchemaObject):
            return None

        return property_object

    def _update_kind(self):
        kind_prop = self._get_property_object("kind")

        if kind_prop is None:
            return

        _, _, kind = self._get_group_version_kind()

        if kind:
            kind_prop.default = kind

    def _update_api_version(self):
        api_version_prop = self._get_property_object("apiVersion")

        if api_version_prop is None:
            return

        group, version, _ = self._get_group_version_kind()

        if version and group:
            api_version_prop.default = f"{group}/{version}"

    def _update_default_fields(self):
        self._update_kind()
        self._update_api_version()

    @model_validator(mode="after")
    def update_default_fields(self):
        """
        Updates some default fields based on k8s specific properties.
        """
        self._update_default_fields()
        return self


class K8sDataModelField(pydantic_v2.DataModelField):
    @model_validator(mode="after")
    def update_default_fields(self):
        """
        Avoids setting default to {} if the field is not a dict.
        """
        if self.default == {} and not self.data_type.is_dict:
            self.default = None
        return self


class K8sOpenAPIParser(OpenAPIParser):
    SCHEMA_OBJECT_TYPE = K8sSchemaObject

    def __init__(
        self, source: Union[str, Path, list[Path], ParseResult], **kwargs: Any
    ):
        target_python_version = kwargs.pop(
            "target_python_version", _get_python_version()
        )
        data_model_field_type = kwargs.pop("data_model_field_type", K8sDataModelField)
        data_model_type = kwargs.pop("data_model_type", pydantic_v2.BaseModel)

        wrap_string_literal = kwargs.pop("wrap_string_literal", True)
        use_double_quotes = kwargs.pop("use_double_quotes", True)
        collapse_root_models = kwargs.pop("collapse_root_models", True)
        use_default_kwarg = kwargs.pop("use_default_kwarg", True)

        super().__init__(
            source=source,
            data_model_field_type=data_model_field_type,
            data_model_type=data_model_type,
            target_python_version=target_python_version,
            wrap_string_literal=wrap_string_literal,
            use_double_quotes=use_double_quotes,
            collapse_root_models=collapse_root_models,
            use_default_kwarg=use_default_kwarg,
            **kwargs,
        )
