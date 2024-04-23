from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from ...apimachinery.pkg import runtime
from ...apimachinery.pkg.apis.meta import v1
from ..core import v1 as v1_1


class Type(Enum):
    OnDelete = "OnDelete"
    RollingUpdate = "RollingUpdate"


class TypeModel(Enum):
    Recreate = "Recreate"
    RollingUpdate = "RollingUpdate"


class StatefulSetOrdinals(BaseModel):
    start: Optional[int] = Field(
        default=0,
        description=(
            "start is the number representing the first replica's index. It may be used"
            " to number replicas from an alternate index (eg: 1-indexed) over the"
            " default 0-indexed names, or to orchestrate progressive movement of"
            " replicas from one StatefulSet to another. If set, replica indices will be"
            " in the range:\n  [.spec.ordinals.start, .spec.ordinals.start +"
            " .spec.replicas).\nIf unset, defaults to 0. Replica indices will be in the"
            " range:\n  [0, .spec.replicas)."
        ),
    )


class StatefulSetPersistentVolumeClaimRetentionPolicy(BaseModel):
    whenDeleted: Optional[str] = Field(
        default=None,
        description=(
            "WhenDeleted specifies what happens to PVCs created from StatefulSet"
            " VolumeClaimTemplates when the StatefulSet is deleted. The default policy"
            " of `Retain` causes PVCs to not be affected by StatefulSet deletion. The"
            " `Delete` policy causes those PVCs to be deleted."
        ),
    )
    whenScaled: Optional[str] = Field(
        default=None,
        description=(
            "WhenScaled specifies what happens to PVCs created from StatefulSet"
            " VolumeClaimTemplates when the StatefulSet is scaled down. The default"
            " policy of `Retain` causes PVCs to not be affected by a scaledown. The"
            " `Delete` policy causes the associated PVCs for any excess pods above the"
            " replica count to be deleted."
        ),
    )


class PodManagementPolicy(Enum):
    OrderedReady = "OrderedReady"
    Parallel = "Parallel"


class TypeModel1(Enum):
    OnDelete = "OnDelete"
    RollingUpdate = "RollingUpdate"


class DaemonSetCondition(BaseModel):
    lastTransitionTime: Optional[datetime] = Field(
        default=None,
        description="Last time the condition transitioned from one status to another.",
    )
    message: Optional[str] = Field(
        default=None,
        description="A human readable message indicating details about the transition.",
    )
    reason: Optional[str] = Field(
        default=None, description="The reason for the condition's last transition."
    )
    status: str = Field(
        ..., description="Status of the condition, one of True, False, Unknown."
    )
    type: str = Field(..., description="Type of DaemonSet condition.")


