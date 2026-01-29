"""
规则合并器核心模块

此包包含规则合并器的核心功能模块：
- constants: 规则相关常量定义
- validators: 规则验证器
- transformers: 规则转换器
- fetchers: 规则获取器
- processors: 规则处理器
- merger: 规则合并器主逻辑
"""

__version__ = "1.0.0"
__author__ = "RuleMerger Team"

from .constants import RuleConstants, RuleSource
from .validators import RuleValidator
from .transformers import RuleTransformer
from .fetchers import RuleFetcher
from .processors import RuleProcessor
from .merger import RulesMerger

__all__ = [
    "RuleConstants",
    "RuleSource",
    "RuleValidator",
    "RuleTransformer",
    "RuleFetcher",
    "RuleProcessor",
    "RulesMerger",
]
