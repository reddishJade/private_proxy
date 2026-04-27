"""
sing-box 规则集转换模块

提供将 Mihomo rule-provider YAML 转换为 sing-box source rule-set JSON 的功能。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class SingBoxRuleSetConverter:
    """
    sing-box source rule-set 转换器

    负责把 Mihomo rule-provider 的 payload 规则转换为 sing-box headless rule。
    """

    domain_fields = {
        "domain": "domain",
        "domain-suffix": "domain_suffix",
        "domain-keyword": "domain_keyword",
        "domain-regex": "domain_regex",
    }

    ip_fields = {
        "ip-cidr": "ip_cidr",
        "ip-cidr6": "ip_cidr",
    }

    def convert_file(
        self,
        source: Path,
        target: Path,
        behavior: Optional[str] = None,
        version: int = 3,
    ) -> None:
        """
        将 Mihomo YAML 文件转换为 sing-box source JSON 文件。

        Args:
            source: Mihomo rule-provider YAML 路径
            target: sing-box source JSON 输出路径
            behavior: 规则行为类型，未指定时根据文件名推断
            version: sing-box rule-set source version
        """
        data: Dict[str, Any] = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
        payload = data.get("payload")
        if not isinstance(payload, list):
            raise ValueError(f"{source} does not contain a payload list")

        detected_behavior = self.infer_behavior(source, behavior)
        rule = self.convert_payload(payload, detected_behavior)
        output = {
            "version": version,
            "rules": [rule] if rule else [],
        }

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def convert_payload(
        self, payload: List[Any], behavior: str
    ) -> Dict[str, List[str]]:
        """
        将 payload 列表转换为 sing-box 单条 headless rule。

        Args:
            payload: Mihomo rule-provider payload
            behavior: 规则行为类型

        Returns:
            Dict[str, List[str]]: sing-box headless rule 字段
        """
        rule: Dict[str, List[str]] = {}

        for item in payload:
            if not isinstance(item, str):
                continue
            if "," in item:
                self._add_classical_rule(rule, item)
            else:
                self._add_simple_rule(rule, item, behavior)

        return rule

    def infer_behavior(self, path: Path, explicit_behavior: Optional[str]) -> str:
        """
        根据显式参数或文件名推断规则行为类型。
        """
        if explicit_behavior:
            return explicit_behavior
        return "ipcidr" if "@ip" in path.stem else "domain"

    def _add_item(self, rule: Dict[str, List[str]], key: str, value: str) -> None:
        value = value.strip()
        if not value:
            return
        rule.setdefault(key, [])
        if value not in rule[key]:
            rule[key].append(value)

    def _add_simple_rule(
        self, rule: Dict[str, List[str]], item: str, behavior: str
    ) -> None:
        item = item.strip()
        if not item:
            return

        if behavior == "ipcidr":
            self._add_item(rule, "ip_cidr", item)
            return

        if item.startswith("+."):
            self._add_item(rule, "domain_suffix", item[2:])
        elif item.startswith("*."):
            escaped_domain = self._regex_escape_domain(item[2:])
            self._add_item(rule, "domain_regex", rf"^[^.]+\.{escaped_domain}$")
        elif item.startswith("."):
            self._add_item(rule, "domain_suffix", item[1:])
        else:
            self._add_item(rule, "domain", item)

    def _add_classical_rule(self, rule: Dict[str, List[str]], item: str) -> None:
        parts = [part.strip() for part in item.split(",")]
        if len(parts) < 2:
            self._add_simple_rule(rule, item, "domain")
            return

        rule_type = parts[0].lower()
        value = parts[1]

        if rule_type in self.domain_fields:
            self._add_item(rule, self.domain_fields[rule_type], value)
        elif rule_type in self.ip_fields:
            self._add_item(rule, self.ip_fields[rule_type], value)

    def _regex_escape_domain(self, domain: str) -> str:
        return re.escape(domain.strip("."))
