#!/usr/bin/env python3
"""Generate Mihomo rule providers from dler-io/Rules Clash providers.

Each Dler provider is a classical Clash rule source.  The source is attached
to both a domain target and an IP-CIDR target; the existing rule merger keeps
only the rules applicable to each target behavior.  Empty halves are removed
before the workflow converts the remaining YAML files to MRS.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Iterable, List

import requests
import yaml


CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent
DEFAULT_API_URL = (
    "https://api.github.com/repos/dler-io/Rules/contents/Clash/Provider?ref=main"
)
OUTPUT_PREFIX = "dler-"

logger = logging.getLogger("dler_ruleset")


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    url: str


def _safe_name(filename: str) -> str:
    stem = Path(filename).stem.strip().lower()
    stem = re.sub(r"[^a-z0-9_.-]+", "_", stem)
    return stem.strip("._") or "unnamed"


def discover_entries(api_url: str = DEFAULT_API_URL) -> List[CatalogEntry]:
    """Discover YAML providers from the Dler GitHub directory."""

    response = requests.get(
        api_url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
    )
    response.raise_for_status()
    items = response.json()
    if not isinstance(items, list):
        raise RuntimeError(f"Unexpected Dler provider index: {api_url}")

    entries: Dict[str, CatalogEntry] = {}
    for item in items:
        if not isinstance(item, dict) or item.get("type") != "file":
            continue

        filename = str(item.get("name", ""))
        if Path(filename).suffix.lower() not in {".yaml", ".yml"}:
            continue

        download_url = item.get("download_url")
        if not isinstance(download_url, str) or not download_url:
            raise RuntimeError(f"Missing Dler download URL for {filename}")

        name = _safe_name(filename)
        entries[name] = CatalogEntry(name=name, url=download_url)

    return sorted(entries.values(), key=lambda item: item.name)


def build_merger_config(
    entries: Iterable[CatalogEntry], output_dir: Path
) -> List[Dict[str, object]]:
    configs: List[Dict[str, object]] = []
    for entry in entries:
        source_config = {
            "type": "http",
            "url": entry.url,
            "format": "yaml",
            "behavior": "classical",
        }

        for target_behavior in ("domain", "ipcidr"):
            suffix = "@ip" if target_behavior == "ipcidr" else ""
            configs.append(
                {
                    "path": str(output_dir / f"{OUTPUT_PREFIX}{entry.name}{suffix}.yaml"),
                    "format": "yaml",
                    "behavior": target_behavior,
                    "upstream": {f"dler_{entry.name}": dict(source_config)},
                }
            )

    return configs


def clean_generated_outputs() -> None:
    """Remove only Dler artifacts owned by this generator."""

    targets = {
        PROJECT_ROOT / "Code" / "output": {"yaml"},
        PROJECT_ROOT / "Mihomo" / "Provider": {"yaml", "mrs"},
    }
    for directory, extensions in targets.items():
        if not directory.exists():
            continue
        for path in directory.glob(f"{OUTPUT_PREFIX}*"):
            if path.is_file() and path.suffix.lstrip(".") in extensions:
                path.unlink()


def remove_empty_provider_files(provider_dir: Path) -> None:
    for path in provider_dir.glob(f"{OUTPUT_PREFIX}*.yaml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise RuntimeError(f"Unable to inspect generated file {path}: {exc}") from exc

        payload = data.get("payload") if isinstance(data, dict) else None
        if isinstance(payload, list) and payload:
            continue

        logger.debug("Removing empty Dler target: %s", path.name)
        path.unlink()


def generate(entries: List[CatalogEntry]) -> None:
    configs = build_merger_config(entries, CODE_DIR / "output")
    if not configs:
        raise RuntimeError("No Dler Clash providers were found")

    clean_generated_outputs()
    config_file: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".yaml",
            prefix=".dler-",
            dir=CODE_DIR,
            delete=False,
        ) as handle:
            yaml.safe_dump(configs, handle, allow_unicode=True, sort_keys=False)
            config_file = Path(handle.name)

        sys.path.insert(0, str(CODE_DIR))
        from core import RulesMerger

        RulesMerger(str(config_file)).merge_rules()
        remove_empty_provider_files(PROJECT_ROOT / "Mihomo" / "Provider")
    finally:
        if config_file and config_file.exists():
            config_file.unlink()

    logger.info("Generated %d Dler split targets from %d providers", len(configs), len(entries))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Mihomo rule providers for dler-io/Rules"
    )
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="Dler provider API URL")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the discovered provider/target counts without writing files",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    entries = discover_entries(args.api_url)
    configs = build_merger_config(entries, CODE_DIR / "output")
    logger.info(
        "Discovered %d Dler Clash providers and %d split targets",
        len(entries),
        len(configs),
    )
    if not args.dry_run:
        generate(entries)


if __name__ == "__main__":
    main()
