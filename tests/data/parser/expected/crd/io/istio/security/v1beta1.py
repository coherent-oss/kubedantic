from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from ...k8s.apimachinery.pkg.apis.meta import v1


class Action(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    AUDIT = "AUDIT"
    CUSTOM = "CUSTOM"


class Provider(BaseModel):
    name: Optional[str] = Field(
        default=None, description="Specifies the name of the extension provider."
    )


class Source(BaseModel):
    ipBlocks: Optional[List[str]] = Field(default=None, description="Optional.")
    namespaces: Optional[List[str]] = Field(default=None, description="Optional.")
    notIpBlocks: Optional[List[str]] = Field(default=None, description="Optional.")
    notNamespaces: Optional[List[str]] = Field(default=None, description="Optional.")
    notPrincipals: Optional[List[str]] = Field(default=None, description="Optional.")
    notRemoteIpBlocks: Optional[List[str]] = Field(
        default=None, description="Optional."
    )
    notRequestPrincipals: Optional[List[str]] = Field(
        default=None, description="Optional."
    )
    principals: Optional[List[str]] = Field(default=None, description="Optional.")
    remoteIpBlocks: Optional[List[str]] = Field(default=None, description="Optional.")
    requestPrincipals: Optional[List[str]] = Field(
        default=None, description="Optional."
    )


class FromItem(BaseModel):
    source: Optional[Source] = Field(
        default=None, description="Source specifies the source of a request."
    )


class Operation(BaseModel):
    hosts: Optional[List[str]] = Field(default=None, description="Optional.")
    methods: Optional[List[str]] = Field(default=None, description="Optional.")
    notHosts: Optional[List[str]] = Field(default=None, description="Optional.")
    notMethods: Optional[List[str]] = Field(default=None, description="Optional.")
    notPaths: Optional[List[str]] = Field(default=None, description="Optional.")
    notPorts: Optional[List[str]] = Field(default=None, description="Optional.")
    paths: Optional[List[str]] = Field(default=None, description="Optional.")
    ports: Optional[List[str]] = Field(default=None, description="Optional.")


class ToItem(BaseModel):
    operation: Optional[Operation] = Field(
        default=None, description="Operation specifies the operation of a request."
    )


class WhenItem(BaseModel):
    key: str = Field(..., description="The name of an Istio attribute.")
    notValues: Optional[List[str]] = Field(default=None, description="Optional.")
    values: Optional[List[str]] = Field(default=None, description="Optional.")


class Rule(BaseModel):
    from_: Optional[List[FromItem]] = Field(
        default=None, alias="from", description="Optional."
    )
    to: Optional[List[ToItem]] = Field(default=None, description="Optional.")
    when: Optional[List[WhenItem]] = Field(default=None, description="Optional.")


class Selector(BaseModel):
    matchLabels: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "One or more labels that indicate a specific set of pods/VMs on which a"
            " policy should be applied."
        ),
    )


class TargetRef(BaseModel):
    group: Optional[str] = Field(
        default=None, description="group is the group of the target resource."
    )
    kind: Optional[str] = Field(
        default=None, description="kind is kind of the target resource."
    )
    name: Optional[str] = Field(
        default=None, description="name is the name of the target resource."
    )
    namespace: Optional[str] = Field(
        default=None, description="namespace is the namespace of the referent."
    )


class Spec(BaseModel):
    action: Optional[Action] = Field(default=None, description="Optional.")
    provider: Optional[Provider] = Field(
        default=None,
        description="Specifies detailed configuration of the CUSTOM action.",
    )
    rules: Optional[List[Rule]] = Field(default=None, description="Optional.")
    selector: Optional[Selector] = Field(default=None, description="Optional.")
    targetRef: Optional[TargetRef] = Field(default=None, description="Optional.")


class SpecModel(BaseModel):
    action: Optional[Action] = Field(default=None, description="Optional.")
    provider: Provider = Field(
        ..., description="Specifies detailed configuration of the CUSTOM action."
    )
    rules: Optional[List[Rule]] = Field(default=None, description="Optional.")
    selector: Optional[Selector] = Field(default=None, description="Optional.")
    targetRef: Optional[TargetRef] = Field(default=None, description="Optional.")


class Mode(Enum):
    UNSET = "UNSET"
    DISABLE = "DISABLE"
    PERMISSIVE = "PERMISSIVE"
    STRICT = "STRICT"


class Mtls(BaseModel):
    mode: Optional[Mode] = Field(
        default=None, description="Defines the mTLS mode used for peer authentication."
    )


class PortLevelMtls(BaseModel):
    mode: Optional[Mode] = Field(
        default=None, description="Defines the mTLS mode used for peer authentication."
    )


