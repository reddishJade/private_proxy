"""
规则转换器模块

提供在不同规则格式之间转换的功能
"""

import re
import logging
from typing import Optional, Callable

from .validators import RuleValidator


class RuleTransformer:
    """
    规则转换器类

    用于在不同规则格式之间转换，支持classical、ipcidr、domain三种行为类型之间的转换
    """

    def __init__(self):
        """初始化转换器"""
        self.validator = RuleValidator()
        self.logger = logging.getLogger(__name__)

    def transform(
        self, rule: str, source_behavior: str, target_behavior: str
    ) -> Optional[str]:
        """
        转换规则格式

        Args:
            rule: 待转换的规则
            source_behavior: 源规则行为类型
            target_behavior: 目标规则行为类型

        Returns:
            Optional[str]: 转换后的规则，失败返回None
        """
        if not rule:
            return None

        # 如果源和目标behavior相同，直接验证
        if source_behavior == target_behavior:
            return self._validate_same_behavior(rule, target_behavior)

        # 如果需要转换格式，先检查原始规则是否可以转换
        if not self._can_transform_rule(rule, source_behavior, target_behavior):
            return None

        transformer = self._get_transformer(source_behavior, target_behavior)
        if not transformer:
            return None

        return transformer(rule)

    def _validate_same_behavior(self, rule: str, behavior: str) -> Optional[str]:
        """
        验证相同行为类型的规则并转换为正确格式

        Args:
            rule: 待验证的规则
            behavior: 行为类型

        Returns:
            Optional[str]: 验证通过并格式化后的规则，失败返回None
        """
        # 检查规则是否应该包含在目标behavior中
        if not self._should_include_rule(rule, behavior):
            return None

        # 对于非classical behavior，需要转换为相应格式
        if behavior == "domain":
            return self._normalize_to_domain_format(rule)
        elif behavior == "ipcidr":
            return self._normalize_to_ipcidr_format(rule)
        else:
            # classical behavior 直接验证
            return self.validator.validate_classical_rule(rule)

    def _normalize_to_domain_format(self, rule: str) -> Optional[str]:
        """
        将规则标准化为domain格式（纯域名格式）

        Args:
            rule: 待标准化的规则

        Returns:
            Optional[str]: 标准化后的规则，失败返回None
        """
        try:
            # 如果规则包含逗号，说明是完整格式的规则
            if "," in rule:
                parts = rule.split(",")
                if len(parts) >= 2:
                    rule_type = parts[0].strip()
                    value = parts[1].strip()
                    # 对于domain behavior的转换策略
                    if rule_type == "DOMAIN":
                        if self.validator._is_valid_domain(value):
                            return value
                    elif rule_type == "DOMAIN-SUFFIX":
                        if self.validator._is_valid_domain(value):
                            return f"+.{value}"
                    # 对于其他域名相关规则类型（如DOMAIN-KEYWORD），在domain behavior中应该被过滤
                    elif rule_type in self.validator.constants.RULE_TYPES.get(
                        "domain", set()
                    ):
                        # 根据严格模式，domain behavior只应该包含纯域名
                        return None
                    else:
                        return None
                return None
            else:
                # 如果是纯域名格式，直接验证并返回
                if rule.startswith("+."):
                    domain = rule[2:]
                    return domain if self.validator._is_valid_domain(domain) else None
                else:
                    return rule if self.validator._is_valid_domain(rule) else None
        except Exception:
            return None

    def _normalize_to_ipcidr_format(self, rule: str) -> Optional[str]:
        """
        将规则标准化为ipcidr格式（纯IP CIDR格式）

        Args:
            rule: 待标准化的规则

        Returns:
            Optional[str]: 标准化后的规则，失败返回None
        """
        try:
            # 如果规则包含逗号，说明是完整格式的规则
            if "," in rule:
                parts = rule.split(",")
                if len(parts) >= 2:
                    rule_type = parts[0].strip()
                    value = parts[1].strip()
                    # 对于IP-CIDR和IP-CIDR6，返回纯IP CIDR
                    if rule_type in {"IP-CIDR", "IP-CIDR6"}:
                        return value
                    # 对于其他IP相关规则类型，保持完整格式
                    elif rule_type in self.validator.constants.RULE_TYPES.get(
                        "ipcidr", set()
                    ):
                        return rule
                return None
            else:
                # 如果是纯IP CIDR格式，直接验证并返回
                import re

                if re.match(
                    self.validator.constants.IPV4_CIDR_PATTERN, rule
                ) or re.match(self.validator.constants.IPV6_CIDR_PATTERN, rule):
                    return rule
                return None
        except Exception:
            return None

    def _can_transform_rule(
        self, rule: str, source_behavior: str, target_behavior: str
    ) -> bool:
        """
        检查规则是否可以从源behavior转换到目标behavior

        Args:
            rule: 待检查的规则
            source_behavior: 源行为类型
            target_behavior: 目标行为类型

        Returns:
            bool: 是否可以转换
        """
        if not rule:
            return False

        try:
            rule_type = rule.split(",")[0]

            # 从classical转换到具体类型时，检查规则类型是否匹配
            if source_behavior == "classical":
                target_types = self.validator.constants.RULE_TYPES.get(
                    target_behavior, set()
                )
                return rule_type in target_types

            return True
        except Exception:
            return False

    def _should_include_rule(self, rule: str, target_behavior: str) -> bool:
        """
        判断规则是否应该包含在目标behavior中

        Args:
            rule: 待判断的规则
            target_behavior: 目标行为类型

        Returns:
            bool: 是否应该包含
        """
        if not rule:
            return False

        try:
            # 如果规则包含逗号，说明是完整格式的规则
            if "," in rule:
                return self._check_complete_rule_inclusion(rule, target_behavior)
            else:
                return self._check_simple_rule_inclusion(rule, target_behavior)
        except Exception:
            return False

    def _check_complete_rule_inclusion(self, rule: str, target_behavior: str) -> bool:
        """
        检查完整格式规则是否应该包含在目标behavior中

        Args:
            rule: 完整格式规则
            target_behavior: 目标行为类型

        Returns:
            bool: 是否应该包含
        """
        rule_type = rule.split(",")[0].strip()
        allowed_types = self.validator.constants.RULE_TYPES.get(target_behavior, set())
        return rule_type in allowed_types

    def _check_simple_rule_inclusion(self, rule: str, target_behavior: str) -> bool:
        """
        检查简单格式规则是否应该包含在目标behavior中

        Args:
            rule: 简单格式规则
            target_behavior: 目标行为类型

        Returns:
            bool: 是否应该包含
        """
        if target_behavior == "domain":
            # 检查是否为有效域名（包括+.格式）
            if rule.startswith("+."):
                return self.validator._is_valid_domain(rule[2:])
            else:
                return self.validator._is_valid_domain(rule)
        elif target_behavior == "ipcidr":
            # 检查是否为有效IP CIDR
            return (
                re.match(self.validator.constants.IPV4_CIDR_PATTERN, rule) is not None
                or re.match(self.validator.constants.IPV6_CIDR_PATTERN, rule)
                is not None
            )
        elif target_behavior == "classical":
            # classical可以包含所有类型
            return True
        else:
            return False

    def _get_transformer(
        self, source_behavior: str, target_behavior: str
    ) -> Optional[Callable]:
        """
        获取对应的转换函数

        Args:
            source_behavior: 源行为类型
            target_behavior: 目标行为类型

        Returns:
            Optional[Callable]: 转换函数，如果不存在返回None
        """
        transformers = {
            ("classical", "ipcidr"): self._classical_to_ipcidr,
            ("classical", "domain"): self._classical_to_domain,
            ("ipcidr", "classical"): self._ipcidr_to_classical,
            ("domain", "classical"): self._domain_to_classical,
        }
        return transformers.get((source_behavior, target_behavior))

    def _classical_to_ipcidr(self, rule: str) -> Optional[str]:
        """
        将经典格式转换为IP CIDR格式

        Args:
            rule: 经典格式规则

        Returns:
            Optional[str]: 转换后的IP CIDR格式规则（纯IP CIDR格式）
        """
        try:
            parts = rule.split(",")
            if len(parts) < 2:
                return None

            rule_type = parts[0].strip()
            value = parts[1].strip()

            # 对于ipcidr相关规则，转换为纯IP CIDR格式
            if rule_type in self.validator.constants.RULE_TYPES.get("ipcidr", set()):
                # 对于IP-CIDR和IP-CIDR6，返回纯IP CIDR
                if rule_type in {"IP-CIDR", "IP-CIDR6"}:
                    return value
                # 对于其他IP相关规则类型（如GEOIP、IP-ASN等），保持完整格式
                return rule

            return None
        except Exception:
            return None

    def _classical_to_domain(self, rule: str) -> Optional[str]:
        """
        将经典格式转换为域名格式

        Args:
            rule: 经典格式规则

        Returns:
            Optional[str]: 转换后的域名格式规则（纯域名格式）
        """
        try:
            parts = rule.split(",")
            if len(parts) < 2:
                return None

            rule_type = parts[0].strip()
            value = parts[1].strip()

            # 对于domain相关规则，转换为纯域名格式
            if rule_type in self.validator.constants.RULE_TYPES.get("domain", set()):
                # 验证域名有效性
                if rule_type in {
                    "DOMAIN",
                    "DOMAIN-SUFFIX",
                } and not self.validator._is_valid_domain(value):
                    return None
                # 对于DOMAIN和DOMAIN-SUFFIX，返回纯域名
                if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
                    return value
                # 对于其他域名相关规则类型，保持完整格式
                return rule

            return None
        except Exception:
            return None

    def _ipcidr_to_classical(self, rule: str) -> Optional[str]:
        """
        将IP CIDR格式转换为经典格式

        Args:
            rule: IP CIDR格式规则

        Returns:
            Optional[str]: 转换后的经典格式规则
        """
        # 如果已经是完整格式，直接返回
        if "," in rule:
            return rule

        # 如果是纯IP CIDR格式，添加前缀
        if ":" in rule:
            return f"IP-CIDR6,{rule}"
        else:
            return f"IP-CIDR,{rule}"

    def _domain_to_classical(self, rule: str) -> Optional[str]:
        """
        将域名格式转换为经典格式

        Args:
            rule: 域名格式规则

        Returns:
            Optional[str]: 转换后的经典格式规则
        """
        # 如果已经是完整格式，直接返回
        if "," in rule:
            return rule

        if rule.startswith("+."):
            suffix = rule[2:]
            if not self.validator._is_valid_domain(suffix):
                return None
            return f"DOMAIN-SUFFIX,{suffix}"

        if not self.validator._is_valid_domain(rule):
            return None
        return f"DOMAIN,{rule}"
