Kubedantic
======================================================

.. image:: https://img.shields.io/pypi/v/kubedantic.svg
   :target: https://pypi.org/project/kubedantic

.. image:: https://img.shields.io/pypi/pyversions/kubedantic.svg

.. image:: https://github.com/coherent-oss/kubedantic/actions/workflows/main.yml/badge.svg
   :target: https://github.com/coherent-oss/kubedantic/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. .. image:: https://readthedocs.org/projects/kubedantic/badge/?version=latest
..    :target: https://kubedantic.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2024-informational
   :target: https://blog.jaraco.com/skeleton


Generate Pydantic models from Kubernetes OpenAPI specifications.

Overview
--------

Kubedantic provides a way to automatically generate Pydantic models using your Kubernetes cluster OpenAPI specifications and `datamodel-code-generator <https://github.com/koxudaxi/datamodel-code-generator>`_.

Usage
-----

1. Make sure you have a Kubernetes cluster running and `kubectl` is configured to access it.
2. Run `kubedantic` to generate the models.

.. code-block:: bash

   $ kubedantic --output-path <destination>

How it works
------------

Kubedantic does the following:

1. Uses the `kubernetes <https://github.com/kubernetes-client/python>`_ library to fetch the openapi specifications from the cluster.
2. Merges the specifications extracted from the openapi specifications into a single schema file (one for the native types and one for the custom resources).
3. Uses `datamodel-code-generator <https://github.com/koxudaxi/datamodel-code-generator>`_ to generate the Pydantic models from each schema file.

Schema files will be cached locally in the `kubedantic_specs/` directory, e.g.:

.. code-block:: bash

   kubedantic_specs/
   ├── k8s.json  # Kubernetes native types
   └── crd.json  # Custom resource definitions

You can control the cache location by using the `--specs-path` option.