class SpecModel1(BaseModel):
    mtls: Optional[Mtls] = Field(
        default=None, description="Mutual TLS settings for workload."
    )
    portLevelMtls: Optional[Dict[str, PortLevelMtls]] = Field(
        default=None, description="Port specific mutual TLS settings."
    )
    selector: Optional[Selector] = Field(
        default=None,
        description=(
            "The selector determines the workloads to apply the PeerAuthentication on."
        ),
    )


class FromHeader(BaseModel):
    name: str = Field(..., description="The HTTP header name.")
    prefix: Optional[str] = Field(
        default=None,
        description="The prefix that should be stripped before decoding the token.",
    )


class OutputClaimToHeader(BaseModel):
    claim: Optional[str] = Field(
        default=None, description="The name of the claim to be copied from."
    )
    header: Optional[str] = Field(
        default=None, description="The name of the header to be created."
    )


class JwtRule(BaseModel):
    audiences: Optional[List[str]] = Field(
        default=None,
        description=(
            "The list of JWT"
            " [audiences](https://tools.ietf.org/html/rfc7519#section-4.1.3) that are"
            " allowed to access."
        ),
    )
    forwardOriginalToken: Optional[bool] = Field(
        default=None,
        description=(
            "If set to true, the original token will be kept for the upstream request."
        ),
    )
    fromCookies: Optional[List[str]] = Field(
        default=None, description="List of cookie names from which JWT is expected."
    )
    fromHeaders: Optional[List[FromHeader]] = Field(
        default=None, description="List of header locations from which JWT is expected."
    )
    fromParams: Optional[List[str]] = Field(
        default=None, description="List of query parameters from which JWT is expected."
    )
    issuer: str = Field(..., description="Identifies the issuer that issued the JWT.")
    jwks: Optional[str] = Field(
        default=None,
        description="JSON Web Key Set of public keys to validate signature of the JWT.",
    )
    jwksUri: Optional[str] = Field(
        default=None,
        description=(
            "URL of the provider's public key set to validate signature of the JWT."
        ),
    )
    jwks_uri: Optional[str] = Field(
        default=None,
        description=(
            "URL of the provider's public key set to validate signature of the JWT."
        ),
    )
    outputClaimToHeaders: Optional[List[OutputClaimToHeader]] = Field(
        default=None,
        description=(
            "This field specifies a list of operations to copy the claim to HTTP"
            " headers on a successfully verified token."
        ),
    )
    outputPayloadToHeader: Optional[str] = Field(
        default=None,
        description=(
            "This field specifies the header name to output a successfully verified JWT"
            " payload to the backend."
        ),
    )


class SpecModel2(BaseModel):
    jwtRules: Optional[List[JwtRule]] = Field(
        default=None,
        description=(
            "Define the list of JWTs that can be validated at the selected workloads'"
            " proxy."
        ),
    )
    selector: Optional[Selector] = Field(default=None, description="Optional.")
    targetRef: Optional[TargetRef] = Field(default=None, description="Optional.")


class AuthorizationPolicy(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="AuthorizationPolicy",
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
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[Union[Spec, SpecModel]] = Field(
        default=None,
        description=(
            "Configuration for access control on workloads. See more details at:"
            " https://istio.io/docs/reference/config/security/authorization-policy.html"
        ),
    )
    status: Optional[Dict[str, Any]] = None


class AuthorizationPolicyList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[AuthorizationPolicy] = Field(
        ...,
        description=(
            "List of authorizationpolicies. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md"
        ),
    )
    kind: Optional[str] = Field(
        default="AuthorizationPolicyList",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1.ListMeta] = Field(
        default=None,
        description=(
            "Standard list metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )


class PeerAuthentication(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="PeerAuthentication",
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
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[SpecModel1] = Field(
        default=None,
        description=(
            "Peer authentication configuration for workloads. See more details at:"
            " https://istio.io/docs/reference/config/security/peer_authentication.html"
        ),
    )
    status: Optional[Dict[str, Any]] = None


class PeerAuthenticationList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[PeerAuthentication] = Field(
        ...,
        description=(
            "List of peerauthentications. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md"
        ),
    )
    kind: Optional[str] = Field(
        default="PeerAuthenticationList",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1.ListMeta] = Field(
        default=None,
        description=(
            "Standard list metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )


class RequestAuthentication(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="RequestAuthentication",
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
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[SpecModel2] = Field(
        default=None,
        description=(
            "Request authentication configuration for workloads. See more details at:"
            " https://istio.io/docs/reference/config/security/request_authentication.html"
        ),
    )
    status: Optional[Dict[str, Any]] = None


class RequestAuthenticationList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="security.istio.io/v1beta1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[RequestAuthentication] = Field(
        ...,
        description=(
            "List of requestauthentications. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md"
        ),
    )
    kind: Optional[str] = Field(
        default="RequestAuthenticationList",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1.ListMeta] = Field(
        default=None,
        description=(
            "Standard list metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
