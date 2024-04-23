from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from ...apimachinery.pkg.apis.meta import v1


class AWSElasticBlockStoreVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type of the volume that you want to mount. Tip:"
            " Ensure that the filesystem type is supported by the host operating"
            ' system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"'
            " if unspecified. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        ),
    )
    partition: Optional[int] = Field(
        default=None,
        description=(
            "partition is the partition in the volume that you want to mount. If"
            " omitted, the default is to mount by volume name. Examples: For volume"
            ' /dev/sda1, you specify the partition as "1". Similarly, the volume'
            ' partition for /dev/sda is "0" (or you can leave the property empty).'
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly value true will force the readOnly setting in VolumeMounts. More"
            " info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        ),
    )
    volumeID: str = Field(
        ...,
        description=(
            "volumeID is unique ID of the persistent disk resource in AWS (Amazon EBS"
            " volume). More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        ),
    )


class CachingMode(Enum):
    None_ = "None"
    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class Kind(Enum):
    Dedicated = "Dedicated"
    Managed = "Managed"
    Shared = "Shared"


class AzureDiskVolumeSource(BaseModel):
    cachingMode: Optional[CachingMode] = Field(
        default=None,
        description=(
            "cachingMode is the Host Caching mode: None, Read Only, Read"
            ' Write.\n\nPossible enum values:\n - `"None"`\n - `"ReadOnly"`\n -'
            ' `"ReadWrite"`'
        ),
    )
    diskName: str = Field(
        ..., description="diskName is the Name of the data disk in the blob storage"
    )
    diskURI: str = Field(
        ..., description="diskURI is the URI of data disk in the blob storage"
    )
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is Filesystem type to mount. Must be a filesystem type supported by"
            ' the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred'
            ' to be "ext4" if unspecified.'
        ),
    )
    kind: Optional[Kind] = Field(
        default=None,
        description=(
            "kind expected values are Shared: multiple blob disks per storage account "
            " Dedicated: single blob disk per storage account  Managed: azure managed"
            " data disk (only in managed availability set). defaults to"
            ' shared\n\nPossible enum values:\n - `"Dedicated"`\n - `"Managed"`\n -'
            ' `"Shared"`'
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly Defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts."
        ),
    )


class AzureFileVolumeSource(BaseModel):
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts."
        ),
    )
    secretName: str = Field(
        ...,
        description=(
            "secretName is the  name of secret that contains Azure Storage Account Name"
            " and Key"
        ),
    )
    shareName: str = Field(..., description="shareName is the azure share Name")


class Capabilities(BaseModel):
    add: Optional[List[str]] = Field(default=None, description="Added capabilities")
    drop: Optional[List[str]] = Field(default=None, description="Removed capabilities")


class ClaimSource(BaseModel):
    resourceClaimName: Optional[str] = Field(
        default=None,
        description=(
            "ResourceClaimName is the name of a ResourceClaim object in the same"
            " namespace as this pod."
        ),
    )
    resourceClaimTemplateName: Optional[str] = Field(
        default=None,
        description=(
            "ResourceClaimTemplateName is the name of a ResourceClaimTemplate object in"
            " the same namespace as this pod.\n\nThe template will be used to create a"
            " new ResourceClaim, which will be bound to this pod. When this pod is"
            " deleted, the ResourceClaim will also be deleted. The name of the"
            " ResourceClaim will be <pod name>-<resource name>, where <resource name>"
            " is the PodResourceClaim.Name. Pod validation will reject the pod if the"
            " concatenated name is not valid for a ResourceClaim (e.g. too long).\n\nAn"
            " existing ResourceClaim with that name that is not owned by the pod will"
            " not be used for the pod to avoid using an unrelated resource by mistake."
            " Scheduling and pod startup are then blocked until the unrelated"
            " ResourceClaim is removed.\n\nThis field is immutable and no changes will"
            " be made to the corresponding ResourceClaim by the control plane after"
            " creating the ResourceClaim."
        ),
    )


class ConfigMapEnvSource(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None, description="Specify whether the ConfigMap must be defined"
    )


class ConfigMapKeySelector(BaseModel):
    key: str = Field(..., description="The key to select.")
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description="Specify whether the ConfigMap or its key must be defined",
    )


class ImagePullPolicy(Enum):
    Always = "Always"
    IfNotPresent = "IfNotPresent"
    Never = "Never"


class TerminationMessagePolicy(Enum):
    FallbackToLogsOnError = "FallbackToLogsOnError"
    File = "File"


class Protocol(Enum):
    SCTP = "SCTP"
    TCP = "TCP"
    UDP = "UDP"


class ContainerPort(BaseModel):
    containerPort: int = Field(
        ...,
        description=(
            "Number of port to expose on the pod's IP address. This must be a valid"
            " port number, 0 < x < 65536."
        ),
    )
    hostIP: Optional[str] = Field(
        default=None, description="What host IP to bind the external port to."
    )
    hostPort: Optional[int] = Field(
        default=None,
        description=(
            "Number of port to expose on the host. If specified, this must be a valid"
            " port number, 0 < x < 65536. If HostNetwork is specified, this must match"
            " ContainerPort. Most containers do not need this."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "If specified, this must be an IANA_SVC_NAME and unique within the pod."
            " Each named port in a pod must have a unique name. Name for the port that"
            " can be referred to by services."
        ),
    )
    protocol: Optional[Protocol] = Field(
        default="TCP",
        description=(
            "Protocol for port. Must be UDP, TCP, or SCTP. Defaults to"
            ' "TCP".\n\nPossible enum values:\n - `"SCTP"` is the SCTP protocol.\n -'
            ' `"TCP"` is the TCP protocol.\n - `"UDP"` is the UDP protocol.'
        ),
    )


class ContainerResizePolicy(BaseModel):
    resourceName: str = Field(
        ...,
        description=(
            "Name of the resource to which this resource resize policy applies."
            " Supported values: cpu, memory."
        ),
    )
    restartPolicy: str = Field(
        ...,
        description=(
            "Restart policy to apply when specified resource is resized. If not"
            " specified, it defaults to NotRequired."
        ),
    )


class ExecAction(BaseModel):
    command: Optional[List[str]] = Field(
        default=None,
        description=(
            "Command is the command line to execute inside the container, the working"
            " directory for the command  is root ('/') in the container's filesystem."
            " The command is simply exec'd, it is not run inside a shell, so"
            " traditional shell instructions ('|', etc) won't work. To use a shell, you"
            " need to explicitly call out to that shell. Exit status of 0 is treated as"
            " live/healthy and non-zero is unhealthy."
        ),
    )


class FCVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs", "ntfs".'
            ' Implicitly inferred to be "ext4" if unspecified.'
        ),
    )
    lun: Optional[int] = Field(
        default=None, description="lun is Optional: FC target lun number"
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly is Optional: Defaults to false (read/write). ReadOnly here will"
            " force the ReadOnly setting in VolumeMounts."
        ),
    )
    targetWWNs: Optional[List[str]] = Field(
        default=None,
        description="targetWWNs is Optional: FC target worldwide names (WWNs)",
    )
    wwids: Optional[List[str]] = Field(
        default=None,
        description=(
            "wwids Optional: FC volume world wide identifiers (wwids) Either wwids or"
            " combination of targetWWNs and lun must be set, but not both"
            " simultaneously."
        ),
    )


class FlockerVolumeSource(BaseModel):
    datasetName: Optional[str] = Field(
        default=None,
        description=(
            "datasetName is Name of the dataset stored as metadata -> name on the"
            " dataset for Flocker should be considered as deprecated"
        ),
    )
    datasetUUID: Optional[str] = Field(
        default=None,
        description=(
            "datasetUUID is the UUID of the dataset. This is unique identifier of a"
            " Flocker dataset"
        ),
    )


class GCEPersistentDiskVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is filesystem type of the volume that you want to mount. Tip:"
            " Ensure that the filesystem type is supported by the host operating"
            ' system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"'
            " if unspecified. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        ),
    )
    partition: Optional[int] = Field(
        default=None,
        description=(
            "partition is the partition in the volume that you want to mount. If"
            " omitted, the default is to mount by volume name. Examples: For volume"
            ' /dev/sda1, you specify the partition as "1". Similarly, the volume'
            ' partition for /dev/sda is "0" (or you can leave the property empty). More'
            " info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        ),
    )
    pdName: str = Field(
        ...,
        description=(
            "pdName is unique name of the PD resource in GCE. Used to identify the disk"
            " in GCE. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to"
            " false. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        ),
    )


class GRPCAction(BaseModel):
    port: int = Field(
        ...,
        description=(
            "Port number of the gRPC service. Number must be in the range 1 to 65535."
        ),
    )
    service: Optional[str] = Field(
        default="",
        description=(
            "Service is the name of the service to place in the gRPC HealthCheckRequest"
            " (see"
            " https://github.com/grpc/grpc/blob/master/doc/health-checking.md).\n\nIf"
            " this is not specified, the default behavior is defined by gRPC."
        ),
    )


class GitRepoVolumeSource(BaseModel):
    directory: Optional[str] = Field(
        default=None,
        description=(
            "directory is the target directory name. Must not contain or start with"
            " '..'.  If '.' is supplied, the volume directory will be the git"
            " repository.  Otherwise, if specified, the volume will contain the git"
            " repository in the subdirectory with the given name."
        ),
    )
    repository: str = Field(..., description="repository is the URL")
    revision: Optional[str] = Field(
        default=None,
        description="revision is the commit hash for the specified revision.",
    )


class GlusterfsVolumeSource(BaseModel):
    endpoints: str = Field(
        ...,
        description=(
            "endpoints is the endpoint name that details Glusterfs topology. More info:"
            " https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        ),
    )
    path: str = Field(
        ...,
        description=(
            "path is the Glusterfs volume path. More info:"
            " https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the Glusterfs volume to be mounted with read-only"
            " permissions. Defaults to false. More info:"
            " https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        ),
    )


class Scheme(Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"


class HTTPHeader(BaseModel):
    name: str = Field(
        ...,
        description=(
            "The header field name. This will be canonicalized upon output, so"
            " case-variant names will be understood as the same header."
        ),
    )
    value: str = Field(..., description="The header field value")


class HostAlias(BaseModel):
    hostnames: Optional[List[str]] = Field(
        default=None, description="Hostnames for the above IP address."
    )
    ip: Optional[str] = Field(
        default=None, description="IP address of the host file entry."
    )


class Type(Enum):
    field_ = ""
    BlockDevice = "BlockDevice"
    CharDevice = "CharDevice"
    Directory = "Directory"
    DirectoryOrCreate = "DirectoryOrCreate"
    File = "File"
    FileOrCreate = "FileOrCreate"
    Socket = "Socket"


class HostPathVolumeSource(BaseModel):
    path: str = Field(
        ...,
        description=(
            "path of the directory on the host. If the path is a symlink, it will"
            " follow the link to the real path. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#hostpath"
        ),
    )
    type: Optional[Type] = Field(
        default=None,
        description=(
            'type for HostPath Volume Defaults to "" More info:'
            " https://kubernetes.io/docs/concepts/storage/volumes#hostpath\n\nPossible"
            ' enum values:\n - `""` For backwards compatible, leave it empty if unset\n'
            ' - `"BlockDevice"` A block device must exist at the given path\n -'
            ' `"CharDevice"` A character device must exist at the given path\n -'
            ' `"Directory"` A directory must exist at the given path\n -'
            ' `"DirectoryOrCreate"` If nothing exists at the given path, an empty'
            " directory will be created there as needed with file mode 0755, having the"
            ' same group and ownership with Kubelet.\n - `"File"` A file must exist at'
            ' the given path\n - `"FileOrCreate"` If nothing exists at the given path,'
            " an empty file will be created there as needed with file mode 0644, having"
            ' the same group and ownership with Kubelet.\n - `"Socket"` A UNIX socket'
            " must exist at the given path"
        ),
    )


class KeyToPath(BaseModel):
    key: str = Field(..., description="key is the key to project.")
    mode: Optional[int] = Field(
        default=None,
        description=(
            "mode is Optional: mode bits used to set permissions on this file. Must be"
            " an octal value between 0000 and 0777 or a decimal value between 0 and"
            " 511. YAML accepts both octal and decimal values, JSON requires decimal"
            " values for mode bits. If not specified, the volume defaultMode will be"
            " used. This might be in conflict with other options that affect the file"
            " mode, like fsGroup, and the result can be other mode bits set."
        ),
    )
    path: str = Field(
        ...,
        description=(
            "path is the relative path of the file to map the key to. May not be an"
            " absolute path. May not contain the path element '..'. May not start with"
            " the string '..'."
        ),
    )


class LocalObjectReference(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )


class NFSVolumeSource(BaseModel):
    path: str = Field(
        ...,
        description=(
            "path that is exported by the NFS server. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the NFS export to be mounted with read-only"
            " permissions. Defaults to false. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        ),
    )
    server: str = Field(
        ...,
        description=(
            "server is the hostname or IP address of the NFS server. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        ),
    )


class Operator(Enum):
    DoesNotExist = "DoesNotExist"
    Exists = "Exists"
    Gt = "Gt"
    In = "In"
    Lt = "Lt"
    NotIn = "NotIn"


class NodeSelectorRequirement(BaseModel):
    key: str = Field(..., description="The label key that the selector applies to.")
    operator: Operator = Field(
        ...,
        description=(
            "Represents a key's relationship to a set of values. Valid operators are"
            " In, NotIn, Exists, DoesNotExist. Gt, and Lt.\n\nPossible enum values:\n -"
            ' `"DoesNotExist"`\n - `"Exists"`\n - `"Gt"`\n - `"In"`\n - `"Lt"`\n -'
            ' `"NotIn"`'
        ),
    )
    values: Optional[List[str]] = Field(
        default=None,
        description=(
            "An array of string values. If the operator is In or NotIn, the values"
            " array must be non-empty. If the operator is Exists or DoesNotExist, the"
            " values array must be empty. If the operator is Gt or Lt, the values array"
            " must have a single element, which will be interpreted as an integer. This"
            " array is replaced during a strategic merge patch."
        ),
    )


class NodeSelectorTerm(BaseModel):
    matchExpressions: Optional[List[NodeSelectorRequirement]] = Field(
        default=None,
        description="A list of node selector requirements by node's labels.",
    )
    matchFields: Optional[List[NodeSelectorRequirement]] = Field(
        default=None,
        description="A list of node selector requirements by node's fields.",
    )


class ObjectFieldSelector(BaseModel):
    apiVersion: Optional[str] = Field(
        default=None,
        description=(
            "Version of the schema the FieldPath is written in terms of, defaults to"
            ' "v1".'
        ),
    )
    fieldPath: str = Field(
        ..., description="Path of the field to select in the specified API version."
    )


class VolumeMode(Enum):
    Block = "Block"
    Filesystem = "Filesystem"


class Phase(Enum):
    Bound = "Bound"
    Lost = "Lost"
    Pending = "Pending"


class ResizeStatus(Enum):
    field_ = ""
    ControllerExpansionFailed = "ControllerExpansionFailed"
    ControllerExpansionInProgress = "ControllerExpansionInProgress"
    NodeExpansionFailed = "NodeExpansionFailed"
    NodeExpansionInProgress = "NodeExpansionInProgress"
    NodeExpansionPending = "NodeExpansionPending"


class PersistentVolumeClaimVolumeSource(BaseModel):
    claimName: str = Field(
        ...,
        description=(
            "claimName is the name of a PersistentVolumeClaim in the same namespace as"
            " the pod using this volume. More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly Will force the ReadOnly setting in VolumeMounts. Default false."
        ),
    )


class PhotonPersistentDiskVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs", "ntfs".'
            ' Implicitly inferred to be "ext4" if unspecified.'
        ),
    )
    pdID: str = Field(
        ...,
        description="pdID is the ID that identifies Photon Controller persistent disk",
    )


class PodDNSConfigOption(BaseModel):
    name: Optional[str] = Field(default=None, description="Required.")
    value: Optional[str] = None


class PodOS(BaseModel):
    name: str = Field(
        ...,
        description=(
            "Name is the name of the operating system. The currently supported values"
            " are linux and windows. Additional value may be defined in future and can"
            " be one of:"
            " https://github.com/opencontainers/runtime-spec/blob/master/config.md#platform-specific-configuration"
            " Clients should expect to handle additional values and treat unrecognized"
            " values in this field as os: null"
        ),
    )


class PodReadinessGate(BaseModel):
    conditionType: str = Field(
        ...,
        description=(
            "ConditionType refers to a condition in the pod's condition list with"
            " matching type."
        ),
    )


class PodResourceClaim(BaseModel):
    name: str = Field(
        ...,
        description=(
            "Name uniquely identifies this resource claim inside the pod. This must be"
            " a DNS_LABEL."
        ),
    )
    source: Optional[ClaimSource] = Field(
        default=None, description="Source describes where to find the ResourceClaim."
    )


class PodSchedulingGate(BaseModel):
    name: str = Field(
        ...,
        description=(
            "Name of the scheduling gate. Each scheduling gate must have a unique name"
            " field."
        ),
    )


class FsGroupChangePolicy(Enum):
    Always = "Always"
    OnRootMismatch = "OnRootMismatch"


class DnsPolicy(Enum):
    ClusterFirst = "ClusterFirst"
    ClusterFirstWithHostNet = "ClusterFirstWithHostNet"
    Default = "Default"
    None_ = "None"


class PreemptionPolicy(Enum):
    Never = "Never"
    PreemptLowerPriority = "PreemptLowerPriority"


class RestartPolicy(Enum):
    Always = "Always"
    Never = "Never"
    OnFailure = "OnFailure"


class PortworxVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fSType represents the filesystem type to mount Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs". Implicitly'
            ' inferred to be "ext4" if unspecified.'
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts."
        ),
    )
    volumeID: str = Field(
        ..., description="volumeID uniquely identifies a Portworx volume"
    )


class PreferredSchedulingTerm(BaseModel):
    preference: NodeSelectorTerm = Field(
        ...,
        description="A node selector term, associated with the corresponding weight.",
    )
    weight: int = Field(
        ...,
        description=(
            "Weight associated with matching the corresponding nodeSelectorTerm, in the"
            " range 1-100."
        ),
    )


class QuobyteVolumeSource(BaseModel):
    group: Optional[str] = Field(
        default=None, description="group to map volume access to Default is no group"
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the Quobyte volume to be mounted with read-only"
            " permissions. Defaults to false."
        ),
    )
    registry: str = Field(
        ...,
        description=(
            "registry represents a single or multiple Quobyte Registry services"
            " specified as a string as host:port pair (multiple entries are separated"
            " with commas) which acts as the central registry for volumes"
        ),
    )
    tenant: Optional[str] = Field(
        default=None,
        description=(
            "tenant owning the given Quobyte volume in the Backend Used with"
            " dynamically provisioned Quobyte volumes, value is set by the plugin"
        ),
    )
    user: Optional[str] = Field(
        default=None,
        description="user to map volume access to Defaults to serivceaccount user",
    )
    volume: str = Field(
        ...,
        description=(
            "volume is a string that references an already created Quobyte volume by"
            " name."
        ),
    )


class RBDVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type of the volume that you want to mount. Tip:"
            " Ensure that the filesystem type is supported by the host operating"
            ' system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"'
            " if unspecified. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#rbd"
        ),
    )
    image: str = Field(
        ...,
        description=(
            "image is the rados image name. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    keyring: Optional[str] = Field(
        default=None,
        description=(
            "keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring."
            " More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    monitors: List[str] = Field(
        ...,
        description=(
            "monitors is a collection of Ceph monitors. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    pool: Optional[str] = Field(
        default=None,
        description=(
            "pool is the rados pool name. Default is rbd. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to"
            " false. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef is name of the authentication secret for RBDUser. If provided"
            " overrides keyring. Default is nil. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )
    user: Optional[str] = Field(
        default=None,
        description=(
            "user is the rados user name. Default is admin. More info:"
            " https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        ),
    )


class ResourceClaim(BaseModel):
    name: str = Field(
        ...,
        description=(
            "Name must match the name of one entry in pod.spec.resourceClaims of the"
            " Pod where this field is used. It makes that resource available inside a"
            " container."
        ),
    )


class SELinuxOptions(BaseModel):
    level: Optional[str] = Field(
        default=None,
        description="Level is SELinux level label that applies to the container.",
    )
    role: Optional[str] = Field(
        default=None,
        description="Role is a SELinux role label that applies to the container.",
    )
    type: Optional[str] = Field(
        default=None,
        description="Type is a SELinux type label that applies to the container.",
    )
    user: Optional[str] = Field(
        default=None,
        description="User is a SELinux user label that applies to the container.",
    )


class ScaleIOVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs", "ntfs".'
            ' Default is "xfs".'
        ),
    )
    gateway: str = Field(
        ..., description="gateway is the host address of the ScaleIO API Gateway."
    )
    protectionDomain: Optional[str] = Field(
        default=None,
        description=(
            "protectionDomain is the name of the ScaleIO Protection Domain for the"
            " configured storage."
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly Defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts."
        ),
    )
    secretRef: LocalObjectReference = Field(
        ...,
        description=(
            "secretRef references to the secret for ScaleIO user and other sensitive"
            " information. If this is not provided, Login operation will fail."
        ),
    )
    sslEnabled: Optional[bool] = Field(
        default=None,
        description=(
            "sslEnabled Flag enable/disable SSL communication with Gateway, default"
            " false"
        ),
    )
    storageMode: Optional[str] = Field(
        default=None,
        description=(
            "storageMode indicates whether the storage for a volume should be"
            " ThickProvisioned or ThinProvisioned. Default is ThinProvisioned."
        ),
    )
    storagePool: Optional[str] = Field(
        default=None,
        description=(
            "storagePool is the ScaleIO Storage Pool associated with the protection"
            " domain."
        ),
    )
    system: str = Field(
        ...,
        description=(
            "system is the name of the storage system as configured in ScaleIO."
        ),
    )
    volumeName: Optional[str] = Field(
        default=None,
        description=(
            "volumeName is the name of a volume already created in the ScaleIO system"
            " that is associated with this volume source."
        ),
    )


class TypeModel(Enum):
    Localhost = "Localhost"
    RuntimeDefault = "RuntimeDefault"
    Unconfined = "Unconfined"


class SeccompProfile(BaseModel):
    localhostProfile: Optional[str] = Field(
        default=None,
        description=(
            "localhostProfile indicates a profile defined in a file on the node should"
            " be used. The profile must be preconfigured on the node to work. Must be a"
            " descending path, relative to the kubelet's configured seccomp profile"
            ' location. Must only be set if type is "Localhost".'
        ),
    )
    type: TypeModel = Field(
        ...,
        description=(
            "type indicates which kind of seccomp profile will be applied. Valid"
            " options are:\n\nLocalhost - a profile defined in a file on the node"
            " should be used. RuntimeDefault - the container runtime default profile"
            " should be used. Unconfined - no profile should be applied.\n\nPossible"
            ' enum values:\n - `"Localhost"` indicates a profile defined in a file on'
            " the node should be used. The file's location relative to"
            ' <kubelet-root-dir>/seccomp.\n - `"RuntimeDefault"` represents the default'
            ' container runtime seccomp profile.\n - `"Unconfined"` indicates no'
            " seccomp profile is applied (A.K.A. unconfined)."
        ),
    )


class SecretEnvSource(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None, description="Specify whether the Secret must be defined"
    )


class SecretKeySelector(BaseModel):
    key: str = Field(
        ...,
        description=(
            "The key of the secret to select from.  Must be a valid secret key."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description="Specify whether the Secret or its key must be defined",
    )


class SecretProjection(BaseModel):
    items: Optional[List[KeyToPath]] = Field(
        default=None,
        description=(
            "items if unspecified, each key-value pair in the Data field of the"
            " referenced Secret will be projected into the volume as a file whose name"
            " is the key and content is the value. If specified, the listed keys will"
            " be projected into the specified paths, and unlisted keys will not be"
            " present. If a key is specified which is not present in the Secret, the"
            " volume setup will error unless it is marked optional. Paths must be"
            " relative and may not contain the '..' path or start with '..'."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description=(
            "optional field specify whether the Secret or its key must be defined"
        ),
    )


class SecretVolumeSource(BaseModel):
    defaultMode: Optional[int] = Field(
        default=None,
        description=(
            "defaultMode is Optional: mode bits used to set permissions on created"
            " files by default. Must be an octal value between 0000 and 0777 or a"
            " decimal value between 0 and 511. YAML accepts both octal and decimal"
            " values, JSON requires decimal values for mode bits. Defaults to 0644."
            " Directories within the path are not affected by this setting. This might"
            " be in conflict with other options that affect the file mode, like"
            " fsGroup, and the result can be other mode bits set."
        ),
    )
    items: Optional[List[KeyToPath]] = Field(
        default=None,
        description=(
            "items If unspecified, each key-value pair in the Data field of the"
            " referenced Secret will be projected into the volume as a file whose name"
            " is the key and content is the value. If specified, the listed keys will"
            " be projected into the specified paths, and unlisted keys will not be"
            " present. If a key is specified which is not present in the Secret, the"
            " volume setup will error unless it is marked optional. Paths must be"
            " relative and may not contain the '..' path or start with '..'."
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description=(
            "optional field specify whether the Secret or its keys must be defined"
        ),
    )
    secretName: Optional[str] = Field(
        default=None,
        description=(
            "secretName is the name of the secret in the pod's namespace to use. More"
            " info: https://kubernetes.io/docs/concepts/storage/volumes#secret"
        ),
    )


class ProcMount(Enum):
    Default = "Default"
    Unmasked = "Unmasked"


class ServiceAccountTokenProjection(BaseModel):
    audience: Optional[str] = Field(
        default=None,
        description=(
            "audience is the intended audience of the token. A recipient of a token"
            " must identify itself with an identifier specified in the audience of the"
            " token, and otherwise should reject the token. The audience defaults to"
            " the identifier of the apiserver."
        ),
    )
    expirationSeconds: Optional[int] = Field(
        default=None,
        description=(
            "expirationSeconds is the requested duration of validity of the service"
            " account token. As the token approaches expiration, the kubelet volume"
            " plugin will proactively rotate the service account token. The kubelet"
            " will start trying to rotate the token if the token is older than 80"
            " percent of its time to live or if the token is older than 24"
            " hours.Defaults to 1 hour and must be at least 10 minutes."
        ),
    )
    path: str = Field(
        ...,
        description=(
            "path is the path relative to the mount point of the file to project the"
            " token into."
        ),
    )


class StorageOSVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs", "ntfs".'
            ' Implicitly inferred to be "ext4" if unspecified.'
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts."
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef specifies the secret to use for obtaining the StorageOS API"
            " credentials.  If not specified, default values will be attempted."
        ),
    )
    volumeName: Optional[str] = Field(
        default=None,
        description=(
            "volumeName is the human-readable name of the StorageOS volume.  Volume"
            " names are only unique within a namespace."
        ),
    )
    volumeNamespace: Optional[str] = Field(
        default=None,
        description=(
            "volumeNamespace specifies the scope of the volume within StorageOS.  If no"
            " namespace is specified then the Pod's namespace will be used.  This"
            " allows the Kubernetes name scoping to be mirrored within StorageOS for"
            " tighter integration. Set VolumeName to any name to override the default"
            ' behaviour. Set to "default" if you are not using namespaces within'
            " StorageOS. Namespaces that do not pre-exist within StorageOS will be"
            " created."
        ),
    )


class Sysctl(BaseModel):
    name: str = Field(..., description="Name of a property to set")
    value: str = Field(..., description="Value of a property to set")


class Effect(Enum):
    NoExecute = "NoExecute"
    NoSchedule = "NoSchedule"
    PreferNoSchedule = "PreferNoSchedule"


class OperatorModel(Enum):
    Equal = "Equal"
    Exists = "Exists"


class Toleration(BaseModel):
    effect: Optional[Effect] = Field(
        default=None,
        description=(
            "Effect indicates the taint effect to match. Empty means match all taint"
            " effects. When specified, allowed values are NoSchedule, PreferNoSchedule"
            ' and NoExecute.\n\nPossible enum values:\n - `"NoExecute"` Evict any'
            " already-running pods that do not tolerate the taint. Currently enforced"
            ' by NodeController.\n - `"NoSchedule"` Do not allow new pods to schedule'
            " onto the node unless they tolerate the taint, but allow all pods"
            " submitted to Kubelet without going through the scheduler to start, and"
            " allow all already-running pods to continue running. Enforced by the"
            ' scheduler.\n - `"PreferNoSchedule"` Like TaintEffectNoSchedule, but the'
            " scheduler tries not to schedule new pods onto the node, rather than"
            " prohibiting new pods from scheduling onto the node entirely. Enforced by"
            " the scheduler."
        ),
    )
    key: Optional[str] = Field(
        default=None,
        description=(
            "Key is the taint key that the toleration applies to. Empty means match all"
            " taint keys. If the key is empty, operator must be Exists; this"
            " combination means to match all values and all keys."
        ),
    )
    operator: Optional[OperatorModel] = Field(
        default=None,
        description=(
            "Operator represents a key's relationship to the value. Valid operators"
            " are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard"
            " for value, so that a pod can tolerate all taints of a particular"
            ' category.\n\nPossible enum values:\n - `"Equal"`\n - `"Exists"`'
        ),
    )
    tolerationSeconds: Optional[int] = Field(
        default=None,
        description=(
            "TolerationSeconds represents the period of time the toleration (which must"
            " be of effect NoExecute, otherwise this field is ignored) tolerates the"
            " taint. By default, it is not set, which means tolerate the taint forever"
            " (do not evict). Zero and negative values will be treated as 0 (evict"
            " immediately) by the system."
        ),
    )
    value: Optional[str] = Field(
        default=None,
        description=(
            "Value is the taint value the toleration matches to. If the operator is"
            " Exists, the value should be empty, otherwise just a regular string."
        ),
    )


class NodeAffinityPolicy(Enum):
    Honor = "Honor"
    Ignore = "Ignore"


class NodeTaintsPolicy(Enum):
    Honor = "Honor"
    Ignore = "Ignore"


class WhenUnsatisfiable(Enum):
    DoNotSchedule = "DoNotSchedule"
    ScheduleAnyway = "ScheduleAnyway"


class TypedLocalObjectReference(BaseModel):
    apiGroup: Optional[str] = Field(
        default=None,
        description=(
            "APIGroup is the group for the resource being referenced. If APIGroup is"
            " not specified, the specified Kind must be in the core API group. For any"
            " other third-party types, APIGroup is required."
        ),
    )
    kind: str = Field(..., description="Kind is the type of resource being referenced")
    name: str = Field(..., description="Name is the name of resource being referenced")


class TypedObjectReference(BaseModel):
    apiGroup: Optional[str] = Field(
        default=None,
        description=(
            "APIGroup is the group for the resource being referenced. If APIGroup is"
            " not specified, the specified Kind must be in the core API group. For any"
            " other third-party types, APIGroup is required."
        ),
    )
    kind: str = Field(..., description="Kind is the type of resource being referenced")
    name: str = Field(..., description="Name is the name of resource being referenced")
    namespace: Optional[str] = Field(
        default=None,
        description=(
            "Namespace is the namespace of resource being referenced Note that when a"
            " namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object"
            " is required in the referent namespace to allow that namespace's owner to"
            " accept the reference. See the ReferenceGrant documentation for details."
            " (Alpha) This field requires the CrossNamespaceVolumeDataSource feature"
            " gate to be enabled."
        ),
    )


class VolumeDevice(BaseModel):
    devicePath: str = Field(
        ...,
        description=(
            "devicePath is the path inside of the container that the device will be"
            " mapped to."
        ),
    )
    name: str = Field(
        ...,
        description="name must match the name of a persistentVolumeClaim in the pod",
    )


class MountPropagation(Enum):
    Bidirectional = "Bidirectional"
    HostToContainer = "HostToContainer"
    None_ = "None"


class VolumeMount(BaseModel):
    mountPath: str = Field(
        ...,
        description=(
            "Path within the container at which the volume should be mounted.  Must not"
            " contain ':'."
        ),
    )
    mountPropagation: Optional[MountPropagation] = Field(
        default=None,
        description=(
            "mountPropagation determines how mounts are propagated from the host to"
            " container and the other way around. When not set, MountPropagationNone is"
            " used. This field is beta in 1.10.\n\nPossible enum values:\n -"
            ' `"Bidirectional"` means that the volume in a container will receive new'
            " mounts from the host or other containers, and its own mounts will be"
            " propagated from the container to the host or other containers. Note that"
            ' this mode is recursively applied to all mounts in the volume ("rshared"'
            ' in Linux terminology).\n - `"HostToContainer"` means that the volume in a'
            " container will receive new mounts from the host or other containers, but"
            " filesystems mounted inside the container won't be propagated to the host"
            " or other containers. Note that this mode is recursively applied to all"
            ' mounts in the volume ("rslave" in Linux terminology).\n - `"None"` means'
            " that the volume in a container will not receive new mounts from the host"
            " or other containers, and filesystems mounted inside the container won't"
            " be propagated to the host or other containers. Note that this mode"
            ' corresponds to "private" in Linux terminology.'
        ),
    )
    name: str = Field(..., description="This must match the Name of a Volume.")
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "Mounted read-only if true, read-write otherwise (false or unspecified)."
            " Defaults to false."
        ),
    )
    subPath: Optional[str] = Field(
        default=None,
        description=(
            "Path within the volume from which the container's volume should be"
            ' mounted. Defaults to "" (volume\'s root).'
        ),
    )
    subPathExpr: Optional[str] = Field(
        default=None,
        description=(
            "Expanded path within the volume from which the container's volume should"
            " be mounted. Behaves similarly to SubPath but environment variable"
            " references $(VAR_NAME) are expanded using the container's environment."
            ' Defaults to "" (volume\'s root). SubPathExpr and SubPath are mutually'
            " exclusive."
        ),
    )


class VsphereVirtualDiskVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is filesystem type to mount. Must be a filesystem type supported by"
            ' the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred'
            ' to be "ext4" if unspecified.'
        ),
    )
    storagePolicyID: Optional[str] = Field(
        default=None,
        description=(
            "storagePolicyID is the storage Policy Based Management (SPBM) profile ID"
            " associated with the StoragePolicyName."
        ),
    )
    storagePolicyName: Optional[str] = Field(
        default=None,
        description=(
            "storagePolicyName is the storage Policy Based Management (SPBM) profile"
            " name."
        ),
    )
    volumePath: str = Field(
        ..., description="volumePath is the path that identifies vSphere volume vmdk"
    )


class WindowsSecurityContextOptions(BaseModel):
    gmsaCredentialSpec: Optional[str] = Field(
        default=None,
        description=(
            "GMSACredentialSpec is where the GMSA admission webhook"
            " (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of"
            " the GMSA credential spec named by the GMSACredentialSpecName field."
        ),
    )
    gmsaCredentialSpecName: Optional[str] = Field(
        default=None,
        description=(
            "GMSACredentialSpecName is the name of the GMSA credential spec to use."
        ),
    )
    hostProcess: Optional[bool] = Field(
        default=None,
        description=(
            "HostProcess determines if a container should be run as a 'Host Process'"
            " container. This field is alpha-level and will only be honored by"
            " components that enable the WindowsHostProcessContainers feature flag."
            " Setting this field without the feature flag will result in errors when"
            " validating the Pod. All of a Pod's containers must have the same"
            " effective HostProcess value (it is not allowed to have a mix of"
            " HostProcess containers and non-HostProcess containers).  In addition, if"
            " HostProcess is true then HostNetwork must also be set to true."
        ),
    )
    runAsUserName: Optional[str] = Field(
        default=None,
        description=(
            "The UserName in Windows to run the entrypoint of the container process."
            " Defaults to the user specified in image metadata if unspecified. May also"
            " be set in PodSecurityContext. If set in both SecurityContext and"
            " PodSecurityContext, the value specified in SecurityContext takes"
            " precedence."
        ),
    )


class ObjectReference(BaseModel):
    apiVersion: Optional[str] = Field(
        default=None, description="API version of the referent."
    )
    fieldPath: Optional[str] = Field(
        default=None,
        description=(
            "If referring to a piece of an object instead of an entire object, this"
            " string should contain a valid JSON/Go field access statement, such as"
            " desiredState.manifest.containers[2]. For example, if the object reference"
            " is to a container within a pod, this would take on a value like:"
            ' "spec.containers{name}" (where "name" refers to the name of the container'
            " that triggered the event) or if no container name is specified"
            ' "spec.containers[2]" (container with index 2 in this pod). This syntax is'
            " chosen only to have some well-defined way of referencing a part of an"
            " object."
        ),
    )
    kind: Optional[str] = Field(
        default=None,
        description=(
            "Kind of the referent. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    namespace: Optional[str] = Field(
        default=None,
        description=(
            "Namespace of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/"
        ),
    )
    resourceVersion: Optional[str] = Field(
        default=None,
        description=(
            "Specific resourceVersion to which this reference is made, if any. More"
            " info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency"
        ),
    )
    uid: Optional[str] = Field(
        default=None,
        description=(
            "UID of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids"
        ),
    )


class CSIVolumeSource(BaseModel):
    driver: str = Field(
        ...,
        description=(
            "driver is the name of the CSI driver that handles this volume. Consult"
            " with your admin for the correct name as registered in the cluster."
        ),
    )
    fsType: Optional[str] = Field(
        default=None,
        description=(
            'fsType to mount. Ex. "ext4", "xfs", "ntfs". If not provided, the empty'
            " value is passed to the associated CSI driver which will determine the"
            " default filesystem to apply."
        ),
    )
    nodePublishSecretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "nodePublishSecretRef is a reference to the secret object containing"
            " sensitive information to pass to the CSI driver to complete the CSI"
            " NodePublishVolume and NodeUnpublishVolume calls. This field is optional,"
            " and  may be empty if no secret is required. If the secret object contains"
            " more than one secret, all secret references are passed."
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly specifies a read-only configuration for the volume. Defaults to"
            " false (read/write)."
        ),
    )
    volumeAttributes: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "volumeAttributes stores driver-specific properties that are passed to the"
            " CSI driver. Consult your driver's documentation for supported values."
        ),
    )


