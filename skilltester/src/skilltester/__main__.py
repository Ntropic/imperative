import argparse
import asyncio
import json
from pathlib import Path

from .loading import discover_paths, import_file, load_suite
from .runner import build_report, run


def main() -> None:
    parser = argparse.ArgumentParser(prog="skilltester")
    parser.add_argument("--skill")
    parser.add_argument("--config")
    parser.add_argument("--examples")
    args = parser.parse_args()

    try:
        paths = discover_paths(
            Path.cwd(), skill=args.skill, config=args.config, examples=args.examples
        )
    except ValueError as error:
        parser.error(str(error))
    config = import_file(paths.config)
    suite = load_suite(paths.examples)
    results = asyncio.run(
        run(
            skill=paths.skill,
            suite=suite,
            llm=config.llm,
        )
    )
    print(json.dumps(build_report(results, suite.tag_options), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
