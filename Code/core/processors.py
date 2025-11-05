"""
规则处理器模块

提供规则清理和处理的功能
"""

import re
import logging
from typing import List

from .constants import DIRTY_CONTENT_PATTERNS
from .transformers import RuleTransformer


class RuleProcessor:
    """
    规则处理器类

    负责清理和处理规则，包括去除注释、过滤脏数据、规则转换等
    """

    def __init__(self):
        """初始化处理器"""
        self.transformer = RuleTransformer()
        self.logger = logging.getLogger(__name__)

    def clean_rule(self, rule: str) -> str:
        """
        清理规则，去除注释和空白

        Args:
            rule: 待清理的规则字符串

        Returns:
            str: 清理后的规则，如果规则无效则返回空字符串
        """
        rule = rule.strip()

        # 跳过空行和注释行
        if not rule or rule.startswith("#"):
            return ""

        # 移除行内注释（在空格后的#）
        cleaned = self._remove_inline_comments(rule)

        # 过滤掉明显的脏数据行
        if self._is_dirty_content(cleaned):
            return ""

        return cleaned

    def _remove_inline_comments(self, rule: str) -> str:
        """
        移除行内注释

        Args:
            rule: 包含可能注释的规则

        Returns:
            str: 移除注释后的规则
        """
        parts = re.split(r"\s+#", rule)
        return parts[0].strip() if len(parts) > 1 else rule.strip()

    def _is_dirty_content(self, content: str) -> bool:
        """
        检查是否为脏数据内容

        Args:
            content: 待检查的内容

        Returns:
            bool: 是否为脏数据
        """
        for pattern in DIRTY_CONTENT_PATTERNS:
            if re.match(pattern, content, re.IGNORECASE):
                return True
        return False

    def process_rules(
        self, rules: List[str], source_behavior: str, target_behavior: str
    ) -> List[str]:
        """
        处理规则列表

        Args:
            rules: 原始规则列表
            source_behavior: 源规则行为类型
            target_behavior: 目标规则行为类型

        Returns:
            List[str]: 处理后的规则列表
        """
        processed_rules = []

        for rule in rules:
            cleaned_rule = self.clean_rule(rule)
            if not cleaned_rule:
                continue

            # 记录原始规则用于调试
            original_rule = cleaned_rule

            transformed_rule = self.transformer.transform(
                cleaned_rule, source_behavior, target_behavior
            )
            if transformed_rule:
                processed_rules.append(transformed_rule)
            else:
                # 如果转换失败，记录调试信息
                self.logger.debug(
                    "规则转换失败: '%s' from %s to %s",
                    original_rule,
                    source_behavior,
                    target_behavior,
                )

        return processed_rules

    def deduplicate_and_sort(self, rules: List[str]) -> List[str]:
        """
        去重并排序规则列表

        Args:
            rules: 规则列表

        Returns:
            List[str]: 去重排序后的规则列表
        """
        return sorted(set(rules))