class CephFSVolumeSource(BaseModel):
    monitors: List[str] = Field(
        ...,
        description=(
            "monitors is Required: Monitors is a collection of Ceph monitors More info:"
            " https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        ),
    )
    path: Optional[str] = Field(
        default=None,
        description=(
            "path is Optional: Used as the mounted root, rather than the full Ceph"
            " tree, default is /"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly is Optional: Defaults to false (read/write). ReadOnly here will"
            " force the ReadOnly setting in VolumeMounts. More info:"
            " https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        ),
    )
    secretFile: Optional[str] = Field(
        default=None,
        description=(
            "secretFile is Optional: SecretFile is the path to key ring for User,"
            " default is /etc/ceph/user.secret More info:"
            " https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef is Optional: SecretRef is reference to the authentication secret"
            " for User, default is empty. More info:"
            " https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        ),
    )
    user: Optional[str] = Field(
        default=None,
        description=(
            "user is optional: User is the rados user name, default is admin More info:"
            " https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        ),
    )


class CinderVolumeSource(BaseModel):
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Examples: "ext4", "xfs", "ntfs".'
            ' Implicitly inferred to be "ext4" if unspecified. More info:'
            " https://examples.k8s.io/mysql-cinder-pd/README.md"
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly defaults to false (read/write). ReadOnly here will force the"
            " ReadOnly setting in VolumeMounts. More info:"
            " https://examples.k8s.io/mysql-cinder-pd/README.md"
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef is optional: points to a secret object containing parameters"
            " used to connect to OpenStack."
        ),
    )
    volumeID: str = Field(
        ...,
        description=(
            "volumeID used to identify the volume in cinder. More info:"
            " https://examples.k8s.io/mysql-cinder-pd/README.md"
        ),
    )


class ConfigMapProjection(BaseModel):
    items: Optional[List[KeyToPath]] = Field(
        default=None,
        description=(
            "items if unspecified, each key-value pair in the Data field of the"
            " referenced ConfigMap will be projected into the volume as a file whose"
            " name is the key and content is the value. If specified, the listed keys"
            " will be projected into the specified paths, and unlisted keys will not be"
            " present. If a key is specified which is not present in the ConfigMap, the"
            " volume setup will error unless it is marked optional. Paths must be"
            " relative and may not contain the '..' path or start with '..'."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description=(
            "optional specify whether the ConfigMap or its keys must be defined"
        ),
    )


class ConfigMapVolumeSource(BaseModel):
    defaultMode: Optional[int] = Field(
        default=None,
        description=(
            "defaultMode is optional: mode bits used to set permissions on created"
            " files by default. Must be an octal value between 0000 and 0777 or a"
            " decimal value between 0 and 511. YAML accepts both octal and decimal"
            " values, JSON requires decimal values for mode bits. Defaults to 0644."
            " Directories within the path are not affected by this setting. This might"
            " be in conflict with other options that affect the file mode, like"
            " fsGroup, and the result can be other mode bits set."
        ),
    )
    items: Optional[List[KeyToPath]] = Field(
        default=None,
        description=(
            "items if unspecified, each key-value pair in the Data field of the"
            " referenced ConfigMap will be projected into the volume as a file whose"
            " name is the key and content is the value. If specified, the listed keys"
            " will be projected into the specified paths, and unlisted keys will not be"
            " present. If a key is specified which is not present in the ConfigMap, the"
            " volume setup will error unless it is marked optional. Paths must be"
            " relative and may not contain the '..' path or start with '..'."
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the referent. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    optional: Optional[bool] = Field(
        default=None,
        description=(
            "optional specify whether the ConfigMap or its keys must be defined"
        ),
    )


class EmptyDirVolumeSource(BaseModel):
    medium: Optional[str] = Field(
        default=None,
        description=(
            "medium represents what type of storage medium should back this directory."
            ' The default is "" which means to use the node\'s default medium. Must be'
            " an empty string (default) or Memory. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#emptydir"
        ),
    )
    sizeLimit: Optional[Union[str, float]] = Field(
        default=None,
        description=(
            "sizeLimit is the total amount of local storage required for this EmptyDir"
            " volume. The size limit is also applicable for memory medium. The maximum"
            " usage on memory medium EmptyDir would be the minimum value between the"
            " SizeLimit specified here and the sum of memory limits of all containers"
            " in a pod. The default is nil which means that the limit is undefined."
            " More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir"
        ),
    )


class EnvFromSource(BaseModel):
    configMapRef: Optional[ConfigMapEnvSource] = Field(
        default=None, description="The ConfigMap to select from"
    )
    prefix: Optional[str] = Field(
        default=None,
        description=(
            "An optional identifier to prepend to each key in the ConfigMap. Must be a"
            " C_IDENTIFIER."
        ),
    )
    secretRef: Optional[SecretEnvSource] = Field(
        default=None, description="The Secret to select from"
    )


class FlexVolumeSource(BaseModel):
    driver: str = Field(
        ..., description="driver is the name of the driver to use for this volume."
    )
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type to mount. Must be a filesystem type"
            ' supported by the host operating system. Ex. "ext4", "xfs", "ntfs". The'
            " default filesystem depends on FlexVolume script."
        ),
    )
    options: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "options is Optional: this field holds extra command options if any."
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly is Optional: defaults to false (read/write). ReadOnly here will"
            " force the ReadOnly setting in VolumeMounts."
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef is Optional: secretRef is reference to the secret object"
            " containing sensitive information to pass to the plugin scripts. This may"
            " be empty if no secret object is specified. If the secret object contains"
            " more than one secret, all secrets are passed to the plugin scripts."
        ),
    )


class HTTPGetAction(BaseModel):
    host: Optional[str] = Field(
        default=None,
        description=(
            "Host name to connect to, defaults to the pod IP. You probably want to set"
            ' "Host" in httpHeaders instead.'
        ),
    )
    httpHeaders: Optional[List[HTTPHeader]] = Field(
        default=None,
        description=(
            "Custom headers to set in the request. HTTP allows repeated headers."
        ),
    )
    path: Optional[str] = Field(
        default=None, description="Path to access on the HTTP server."
    )
    port: Union[int, str] = Field(
        ...,
        description=(
            "Name or number of the port to access on the container. Number must be in"
            " the range 1 to 65535. Name must be an IANA_SVC_NAME."
        ),
    )
    scheme: Optional[Scheme] = Field(
        default=None,
        description=(
            "Scheme to use for connecting to the host. Defaults to HTTP.\n\nPossible"
            ' enum values:\n - `"HTTP"` means that the scheme used will be http://\n -'
            ' `"HTTPS"` means that the scheme used will be https://'
        ),
    )


class ISCSIVolumeSource(BaseModel):
    chapAuthDiscovery: Optional[bool] = Field(
        default=None,
        description=(
            "chapAuthDiscovery defines whether support iSCSI Discovery CHAP"
            " authentication"
        ),
    )
    chapAuthSession: Optional[bool] = Field(
        default=None,
        description=(
            "chapAuthSession defines whether support iSCSI Session CHAP authentication"
        ),
    )
    fsType: Optional[str] = Field(
        default=None,
        description=(
            "fsType is the filesystem type of the volume that you want to mount. Tip:"
            " Ensure that the filesystem type is supported by the host operating"
            ' system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4"'
            " if unspecified. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#iscsi"
        ),
    )
    initiatorName: Optional[str] = Field(
        default=None,
        description=(
            "initiatorName is the custom iSCSI Initiator Name. If initiatorName is"
            " specified with iscsiInterface simultaneously, new iSCSI interface <target"
            " portal>:<volume name> will be created for the connection."
        ),
    )
    iqn: str = Field(..., description="iqn is the target iSCSI Qualified Name.")
    iscsiInterface: Optional[str] = Field(
        default=None,
        description=(
            "iscsiInterface is the interface Name that uses an iSCSI transport."
            " Defaults to 'default' (tcp)."
        ),
    )
    lun: int = Field(..., description="lun represents iSCSI Target Lun number.")
    portals: Optional[List[str]] = Field(
        default=None,
        description=(
            "portals is the iSCSI Target Portal List. The portal is either an IP or"
            " ip_addr:port if the port is other than default (typically TCP ports 860"
            " and 3260)."
        ),
    )
    readOnly: Optional[bool] = Field(
        default=None,
        description=(
            "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to"
            " false."
        ),
    )
    secretRef: Optional[LocalObjectReference] = Field(
        default=None,
        description=(
            "secretRef is the CHAP Secret for iSCSI target and initiator authentication"
        ),
    )
    targetPortal: str = Field(
        ...,
        description=(
            "targetPortal is iSCSI Target Portal. The Portal is either an IP or"
            " ip_addr:port if the port is other than default (typically TCP ports 860"
            " and 3260)."
        ),
    )


class NodeSelector(BaseModel):
    nodeSelectorTerms: List[NodeSelectorTerm] = Field(
        ..., description="Required. A list of node selector terms. The terms are ORed."
    )


class PersistentVolumeClaimCondition(BaseModel):
    lastProbeTime: Optional[datetime] = Field(
        default=None, description="lastProbeTime is the time we probed the condition."
    )
    lastTransitionTime: Optional[datetime] = Field(
        default=None,
        description=(
            "lastTransitionTime is the time the condition transitioned from one status"
            " to another."
        ),
    )
    message: Optional[str] = Field(
        default=None,
        description=(
            "message is the human-readable message indicating details about last"
            " transition."
        ),
    )
    reason: Optional[str] = Field(
        default=None,
        description=(
            "reason is a unique, this should be a short, machine understandable string"
            " that gives the reason for condition's last transition. If it reports"
            ' "ResizeStarted" that means the underlying persistent volume is being'
            " resized."
        ),
    )
    status: str
    type: str


class PersistentVolumeClaimStatus(BaseModel):
    accessModes: Optional[List[str]] = Field(
        default=None,
        description=(
            "accessModes contains the actual access modes the volume backing the PVC"
            " has. More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1"
        ),
    )
    allocatedResources: Optional[Dict[str, Union[str, float]]] = Field(
        default=None,
        description=(
            "allocatedResources is the storage resource within AllocatedResources"
            " tracks the capacity allocated to a PVC. It may be larger than the actual"
            " capacity when a volume expansion operation is requested. For storage"
            " quota, the larger value from allocatedResources and PVC.spec.resources is"
            " used. If allocatedResources is not set, PVC.spec.resources alone is used"
            " for quota calculation. If a volume expansion capacity request is lowered,"
            " allocatedResources is only lowered if there are no expansion operations"
            " in progress and if the actual volume capacity is equal or lower than the"
            " requested capacity. This is an alpha field and requires enabling"
            " RecoverVolumeExpansionFailure feature."
        ),
    )
    capacity: Optional[Dict[str, Union[str, float]]] = Field(
        default=None,
        description=(
            "capacity represents the actual resources of the underlying volume."
        ),
    )
    conditions: Optional[List[PersistentVolumeClaimCondition]] = Field(
        default=None,
        description=(
            "conditions is the current Condition of persistent volume claim. If"
            " underlying persistent volume is being resized then the Condition will be"
            " set to 'ResizeStarted'."
        ),
    )
    phase: Optional[Phase] = Field(
        default=None,
        description=(
            "phase represents the current phase of PersistentVolumeClaim.\n\nPossible"
            ' enum values:\n - `"Bound"` used for PersistentVolumeClaims that are'
            ' bound\n - `"Lost"` used for PersistentVolumeClaims that lost their'
            " underlying PersistentVolume. The claim was bound to a PersistentVolume"
            " and this volume does not exist any longer and all data on it was lost.\n"
            ' - `"Pending"` used for PersistentVolumeClaims that are not yet bound'
        ),
    )
    resizeStatus: Optional[ResizeStatus] = Field(
        default=None,
        description=(
            "resizeStatus stores status of resize operation. ResizeStatus is not set by"
            " default but when expansion is complete resizeStatus is set to empty"
            " string by resize controller or kubelet. This is an alpha field and"
            " requires enabling RecoverVolumeExpansionFailure feature.\n\nPossible enum"
            ' values:\n - `""` When expansion is complete, the empty string is set by'
            ' resize controller or kubelet.\n - `"ControllerExpansionFailed"` State set'
            " when expansion has failed in resize controller with a terminal error."
            " Transient errors such as timeout should not set this status and should"
            " leave ResizeStatus unmodified, so as resize controller can resume the"
            ' volume expansion.\n - `"ControllerExpansionInProgress"` State set when'
            " resize controller starts expanding the volume in control-plane\n -"
            ' `"NodeExpansionFailed"` State set when expansion has failed in kubelet'
            " with a terminal error. Transient errors don't set NodeExpansionFailed.\n"
            ' - `"NodeExpansionInProgress"` State set when kubelet starts expanding the'
            ' volume.\n - `"NodeExpansionPending"` State set when resize controller has'
            " finished expanding the volume but further expansion is needed on the"
            " node."
        ),
    )


class PodDNSConfig(BaseModel):
    nameservers: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of DNS name server IP addresses. This will be appended to the base"
            " nameservers generated from DNSPolicy. Duplicated nameservers will be"
            " removed."
        ),
    )
    options: Optional[List[PodDNSConfigOption]] = Field(
        default=None,
        description=(
            "A list of DNS resolver options. This will be merged with the base options"
            " generated from DNSPolicy. Duplicated entries will be removed. Resolution"
            " options given in Options will override those that appear in the base"
            " DNSPolicy."
        ),
    )
    searches: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of DNS search domains for host-name lookup. This will be appended"
            " to the base search paths generated from DNSPolicy. Duplicated search"
            " paths will be removed."
        ),
    )


