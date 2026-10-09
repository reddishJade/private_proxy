#!/usr/bin/env python3
"""Generate normalized rule providers from ruleset.skk.moe.

The site publishes the same logical rule set in several Clash directories:

* ``domainset`` contains Clash wildcard domain rules;
* ``non_ip`` contains classical rules and may include both domains and IP
  CIDRs;
* ``ip`` contains IP CIDRs (and, occasionally, classical rules mixed in).

The rule merger is used for the actual normalization of the Clash sources.  A
separate ``skk-`` prefix keeps these site-wide outputs independent from the
repository's curated rule groups.  The generated Clash YAML files become MRS.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import DefaultDict, Dict, Iterable, List, Sequence
from urllib.parse import unquote, urljoin, urlparse

import requests
import yaml


CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent
DEFAULT_INDEX_URL = "https://ruleset.skk.moe/"
OUTPUT_PREFIX = "skk-"
SUPPORTED_CATEGORIES = {"domainset", "non_ip", "ip"}

logger = logging.getLogger("skk_ruleset")


@dataclass(frozen=True)
class CatalogEntry:
    """One downloadable rule source listed by the SKK index."""

    category: str
    name: str
    url: str
    format: str


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: List[str] = []

    def handle_starttag(self, tag: str, attrs: Sequence[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.hrefs.append(value)


def _safe_name(name: str) -> str:
    """Return a stable filename component for a catalog item."""

    name = unquote(name).strip()
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    return name.strip("._") or "unnamed"


def discover_clash_entries(index_html: str, index_url: str = DEFAULT_INDEX_URL) -> List[CatalogEntry]:
    """Discover Clash rule files from the site's HTML index.

    The index is the source of truth, so adding a new SKK rule does not
    require editing this repository.  Only files under
    ``Clash/{category}`` are accepted; links to modules, mock files, and other
    site assets are intentionally ignored.
    """

    parser = _LinkParser()
    parser.feed(index_html)

    entries: Dict[tuple[str, str, str], CatalogEntry] = {}
    for href in parser.hrefs:
        absolute_url = urljoin(index_url, href)
        path = urlparse(absolute_url).path.strip("/")
        parts = path.split("/")
        if len(parts) != 3 or parts[0] != "Clash":
            continue

        category = parts[1]
        if category not in SUPPORTED_CATEGORIES:
            continue

        filename = parts[2]
        suffix = Path(filename).suffix.lower()
        supported_suffixes = {".txt", ".text", ".yaml", ".yml"}
        if suffix not in supported_suffixes:
            continue

        name = _safe_name(Path(filename).stem)
        if name.startswith("my_"):
            continue
        file_format = "yaml" if suffix in {".yaml", ".yml"} else "txt"
        entries[(parts[0], category, name)] = CatalogEntry(
            category=category,
            name=name,
            url=absolute_url,
            format=file_format,
        )

    return sorted(entries.values(), key=lambda item: (item.category, item.name))


def _fetch_index(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _source_config(entry: CatalogEntry, behavior: str) -> Dict[str, str]:
    return {
        "type": "http",
        "url": entry.url,
        "format": entry.format,
        "behavior": behavior,
    }


def build_merger_config(
    entries: Iterable[CatalogEntry], output_dir: Path
) -> List[Dict[str, object]]:
    """Build rule-merger targets, splitting classical ``non_ip`` sources.

    Entries with the same stem are merged into one logical output.  A
    ``non_ip`` source is deliberately attached to both targets: the merger's
    behavior conversion retains its domain rules in the domain target and its
    IP-CIDR rules in the IP target.
    """

    grouped: DefaultDict[str, DefaultDict[str, List[tuple[CatalogEntry, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for entry in entries:
        if entry.category == "domainset":
            grouped[entry.name]["domain"].append((entry, "domain"))
        elif entry.category == "ip":
            grouped[entry.name]["ipcidr"].append((entry, "ipcidr"))
        elif entry.category == "non_ip":
            grouped[entry.name]["domain"].append((entry, "classical"))
            grouped[entry.name]["ipcidr"].append((entry, "classical"))

    configs: List[Dict[str, object]] = []
    for name in sorted(grouped):
        targets = grouped[name]
        for target_behavior in ("domain", "ipcidr"):
            sources = targets.get(target_behavior, [])
            if not sources:
                continue

            upstream: Dict[str, Dict[str, str]] = {}
            for index, (entry, source_behavior) in enumerate(sources):
                source_key = f"{entry.category}_{entry.name}_{index}"
                upstream[source_key] = _source_config(entry, source_behavior)

            suffix = "@ip" if target_behavior == "ipcidr" else ""
            configs.append(
                {
                    "path": str(output_dir / f"{OUTPUT_PREFIX}{name}{suffix}.yaml"),
                    "format": "yaml",
                    "behavior": target_behavior,
                    "upstream": upstream,
                }
            )

    return configs


def _generated_file_patterns() -> Dict[Path, str]:
    return {
        PROJECT_ROOT / "Code" / "output": "yaml",
        PROJECT_ROOT / "Mihomo" / "Provider": "yaml|mrs",
    }


def clean_generated_outputs() -> None:
    """Remove only artifacts owned by this generator before regeneration."""

    for directory, extensions in _generated_file_patterns().items():
        allowed = set(extensions.split("|"))
        if not directory.exists():
            continue
        for path in directory.glob(f"{OUTPUT_PREFIX}*"):
            if path.is_file() and path.suffix.lstrip(".") in allowed:
                path.unlink()


def remove_empty_provider_files(provider_dir: Path) -> None:
    """Do not send empty split targets to the binary converters."""

    for path in provider_dir.glob(f"{OUTPUT_PREFIX}*.yaml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise RuntimeError(f"Unable to inspect generated file {path}: {exc}") from exc

        payload = data.get("payload") if isinstance(data, dict) else None
        if isinstance(payload, list) and payload:
            continue

        # Empty targets are expected for marker-only/deprecated sources and
        # for the ipcidr half of a non_ip source with no IP rules.  Keep the
        # workflow quiet; the file is removed before binary conversion.
        logger.debug("Removing empty SKK target: %s", path.name)
        path.unlink()


def generate(entries: List[CatalogEntry]) -> None:
    output_dir = CODE_DIR / "output"
    configs = build_merger_config(entries, output_dir)
    if not configs:
        raise RuntimeError("No supported Clash rules were found on the SKK index")

    clean_generated_outputs()

    config_file: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".yaml",
            prefix=".skk-",
            dir=CODE_DIR,
            delete=False,
        ) as handle:
            yaml.safe_dump(configs, handle, allow_unicode=True, sort_keys=False)
            config_file = Path(handle.name)

        # Import only after the temporary config is ready.  This keeps the
        # script usable from the repository root and from the Code directory.
        sys.path.insert(0, str(CODE_DIR))
        from core import RulesMerger

        merger = RulesMerger(str(config_file))
        merger.merge_rules()
        remove_empty_provider_files(PROJECT_ROOT / "Mihomo" / "Provider")
    finally:
        if config_file and config_file.exists():
            config_file.unlink()

    logger.info(
        "Generated %d SKK targets from %d Clash sources",
        len(configs),
        len(entries),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate rule-merger targets for ruleset.skk.moe"
    )
    parser.add_argument(
        "--index-url",
        default=DEFAULT_INDEX_URL,
        help="SKK ruleset index URL",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the discovered source/target counts without writing files",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    clash_entries = discover_clash_entries(_fetch_index(args.index_url), args.index_url)
    configs = build_merger_config(clash_entries, CODE_DIR / "output")
    logger.info(
        "Discovered %d Clash sources and %d split targets",
        len(clash_entries),
        len(configs),
    )

    if not args.dry_run:
        generate(clash_entries)


if __name__ == "__main__":
    main()