class DaemonSetStatus(BaseModel):
    collisionCount: Optional[int] = Field(
        default=None,
        description=(
            "Count of hash collisions for the DaemonSet. The DaemonSet controller uses"
            " this field as a collision avoidance mechanism when it needs to create the"
            " name for the newest ControllerRevision."
        ),
    )
    conditions: Optional[List[DaemonSetCondition]] = Field(
        default=None,
        description=(
            "Represents the latest available observations of a DaemonSet's current"
            " state."
        ),
    )
    currentNumberScheduled: int = Field(
        ...,
        description=(
            "The number of nodes that are running at least 1 daemon pod and are"
            " supposed to run the daemon pod. More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        ),
    )
    desiredNumberScheduled: int = Field(
        ...,
        description=(
            "The total number of nodes that should be running the daemon pod (including"
            " nodes correctly running the daemon pod). More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        ),
    )
    numberAvailable: Optional[int] = Field(
        default=None,
        description=(
            "The number of nodes that should be running the daemon pod and have one or"
            " more of the daemon pod running and available (ready for at least"
            " spec.minReadySeconds)"
        ),
    )
    numberMisscheduled: int = Field(
        ...,
        description=(
            "The number of nodes that are running the daemon pod, but are not supposed"
            " to run the daemon pod. More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        ),
    )
    numberReady: int = Field(
        ...,
        description=(
            "numberReady is the number of nodes that should be running the daemon pod"
            " and have one or more of the daemon pod running with a Ready Condition."
        ),
    )
    numberUnavailable: Optional[int] = Field(
        default=None,
        description=(
            "The number of nodes that should be running the daemon pod and have none of"
            " the daemon pod running and available (ready for at least"
            " spec.minReadySeconds)"
        ),
    )
    observedGeneration: Optional[int] = Field(
        default=None,
        description="The most recent generation observed by the daemon set controller.",
    )
    updatedNumberScheduled: Optional[int] = Field(
        default=None,
        description="The total number of nodes that are running updated daemon pod",
    )


class DeploymentCondition(BaseModel):
    lastTransitionTime: Optional[datetime] = Field(
        default=None,
        description="Last time the condition transitioned from one status to another.",
    )
    lastUpdateTime: Optional[datetime] = Field(
        default=None, description="The last time this condition was updated."
    )
    message: Optional[str] = Field(
        default=None,
        description="A human readable message indicating details about the transition.",
    )
    reason: Optional[str] = Field(
        default=None, description="The reason for the condition's last transition."
    )
    status: str = Field(
        ..., description="Status of the condition, one of True, False, Unknown."
    )
    type: str = Field(..., description="Type of deployment condition.")


class DeploymentStatus(BaseModel):
    availableReplicas: Optional[int] = Field(
        default=None,
        description=(
            "Total number of available pods (ready for at least minReadySeconds)"
            " targeted by this deployment."
        ),
    )
    collisionCount: Optional[int] = Field(
        default=None,
        description=(
            "Count of hash collisions for the Deployment. The Deployment controller"
            " uses this field as a collision avoidance mechanism when it needs to"
            " create the name for the newest ReplicaSet."
        ),
    )
    conditions: Optional[List[DeploymentCondition]] = Field(
        default=None,
        description=(
            "Represents the latest available observations of a deployment's current"
            " state."
        ),
    )
    observedGeneration: Optional[int] = Field(
        default=None,
        description="The generation observed by the deployment controller.",
    )
    readyReplicas: Optional[int] = Field(
        default=None,
        description=(
            "readyReplicas is the number of pods targeted by this Deployment with a"
            " Ready Condition."
        ),
    )
    replicas: Optional[int] = Field(
        default=None,
        description=(
            "Total number of non-terminated pods targeted by this deployment (their"
            " labels match the selector)."
        ),
    )
    unavailableReplicas: Optional[int] = Field(
        default=None,
        description=(
            "Total number of unavailable pods targeted by this deployment. This is the"
            " total number of pods that are still required for the deployment to have"
            " 100% available capacity. They may either be pods that are running but not"
            " yet available or pods that still have not been created."
        ),
    )
    updatedReplicas: Optional[int] = Field(
        default=None,
        description=(
            "Total number of non-terminated pods targeted by this deployment that have"
            " the desired template spec."
        ),
    )


class ReplicaSetCondition(BaseModel):
    lastTransitionTime: Optional[datetime] = Field(
        default=None,
        description=(
            "The last time the condition transitioned from one status to another."
        ),
    )
    message: Optional[str] = Field(
        default=None,
        description="A human readable message indicating details about the transition.",
    )
    reason: Optional[str] = Field(
        default=None, description="The reason for the condition's last transition."
    )
    status: str = Field(
        ..., description="Status of the condition, one of True, False, Unknown."
    )
    type: str = Field(..., description="Type of replica set condition.")


class ReplicaSetStatus(BaseModel):
    availableReplicas: Optional[int] = Field(
        default=None,
        description=(
            "The number of available replicas (ready for at least minReadySeconds) for"
            " this replica set."
        ),
    )
    conditions: Optional[List[ReplicaSetCondition]] = Field(
        default=None,
        description=(
            "Represents the latest available observations of a replica set's current"
            " state."
        ),
    )
    fullyLabeledReplicas: Optional[int] = Field(
        default=None,
        description=(
            "The number of pods that have labels matching the labels of the pod"
            " template of the replicaset."
        ),
    )
    observedGeneration: Optional[int] = Field(
        default=None,
        description=(
            "ObservedGeneration reflects the generation of the most recently observed"
            " ReplicaSet."
        ),
    )
    readyReplicas: Optional[int] = Field(
        default=None,
        description=(
            "readyReplicas is the number of pods targeted by this ReplicaSet with a"
            " Ready Condition."
        ),
    )
    replicas: int = Field(
        ...,
        description=(
            "Replicas is the most recently observed number of replicas. More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller"
        ),
    )


class RollingUpdateDaemonSet(BaseModel):
    maxSurge: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The maximum number of nodes with an existing available DaemonSet pod that"
            " can have an updated DaemonSet pod during during an update. Value can be"
            " an absolute number (ex: 5) or a percentage of desired pods (ex: 10%)."
            " This can not be 0 if MaxUnavailable is 0. Absolute number is calculated"
            " from percentage by rounding up to a minimum of 1. Default value is 0."
            " Example: when this is set to 30%, at most 30% of the total number of"
            " nodes that should be running the daemon pod (i.e."
            " status.desiredNumberScheduled) can have their a new pod created before"
            " the old pod is marked as deleted. The update starts by launching new pods"
            " on 30% of nodes. Once an updated pod is available (Ready for at least"
            " minReadySeconds) the old DaemonSet pod on that node is marked deleted. If"
            " the old pod becomes unavailable for any reason (Ready transitions to"
            " false, is evicted, or is drained) an updated pod is immediatedly created"
            " on that node without considering surge limits. Allowing surge implies the"
            " possibility that the resources consumed by the daemonset on any given"
            " node can double if the readiness check fails, and so resource intensive"
            " daemonsets should take into account that they may cause evictions during"
            " disruption."
        ),
    )
    maxUnavailable: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The maximum number of DaemonSet pods that can be unavailable during the"
            " update. Value can be an absolute number (ex: 5) or a percentage of total"
            " number of DaemonSet pods at the start of the update (ex: 10%). Absolute"
            " number is calculated from percentage by rounding up. This cannot be 0 if"
            " MaxSurge is 0 Default value is 1. Example: when this is set to 30%, at"
            " most 30% of the total number of nodes that should be running the daemon"
            " pod (i.e. status.desiredNumberScheduled) can have their pods stopped for"
            " an update at any given time. The update starts by stopping at most 30% of"
            " those DaemonSet pods and then brings up new DaemonSet pods in their"
            " place. Once the new pods are available, it then proceeds onto other"
            " DaemonSet pods, thus ensuring that at least 70% of original number of"
            " DaemonSet pods are available at all times during the update."
        ),
    )


