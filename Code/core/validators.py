"""
规则验证器模块

提供各种规则类型的验证功能
"""

import re
import logging
from typing import Optional

from .constants import RuleConstants, DIRTY_DOMAIN_PATTERNS


class RuleValidator:
    """
    规则验证器类

    提供对不同类型规则的验证功能，包括经典规则、IP CIDR规则和域名规则
    """

    def __init__(self):
        """初始化验证器"""
        self.constants = RuleConstants()
        self.logger = logging.getLogger(__name__)

    def validate_classical_rule(self, rule: str) -> Optional[str]:
        """
        验证经典格式规则

        Args:
            rule: 待验证的规则字符串

        Returns:
            Optional[str]: 验证通过的规则，失败返回None
        """
        try:
            # 如果规则不包含逗号，可能是纯域名或IP格式，需要添加前缀
            if "," not in rule:
                return self._handle_simple_rule(rule)

            parts = rule.split(",")
            if len(parts) < 2:
                return None

            rule_type = parts[0].strip()
            value = parts[1].strip()

            # 根据规则类型验证值的格式
            return self._validate_rule_by_type(rule_type, value, rule)

        except (ValueError, IndexError, AttributeError) as e:
            self.logger.debug("规则验证失败: %s, 错误: %s", rule, str(e))
            return None

    def _handle_simple_rule(self, rule: str) -> Optional[str]:
        """
        处理简单格式的规则（不包含逗号的规则）

        Args:
            rule: 简单格式的规则

        Returns:
            Optional[str]: 处理后的规则，失败返回None
        """
        # 尝试识别为域名
        if self.is_valid_domain(rule):
            return f"DOMAIN,{rule}"

        # 尝试识别为域名后缀（+.格式）
        if rule.startswith("+.") and self.is_valid_domain(rule[2:]):
            return f"DOMAIN-SUFFIX,{rule[2:]}"

        # 尝试识别为IP CIDR
        if re.match(self.constants.ipv4_cidr_pattern, rule) or re.match(
            self.constants.ipv6_cidr_pattern, rule
        ):
            return f"IP-CIDR6,{rule}" if ":" in rule else f"IP-CIDR,{rule}"

        return None

    def _validate_rule_by_type(
        self, rule_type: str, value: str, original_rule: str
    ) -> Optional[str]:
        """
        根据规则类型验证值

        Args:
            rule_type: 规则类型
            value: 规则值
            original_rule: 原始规则字符串

        Returns:
            Optional[str]: 验证通过的规则，失败返回None
        """
        if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
            return original_rule if self.is_valid_domain(value) else None
        elif rule_type == "IP-CIDR":
            return (
                original_rule
                if re.match(self.constants.ipv4_cidr_pattern, value)
                else None
            )
        elif rule_type == "IP-CIDR6":
            return (
                original_rule
                if re.match(self.constants.ipv6_cidr_pattern, value)
                else None
            )
        else:
            # 对于其他类型的规则，进行基本验证
            return original_rule if value else None

    def is_valid_domain(self, domain: str) -> bool:
        """
        验证是否为有效域名，过滤脏数据

        Args:
            domain: 待验证的域名

        Returns:
            bool: 是否为有效域名
        """
        if not domain or not re.match(self.constants.domain_pattern, domain):
            return False

        # 过滤明显的脏数据域名
        for pattern in DIRTY_DOMAIN_PATTERNS:
            if re.match(pattern, domain, re.IGNORECASE):
                return False

        return True

    def validate_ipcidr_rule(self, rule: str) -> Optional[str]:
        """
        验证IP CIDR规则

        Args:
            rule: 待验证的IP CIDR规则

        Returns:
            Optional[str]: 验证通过的规则，失败返回None
        """
        try:
            # 如果是完整的规则格式（如 "IP-CIDR,192.168.1.0/24" 或 "IP-ASN,13335"）
            if "," in rule:
                parts = rule.split(",")
                if len(parts) >= 2:
                    rule_type = parts[0].strip()
                    # 检查规则类型是否属于ipcidr类型
                    if rule_type in self.constants.rule_types.get("ipcidr", set()):
                        return rule
                return None
            # 如果是纯IP CIDR格式，添加前缀
            else:
                return self._handle_pure_ipcidr(rule)

        except (ValueError, IndexError, AttributeError) as e:
            self.logger.debug("IP CIDR规则验证失败: %s, 错误: %s", rule, str(e))
            return None

    def _handle_pure_ipcidr(self, rule: str) -> Optional[str]:
        """
        处理纯IP CIDR格式的规则

        Args:
            rule: 纯IP CIDR格式规则

        Returns:
            Optional[str]: 处理后的规则，失败返回None
        """
        if re.match(self.constants.ipv4_cidr_pattern, rule):
            return f"IP-CIDR,{rule}"
        elif re.match(self.constants.ipv6_cidr_pattern, rule):
            return f"IP-CIDR6,{rule}"
        return None

    def validate_domain_rule(self, rule: str) -> Optional[str]:
        """
        验证域名规则

        Args:
            rule: 待验证的域名规则

        Returns:
            Optional[str]: 验证通过的规则，失败返回None
        """
        try:
            # 如果是完整的规则格式（如 "DOMAIN,example.com" 或 "GEOSITE,youtube"）
            if "," in rule:
                return self._handle_complete_domain_rule(rule)
            # 如果是纯域名格式，添加前缀
            else:
                return self._handle_pure_domain_rule(rule)

        except (ValueError, IndexError, AttributeError) as e:
            self.logger.debug("域名规则验证失败: %s, 错误: %s", rule, str(e))
            return None

    def _handle_complete_domain_rule(self, rule: str) -> Optional[str]:
        """
        处理完整格式的域名规则

        Args:
            rule: 完整格式的域名规则

        Returns:
            Optional[str]: 处理后的规则，失败返回None
        """
        parts = rule.split(",")
        if len(parts) >= 2:
            rule_type = parts[0].strip()
            value = parts[1].strip()
            # 检查规则类型是否属于domain类型
            if rule_type in self.constants.rule_types.get("domain", set()):
                # 对于DOMAIN和DOMAIN-SUFFIX类型，验证域名有效性
                if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
                    return rule if self.is_valid_domain(value) else None
                # 其他类型直接通过
                return rule
        return None

    def _handle_pure_domain_rule(self, rule: str) -> Optional[str]:
        """
        处理纯域名格式的规则

        Args:
            rule: 纯域名格式规则

        Returns:
            Optional[str]: 处理后的规则，失败返回None
        """
        # 处理域名格式：+.example.com 或 example.com
        if rule.startswith("+."):
            domain = rule[2:]
            if self.is_valid_domain(domain):
                return f"DOMAIN-SUFFIX,{domain}"
        else:
            if self.is_valid_domain(rule):
                return f"DOMAIN,{rule}"
        return None
