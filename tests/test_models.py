from kubedantic.models.io.k8s.api.apps.v1 import Deployment, DeploymentSpec
from kubedantic.models.io.k8s.api.core.v1 import PodTemplateSpec
from kubedantic.models.io.k8s.apimachinery.pkg.apis.meta.v1 import (
    LabelSelector,
    ObjectMeta,
)


def test_deployment():
    deployment = Deployment(
        metadata=ObjectMeta(name="test"),
        spec=DeploymentSpec(
            replicas=1,
            selector=LabelSelector(matchLabels={"app": "test"}),
            template=PodTemplateSpec(
                metadata=ObjectMeta(labels={"app": "test"}),
            ),
        ),
    )

    assert deployment.apiVersion == "apps/v1"
    assert deployment.kind == "Deployment"
    assert deployment.metadata is not None
    assert deployment.metadata.name == "test"
    assert deployment.spec is not None
    assert deployment.spec.replicas == 1
    assert deployment.spec.selector.matchLabels == {"app": "test"}
    assert deployment.spec.template.metadata is not None
    assert deployment.spec.template.metadata.labels == {"app": "test"}
