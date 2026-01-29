"""
规则相关常量定义模块

包含规则类型定义、正则表达式模式等常量
"""

from dataclasses import dataclass, field
from typing import Dict, Set, Literal


@dataclass
class RuleConstants:
    """
    规则相关的常量定义类

    定义了各种规则类型的分类和用于验证的正则表达式模式
    """

    rule_types: Dict[str, Set[str]] = field(
        default_factory=dict
    )  # 存储不同类型规则的集合

    # 域名正则表达式（支持下划线）
    domain_pattern: str = (
        r"^[a-zA-Z0-9_]([a-zA-Z0-9_-]*[a-zA-Z0-9_])?(\.[a-zA-Z0-9_]([a-zA-Z0-9_-]*[a-zA-Z0-9_])?)*$"
    )

    # IPv4 CIDR正则表达式
    ipv4_cidr_pattern: str = r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"

    # IPv6 CIDR正则表达式
    ipv6_cidr_pattern: str = r"^([0-9a-fA-F:]+)/\d{1,3}$"

    def __post_init__(self):
        """初始化规则类型分类"""
        # 域名相关规则类型
        domain_rules = {
            "DOMAIN",
            "DOMAIN-SUFFIX",
            "DOMAIN-KEYWORD",
            "DOMAIN-WILDCARD",
            "DOMAIN-REGEX",
        }

        # IP相关规则类型
        ip_rules = {"IP-CIDR", "IP-CIDR6", "IP-SUFFIX", "IP-ASN", "GEOIP"}

        # 端口相关规则类型
        port_rules = {"DST-PORT", "SRC-PORT", "IN-PORT"}

        # 进程相关规则类型
        process_rules = {
            "PROCESS-PATH",
            "PROCESS-NAME",
            "PROCESS-PATH-REGEX",
            "PROCESS-NAME-REGEX",
        }

        # 其他规则类型
        other_rules = {"IN-TYPE", "IN-USER", "IN-NAME", "UID", "NETWORK", "DSCP"}

        # 初始化规则类型集合
        self.rule_types = {
            "domain": domain_rules,  # 域名规则类型
            "ipcidr": ip_rules,  # IP相关规则类型
            "classical": domain_rules
            | ip_rules
            | port_rules
            | process_rules
            | other_rules,  # 经典规则类型（包含所有）
        }


@dataclass
class RuleSource:
    """
    规则源配置数据类

    定义规则来源的属性，包括类型、URL、路径、行为类型和格式
    """

    type: Literal["http", "file"]  # 规则源类型：http或文件
    url: str = ""  # HTTP URL
    path: str = ""  # 本地文件路径
    behavior: Literal["classical", "ipcidr", "domain"] = "classical"  # 规则行为类型
    format: str = "yaml"  # 规则文件格式


# 脏数据过滤模式常量
DIRTY_DOMAIN_PATTERNS = [
    r".*_rul[e3]s[e3]t.*",  # 匹配 ruleset 变形
    r".*_made_by_.*",  # 匹配 made_by 模式
    r"^[0-9][a-z0-9_]*_.*",  # 匹配数字开头的混合字符串
    r".*sukkaw.*",  # 匹配 sukkaw 相关
    r".*5ukk4w.*",  # 匹配 5ukk4w 变形
    r".*update.*time.*",  # 匹配包含update time的脏数据
    r".*[0-9]{4}-[0-9]{2}-[0-9]{2}.*",  # 匹配包含日期的脏数据
]

DIRTY_CONTENT_PATTERNS = [
    r".*update.*time.*",
    r".*更新时间.*",
    r".*规则数量.*",
    r".*[0-9]{4}-[0-9]{2}-[0-9]{2}.*",
    r".*payload.*",
    r".*---.*",
]