class RollingUpdateDeployment(BaseModel):
    maxSurge: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The maximum number of pods that can be scheduled above the desired number"
            " of pods. Value can be an absolute number (ex: 5) or a percentage of"
            " desired pods (ex: 10%). This can not be 0 if MaxUnavailable is 0."
            " Absolute number is calculated from percentage by rounding up. Defaults to"
            " 25%. Example: when this is set to 30%, the new ReplicaSet can be scaled"
            " up immediately when the rolling update starts, such that the total number"
            " of old and new pods do not exceed 130% of desired pods. Once old pods"
            " have been killed, new ReplicaSet can be scaled up further, ensuring that"
            " total number of pods running at any time during the update is at most"
            " 130% of desired pods."
        ),
    )
    maxUnavailable: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The maximum number of pods that can be unavailable during the update."
            " Value can be an absolute number (ex: 5) or a percentage of desired pods"
            " (ex: 10%). Absolute number is calculated from percentage by rounding"
            " down. This can not be 0 if MaxSurge is 0. Defaults to 25%. Example: when"
            " this is set to 30%, the old ReplicaSet can be scaled down to 70% of"
            " desired pods immediately when the rolling update starts. Once new pods"
            " are ready, old ReplicaSet can be scaled down further, followed by scaling"
            " up the new ReplicaSet, ensuring that the total number of pods available"
            " at all times during the update is at least 70% of desired pods."
        ),
    )


