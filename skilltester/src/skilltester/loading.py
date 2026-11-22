from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Literal, get_args, get_origin, get_type_hints, is_typeddict
from uuid import uuid4

from pydantic import TypeAdapter

from .models import Suite


IGNORED_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__"}


@dataclass(frozen=True)
class Paths:
    skill: Path
    config: Path
    examples: Path


def _files(root: Path, name: str) -> list[Path]:
    return sorted(
        path.resolve()
        for path in root.rglob(name)
        if not any(part in IGNORED_DIRECTORIES or part.startswith(".") for part in path.parts)
    )


def _existing(path: str | Path, label: str) -> Path:
    resolved = Path(path).resolve()
    if not resolved.is_file():
        raise ValueError(f"{label} file not found: {resolved}")
    return resolved


def _one(label: str, paths: list[Path]) -> Path:
    if len(paths) != 1:
        found = ", ".join(str(path) for path in paths) or "none"
        raise ValueError(f"expected one {label}, found {len(paths)}: {found}")
    return paths[0]


def discover_paths(
    root: str | Path = ".",
    *,
    skill: str | Path | None = None,
    config: str | Path | None = None,
    examples: str | Path | None = None,
) -> Paths:
    root = Path(root).resolve()
    skill_path = _existing(skill, "skill") if skill else _one("SKILL.md", _files(root, "SKILL.md"))
    skill_name = skill_path.parent.name

    config_path = _existing(config, "config") if config else None
    examples_path = _existing(examples, "examples") if examples else None
    if config_path and not examples_path and (config_path.parent / "examples.py").is_file():
        examples_path = (config_path.parent / "examples.py").resolve()
    if examples_path and not config_path and (examples_path.parent / "config.py").is_file():
        config_path = (examples_path.parent / "config.py").resolve()

    if not config_path or not examples_path:
        pairs = [
            (path.parent / "config.py", path)
            for path in _files(root, "examples.py")
            if (path.parent / "config.py").is_file()
        ]
        matching = [pair for pair in pairs if pair[0].parent.name == skill_name]
        selected = matching if matching else pairs
        if len(selected) != 1:
            found = ", ".join(str(pair[0].parent) for pair in selected) or "none"
            raise ValueError(
                f"expected one config.py/examples.py pair for {skill_name!r}, "
                f"found {len(selected)}: {found}"
            )
        config_path = config_path or selected[0][0].resolve()
        examples_path = examples_path or selected[0][1].resolve()

    return Paths(skill=skill_path, config=config_path, examples=examples_path)


def import_file(path: str | Path) -> ModuleType:
    path = Path(path).resolve()
    spec = spec_from_file_location(f"skilltester_{uuid4().hex}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_suite(path: str | Path) -> Suite:
    module = import_file(path)
    tag_type = getattr(module, "Tags", None)
    tag_options = None
    examples = module.examples
    if tag_type is not None:
        if not is_typeddict(tag_type):
            raise ValueError("Tags must be a TypedDict")
        hints = get_type_hints(tag_type)
        if set(tag_type.__required_keys__) != set(hints):
            raise ValueError("every Tags key must be required")
        tag_options = {}
        for key, annotation in hints.items():
            if get_origin(annotation) is not Literal:
                raise ValueError(f"Tags.{key} must use Literal")
            options = get_args(annotation)
            if not options or any(not isinstance(option, str) for option in options):
                raise ValueError(f"Tags.{key} must contain string Literals")
            tag_options[key] = frozenset(options)
        adapter = TypeAdapter(tag_type)
        validated_examples = []
        for example in examples:
            tags = example.get("tags")
            if not isinstance(tags, dict) or set(tags) != set(hints):
                raise ValueError("every example must define exactly the keys in Tags")
            validated_examples.append(
                {**example, "tags": adapter.validate_python(tags)}
            )
        examples = validated_examples
    return Suite.model_validate(
        {
            "system_prompt": module.system_prompt,
            "response_types": module.response_types,
            "examples": examples,
            "truth_table": getattr(module, "truth_table", None),
            "tag_options": tag_options,
        }
    )
