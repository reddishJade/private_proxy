#!/usr/bin/env python3
"""
sing-box 规则集转换入口
"""

from __future__ import annotations

import argparse
from pathlib import Path

from core import SingBoxRuleSetConverter


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Mihomo rule-provider YAML to sing-box source JSON."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--behavior", choices=["domain", "ipcidr", "classical"])
    parser.add_argument("--version", type=int, default=3)
    args = parser.parse_args()

    converter = SingBoxRuleSetConverter()
    converter.convert_file(args.source, args.target, args.behavior, args.version)


if __name__ == "__main__":
    main()