class RollingUpdateStatefulSetStrategy(BaseModel):
    maxUnavailable: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The maximum number of pods that can be unavailable during the update."
            " Value can be an absolute number (ex: 5) or a percentage of desired pods"
            " (ex: 10%). Absolute number is calculated from percentage by rounding up."
            " This can not be 0. Defaults to 1. This field is alpha-level and is only"
            " honored by servers that enable the MaxUnavailableStatefulSet feature. The"
            " field applies to all pods in the range 0 to Replicas-1. That means if"
            " there is any unavailable pod in the range 0 to Replicas-1, it will be"
            " counted towards MaxUnavailable."
        ),
    )
    partition: Optional[int] = Field(
        default=None,
        description=(
            "Partition indicates the ordinal at which the StatefulSet should be"
            " partitioned for updates. During a rolling update, all pods from ordinal"
            " Replicas-1 to Partition are updated. All pods from ordinal Partition-1 to"
            " 0 remain untouched. This is helpful in being able to do a canary based"
            " deployment. The default value is 0."
        ),
    )


class StatefulSetCondition(BaseModel):
    lastTransitionTime: Optional[datetime] = Field(
        default=None,
        description="Last time the condition transitioned from one status to another.",
    )
    message: Optional[str] = Field(
        default=None,
        description="A human readable message indicating details about the transition.",
    )
    reason: Optional[str] = Field(
        default=None, description="The reason for the condition's last transition."
    )
    status: str = Field(
        ..., description="Status of the condition, one of True, False, Unknown."
    )
    type: str = Field(..., description="Type of statefulset condition.")


class StatefulSetStatus(BaseModel):
    availableReplicas: Optional[int] = Field(
        default=0,
        description=(
            "Total number of available pods (ready for at least minReadySeconds)"
            " targeted by this statefulset."
        ),
    )
    collisionCount: Optional[int] = Field(
        default=None,
        description=(
            "collisionCount is the count of hash collisions for the StatefulSet. The"
            " StatefulSet controller uses this field as a collision avoidance mechanism"
            " when it needs to create the name for the newest ControllerRevision."
        ),
    )
    conditions: Optional[List[StatefulSetCondition]] = Field(
        default=None,
        description=(
            "Represents the latest available observations of a statefulset's current"
            " state."
        ),
    )
    currentReplicas: Optional[int] = Field(
        default=None,
        description=(
            "currentReplicas is the number of Pods created by the StatefulSet"
            " controller from the StatefulSet version indicated by currentRevision."
        ),
    )
    currentRevision: Optional[str] = Field(
        default=None,
        description=(
            "currentRevision, if not empty, indicates the version of the StatefulSet"
            " used to generate Pods in the sequence [0,currentReplicas)."
        ),
    )
    observedGeneration: Optional[int] = Field(
        default=None,
        description=(
            "observedGeneration is the most recent generation observed for this"
            " StatefulSet. It corresponds to the StatefulSet's generation, which is"
            " updated on mutation by the API Server."
        ),
    )
    readyReplicas: Optional[int] = Field(
        default=None,
        description=(
            "readyReplicas is the number of pods created for this StatefulSet with a"
            " Ready Condition."
        ),
    )
    replicas: int = Field(
        ...,
        description=(
            "replicas is the number of Pods created by the StatefulSet controller."
        ),
    )
    updateRevision: Optional[str] = Field(
        default=None,
        description=(
            "updateRevision, if not empty, indicates the version of the StatefulSet"
            " used to generate Pods in the sequence [replicas-updatedReplicas,replicas)"
        ),
    )
    updatedReplicas: Optional[int] = Field(
        default=None,
        description=(
            "updatedReplicas is the number of Pods created by the StatefulSet"
            " controller from the StatefulSet version indicated by updateRevision."
        ),
    )


