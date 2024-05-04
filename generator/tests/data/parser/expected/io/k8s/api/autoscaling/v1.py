from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ...apimachinery.pkg.apis.meta import v1


class ScaleSpec(BaseModel):
    replicas: Optional[int] = Field(
        default=None,
        description=(
            "replicas is the desired number of instances for the scaled object."
        ),
    )


class ScaleStatus(BaseModel):
    replicas: int = Field(
        ...,
        description=(
            "replicas is the actual number of observed instances of the scaled object."
        ),
    )
    selector: Optional[str] = Field(
        default=None,
        description=(
            "selector is the label query over pods that should match the replicas"
            " count. This is same as the label selector but in the string format to"
            " avoid introspection by clients. The string will be in the same format as"
            " the query-param syntax. More info about label selectors:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/"
        ),
    )


class Scale(BaseModel):
    apiVersion: Optional[str] = Field(
        default="autoscaling/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="Scale",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1.ObjectMeta] = Field(
        default=None,
        description=(
            "Standard object metadata; More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata."
        ),
    )
    spec: Optional[ScaleSpec] = Field(
        default=None,
        description=(
            "spec defines the behavior of the scale. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status."
        ),
    )
    status: Optional[ScaleStatus] = Field(
        default=None,
        description=(
            "status is the current status of the scale. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status."
            " Read-only."
        ),
    )