class PodSecurityContext(BaseModel):
    fsGroup: Optional[int] = Field(
        default=None,
        description=(
            "A special supplemental group that applies to all containers in a pod. Some"
            " volume types allow the Kubelet to change the ownership of that volume to"
            " be owned by the pod:\n\n1. The owning GID will be the FSGroup 2. The"
            " setgid bit is set (new files created in the volume will be owned by"
            " FSGroup) 3. The permission bits are OR'd with rw-rw----\n\nIf unset, the"
            " Kubelet will not modify the ownership and permissions of any volume. Note"
            " that this field cannot be set when spec.os.name is windows."
        ),
    )
    fsGroupChangePolicy: Optional[FsGroupChangePolicy] = Field(
        default=None,
        description=(
            "fsGroupChangePolicy defines behavior of changing ownership and permission"
            " of the volume before being exposed inside Pod. This field will only apply"
            " to volume types which support fsGroup based ownership(and permissions)."
            " It will have no effect on ephemeral volume types such as: secret,"
            ' configmaps and emptydir. Valid values are "OnRootMismatch" and "Always".'
            ' If not specified, "Always" is used. Note that this field cannot be set'
            ' when spec.os.name is windows.\n\nPossible enum values:\n - `"Always"`'
            " indicates that volume's ownership and permissions should always be"
            " changed whenever volume is mounted inside a Pod. This the default"
            ' behavior.\n - `"OnRootMismatch"` indicates that volume\'s ownership and'
            " permissions will be changed only when permission and ownership of root"
            " directory does not match with expected permissions on the volume. This"
            " can help shorten the time it takes to change ownership and permissions of"
            " a volume."
        ),
    )
    runAsGroup: Optional[int] = Field(
        default=None,
        description=(
            "The GID to run the entrypoint of the container process. Uses runtime"
            " default if unset. May also be set in SecurityContext.  If set in both"
            " SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence for that container. Note that this field"
            " cannot be set when spec.os.name is windows."
        ),
    )
    runAsNonRoot: Optional[bool] = Field(
        default=None,
        description=(
            "Indicates that the container must run as a non-root user. If true, the"
            " Kubelet will validate the image at runtime to ensure that it does not run"
            " as UID 0 (root) and fail to start the container if it does. If unset or"
            " false, no such validation will be performed. May also be set in"
            " SecurityContext.  If set in both SecurityContext and PodSecurityContext,"
            " the value specified in SecurityContext takes precedence."
        ),
    )
    runAsUser: Optional[int] = Field(
        default=None,
        description=(
            "The UID to run the entrypoint of the container process. Defaults to user"
            " specified in image metadata if unspecified. May also be set in"
            " SecurityContext.  If set in both SecurityContext and PodSecurityContext,"
            " the value specified in SecurityContext takes precedence for that"
            " container. Note that this field cannot be set when spec.os.name is"
            " windows."
        ),
    )
    seLinuxOptions: Optional[SELinuxOptions] = Field(
        default=None,
        description=(
            "The SELinux context to be applied to all containers. If unspecified, the"
            " container runtime will allocate a random SELinux context for each"
            " container.  May also be set in SecurityContext.  If set in both"
            " SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence for that container. Note that this field"
            " cannot be set when spec.os.name is windows."
        ),
    )
    seccompProfile: Optional[SeccompProfile] = Field(
        default=None,
        description=(
            "The seccomp options to use by the containers in this pod. Note that this"
            " field cannot be set when spec.os.name is windows."
        ),
    )
    supplementalGroups: Optional[List[int]] = Field(
        default=None,
        description=(
            "A list of groups applied to the first process run in each container, in"
            " addition to the container's primary GID, the fsGroup (if specified), and"
            " group memberships defined in the container image for the uid of the"
            " container process. If unspecified, no additional groups are added to any"
            " container. Note that group memberships defined in the container image for"
            " the uid of the container process are still effective, even if they are"
            " not included in this list. Note that this field cannot be set when"
            " spec.os.name is windows."
        ),
    )
    sysctls: Optional[List[Sysctl]] = Field(
        default=None,
        description=(
            "Sysctls hold a list of namespaced sysctls used for the pod. Pods with"
            " unsupported sysctls (by the container runtime) might fail to launch. Note"
            " that this field cannot be set when spec.os.name is windows."
        ),
    )
    windowsOptions: Optional[WindowsSecurityContextOptions] = Field(
        default=None,
        description=(
            "The Windows specific settings applied to all containers. If unspecified,"
            " the options within a container's SecurityContext will be used. If set in"
            " both SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence. Note that this field cannot be set when"
            " spec.os.name is linux."
        ),
    )


class ResourceFieldSelector(BaseModel):
    containerName: Optional[str] = Field(
        default=None,
        description="Container name: required for volumes, optional for env vars",
    )
    divisor: Optional[Union[str, float]] = Field(
        default=None,
        description=(
            'Specifies the output format of the exposed resources, defaults to "1"'
        ),
    )
    resource: str = Field(..., description="Required: resource to select")