class StatefulSetUpdateStrategy(BaseModel):
    rollingUpdate: Optional[RollingUpdateStatefulSetStrategy] = Field(
        default=None,
        description=(
            "RollingUpdate is used to communicate parameters when Type is"
            " RollingUpdateStatefulSetStrategyType."
        ),
    )
    type: Optional[TypeModel1] = Field(
        default=None,
        description=(
            "Type indicates the type of the StatefulSetUpdateStrategy. Default is"
            ' RollingUpdate.\n\nPossible enum values:\n - `"OnDelete"` triggers the'
            " legacy behavior. Version tracking and ordered rolling restarts are"
            " disabled. Pods are recreated from the StatefulSetSpec when they are"
            " manually deleted. When a scale operation is performed with this"
            " strategy,specification version indicated by the StatefulSet's"
            ' currentRevision.\n - `"RollingUpdate"` indicates that update will be'
            " applied to all Pods in the StatefulSet with respect to the StatefulSet"
            " ordering constraints. When a scale operation is performed with this"
            " strategy, new Pods will be created from the specification version"
            " indicated by the StatefulSet's updateRevision."
        ),
    )


class ControllerRevision(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    data: Optional[runtime.RawExtension] = Field(
        default=None, description="Data is the serialized representation of the state."
    )
    kind: Optional[str] = Field(
        default="ControllerRevision",
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
    revision: int = Field(
        ...,
        description="Revision indicates the revision of the state represented by Data.",
    )


class ControllerRevisionList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[ControllerRevision] = Field(
        ..., description="Items is the list of ControllerRevisions"
    )
    kind: Optional[str] = Field(
        default="ControllerRevisionList",
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
            "More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )


class DaemonSetUpdateStrategy(BaseModel):
    rollingUpdate: Optional[RollingUpdateDaemonSet] = Field(
        default=None,
        description=(
            'Rolling update config params. Present only if type = "RollingUpdate".'
        ),
    )
    type: Optional[Type] = Field(
        default=None,
        description=(
            'Type of daemon set update. Can be "RollingUpdate" or "OnDelete". Default'
            ' is RollingUpdate.\n\nPossible enum values:\n - `"OnDelete"` Replace the'
            ' old daemons only when it\'s killed\n - `"RollingUpdate"` Replace the old'
            " daemons by new ones using rolling update i.e replace them on each node"
            " one after the other."
        ),
    )


class DeploymentStrategy(BaseModel):
    rollingUpdate: Optional[RollingUpdateDeployment] = Field(
        default=None,
        description=(
            "Rolling update config params. Present only if DeploymentStrategyType ="
            " RollingUpdate."
        ),
    )
    type: Optional[TypeModel] = Field(
        default=None,
        description=(
            'Type of deployment. Can be "Recreate" or "RollingUpdate". Default is'
            ' RollingUpdate.\n\nPossible enum values:\n - `"Recreate"` Kill all'
            ' existing pods before creating new ones.\n - `"RollingUpdate"` Replace the'
            " old ReplicaSets by new one using rolling update i.e gradually scale down"
            " the old ReplicaSets and scale up the new one."
        ),
    )


class DaemonSetSpec(BaseModel):
    minReadySeconds: Optional[int] = Field(
        default=None,
        description=(
            "The minimum number of seconds for which a newly created DaemonSet pod"
            " should be ready without any of its container crashing, for it to be"
            " considered available. Defaults to 0 (pod will be considered available as"
            " soon as it is ready)."
        ),
    )
    revisionHistoryLimit: Optional[int] = Field(
        default=None,
        description=(
            "The number of old history to retain to allow rollback. This is a pointer"
            " to distinguish between explicit zero and not specified. Defaults to 10."
        ),
    )
    selector: v1.LabelSelector = Field(
        ...,
        description=(
            "A label query over pods that are managed by the daemon set. Must match in"
            " order to be controlled. It must match the pod template's labels. More"
            " info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        ),
    )
    template: v1_1.PodTemplateSpec = Field(
        ...,
        description=(
            "An object that describes the pod that will be created. The DaemonSet will"
            " create exactly one copy of this pod on every node that matches the"
            " template's node selector (or on every node if no node selector is"
            " specified). The only allowed template.spec.restartPolicy value is"
            ' "Always". More info:'
            " https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template"
        ),
    )
    updateStrategy: Optional[DaemonSetUpdateStrategy] = Field(
        default=None,
        description=(
            "An update strategy to replace existing DaemonSet pods with new pods."
        ),
    )


class DeploymentSpec(BaseModel):
    minReadySeconds: Optional[int] = Field(
        default=None,
        description=(
            "Minimum number of seconds for which a newly created pod should be ready"
            " without any of its container crashing, for it to be considered available."
            " Defaults to 0 (pod will be considered available as soon as it is ready)"
        ),
    )
    paused: Optional[bool] = Field(
        default=None, description="Indicates that the deployment is paused."
    )
    progressDeadlineSeconds: Optional[int] = Field(
        default=None,
        description=(
            "The maximum time in seconds for a deployment to make progress before it is"
            " considered to be failed. The deployment controller will continue to"
            " process failed deployments and a condition with a"
            " ProgressDeadlineExceeded reason will be surfaced in the deployment"
            " status. Note that progress will not be estimated during the time a"
            " deployment is paused. Defaults to 600s."
        ),
    )
    replicas: Optional[int] = Field(
        default=None,
        description=(
            "Number of desired pods. This is a pointer to distinguish between explicit"
            " zero and not specified. Defaults to 1."
        ),
    )
    revisionHistoryLimit: Optional[int] = Field(
        default=None,
        description=(
            "The number of old ReplicaSets to retain to allow rollback. This is a"
            " pointer to distinguish between explicit zero and not specified. Defaults"
            " to 10."
        ),
    )
    selector: v1.LabelSelector = Field(
        ...,
        description=(
            "Label selector for pods. Existing ReplicaSets whose pods are selected by"
            " this will be the ones affected by this deployment. It must match the pod"
            " template's labels."
        ),
    )
    strategy: Optional[DeploymentStrategy] = Field(
        default=None,
        description=(
            "The deployment strategy to use to replace existing pods with new ones."
        ),
    )
    template: v1_1.PodTemplateSpec = Field(
        ...,
        description=(
            "Template describes the pods that will be created. The only allowed"
            ' template.spec.restartPolicy value is "Always".'
        ),
    )


class ReplicaSetSpec(BaseModel):
    minReadySeconds: Optional[int] = Field(
        default=None,
        description=(
            "Minimum number of seconds for which a newly created pod should be ready"
            " without any of its container crashing, for it to be considered available."
            " Defaults to 0 (pod will be considered available as soon as it is ready)"
        ),
    )
    replicas: Optional[int] = Field(
        default=None,
        description=(
            "Replicas is the number of desired replicas. This is a pointer to"
            " distinguish between explicit zero and unspecified. Defaults to 1. More"
            " info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller"
        ),
    )
    selector: v1.LabelSelector = Field(
        ...,
        description=(
            "Selector is a label query over pods that should match the replica count."
            " Label keys and values that must match in order to be controlled by this"
            " replica set. It must match the pod template's labels. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        ),
    )
    template: Optional[v1_1.PodTemplateSpec] = Field(
        default=None,
        description=(
            "Template is the object that describes the pod that will be created if"
            " insufficient replicas are detected. More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template"
        ),
    )


class StatefulSetSpec(BaseModel):
    minReadySeconds: Optional[int] = Field(
        default=None,
        description=(
            "Minimum number of seconds for which a newly created pod should be ready"
            " without any of its container crashing for it to be considered available."
            " Defaults to 0 (pod will be considered available as soon as it is ready)"
        ),
    )
    ordinals: Optional[StatefulSetOrdinals] = Field(
        default=None,
        description=(
            "ordinals controls the numbering of replica indices in a StatefulSet. The"
            ' default ordinals behavior assigns a "0" index to the first replica and'
            " increments the index by one for each additional replica requested. Using"
            " the ordinals field requires the StatefulSetStartOrdinal feature gate to"
            " be enabled, which is beta."
        ),
    )
    persistentVolumeClaimRetentionPolicy: Optional[
        StatefulSetPersistentVolumeClaimRetentionPolicy
    ] = Field(
        default=None,
        description=(
            "persistentVolumeClaimRetentionPolicy describes the lifecycle of persistent"
            " volume claims created from volumeClaimTemplates. By default, all"
            " persistent volume claims are created as needed and retained until"
            " manually deleted. This policy allows the lifecycle to be altered, for"
            " example by deleting persistent volume claims when their stateful set is"
            " deleted, or when their pod is scaled down. This requires the"
            " StatefulSetAutoDeletePVC feature gate to be enabled, which is alpha. "
            " +optional"
        ),
    )
    podManagementPolicy: Optional[PodManagementPolicy] = Field(
        default=None,
        description=(
            "podManagementPolicy controls how pods are created during initial scale up,"
            " when replacing pods on nodes, or when scaling down. The default policy is"
            " `OrderedReady`, where pods are created in increasing order (pod-0, then"
            " pod-1, etc) and the controller will wait until each pod is ready before"
            " continuing. When scaling down, the pods are removed in the opposite"
            " order. The alternative policy is `Parallel` which will create pods in"
            " parallel to match the desired scale without waiting, and on scale down"
            " will delete all pods at once.\n\nPossible enum values:\n -"
            ' `"OrderedReady"` will create pods in strictly increasing order on scale'
            " up and strictly decreasing order on scale down, progressing only when the"
            " previous pod is ready or terminated. At most one pod will be changed at"
            ' any time.\n - `"Parallel"` will create and delete pods as soon as the'
            " stateful set replica count is changed, and will not wait for pods to be"
            " ready or complete termination."
        ),
    )
    replicas: Optional[int] = Field(
        default=None,
        description=(
            "replicas is the desired number of replicas of the given Template. These"
            " are replicas in the sense that they are instantiations of the same"
            " Template, but individual replicas also have a consistent identity. If"
            " unspecified, defaults to 1."
        ),
    )
    revisionHistoryLimit: Optional[int] = Field(
        default=None,
        description=(
            "revisionHistoryLimit is the maximum number of revisions that will be"
            " maintained in the StatefulSet's revision history. The revision history"
            " consists of all revisions not represented by a currently applied"
            " StatefulSetSpec version. The default value is 10."
        ),
    )
    selector: v1.LabelSelector = Field(
        ...,
        description=(
            "selector is a label query over pods that should match the replica count."
            " It must match the pod template's labels. More info:"
            " https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        ),
    )
    serviceName: str = Field(
        ...,
        description=(
            "serviceName is the name of the service that governs this StatefulSet. This"
            " service must exist before the StatefulSet, and is responsible for the"
            " network identity of the set. Pods get DNS/hostnames that follow the"
            " pattern: pod-specific-string.serviceName.default.svc.cluster.local where"
            ' "pod-specific-string" is managed by the StatefulSet controller.'
        ),
    )
    template: v1_1.PodTemplateSpec = Field(
        ...,
        description=(
            "template is the object that describes the pod that will be created if"
            " insufficient replicas are detected. Each pod stamped out by the"
            " StatefulSet will fulfill this Template, but have a unique identity from"
            " the rest of the StatefulSet. Each pod will be named with the format"
            " <statefulsetname>-<podindex>. For example, a pod in a StatefulSet named"
            ' "web" with index number "3" would be named "web-3". The only allowed'
            ' template.spec.restartPolicy value is "Always".'
        ),
    )
    updateStrategy: Optional[StatefulSetUpdateStrategy] = Field(
        default=None,
        description=(
            "updateStrategy indicates the StatefulSetUpdateStrategy that will be"
            " employed to update Pods in the StatefulSet when a revision is made to"
            " Template."
        ),
    )
    volumeClaimTemplates: Optional[List[v1_1.PersistentVolumeClaim]] = Field(
        default=None,
        description=(
            "volumeClaimTemplates is a list of claims that pods are allowed to"
            " reference. The StatefulSet controller is responsible for mapping network"
            " identities to claims in a way that maintains the identity of a pod. Every"
            " claim in this list must have at least one matching (by name) volumeMount"
            " in one container in the template. A claim in this list takes precedence"
            " over any volumes in the template, with the same name."
        ),
    )


class DaemonSet(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="DaemonSet",
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
    spec: Optional[DaemonSetSpec] = Field(
        default=None,
        description=(
            "The desired behavior of this daemon set. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )
    status: Optional[DaemonSetStatus] = Field(
        default=None,
        description=(
            "The current status of this daemon set. This data may be out of date by"
            " some window of time. Populated by the system. Read-only. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )


class DaemonSetList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[DaemonSet] = Field(..., description="A list of daemon sets.")
    kind: Optional[str] = Field(
        default="DaemonSetList",
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
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )


class Deployment(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="Deployment",
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
    spec: Optional[DeploymentSpec] = Field(
        default=None,
        description="Specification of the desired behavior of the Deployment.",
    )
    status: Optional[DeploymentStatus] = Field(
        default=None, description="Most recently observed status of the Deployment."
    )


class DeploymentList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[Deployment] = Field(
        ..., description="Items is the list of Deployments."
    )
    kind: Optional[str] = Field(
        default="DeploymentList",
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1.ListMeta] = Field(
        default=None, description="Standard list metadata."
    )


class ReplicaSet(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="ReplicaSet",
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
            "If the Labels of a ReplicaSet are empty, they are defaulted to be the same"
            " as the Pod(s) that the ReplicaSet manages. Standard object's metadata."
            " More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[ReplicaSetSpec] = Field(
        default=None,
        description=(
            "Spec defines the specification of the desired behavior of the ReplicaSet."
            " More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )
    status: Optional[ReplicaSetStatus] = Field(
        default=None,
        description=(
            "Status is the most recently observed status of the ReplicaSet. This data"
            " may be out of date by some window of time. Populated by the system."
            " Read-only. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )


class ReplicaSetList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[ReplicaSet] = Field(
        ...,
        description=(
            "List of ReplicaSets. More info:"
            " https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller"
        ),
    )
    kind: Optional[str] = Field(
        default="ReplicaSetList",
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


class StatefulSet(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        default="StatefulSet",
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
    spec: Optional[StatefulSetSpec] = Field(
        default=None,
        description="Spec defines the desired identities of pods in this set.",
    )
    status: Optional[StatefulSetStatus] = Field(
        default=None,
        description=(
            "Status is the current status of Pods in this StatefulSet. This data may be"
            " out of date by some window of time."
        ),
    )


class StatefulSetList(BaseModel):
    apiVersion: Optional[str] = Field(
        default="apps/v1",
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[StatefulSet] = Field(
        ..., description="Items is the list of stateful sets."
    )
    kind: Optional[str] = Field(
        default="StatefulSetList",
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
            "Standard list's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
