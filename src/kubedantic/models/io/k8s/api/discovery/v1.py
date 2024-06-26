# generated by datamodel-codegen:
#   timestamp: 2024-04-28T19:06:26+00:00
#   k8s version: v1.30.0

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ...apimachinery.pkg.apis.meta import v1 as v1_1
from ..core import v1


class EndpointConditions(BaseModel):
    ready: Optional[bool] = Field(
        default=None,
        description=(
            "ready indicates that this endpoint is prepared to receive traffic,"
            " according to whatever system is managing the endpoint. A nil value"
            " indicates an unknown state. In most cases consumers should interpret this"
            " unknown state as ready. For compatibility reasons, ready should never be"
            ' "true" for terminating endpoints, except when the normal readiness'
            " behavior is being explicitly overridden, for example when the associated"
            " Service has set the publishNotReadyAddresses flag."
        ),
    )
    serving: Optional[bool] = Field(
        default=None,
        description=(
            "serving is identical to ready except that it is set regardless of the"
            " terminating state of endpoints. This condition should be set to true for"
            " a ready endpoint that is terminating. If nil, consumers should defer to"
            " the ready condition."
        ),
    )
    terminating: Optional[bool] = Field(
        default=None,
        description=(
            "terminating indicates that this endpoint is terminating. A nil value"
            " indicates an unknown state. Consumers should interpret this unknown state"
            " to mean that the endpoint is not terminating."
        ),
    )


class EndpointPort(BaseModel):
    appProtocol: Optional[str] = Field(
        default=None,
        description=(
            "The application protocol for this port. This is used as a hint for"
            " implementations to offer richer behavior for protocols that they"
            " understand. This field follows standard Kubernetes label syntax. Valid"
            " values are either:\n\n* Un-prefixed protocol names - reserved for IANA"
            " standard service names (as per RFC-6335 and"
            " https://www.iana.org/assignments/service-names).\n\n* Kubernetes-defined"
            " prefixed names:\n  * 'kubernetes.io/h2c' - HTTP/2 prior knowledge over"
            " cleartext as described in"
            " https://www.rfc-editor.org/rfc/rfc9113.html#name-starting-http-2-with-prior-\n"
            "  * 'kubernetes.io/ws'  - WebSocket over cleartext as described in"
            " https://www.rfc-editor.org/rfc/rfc6455\n  * 'kubernetes.io/wss' -"
            " WebSocket over TLS as described in"
            " https://www.rfc-editor.org/rfc/rfc6455\n\n* Other protocols should use"
            " implementation-defined prefixed names such as"
            " mycompany.com/my-custom-protocol."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "name represents the name of this port. All ports in an EndpointSlice must"
            " have a unique name. If the EndpointSlice is derived from a Kubernetes"
            " service, this corresponds to the Service.ports[].name. Name must either"
            " be an empty string or pass DNS_LABEL validation: * must be no more than"
            " 63 characters long. * must consist of lower case alphanumeric characters"
            " or '-'. * must start and end with an alphanumeric character. Default is"
            " empty string."
        ),
    )
    port: Optional[int] = Field(
        default=None,
        description=(
            "port represents the port number of the endpoint. If this is not specified,"
            " ports are not restricted and must be interpreted in the context of the"
            " specific consumer."
        ),
    )
    protocol: Optional[str] = Field(
        default=None,
        description=(
            "protocol represents the IP protocol for this port. Must be UDP, TCP, or"
            " SCTP. Default is TCP."
        ),
    )


class ForZone(BaseModel):
    name: str = Field(..., description="name represents the name of the zone.")


class EndpointHints(BaseModel):
    forZones: Optional[List[ForZone]] = Field(
        default=None,
        description=(
            "forZones indicates the zone(s) this endpoint should be consumed by to"
            " enable topology aware routing."
        ),
    )


class Endpoint(BaseModel):
    addresses: List[str] = Field(
        ...,
        description=(
            "addresses of this endpoint. The contents of this field are interpreted"
            " according to the corresponding EndpointSlice addressType field. Consumers"
            " must handle different types of addresses in the context of their own"
            " capabilities. This must contain at least one address but no more than"
            " 100. These are all assumed to be fungible and clients may choose to only"
            " use the first element. Refer to: https://issue.k8s.io/106267"
        ),
    )
    conditions: Optional[EndpointConditions] = Field(
        default=None,
        description=(
            "conditions contains information about the current status of the endpoint."
        ),
    )
    deprecatedTopology: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "deprecatedTopology contains topology information part of the v1beta1 API."
            " This field is deprecated, and will be removed when the v1beta1 API is"
            " removed (no sooner than kubernetes v1.24).  While this field can hold"
            " values, it is not writable through the v1 API, and any attempts to write"
            " to it will be silently ignored. Topology information can be found in the"
            " zone and nodeName fields instead."
        ),
    )
    hints: Optional[EndpointHints] = Field(
        default=None,
        description=(
            "hints contains information associated with how an endpoint should be"
            " consumed."
        ),
    )
    hostname: Optional[str] = Field(
        default=None,
        description=(
            "hostname of this endpoint. This field may be used by consumers of"
            " endpoints to distinguish endpoints from each other (e.g. in DNS names)."
            " Multiple endpoints which use the same hostname should be considered"
            " fungible (e.g. multiple A values in DNS). Must be lowercase and pass DNS"
            " Label (RFC 1123) validation."
        ),
    )
    nodeName: Optional[str] = Field(
        default=None,
        description=(
            "nodeName represents the name of the Node hosting this endpoint. This can"
            " be used to determine endpoints local to a Node."
        ),
    )
    targetRef: Optional[v1.ObjectReference] = Field(
        default=None,
        description=(
            "targetRef is a reference to a Kubernetes object that represents this"
            " endpoint."
        ),
    )
    zone: Optional[str] = Field(
        default=None,
        description="zone is the name of the Zone this endpoint exists in.",
    )


class EndpointSlice(BaseModel):
    addressType: str = Field(
        ...,
        description=(
            "addressType specifies the type of address carried by this EndpointSlice."
            " All addresses in this slice must be the same type. This field is"
            " immutable after creation. The following address types are currently"
            " supported: * IPv4: Represents an IPv4 Address. * IPv6: Represents an IPv6"
            " Address. * FQDN: Represents a Fully Qualified Domain Name."
        ),
    )
    apiVersion: Optional[str] = Field(
        default="discovery.k8s.io/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    endpoints: List[Endpoint] = Field(
        ...,
        description=(
            "endpoints is a list of unique endpoints in this slice. Each slice may"
            " include a maximum of 1000 endpoints."
        ),
    )
    kind: Optional[str] = Field(
        default="EndpointSlice",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ObjectMeta] = Field(
        default=None, description="Standard object's metadata."
    )
    ports: Optional[List[EndpointPort]] = Field(
        default=None,
        description=(
            "ports specifies the list of network ports exposed by each endpoint in this"
            " slice. Each port must have a unique name. When ports is empty, it"
            " indicates that there are no defined ports. When a port is defined with a"
            ' nil port value, it indicates "all ports". Each slice may include a'
            " maximum of 100 ports."
        ),
    )


class EndpointSliceList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="discovery.k8s.io/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[EndpointSlice] = Field(
        ..., description="items is the list of endpoint slices"
    )
    kind: Optional[str] = Field(
        default="EndpointSliceList",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ListMeta] = Field(
        default=None, description="Standard list metadata."
    )