class ResourceRequirements(BaseModel):
    claims: Optional[List[ResourceClaim]] = Field(
        default=None,
        description=(
            "Claims lists the names of resources, defined in spec.resourceClaims, that"
            " are used by this container.\n\nThis is an alpha field and requires"
            " enabling the DynamicResourceAllocation feature gate.\n\nThis field is"
            " immutable. It can only be set for containers."
        ),
    )
    limits: Optional[Dict[str, Union[str, float]]] = Field(
        default=None,
        description=(
            "Limits describes the maximum amount of compute resources allowed. More"
            " info:"
            " https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        ),
    )
    requests: Optional[Dict[str, Union[str, float]]] = Field(
        default=None,
        description=(
            "Requests describes the minimum amount of compute resources required. If"
            " Requests is omitted for a container, it defaults to Limits if that is"
            " explicitly specified, otherwise to an implementation-defined value."
            " Requests cannot exceed Limits. More info:"
            " https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        ),
    )


class SecurityContext(BaseModel):
    allowPrivilegeEscalation: Optional[bool] = Field(
        default=None,
        description=(
            "AllowPrivilegeEscalation controls whether a process can gain more"
            " privileges than its parent process. This bool directly controls if the"
            " no_new_privs flag will be set on the container process."
            " AllowPrivilegeEscalation is true always when the container is: 1) run as"
            " Privileged 2) has CAP_SYS_ADMIN Note that this field cannot be set when"
            " spec.os.name is windows."
        ),
    )
    capabilities: Optional[Capabilities] = Field(
        default=None,
        description=(
            "The capabilities to add/drop when running containers. Defaults to the"
            " default set of capabilities granted by the container runtime. Note that"
            " this field cannot be set when spec.os.name is windows."
        ),
    )
    privileged: Optional[bool] = Field(
        default=None,
        description=(
            "Run container in privileged mode. Processes in privileged containers are"
            " essentially equivalent to root on the host. Defaults to false. Note that"
            " this field cannot be set when spec.os.name is windows."
        ),
    )
    procMount: Optional[ProcMount] = Field(
        default=None,
        description=(
            "procMount denotes the type of proc mount to use for the containers. The"
            " default is DefaultProcMount which uses the container runtime defaults for"
            " readonly paths and masked paths. This requires the ProcMountType feature"
            " flag to be enabled. Note that this field cannot be set when spec.os.name"
            ' is windows.\n\nPossible enum values:\n - `"Default"` uses the container'
            " runtime defaults for readonly and masked paths for /proc. Most container"
            " runtimes mask certain paths in /proc to avoid accidental security"
            ' exposure of special devices or information.\n - `"Unmasked"` bypasses the'
            " default masking behavior of the container runtime and ensures the newly"
            " created /proc the container stays in tact with no modifications."
        ),
    )
    readOnlyRootFilesystem: Optional[bool] = Field(
        default=None,
        description=(
            "Whether this container has a read-only root filesystem. Default is false."
            " Note that this field cannot be set when spec.os.name is windows."
        ),
    )
    runAsGroup: Optional[int] = Field(
        default=None,
        description=(
            "The GID to run the entrypoint of the container process. Uses runtime"
            " default if unset. May also be set in PodSecurityContext.  If set in both"
            " SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence. Note that this field cannot be set when"
            " spec.os.name is windows."
        ),
    )
    runAsNonRoot: Optional[bool] = Field(
        default=None,
        description=(
            "Indicates that the container must run as a non-root user. If true, the"
            " Kubelet will validate the image at runtime to ensure that it does not run"
            " as UID 0 (root) and fail to start the container if it does. If unset or"
            " false, no such validation will be performed. May also be set in"
            " PodSecurityContext.  If set in both SecurityContext and"
            " PodSecurityContext, the value specified in SecurityContext takes"
            " precedence."
        ),
    )
    runAsUser: Optional[int] = Field(
        default=None,
        description=(
            "The UID to run the entrypoint of the container process. Defaults to user"
            " specified in image metadata if unspecified. May also be set in"
            " PodSecurityContext.  If set in both SecurityContext and"
            " PodSecurityContext, the value specified in SecurityContext takes"
            " precedence. Note that this field cannot be set when spec.os.name is"
            " windows."
        ),
    )
    seLinuxOptions: Optional[SELinuxOptions] = Field(
        default=None,
        description=(
            "The SELinux context to be applied to the container. If unspecified, the"
            " container runtime will allocate a random SELinux context for each"
            " container.  May also be set in PodSecurityContext.  If set in both"
            " SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence. Note that this field cannot be set when"
            " spec.os.name is windows."
        ),
    )
    seccompProfile: Optional[SeccompProfile] = Field(
        default=None,
        description=(
            "The seccomp options to use by this container. If seccomp options are"
            " provided at both the pod & container level, the container options"
            " override the pod options. Note that this field cannot be set when"
            " spec.os.name is windows."
        ),
    )
    windowsOptions: Optional[WindowsSecurityContextOptions] = Field(
        default=None,
        description=(
            "The Windows specific settings applied to all containers. If unspecified,"
            " the options from the PodSecurityContext will be used. If set in both"
            " SecurityContext and PodSecurityContext, the value specified in"
            " SecurityContext takes precedence. Note that this field cannot be set when"
            " spec.os.name is linux."
        ),
    )


class TCPSocketAction(BaseModel):
    host: Optional[str] = Field(
        default=None,
        description="Optional: Host name to connect to, defaults to the pod IP.",
    )
    port: Union[int, str] = Field(
        ...,
        description=(
            "Number or name of the port to access on the container. Number must be in"
            " the range 1 to 65535. Name must be an IANA_SVC_NAME."
        ),
    )


class DownwardAPIVolumeFile(BaseModel):
    fieldRef: Optional[ObjectFieldSelector] = Field(
        default=None,
        description=(
            "Required: Selects a field of the pod: only annotations, labels, name and"
            " namespace are supported."
        ),
    )
    mode: Optional[int] = Field(
        default=None,
        description=(
            "Optional: mode bits used to set permissions on this file, must be an octal"
            " value between 0000 and 0777 or a decimal value between 0 and 511. YAML"
            " accepts both octal and decimal values, JSON requires decimal values for"
            " mode bits. If not specified, the volume defaultMode will be used. This"
            " might be in conflict with other options that affect the file mode, like"
            " fsGroup, and the result can be other mode bits set."
        ),
    )
    path: str = Field(
        ...,
        description=(
            "Required: Path is  the relative path name of the file to be created. Must"
            " not be absolute or contain the '..' path. Must be utf-8 encoded. The"
            " first item of the relative path must not start with '..'"
        ),
    )
    resourceFieldRef: Optional[ResourceFieldSelector] = Field(
        default=None,
        description=(
            "Selects a resource of the container: only resources limits and requests"
            " (limits.cpu, limits.memory, requests.cpu and requests.memory) are"
            " currently supported."
        ),
    )


class DownwardAPIVolumeSource(BaseModel):
    defaultMode: Optional[int] = Field(
        default=None,
        description=(
            "Optional: mode bits to use on created files by default. Must be a"
            " Optional: mode bits used to set permissions on created files by default."
            " Must be an octal value between 0000 and 0777 or a decimal value between 0"
            " and 511. YAML accepts both octal and decimal values, JSON requires"
            " decimal values for mode bits. Defaults to 0644. Directories within the"
            " path are not affected by this setting. This might be in conflict with"
            " other options that affect the file mode, like fsGroup, and the result can"
            " be other mode bits set."
        ),
    )
    items: Optional[List[DownwardAPIVolumeFile]] = Field(
        default=None, description="Items is a list of downward API volume file"
    )


class EnvVarSource(BaseModel):
    configMapKeyRef: Optional[ConfigMapKeySelector] = Field(
        default=None, description="Selects a key of a ConfigMap."
    )
    fieldRef: Optional[ObjectFieldSelector] = Field(
        default=None,
        description=(
            "Selects a field of the pod: supports metadata.name, metadata.namespace,"
            " `metadata.labels['<KEY>']`, `metadata.annotations['<KEY>']`,"
            " spec.nodeName, spec.serviceAccountName, status.hostIP, status.podIP,"
            " status.podIPs."
        ),
    )
    resourceFieldRef: Optional[ResourceFieldSelector] = Field(
        default=None,
        description=(
            "Selects a resource of the container: only resources limits and requests"
            " (limits.cpu, limits.memory, limits.ephemeral-storage, requests.cpu,"
            " requests.memory and requests.ephemeral-storage) are currently supported."
        ),
    )
    secretKeyRef: Optional[SecretKeySelector] = Field(
        default=None, description="Selects a key of a secret in the pod's namespace"
    )


class LifecycleHandler(BaseModel):
    exec: Optional[ExecAction] = Field(
        default=None, description="Exec specifies the action to take."
    )
    httpGet: Optional[HTTPGetAction] = Field(
        default=None, description="HTTPGet specifies the http request to perform."
    )
    tcpSocket: Optional[TCPSocketAction] = Field(
        default=None,
        description=(
            "Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for"
            " the backward compatibility. There are no validation of this field and"
            " lifecycle hooks will fail in runtime when tcp handler is specified."
        ),
    )


class NodeAffinity(BaseModel):
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[PreferredSchedulingTerm]
    ] = Field(
        default=None,
        description=(
            "The scheduler will prefer to schedule pods to nodes that satisfy the"
            " affinity expressions specified by this field, but it may choose a node"
            " that violates one or more of the expressions. The node that is most"
            " preferred is the one with the greatest sum of weights, i.e. for each node"
            " that meets all of the scheduling requirements (resource request,"
            " requiredDuringScheduling affinity expressions, etc.), compute a sum by"
            ' iterating through the elements of this field and adding "weight" to the'
            " sum if the node matches the corresponding matchExpressions; the node(s)"
            " with the highest sum are the most preferred."
        ),
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[NodeSelector] = Field(
        default=None,
        description=(
            "If the affinity requirements specified by this field are not met at"
            " scheduling time, the pod will not be scheduled onto the node. If the"
            " affinity requirements specified by this field cease to be met at some"
            " point during pod execution (e.g. due to an update), the system may or may"
            " not try to eventually evict the pod from its node."
        ),
    )


class PersistentVolumeClaimSpec(BaseModel):
    accessModes: Optional[List[str]] = Field(
        default=None,
        description=(
            "accessModes contains the desired access modes the volume should have. More"
            " info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1"
        ),
    )
    dataSource: Optional[TypedLocalObjectReference] = Field(
        default=None,
        description=(
            "dataSource field can be used to specify either: * An existing"
            " VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An"
            " existing PVC (PersistentVolumeClaim) If the provisioner or an external"
            " controller can support the specified data source, it will create a new"
            " volume based on the contents of the specified data source. When the"
            " AnyVolumeDataSource feature gate is enabled, dataSource contents will be"
            " copied to dataSourceRef, and dataSourceRef contents will be copied to"
            " dataSource when dataSourceRef.namespace is not specified. If the"
            " namespace is specified, then dataSourceRef will not be copied to"
            " dataSource."
        ),
    )
    dataSourceRef: Optional[TypedObjectReference] = Field(
        default=None,
        description=(
            "dataSourceRef specifies the object from which to populate the volume with"
            " data, if a non-empty volume is desired. This may be any object from a"
            " non-empty API group (non core object) or a PersistentVolumeClaim object."
            " When this field is specified, volume binding will only succeed if the"
            " type of the specified object matches some installed volume populator or"
            " dynamic provisioner. This field will replace the functionality of the"
            " dataSource field and as such if both fields are non-empty, they must have"
            " the same value. For backwards compatibility, when namespace isn't"
            " specified in dataSourceRef, both fields (dataSource and dataSourceRef)"
            " will be set to the same value automatically if one of them is empty and"
            " the other is non-empty. When namespace is specified in dataSourceRef,"
            " dataSource isn't set to the same value and must be empty. There are three"
            " important differences between dataSource and dataSourceRef: * While"
            " dataSource only allows two specific types of objects, dataSourceRef\n "
            " allows any non-core object, as well as PersistentVolumeClaim objects.\n*"
            " While dataSource ignores disallowed values (dropping them),"
            " dataSourceRef\n  preserves all values, and generates an error if a"
            " disallowed value is\n  specified.\n* While dataSource only allows local"
            " objects, dataSourceRef allows objects\n  in any namespaces.\n(Beta) Using"
            " this field requires the AnyVolumeDataSource feature gate to be enabled."
            " (Alpha) Using the namespace field of dataSourceRef requires the"
            " CrossNamespaceVolumeDataSource feature gate to be enabled."
        ),
    )
    resources: Optional[ResourceRequirements] = Field(
        default=None,
        description=(
            "resources represents the minimum resources the volume should have. If"
            " RecoverVolumeExpansionFailure feature is enabled users are allowed to"
            " specify resource requirements that are lower than previous value but must"
            " still be higher than capacity recorded in the status field of the claim."
            " More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources"
        ),
    )
    selector: Optional[v1.LabelSelector] = Field(
        default=None,
        description="selector is a label query over volumes to consider for binding.",
    )
    storageClassName: Optional[str] = Field(
        default=None,
        description=(
            "storageClassName is the name of the StorageClass required by the claim."
            " More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1"
        ),
    )
    volumeMode: Optional[VolumeMode] = Field(
        default=None,
        description=(
            "volumeMode defines what type of volume is required by the claim. Value of"
            " Filesystem is implied when not included in claim spec.\n\nPossible enum"
            ' values:\n - `"Block"` means the volume will not be formatted with a'
            ' filesystem and will remain a raw block device.\n - `"Filesystem"` means'
            " the volume will be or is formatted with a filesystem."
        ),
    )
    volumeName: Optional[str] = Field(
        default=None,
        description=(
            "volumeName is the binding reference to the PersistentVolume backing this"
            " claim."
        ),
    )


class PersistentVolumeClaimTemplate(BaseModel):
    metadata: Optional[v1.ObjectMeta] = Field(
        default=None,
        description=(
            "May contain labels and annotations that will be copied into the PVC when"
            " creating it. No other fields are allowed and will be rejected during"
            " validation."
        ),
    )
    spec: PersistentVolumeClaimSpec = Field(
        ...,
        description=(
            "The specification for the PersistentVolumeClaim. The entire content is"
            " copied unchanged into the PVC that gets created from this template. The"
            " same fields as in a PersistentVolumeClaim are also valid here."
        ),
    )


class PodAffinityTerm(BaseModel):
    labelSelector: Optional[v1.LabelSelector] = Field(
        default=None,
        description="A label query over a set of resources, in this case pods.",
    )
    namespaceSelector: Optional[v1.LabelSelector] = Field(
        default=None,
        description=(
            "A label query over the set of namespaces that the term applies to. The"
            " term is applied to the union of the namespaces selected by this field and"
            " the ones listed in the namespaces field. null selector and null or empty"
            ' namespaces list means "this pod\'s namespace". An empty selector ({})'
            " matches all namespaces."
        ),
    )
    namespaces: Optional[List[str]] = Field(
        default=None,
        description=(
            "namespaces specifies a static list of namespace names that the term"
            " applies to. The term is applied to the union of the namespaces listed in"
            " this field and the ones selected by namespaceSelector. null or empty"
            ' namespaces list and null namespaceSelector means "this pod\'s namespace".'
        ),
    )
    topologyKey: str = Field(
        ...,
        description=(
            "This pod should be co-located (affinity) or not co-located (anti-affinity)"
            " with the pods matching the labelSelector in the specified namespaces,"
            " where co-located is defined as running on a node whose value of the label"
            " with key topologyKey matches that of any node on which any of the"
            " selected pods is running. Empty topologyKey is not allowed."
        ),
    )


class Probe(BaseModel):
    exec: Optional[ExecAction] = Field(
        default=None, description="Exec specifies the action to take."
    )
    failureThreshold: Optional[int] = Field(
        default=None,
        description=(
            "Minimum consecutive failures for the probe to be considered failed after"
            " having succeeded. Defaults to 3. Minimum value is 1."
        ),
    )
    grpc: Optional[GRPCAction] = Field(
        default=None, description="GRPC specifies an action involving a GRPC port."
    )
    httpGet: Optional[HTTPGetAction] = Field(
        default=None, description="HTTPGet specifies the http request to perform."
    )
    initialDelaySeconds: Optional[int] = Field(
        default=None,
        description=(
            "Number of seconds after the container has started before liveness probes"
            " are initiated. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        ),
    )
    periodSeconds: Optional[int] = Field(
        default=None,
        description=(
            "How often (in seconds) to perform the probe. Default to 10 seconds."
            " Minimum value is 1."
        ),
    )
    successThreshold: Optional[int] = Field(
        default=None,
        description=(
            "Minimum consecutive successes for the probe to be considered successful"
            " after having failed. Defaults to 1. Must be 1 for liveness and startup."
            " Minimum value is 1."
        ),
    )
    tcpSocket: Optional[TCPSocketAction] = Field(
        default=None, description="TCPSocket specifies an action involving a TCP port."
    )
    terminationGracePeriodSeconds: Optional[int] = Field(
        default=None,
        description=(
            "Optional duration in seconds the pod needs to terminate gracefully upon"
            " probe failure. The grace period is the duration in seconds after the"
            " processes running in the pod are sent a termination signal and the time"
            " when the processes are forcibly halted with a kill signal. Set this value"
            " longer than the expected cleanup time for your process. If this value is"
            " nil, the pod's terminationGracePeriodSeconds will be used. Otherwise,"
            " this value overrides the value provided by the pod spec. Value must be"
            " non-negative integer. The value zero indicates stop immediately via the"
            " kill signal (no opportunity to shut down). This is a beta field and"
            " requires enabling ProbeTerminationGracePeriod feature gate. Minimum value"
            " is 1. spec.terminationGracePeriodSeconds is used if unset."
        ),
    )
    timeoutSeconds: Optional[int] = Field(
        default=None,
        description=(
            "Number of seconds after which the probe times out. Defaults to 1 second."
            " Minimum value is 1. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        ),
    )


class TopologySpreadConstraint(BaseModel):
    labelSelector: Optional[v1.LabelSelector] = Field(
        default=None,
        description=(
            "LabelSelector is used to find matching pods. Pods that match this label"
            " selector are counted to determine the number of pods in their"
            " corresponding topology domain."
        ),
    )
    matchLabelKeys: Optional[List[str]] = Field(
        default=None,
        description=(
            "MatchLabelKeys is a set of pod label keys to select the pods over which"
            " spreading will be calculated. The keys are used to lookup values from the"
            " incoming pod labels, those key-value labels are ANDed with labelSelector"
            " to select the group of existing pods over which spreading will be"
            " calculated for the incoming pod. The same key is forbidden to exist in"
            " both MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when"
            " LabelSelector isn't set. Keys that don't exist in the incoming pod labels"
            " will be ignored. A null or empty list means only match against"
            " labelSelector.\n\nThis is a beta field and requires the"
            " MatchLabelKeysInPodTopologySpread feature gate to be enabled (enabled by"
            " default)."
        ),
    )
    maxSkew: int = Field(
        ...,
        description=(
            "MaxSkew describes the degree to which pods may be unevenly distributed."
            " When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted"
            " difference between the number of matching pods in the target topology and"
            " the global minimum. The global minimum is the minimum number of matching"
            " pods in an eligible domain or zero if the number of eligible domains is"
            " less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to"
            " 1, and pods with the same labelSelector spread as 2/2/1: In this case,"
            " the global minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P "
            "  | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to"
            " become 2/2/2; scheduling it onto zone1(zone2) would make the"
            " ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2,"
            " incoming pod can be scheduled onto any zone. When"
            " `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence"
            " to topologies that satisfy it. It's a required field. Default value is 1"
            " and 0 is not allowed."
        ),
    )
    minDomains: Optional[int] = Field(
        default=None,
        description=(
            "MinDomains indicates a minimum number of eligible domains. When the number"
            " of eligible domains with matching topology keys is less than minDomains,"
            ' Pod Topology Spread treats "global minimum" as 0, and then the'
            " calculation of Skew is performed. And when the number of eligible domains"
            " with matching topology keys equals or greater than minDomains, this value"
            " has no effect on scheduling. As a result, when the number of eligible"
            " domains is less than minDomains, scheduler won't schedule more than"
            " maxSkew Pods to those domains. If value is nil, the constraint behaves as"
            " if MinDomains is equal to 1. Valid values are integers greater than 0."
            " When value is not nil, WhenUnsatisfiable must be DoNotSchedule.\n\nFor"
            " example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5"
            " and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 |"
            " zone3 | |  P P  |  P P  |  P P  | The number of domains is less than"
            ' 5(MinDomains), so "global minimum" is treated as 0. In this situation,'
            " new pod with the same labelSelector cannot be scheduled, because computed"
            " skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones,"
            " it will violate MaxSkew.\n\nThis is a beta field and requires the"
            " MinDomainsInPodTopologySpread feature gate to be enabled (enabled by"
            " default)."
        ),
    )
    nodeAffinityPolicy: Optional[NodeAffinityPolicy] = Field(
        default=None,
        description=(
            "NodeAffinityPolicy indicates how we will treat Pod's"
            " nodeAffinity/nodeSelector when calculating pod topology spread skew."
            " Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are"
            " included in the calculations. - Ignore: nodeAffinity/nodeSelector are"
            " ignored. All nodes are included in the calculations.\n\nIf this value is"
            " nil, the behavior is equivalent to the Honor policy. This is a beta-level"
            " feature default enabled by the NodeInclusionPolicyInPodTopologySpread"
            ' feature flag.\n\nPossible enum values:\n - `"Honor"` means use this'
            " scheduling directive when calculating pod topology spread skew.\n -"
            ' `"Ignore"` means ignore this scheduling directive when calculating pod'
            " topology spread skew."
        ),
    )
    nodeTaintsPolicy: Optional[NodeTaintsPolicy] = Field(
        default=None,
        description=(
            "NodeTaintsPolicy indicates how we will treat node taints when calculating"
            " pod topology spread skew. Options are: - Honor: nodes without taints,"
            " along with tainted nodes for which the incoming pod has a toleration, are"
            " included. - Ignore: node taints are ignored. All nodes are"
            " included.\n\nIf this value is nil, the behavior is equivalent to the"
            " Ignore policy. This is a beta-level feature default enabled by the"
            " NodeInclusionPolicyInPodTopologySpread feature flag.\n\nPossible enum"
            ' values:\n - `"Honor"` means use this scheduling directive when'
            ' calculating pod topology spread skew.\n - `"Ignore"` means ignore this'
            " scheduling directive when calculating pod topology spread skew."
        ),
    )
    topologyKey: str = Field(
        ...,
        description=(
            "TopologyKey is the key of node labels. Nodes that have a label with this"
            " key and identical values are considered to be in the same topology. We"
            ' consider each <key, value> as a "bucket", and try to put balanced number'
            " of pods into each bucket. We define a domain as a particular instance of"
            " a topology. Also, we define an eligible domain as a domain whose nodes"
            " meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If"
            ' TopologyKey is "kubernetes.io/hostname", each Node is a domain of that'
            ' topology. And, if TopologyKey is "topology.kubernetes.io/zone", each zone'
            " is a domain of that topology. It's a required field."
        ),
    )
    whenUnsatisfiable: WhenUnsatisfiable = Field(
        ...,
        description=(
            "WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy"
            " the spread constraint. - DoNotSchedule (default) tells the scheduler not"
            " to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod"
            " in any location,\n  but giving higher precedence to topologies that would"
            ' help reduce the\n  skew.\nA constraint is considered "Unsatisfiable" for'
            " an incoming pod if and only if every possible node assignment for that"
            ' pod would violate "MaxSkew" on some topology. For example, in a 3-zone'
            " cluster, MaxSkew is set to 1, and pods with the same labelSelector spread"
            " as 3/1/1: | zone1 | zone2 | zone3 | | P P P |   P   |   P   | If"
            " WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be"
            " scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on"
            " zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still"
            " be imbalanced, but scheduler won't make it *more* imbalanced. It's a"
            ' required field.\n\nPossible enum values:\n - `"DoNotSchedule"` instructs'
            " the scheduler not to schedule the pod when constraints are not"
            ' satisfied.\n - `"ScheduleAnyway"` instructs the scheduler to schedule the'
            " pod even if constraints are not satisfied."
        ),
    )


class WeightedPodAffinityTerm(BaseModel):
    podAffinityTerm: PodAffinityTerm = Field(
        ...,
        description=(
            "Required. A pod affinity term, associated with the corresponding weight."
        ),
    )
    weight: int = Field(
        ...,
        description=(
            "weight associated with matching the corresponding podAffinityTerm, in the"
            " range 1-100."
        ),
    )


class DownwardAPIProjection(BaseModel):
    items: Optional[List[DownwardAPIVolumeFile]] = Field(
        default=None, description="Items is a list of DownwardAPIVolume file"
    )


class EnvVar(BaseModel):
    name: str = Field(
        ..., description="Name of the environment variable. Must be a C_IDENTIFIER."
    )
    value: Optional[str] = Field(
        default=None,
        description=(
            "Variable references $(VAR_NAME) are expanded using the previously defined"
            " environment variables in the container and any service environment"
            " variables. If a variable cannot be resolved, the reference in the input"
            " string will be unchanged. Double $$ are reduced to a single $, which"
            ' allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will'
            ' produce the string literal "$(VAR_NAME)". Escaped references will never'
            " be expanded, regardless of whether the variable exists or not. Defaults"
            ' to "".'
        ),
    )
    valueFrom: Optional[EnvVarSource] = Field(
        default=None,
        description=(
            "Source for the environment variable's value. Cannot be used if value is"
            " not empty."
        ),
    )


class EphemeralVolumeSource(BaseModel):
    volumeClaimTemplate: Optional[PersistentVolumeClaimTemplate] = Field(
        default=None,
        description=(
            "Will be used to create a stand-alone PVC to provision the volume. The pod"
            " in which this EphemeralVolumeSource is embedded will be the owner of the"
            " PVC, i.e. the PVC will be deleted together with the pod.  The name of the"
            " PVC will be `<pod name>-<volume name>` where `<volume name>` is the name"
            " from the `PodSpec.Volumes` array entry. Pod validation will reject the"
            " pod if the concatenated name is not valid for a PVC (for example, too"
            " long).\n\nAn existing PVC with that name that is not owned by the pod"
            " will *not* be used for the pod to avoid using an unrelated volume by"
            " mistake. Starting the pod is then blocked until the unrelated PVC is"
            " removed. If such a pre-created PVC is meant to be used by the pod, the"
            " PVC has to updated with an owner reference to the pod once the pod"
            " exists. Normally this should not be necessary, but it may be useful when"
            " manually reconstructing a broken cluster.\n\nThis field is read-only and"
            " no changes will be made by Kubernetes to the PVC after it has been"
            " created.\n\nRequired, must not be nil."
        ),
    )


class Lifecycle(BaseModel):
    postStart: Optional[LifecycleHandler] = Field(
        default=None,
        description=(
            "PostStart is called immediately after a container is created. If the"
            " handler fails, the container is terminated and restarted according to its"
            " restart policy. Other management of the container blocks until the hook"
            " completes. More info:"
            " https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks"
        ),
    )
    preStop: Optional[LifecycleHandler] = Field(
        default=None,
        description=(
            "PreStop is called immediately before a container is terminated due to an"
            " API request or management event such as liveness/startup probe failure,"
            " preemption, resource contention, etc. The handler is not called if the"
            " container crashes or exits. The Pod's termination grace period countdown"
            " begins before the PreStop hook is executed. Regardless of the outcome of"
            " the handler, the container will eventually terminate within the Pod's"
            " termination grace period (unless delayed by finalizers). Other management"
            " of the container blocks until the hook completes or until the termination"
            " grace period is reached. More info:"
            " https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks"
        ),
    )


class PersistentVolumeClaim(BaseModel):
    apiVersion: Optional[str] = Field(
        default=None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="PersistentVolumeClaim",
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
    spec: Optional[PersistentVolumeClaimSpec] = Field(
        default=None,
        description=(
            "spec defines the desired characteristics of a volume requested by a pod"
            " author. More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        ),
    )
    status: Optional[PersistentVolumeClaimStatus] = Field(
        default=None,
        description=(
            "status represents the current information/status of a persistent volume"
            " claim. Read-only. More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        ),
    )


class PodAffinity(BaseModel):
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[WeightedPodAffinityTerm]
    ] = Field(
        default=None,
        description=(
            "The scheduler will prefer to schedule pods to nodes that satisfy the"
            " affinity expressions specified by this field, but it may choose a node"
            " that violates one or more of the expressions. The node that is most"
            " preferred is the one with the greatest sum of weights, i.e. for each node"
            " that meets all of the scheduling requirements (resource request,"
            " requiredDuringScheduling affinity expressions, etc.), compute a sum by"
            ' iterating through the elements of this field and adding "weight" to the'
            " sum if the node has pods which matches the corresponding podAffinityTerm;"
            " the node(s) with the highest sum are the most preferred."
        ),
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[List[PodAffinityTerm]] = (
        Field(
            default=None,
            description=(
                "If the affinity requirements specified by this field are not met at"
                " scheduling time, the pod will not be scheduled onto the node. If the"
                " affinity requirements specified by this field cease to be met at some"
                " point during pod execution (e.g. due to a pod label update), the"
                " system may or may not try to eventually evict the pod from its node."
                " When there are multiple elements, the lists of nodes corresponding to"
                " each podAffinityTerm are intersected, i.e. all terms must be"
                " satisfied."
            ),
        )
    )


class PodAntiAffinity(BaseModel):
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[WeightedPodAffinityTerm]
    ] = Field(
        default=None,
        description=(
            "The scheduler will prefer to schedule pods to nodes that satisfy the"
            " anti-affinity expressions specified by this field, but it may choose a"
            " node that violates one or more of the expressions. The node that is most"
            " preferred is the one with the greatest sum of weights, i.e. for each node"
            " that meets all of the scheduling requirements (resource request,"
            " requiredDuringScheduling anti-affinity expressions, etc.), compute a sum"
            ' by iterating through the elements of this field and adding "weight" to'
            " the sum if the node has pods which matches the corresponding"
            " podAffinityTerm; the node(s) with the highest sum are the most preferred."
        ),
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[List[PodAffinityTerm]] = (
        Field(
            default=None,
            description=(
                "If the anti-affinity requirements specified by this field are not met"
                " at scheduling time, the pod will not be scheduled onto the node. If"
                " the anti-affinity requirements specified by this field cease to be"
                " met at some point during pod execution (e.g. due to a pod label"
                " update), the system may or may not try to eventually evict the pod"
                " from its node. When there are multiple elements, the lists of nodes"
                " corresponding to each podAffinityTerm are intersected, i.e. all terms"
                " must be satisfied."
            ),
        )
    )


class VolumeProjection(BaseModel):
    configMap: Optional[ConfigMapProjection] = Field(
        default=None,
        description="configMap information about the configMap data to project",
    )
    downwardAPI: Optional[DownwardAPIProjection] = Field(
        default=None,
        description="downwardAPI information about the downwardAPI data to project",
    )
    secret: Optional[SecretProjection] = Field(
        default=None, description="secret information about the secret data to project"
    )
    serviceAccountToken: Optional[ServiceAccountTokenProjection] = Field(
        default=None,
        description=(
            "serviceAccountToken is information about the serviceAccountToken data to"
            " project"
        ),
    )


class Affinity(BaseModel):
    nodeAffinity: Optional[NodeAffinity] = Field(
        default=None,
        description="Describes node affinity scheduling rules for the pod.",
    )
    podAffinity: Optional[PodAffinity] = Field(
        default=None,
        description=(
            "Describes pod affinity scheduling rules (e.g. co-locate this pod in the"
            " same node, zone, etc. as some other pod(s))."
        ),
    )
    podAntiAffinity: Optional[PodAntiAffinity] = Field(
        default=None,
        description=(
            "Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod"
            " in the same node, zone, etc. as some other pod(s))."
        ),
    )


class Container(BaseModel):
    args: Optional[List[str]] = Field(
        default=None,
        description=(
            "Arguments to the entrypoint. The container image's CMD is used if this is"
            " not provided. Variable references $(VAR_NAME) are expanded using the"
            " container's environment. If a variable cannot be resolved, the reference"
            " in the input string will be unchanged. Double $$ are reduced to a single"
            ' $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)"'
            ' will produce the string literal "$(VAR_NAME)". Escaped references will'
            " never be expanded, regardless of whether the variable exists or not."
            " Cannot be updated. More info:"
            " https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell"
        ),
    )
    command: Optional[List[str]] = Field(
        default=None,
        description=(
            "Entrypoint array. Not executed within a shell. The container image's"
            " ENTRYPOINT is used if this is not provided. Variable references"
            " $(VAR_NAME) are expanded using the container's environment. If a"
            " variable cannot be resolved, the reference in the input string will be"
            " unchanged. Double $$ are reduced to a single $, which allows for escaping"
            ' the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string'
            ' literal "$(VAR_NAME)". Escaped references will never be expanded,'
            " regardless of whether the variable exists or not. Cannot be updated. More"
            " info:"
            " https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell"
        ),
    )
    env: Optional[List[EnvVar]] = Field(
        default=None,
        description=(
            "List of environment variables to set in the container. Cannot be updated."
        ),
    )
    envFrom: Optional[List[EnvFromSource]] = Field(
        default=None,
        description=(
            "List of sources to populate environment variables in the container. The"
            " keys defined within a source must be a C_IDENTIFIER. All invalid keys"
            " will be reported as an event when the container is starting. When a key"
            " exists in multiple sources, the value associated with the last source"
            " will take precedence. Values defined by an Env with a duplicate key will"
            " take precedence. Cannot be updated."
        ),
    )
    image: Optional[str] = Field(
        default=None,
        description=(
            "Container image name. More info:"
            " https://kubernetes.io/docs/concepts/containers/images This field is"
            " optional to allow higher level config management to default or override"
            " container images in workload controllers like Deployments and"
            " StatefulSets."
        ),
    )
    imagePullPolicy: Optional[ImagePullPolicy] = Field(
        default=None,
        description=(
            "Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always"
            " if :latest tag is specified, or IfNotPresent otherwise. Cannot be"
            " updated. More info:"
            " https://kubernetes.io/docs/concepts/containers/images#updating-images\n\nPossible"
            ' enum values:\n - `"Always"` means that kubelet always attempts to pull'
            " the latest image. Container will fail If the pull fails.\n -"
            ' `"IfNotPresent"` means that kubelet pulls if the image isn\'t present on'
            " disk. Container will fail if the image isn't present and the pull"
            ' fails.\n - `"Never"` means that kubelet never pulls an image, but only'
            " uses a local image. Container will fail if the image isn't present"
        ),
    )
    lifecycle: Optional[Lifecycle] = Field(
        default=None,
        description=(
            "Actions that the management system should take in response to container"
            " lifecycle events. Cannot be updated."
        ),
    )
    livenessProbe: Optional[Probe] = Field(
        default=None,
        description=(
            "Periodic probe of container liveness. Container will be restarted if the"
            " probe fails. Cannot be updated. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        ),
    )
    name: str = Field(
        ...,
        description=(
            "Name of the container specified as a DNS_LABEL. Each container in a pod"
            " must have a unique name (DNS_LABEL). Cannot be updated."
        ),
    )
    ports: Optional[List[ContainerPort]] = Field(
        default=None,
        description=(
            "List of ports to expose from the container. Not specifying a port here"
            " DOES NOT prevent that port from being exposed. Any port which is"
            ' listening on the default "0.0.0.0" address inside a container will be'
            " accessible from the network. Modifying this array with strategic merge"
            " patch may corrupt the data. For more information See"
            " https://github.com/kubernetes/kubernetes/issues/108255. Cannot be"
            " updated."
        ),
    )
    readinessProbe: Optional[Probe] = Field(
        default=None,
        description=(
            "Periodic probe of container service readiness. Container will be removed"
            " from service endpoints if the probe fails. Cannot be updated. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        ),
    )
    resizePolicy: Optional[List[ContainerResizePolicy]] = Field(
        default=None, description="Resources resize policy for the container."
    )
    resources: Optional[ResourceRequirements] = Field(
        default=None,
        description=(
            "Compute Resources required by this container. Cannot be updated. More"
            " info:"
            " https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        ),
    )
    securityContext: Optional[SecurityContext] = Field(
        default=None,
        description=(
            "SecurityContext defines the security options the container should be run"
            " with. If set, the fields of SecurityContext override the equivalent"
            " fields of PodSecurityContext. More info:"
            " https://kubernetes.io/docs/tasks/configure-pod-container/security-context/"
        ),
    )
    startupProbe: Optional[Probe] = Field(
        default=None,
        description=(
            "StartupProbe indicates that the Pod has successfully initialized. If"
            " specified, no other probes are executed until this completes"
            " successfully. If this probe fails, the Pod will be restarted, just as if"
            " the livenessProbe failed. This can be used to provide different probe"
            " parameters at the beginning of a Pod's lifecycle, when it might take a"
            " long time to load data or warm a cache, than during steady-state"
            " operation. This cannot be updated. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        ),
    )
    stdin: Optional[bool] = Field(
        default=None,
        description=(
            "Whether this container should allocate a buffer for stdin in the container"
            " runtime. If this is not set, reads from stdin in the container will"
            " always result in EOF. Default is false."
        ),
    )
    stdinOnce: Optional[bool] = Field(
        default=None,
        description=(
            "Whether the container runtime should close the stdin channel after it has"
            " been opened by a single attach. When stdin is true the stdin stream will"
            " remain open across multiple attach sessions. If stdinOnce is set to true,"
            " stdin is opened on container start, is empty until the first client"
            " attaches to stdin, and then remains open and accepts data until the"
            " client disconnects, at which time stdin is closed and remains closed"
            " until the container is restarted. If this flag is false, a container"
            " processes that reads from stdin will never receive an EOF. Default is"
            " false"
        ),
    )
    terminationMessagePath: Optional[str] = Field(
        default=None,
        description=(
            "Optional: Path at which the file to which the container's termination"
            " message will be written is mounted into the container's filesystem."
            " Message written is intended to be brief final status, such as an"
            " assertion failure message. Will be truncated by the node if greater than"
            " 4096 bytes. The total message length across all containers will be"
            " limited to 12kb. Defaults to /dev/termination-log. Cannot be updated."
        ),
    )
    terminationMessagePolicy: Optional[TerminationMessagePolicy] = Field(
        default=None,
        description=(
            "Indicate how the termination message should be populated. File will use"
            " the contents of terminationMessagePath to populate the container status"
            " message on both success and failure. FallbackToLogsOnError will use the"
            " last chunk of container log output if the termination message file is"
            " empty and the container exited with an error. The log output is limited"
            " to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot"
            ' be updated.\n\nPossible enum values:\n - `"FallbackToLogsOnError"` will'
            " read the most recent contents of the container logs for the container"
            " status message when the container exits with an error and the"
            ' terminationMessagePath has no contents.\n - `"File"` is the default'
            " behavior and will set the container status message to the contents of the"
            " container's terminationMessagePath when the container exits."
        ),
    )
    tty: Optional[bool] = Field(
        default=None,
        description=(
            "Whether this container should allocate a TTY for itself, also requires"
            " 'stdin' to be true. Default is false."
        ),
    )
    volumeDevices: Optional[List[VolumeDevice]] = Field(
        default=None,
        description=(
            "volumeDevices is the list of block devices to be used by the container."
        ),
    )
    volumeMounts: Optional[List[VolumeMount]] = Field(
        default=None,
        description=(
            "Pod volumes to mount into the container's filesystem. Cannot be updated."
        ),
    )
    workingDir: Optional[str] = Field(
        default=None,
        description=(
            "Container's working directory. If not specified, the container runtime's"
            " default will be used, which might be configured in the container image."
            " Cannot be updated."
        ),
    )


class EphemeralContainer(BaseModel):
    args: Optional[List[str]] = Field(
        default=None,
        description=(
            "Arguments to the entrypoint. The image's CMD is used if this is not"
            " provided. Variable references $(VAR_NAME) are expanded using the"
            " container's environment. If a variable cannot be resolved, the reference"
            " in the input string will be unchanged. Double $$ are reduced to a single"
            ' $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)"'
            ' will produce the string literal "$(VAR_NAME)". Escaped references will'
            " never be expanded, regardless of whether the variable exists or not."
            " Cannot be updated. More info:"
            " https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell"
        ),
    )
    command: Optional[List[str]] = Field(
        default=None,
        description=(
            "Entrypoint array. Not executed within a shell. The image's ENTRYPOINT is"
            " used if this is not provided. Variable references $(VAR_NAME) are"
            " expanded using the container's environment. If a variable cannot be"
            " resolved, the reference in the input string will be unchanged. Double $$"
            " are reduced to a single $, which allows for escaping the $(VAR_NAME)"
            ' syntax: i.e. "$$(VAR_NAME)" will produce the string literal'
            ' "$(VAR_NAME)". Escaped references will never be expanded, regardless of'
            " whether the variable exists or not. Cannot be updated. More info:"
            " https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell"
        ),
    )
    env: Optional[List[EnvVar]] = Field(
        default=None,
        description=(
            "List of environment variables to set in the container. Cannot be updated."
        ),
    )
    envFrom: Optional[List[EnvFromSource]] = Field(
        default=None,
        description=(
            "List of sources to populate environment variables in the container. The"
            " keys defined within a source must be a C_IDENTIFIER. All invalid keys"
            " will be reported as an event when the container is starting. When a key"
            " exists in multiple sources, the value associated with the last source"
            " will take precedence. Values defined by an Env with a duplicate key will"
            " take precedence. Cannot be updated."
        ),
    )
    image: Optional[str] = Field(
        default=None,
        description=(
            "Container image name. More info:"
            " https://kubernetes.io/docs/concepts/containers/images"
        ),
    )
    imagePullPolicy: Optional[ImagePullPolicy] = Field(
        default=None,
        description=(
            "Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always"
            " if :latest tag is specified, or IfNotPresent otherwise. Cannot be"
            " updated. More info:"
            " https://kubernetes.io/docs/concepts/containers/images#updating-images\n\nPossible"
            ' enum values:\n - `"Always"` means that kubelet always attempts to pull'
            " the latest image. Container will fail If the pull fails.\n -"
            ' `"IfNotPresent"` means that kubelet pulls if the image isn\'t present on'
            " disk. Container will fail if the image isn't present and the pull"
            ' fails.\n - `"Never"` means that kubelet never pulls an image, but only'
            " uses a local image. Container will fail if the image isn't present"
        ),
    )
    lifecycle: Optional[Lifecycle] = Field(
        default=None, description="Lifecycle is not allowed for ephemeral containers."
    )
    livenessProbe: Optional[Probe] = Field(
        default=None, description="Probes are not allowed for ephemeral containers."
    )
    name: str = Field(
        ...,
        description=(
            "Name of the ephemeral container specified as a DNS_LABEL. This name must"
            " be unique among all containers, init containers and ephemeral containers."
        ),
    )
    ports: Optional[List[ContainerPort]] = Field(
        default=None, description="Ports are not allowed for ephemeral containers."
    )
    readinessProbe: Optional[Probe] = Field(
        default=None, description="Probes are not allowed for ephemeral containers."
    )
    resizePolicy: Optional[List[ContainerResizePolicy]] = Field(
        default=None, description="Resources resize policy for the container."
    )
    resources: Optional[ResourceRequirements] = Field(
        default=None,
        description=(
            "Resources are not allowed for ephemeral containers. Ephemeral containers"
            " use spare resources already allocated to the pod."
        ),
    )
    securityContext: Optional[SecurityContext] = Field(
        default=None,
        description=(
            "Optional: SecurityContext defines the security options the ephemeral"
            " container should be run with. If set, the fields of SecurityContext"
            " override the equivalent fields of PodSecurityContext."
        ),
    )
    startupProbe: Optional[Probe] = Field(
        default=None, description="Probes are not allowed for ephemeral containers."
    )
    stdin: Optional[bool] = Field(
        default=None,
        description=(
            "Whether this container should allocate a buffer for stdin in the container"
            " runtime. If this is not set, reads from stdin in the container will"
            " always result in EOF. Default is false."
        ),
    )
    stdinOnce: Optional[bool] = Field(
        default=None,
        description=(
            "Whether the container runtime should close the stdin channel after it has"
            " been opened by a single attach. When stdin is true the stdin stream will"
            " remain open across multiple attach sessions. If stdinOnce is set to true,"
            " stdin is opened on container start, is empty until the first client"
            " attaches to stdin, and then remains open and accepts data until the"
            " client disconnects, at which time stdin is closed and remains closed"
            " until the container is restarted. If this flag is false, a container"
            " processes that reads from stdin will never receive an EOF. Default is"
            " false"
        ),
    )
    targetContainerName: Optional[str] = Field(
        default=None,
        description=(
            "If set, the name of the container from PodSpec that this ephemeral"
            " container targets. The ephemeral container will be run in the namespaces"
            " (IPC, PID, etc) of this container. If not set then the ephemeral"
            " container uses the namespaces configured in the Pod spec.\n\nThe"
            " container runtime must implement support for this feature. If the runtime"
            " does not support namespace targeting then the result of setting this"
            " field is undefined."
        ),
    )
    terminationMessagePath: Optional[str] = Field(
        default=None,
        description=(
            "Optional: Path at which the file to which the container's termination"
            " message will be written is mounted into the container's filesystem."
            " Message written is intended to be brief final status, such as an"
            " assertion failure message. Will be truncated by the node if greater than"
            " 4096 bytes. The total message length across all containers will be"
            " limited to 12kb. Defaults to /dev/termination-log. Cannot be updated."
        ),
    )
    terminationMessagePolicy: Optional[TerminationMessagePolicy] = Field(
        default=None,
        description=(
            "Indicate how the termination message should be populated. File will use"
            " the contents of terminationMessagePath to populate the container status"
            " message on both success and failure. FallbackToLogsOnError will use the"
            " last chunk of container log output if the termination message file is"
            " empty and the container exited with an error. The log output is limited"
            " to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot"
            ' be updated.\n\nPossible enum values:\n - `"FallbackToLogsOnError"` will'
            " read the most recent contents of the container logs for the container"
            " status message when the container exits with an error and the"
            ' terminationMessagePath has no contents.\n - `"File"` is the default'
            " behavior and will set the container status message to the contents of the"
            " container's terminationMessagePath when the container exits."
        ),
    )
    tty: Optional[bool] = Field(
        default=None,
        description=(
            "Whether this container should allocate a TTY for itself, also requires"
            " 'stdin' to be true. Default is false."
        ),
    )
    volumeDevices: Optional[List[VolumeDevice]] = Field(
        default=None,
        description=(
            "volumeDevices is the list of block devices to be used by the container."
        ),
    )
    volumeMounts: Optional[List[VolumeMount]] = Field(
        default=None,
        description=(
            "Pod volumes to mount into the container's filesystem. Subpath mounts are"
            " not allowed for ephemeral containers. Cannot be updated."
        ),
    )
    workingDir: Optional[str] = Field(
        default=None,
        description=(
            "Container's working directory. If not specified, the container runtime's"
            " default will be used, which might be configured in the container image."
            " Cannot be updated."
        ),
    )


class ProjectedVolumeSource(BaseModel):
    defaultMode: Optional[int] = Field(
        default=None,
        description=(
            "defaultMode are the mode bits used to set permissions on created files by"
            " default. Must be an octal value between 0000 and 0777 or a decimal value"
            " between 0 and 511. YAML accepts both octal and decimal values, JSON"
            " requires decimal values for mode bits. Directories within the path are"
            " not affected by this setting. This might be in conflict with other"
            " options that affect the file mode, like fsGroup, and the result can be"
            " other mode bits set."
        ),
    )
    sources: Optional[List[VolumeProjection]] = Field(
        default=None, description="sources is the list of volume projections"
    )


class Volume(BaseModel):
    awsElasticBlockStore: Optional[AWSElasticBlockStoreVolumeSource] = Field(
        default=None,
        description=(
            "awsElasticBlockStore represents an AWS Disk resource that is attached to a"
            " kubelet's host machine and then exposed to the pod. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        ),
    )
    azureDisk: Optional[AzureDiskVolumeSource] = Field(
        default=None,
        description=(
            "azureDisk represents an Azure Data Disk mount on the host and bind mount"
            " to the pod."
        ),
    )
    azureFile: Optional[AzureFileVolumeSource] = Field(
        default=None,
        description=(
            "azureFile represents an Azure File Service mount on the host and bind"
            " mount to the pod."
        ),
    )
    cephfs: Optional[CephFSVolumeSource] = Field(
        default=None,
        description=(
            "cephFS represents a Ceph FS mount on the host that shares a pod's lifetime"
        ),
    )
    cinder: Optional[CinderVolumeSource] = Field(
        default=None,
        description=(
            "cinder represents a cinder volume attached and mounted on kubelets host"
            " machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md"
        ),
    )
    configMap: Optional[ConfigMapVolumeSource] = Field(
        default=None,
        description="configMap represents a configMap that should populate this volume",
    )
    csi: Optional[CSIVolumeSource] = Field(
        default=None,
        description=(
            "csi (Container Storage Interface) represents ephemeral storage that is"
            " handled by certain external CSI drivers (Beta feature)."
        ),
    )
    downwardAPI: Optional[DownwardAPIVolumeSource] = Field(
        default=None,
        description=(
            "downwardAPI represents downward API about the pod that should populate"
            " this volume"
        ),
    )
    emptyDir: Optional[EmptyDirVolumeSource] = Field(
        default=None,
        description=(
            "emptyDir represents a temporary directory that shares a pod's lifetime."
            " More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir"
        ),
    )
    ephemeral: Optional[EphemeralVolumeSource] = Field(
        default=None,
        description=(
            "ephemeral represents a volume that is handled by a cluster storage driver."
            " The volume's lifecycle is tied to the pod that defines it - it will be"
            " created before the pod starts, and deleted when the pod is"
            " removed.\n\nUse this if: a) the volume is only needed while the pod runs,"
            " b) features of normal volumes like restoring from snapshot or capacity\n "
            "  tracking are needed,\nc) the storage driver is specified through a"
            " storage class, and d) the storage driver supports dynamic volume"
            " provisioning through\n   a PersistentVolumeClaim (see"
            " EphemeralVolumeSource for more\n   information on the connection between"
            " this volume type\n   and PersistentVolumeClaim).\n\nUse"
            " PersistentVolumeClaim or one of the vendor-specific APIs for volumes that"
            " persist for longer than the lifecycle of an individual pod.\n\nUse CSI"
            " for light-weight local ephemeral volumes if the CSI driver is meant to be"
            " used that way - see the documentation of the driver for more"
            " information.\n\nA pod can use both types of ephemeral volumes and"
            " persistent volumes at the same time."
        ),
    )
    fc: Optional[FCVolumeSource] = Field(
        default=None,
        description=(
            "fc represents a Fibre Channel resource that is attached to a kubelet's"
            " host machine and then exposed to the pod."
        ),
    )
    flexVolume: Optional[FlexVolumeSource] = Field(
        default=None,
        description=(
            "flexVolume represents a generic volume resource that is"
            " provisioned/attached using an exec based plugin."
        ),
    )
    flocker: Optional[FlockerVolumeSource] = Field(
        default=None,
        description=(
            "flocker represents a Flocker volume attached to a kubelet's host machine."
            " This depends on the Flocker control service being running"
        ),
    )
    gcePersistentDisk: Optional[GCEPersistentDiskVolumeSource] = Field(
        default=None,
        description=(
            "gcePersistentDisk represents a GCE Disk resource that is attached to a"
            " kubelet's host machine and then exposed to the pod. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        ),
    )
    gitRepo: Optional[GitRepoVolumeSource] = Field(
        default=None,
        description=(
            "gitRepo represents a git repository at a particular revision. DEPRECATED:"
            " GitRepo is deprecated. To provision a container with a git repo, mount an"
            " EmptyDir into an InitContainer that clones the repo using git, then mount"
            " the EmptyDir into the Pod's container."
        ),
    )
    glusterfs: Optional[GlusterfsVolumeSource] = Field(
        default=None,
        description=(
            "glusterfs represents a Glusterfs mount on the host that shares a pod's"
            " lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md"
        ),
    )
    hostPath: Optional[HostPathVolumeSource] = Field(
        default=None,
        description=(
            "hostPath represents a pre-existing file or directory on the host machine"
            " that is directly exposed to the container. This is generally used for"
            " system agents or other privileged things that are allowed to see the host"
            " machine. Most containers will NOT need this. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#hostpath"
        ),
    )
    iscsi: Optional[ISCSIVolumeSource] = Field(
        default=None,
        description=(
            "iscsi represents an ISCSI Disk resource that is attached to a kubelet's"
            " host machine and then exposed to the pod. More info:"
            " https://examples.k8s.io/volumes/iscsi/README.md"
        ),
    )
    name: str = Field(
        ...,
        description=(
            "name of the volume. Must be a DNS_LABEL and unique within the pod. More"
            " info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    )
    nfs: Optional[NFSVolumeSource] = Field(
        default=None,
        description=(
            "nfs represents an NFS mount on the host that shares a pod's lifetime More"
            " info: https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        ),
    )
    persistentVolumeClaim: Optional[PersistentVolumeClaimVolumeSource] = Field(
        default=None,
        description=(
            "persistentVolumeClaimVolumeSource represents a reference to a"
            " PersistentVolumeClaim in the same namespace. More info:"
            " https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        ),
    )
    photonPersistentDisk: Optional[PhotonPersistentDiskVolumeSource] = Field(
        default=None,
        description=(
            "photonPersistentDisk represents a PhotonController persistent disk"
            " attached and mounted on kubelets host machine"
        ),
    )
    portworxVolume: Optional[PortworxVolumeSource] = Field(
        default=None,
        description=(
            "portworxVolume represents a portworx volume attached and mounted on"
            " kubelets host machine"
        ),
    )
    projected: Optional[ProjectedVolumeSource] = Field(
        default=None,
        description=(
            "projected items for all in one resources secrets, configmaps, and"
            " downward API"
        ),
    )
    quobyte: Optional[QuobyteVolumeSource] = Field(
        default=None,
        description=(
            "quobyte represents a Quobyte mount on the host that shares a pod's"
            " lifetime"
        ),
    )
    rbd: Optional[RBDVolumeSource] = Field(
        default=None,
        description=(
            "rbd represents a Rados Block Device mount on the host that shares a pod's"
            " lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md"
        ),
    )
    scaleIO: Optional[ScaleIOVolumeSource] = Field(
        default=None,
        description=(
            "scaleIO represents a ScaleIO persistent volume attached and mounted on"
            " Kubernetes nodes."
        ),
    )
    secret: Optional[SecretVolumeSource] = Field(
        default=None,
        description=(
            "secret represents a secret that should populate this volume. More info:"
            " https://kubernetes.io/docs/concepts/storage/volumes#secret"
        ),
    )
    storageos: Optional[StorageOSVolumeSource] = Field(
        default=None,
        description=(
            "storageOS represents a StorageOS volume attached and mounted on Kubernetes"
            " nodes."
        ),
    )
    vsphereVolume: Optional[VsphereVirtualDiskVolumeSource] = Field(
        default=None,
        description=(
            "vsphereVolume represents a vSphere volume attached and mounted on kubelets"
            " host machine"
        ),
    )


class PodSpec(BaseModel):
    activeDeadlineSeconds: Optional[int] = Field(
        default=None,
        description=(
            "Optional duration in seconds the pod may be active on the node relative to"
            " StartTime before the system will actively try to mark it failed and kill"
            " associated containers. Value must be a positive integer."
        ),
    )
    affinity: Optional[Affinity] = Field(
        default=None, description="If specified, the pod's scheduling constraints"
    )
    automountServiceAccountToken: Optional[bool] = Field(
        default=None,
        description=(
            "AutomountServiceAccountToken indicates whether a service account token"
            " should be automatically mounted."
        ),
    )
    containers: List[Container] = Field(
        ...,
        description=(
            "List of containers belonging to the pod. Containers cannot currently be"
            " added or removed. There must be at least one container in a Pod. Cannot"
            " be updated."
        ),
    )
    dnsConfig: Optional[PodDNSConfig] = Field(
        default=None,
        description=(
            "Specifies the DNS parameters of a pod. Parameters specified here will be"
            " merged to the generated DNS configuration based on DNSPolicy."
        ),
    )
    dnsPolicy: Optional[DnsPolicy] = Field(
        default=None,
        description=(
            'Set DNS policy for the pod. Defaults to "ClusterFirst". Valid values are'
            " 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS"
            " parameters given in DNSConfig will be merged with the policy selected"
            " with DNSPolicy. To have DNS options set along with hostNetwork, you have"
            " to specify DNS policy explicitly to"
            " 'ClusterFirstWithHostNet'.\n\nPossible enum values:\n -"
            ' `"ClusterFirst"` indicates that the pod should use cluster DNS first'
            " unless hostNetwork is true, if it is available, then fall back on the"
            " default (as determined by kubelet) DNS settings.\n -"
            ' `"ClusterFirstWithHostNet"` indicates that the pod should use cluster'
            " DNS first, if it is available, then fall back on the default (as"
            ' determined by kubelet) DNS settings.\n - `"Default"` indicates that the'
            " pod should use the default (as determined by kubelet) DNS settings.\n -"
            ' `"None"` indicates that the pod should use empty DNS settings. DNS'
            " parameters such as nameservers and search paths should be defined via"
            " DNSConfig."
        ),
    )
    enableServiceLinks: Optional[bool] = Field(
        default=None,
        description=(
            "EnableServiceLinks indicates whether information about services should be"
            " injected into pod's environment variables, matching the syntax of Docker"
            " links. Optional: Defaults to true."
        ),
    )
    ephemeralContainers: Optional[List[EphemeralContainer]] = Field(
        default=None,
        description=(
            "List of ephemeral containers run in this pod. Ephemeral containers may be"
            " run in an existing pod to perform user-initiated actions such as"
            " debugging. This list cannot be specified when creating a pod, and it"
            " cannot be modified by updating the pod spec. In order to add an ephemeral"
            " container to an existing pod, use the pod's ephemeralcontainers"
            " subresource."
        ),
    )
    hostAliases: Optional[List[HostAlias]] = Field(
        default=None,
        description=(
            "HostAliases is an optional list of hosts and IPs that will be injected"
            " into the pod's hosts file if specified. This is only valid for"
            " non-hostNetwork pods."
        ),
    )
    hostIPC: Optional[bool] = Field(
        default=None,
        description="Use the host's ipc namespace. Optional: Default to false.",
    )
    hostNetwork: Optional[bool] = Field(
        default=None,
        description=(
            "Host networking requested for this pod. Use the host's network namespace."
            " If this option is set, the ports that will be used must be specified."
            " Default to false."
        ),
    )
    hostPID: Optional[bool] = Field(
        default=None,
        description="Use the host's pid namespace. Optional: Default to false.",
    )
    hostUsers: Optional[bool] = Field(
        default=None,
        description=(
            "Use the host's user namespace. Optional: Default to true. If set to true"
            " or not present, the pod will be run in the host user namespace, useful"
            " for when the pod needs a feature only available to the host user"
            " namespace, such as loading a kernel module with CAP_SYS_MODULE. When set"
            " to false, a new userns is created for the pod. Setting false is useful"
            " for mitigating container breakout vulnerabilities even allowing users to"
            " run their containers as root without actually having root privileges on"
            " the host. This field is alpha-level and is only honored by servers that"
            " enable the UserNamespacesSupport feature."
        ),
    )
    hostname: Optional[str] = Field(
        default=None,
        description=(
            "Specifies the hostname of the Pod If not specified, the pod's hostname"
            " will be set to a system-defined value."
        ),
    )
    imagePullSecrets: Optional[List[LocalObjectReference]] = Field(
        default=None,
        description=(
            "ImagePullSecrets is an optional list of references to secrets in the same"
            " namespace to use for pulling any of the images used by this PodSpec. If"
            " specified, these secrets will be passed to individual puller"
            " implementations for them to use. More info:"
            " https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod"
        ),
    )
    initContainers: Optional[List[Container]] = Field(
        default=None,
        description=(
            "List of initialization containers belonging to the pod. Init containers"
            " are executed in order prior to containers being started. If any init"
            " container fails, the pod is considered to have failed and is handled"
            " according to its restartPolicy. The name for an init container or normal"
            " container must be unique among all containers. Init containers may not"
            " have Lifecycle actions, Readiness probes, Liveness probes, or Startup"
            " probes. The resourceRequirements of an init container are taken into"
            " account during scheduling by finding the highest request/limit for each"
            " resource type, and then using the max of of that value or the sum of the"
            " normal containers. Limits are applied to init containers in a similar"
            " fashion. Init containers cannot currently be added or removed. Cannot be"
            " updated. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/init-containers/"
        ),
    )
    nodeName: Optional[str] = Field(
        default=None,
        description=(
            "NodeName is a request to schedule this pod onto a specific node. If it is"
            " non-empty, the scheduler simply schedules this pod onto that node,"
            " assuming that it fits resource requirements."
        ),
    )
    nodeSelector: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "NodeSelector is a selector which must be true for the pod to fit on a"
            " node. Selector which must match a node's labels for the pod to be"
            " scheduled on that node. More info:"
            " https://kubernetes.io/docs/concepts/configuration/assign-pod-node/"
        ),
    )
    os: Optional[PodOS] = Field(
        default=None,
        description=(
            "Specifies the OS of the containers in the pod. Some pod and container"
            " fields are restricted if this is set.\n\nIf the OS field is set to linux,"
            " the following fields must be unset: -securityContext.windowsOptions\n\nIf"
            " the OS field is set to windows, following fields must be unset: -"
            " spec.hostPID - spec.hostIPC - spec.hostUsers -"
            " spec.securityContext.seLinuxOptions - spec.securityContext.seccompProfile"
            " - spec.securityContext.fsGroup - spec.securityContext.fsGroupChangePolicy"
            " - spec.securityContext.sysctls - spec.shareProcessNamespace -"
            " spec.securityContext.runAsUser - spec.securityContext.runAsGroup -"
            " spec.securityContext.supplementalGroups -"
            " spec.containers[*].securityContext.seLinuxOptions -"
            " spec.containers[*].securityContext.seccompProfile -"
            " spec.containers[*].securityContext.capabilities -"
            " spec.containers[*].securityContext.readOnlyRootFilesystem -"
            " spec.containers[*].securityContext.privileged -"
            " spec.containers[*].securityContext.allowPrivilegeEscalation -"
            " spec.containers[*].securityContext.procMount -"
            " spec.containers[*].securityContext.runAsUser -"
            " spec.containers[*].securityContext.runAsGroup"
        ),
    )
    overhead: Optional[Dict[str, Union[str, float]]] = Field(
        default=None,
        description=(
            "Overhead represents the resource overhead associated with running a pod"
            " for a given RuntimeClass. This field will be autopopulated at admission"
            " time by the RuntimeClass admission controller. If the RuntimeClass"
            " admission controller is enabled, overhead must not be set in Pod create"
            " requests. The RuntimeClass admission controller will reject Pod create"
            " requests which have the overhead already set. If RuntimeClass is"
            " configured and selected in the PodSpec, Overhead will be set to the value"
            " defined in the corresponding RuntimeClass, otherwise it will remain unset"
            " and treated as zero. More info:"
            " https://git.k8s.io/enhancements/keps/sig-node/688-pod-overhead/README.md"
        ),
    )
    preemptionPolicy: Optional[PreemptionPolicy] = Field(
        default=None,
        description=(
            "PreemptionPolicy is the Policy for preempting pods with lower priority."
            " One of Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if"
            ' unset.\n\nPossible enum values:\n - `"Never"` means that pod never'
            ' preempts other pods with lower priority.\n - `"PreemptLowerPriority"`'
            " means that pod can preempt other pods with lower priority."
        ),
    )
    priority: Optional[int] = Field(
        default=None,
        description=(
            "The priority value. Various system components use this field to find the"
            " priority of the pod. When Priority Admission Controller is enabled, it"
            " prevents users from setting this field. The admission controller"
            " populates this field from PriorityClassName. The higher the value, the"
            " higher the priority."
        ),
    )
    priorityClassName: Optional[str] = Field(
        default=None,
        description=(
            'If specified, indicates the pod\'s priority. "system-node-critical" and'
            ' "system-cluster-critical" are two special keywords which indicate the'
            " highest priorities with the former being the highest priority. Any other"
            " name must be defined by creating a PriorityClass object with that name."
            " If not specified, the pod priority will be default or zero if there is no"
            " default."
        ),
    )
    readinessGates: Optional[List[PodReadinessGate]] = Field(
        default=None,
        description=(
            "If specified, all readiness gates will be evaluated for pod readiness. A"
            " pod is ready when all its containers are ready AND all conditions"
            ' specified in the readiness gates have status equal to "True" More info:'
            " https://git.k8s.io/enhancements/keps/sig-network/580-pod-readiness-gates"
        ),
    )
    resourceClaims: Optional[List[PodResourceClaim]] = Field(
        default=None,
        description=(
            "ResourceClaims defines which ResourceClaims must be allocated and reserved"
            " before the Pod is allowed to start. The resources will be made available"
            " to those containers which consume them by name.\n\nThis is an alpha field"
            " and requires enabling the DynamicResourceAllocation feature gate.\n\nThis"
            " field is immutable."
        ),
    )
    restartPolicy: Optional[RestartPolicy] = Field(
        default=None,
        description=(
            "Restart policy for all containers within the pod. One of Always,"
            " OnFailure, Never. In some contexts, only a subset of those values may be"
            " permitted. Default to Always. More info:"
            " https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy\n\nPossible"
            ' enum values:\n - `"Always"`\n - `"Never"`\n - `"OnFailure"`'
        ),
    )
    runtimeClassName: Optional[str] = Field(
        default=None,
        description=(
            "RuntimeClassName refers to a RuntimeClass object in the node.k8s.io group,"
            " which should be used to run this pod.  If no RuntimeClass resource"
            " matches the named class, the pod will not be run. If unset or empty, the"
            ' "legacy" RuntimeClass will be used, which is an implicit class with an'
            " empty definition that uses the default runtime handler. More info:"
            " https://git.k8s.io/enhancements/keps/sig-node/585-runtime-class"
        ),
    )
    schedulerName: Optional[str] = Field(
        default=None,
        description=(
            "If specified, the pod will be dispatched by specified scheduler. If not"
            " specified, the pod will be dispatched by default scheduler."
        ),
    )
    schedulingGates: Optional[List[PodSchedulingGate]] = Field(
        default=None,
        description=(
            "SchedulingGates is an opaque list of values that if specified will block"
            " scheduling the pod. If schedulingGates is not empty, the pod will stay in"
            " the SchedulingGated state and the scheduler will not attempt to schedule"
            " the pod.\n\nSchedulingGates can only be set at pod creation time, and be"
            " removed only afterwards.\n\nThis is a beta feature enabled by the"
            " PodSchedulingReadiness feature gate."
        ),
    )
    securityContext: Optional[PodSecurityContext] = Field(
        default=None,
        description=(
            "SecurityContext holds pod-level security attributes and common container"
            " settings. Optional: Defaults to empty.  See type description for default"
            " values of each field."
        ),
    )
    serviceAccount: Optional[str] = Field(
        default=None,
        description=(
            "DeprecatedServiceAccount is a depreciated alias for ServiceAccountName."
            " Deprecated: Use serviceAccountName instead."
        ),
    )
    serviceAccountName: Optional[str] = Field(
        default=None,
        description=(
            "ServiceAccountName is the name of the ServiceAccount to use to run this"
            " pod. More info:"
            " https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/"
        ),
    )
    setHostnameAsFQDN: Optional[bool] = Field(
        default=None,
        description=(
            "If true the pod's hostname will be configured as the pod's FQDN, rather"
            " than the leaf name (the default). In Linux containers, this means setting"
            " the FQDN in the hostname field of the kernel (the nodename field of"
            " struct utsname). In Windows containers, this means setting the registry"
            " value of hostname for the registry key"
            " HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters"
            " to FQDN. If a pod does not have FQDN, this has no effect. Default to"
            " false."
        ),
    )
    shareProcessNamespace: Optional[bool] = Field(
        default=None,
        description=(
            "Share a single process namespace between all of the containers in a pod."
            " When this is set containers will be able to view and signal processes"
            " from other containers in the same pod, and the first process in each"
            " container will not be assigned PID 1. HostPID and ShareProcessNamespace"
            " cannot both be set. Optional: Default to false."
        ),
    )
    subdomain: Optional[str] = Field(
        default=None,
        description=(
            "If specified, the fully qualified Pod hostname will be"
            ' "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not'
            " specified, the pod will not have a domainname at all."
        ),
    )
    terminationGracePeriodSeconds: Optional[int] = Field(
        default=None,
        description=(
            "Optional duration in seconds the pod needs to terminate gracefully. May be"
            " decreased in delete request. Value must be non-negative integer. The"
            " value zero indicates stop immediately via the kill signal (no opportunity"
            " to shut down). If this value is nil, the default grace period will be"
            " used instead. The grace period is the duration in seconds after the"
            " processes running in the pod are sent a termination signal and the time"
            " when the processes are forcibly halted with a kill signal. Set this value"
            " longer than the expected cleanup time for your process. Defaults to 30"
            " seconds."
        ),
    )
    tolerations: Optional[List[Toleration]] = Field(
        default=None, description="If specified, the pod's tolerations."
    )
    topologySpreadConstraints: Optional[List[TopologySpreadConstraint]] = Field(
        default=None,
        description=(
            "TopologySpreadConstraints describes how a group of pods ought to spread"
            " across topology domains. Scheduler will schedule pods in a way which"
            " abides by the constraints. All topologySpreadConstraints are ANDed."
        ),
    )
    volumes: Optional[List[Volume]] = Field(
        default=None,
        description=(
            "List of volumes that can be mounted by containers belonging to the pod."
            " More info: https://kubernetes.io/docs/concepts/storage/volumes"
        ),
    )


class PodTemplateSpec(BaseModel):
    metadata: Optional[v1.ObjectMeta] = Field(
        default=None,
        description=(
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[PodSpec] = Field(
        default=None,
        description=(
            "Specification of the desired behavior of the pod. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )
