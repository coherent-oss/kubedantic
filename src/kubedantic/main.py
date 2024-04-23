import argparse
import logging
import sys
from pathlib import Path

from datamodel_code_generator.parser.base import Result

from kubedantic.extractor import K8sOpenAPIExtractor
from kubedantic.parser import K8sOpenAPIParser


def _get_options(args):
    parser = argparse.ArgumentParser(
        description="Generates Python data models from Kubernetes OpenAPI specs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--log-level",
        "-l",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    parser.add_argument(
        "--output-path",
        "-o",
        default="kubedantic_models",
        help="Output directory where the Python data models will be put at.",
    )
    parser.add_argument(
        "--specs-path",
        "-s",
        default="kubedantic_specs",
        help="Output directory where the Kubernetes OpenAPI specs will be put at.",
    )

    return parser.parse_args(args)


def _write_result(path: tuple[str, ...], result: Result, output_path: Path):
    output_file = output_path.joinpath(*path[1:]).with_suffix(".py")
    logging.info("Generating %s", output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as out_file:
        out_file.write(result.body)


def _generate_models(output_path: Path, specs_path: Path):
    extractor = K8sOpenAPIExtractor(output_path=specs_path)
    parser = K8sOpenAPIParser(source=extractor.extract())

    results: dict[tuple[str, ...], Result] = parser.parse()  # type: ignore

    for name, result in sorted(results.items()):
        _write_result(name, result, output_path)


def run(args):
    options = _get_options(args)

    log_level = logging.getLevelName(options.log_level)
    logging.basicConfig(level=log_level)

    output_path = Path(options.output_path)
    specs_path = Path(options.specs_path)

    _generate_models(output_path, specs_path)


def main():  # pragma: no cover
    run(sys.argv[1:])


if __name__ == "__main__":  # pragma: no cover
    main()
