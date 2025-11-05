"""
工具模块

提供一些实用的工具功能，如规则统计、配置验证等
"""

import yaml
import logging
from typing import Dict, List, Tuple
from pathlib import Path
from collections import Counter

from core import RuleValidator, RuleConstants


class RuleAnalyzer:
    """
    规则分析器
    
    提供规则统计和分析功能
    """
    
    def __init__(self):
        """初始化分析器"""
        self.validator = RuleValidator()
        self.constants = RuleConstants()
        self.logger = logging.getLogger(__name__)

    def analyze_rules(self, rules: List[str]) -> Dict:
        """
        分析规则列表
        
        Args:
            rules: 规则列表
            
        Returns:
            Dict: 分析结果
        """
        stats = {
            'total_rules': len(rules),
            'valid_rules': 0,
            'invalid_rules': 0,
            'rule_types': Counter(),
            'domains': 0,
            'ip_cidrs': 0,
            'empty_or_comments': 0
        }
        
        for rule in rules:
            rule = rule.strip()
            
            # 统计空行和注释
            if not rule or rule.startswith('#'):
                stats['empty_or_comments'] += 1
                continue
            
            # 验证规则
            validated_rule = self.validator.validate_classical_rule(rule)
            if validated_rule:
                stats['valid_rules'] += 1
                
                # 统计规则类型
                rule_type = self._extract_rule_type(validated_rule)
                if rule_type:
                    stats['rule_types'][rule_type] += 1
                    
                    # 统计域名和IP规则
                    if rule_type in self.constants.RULE_TYPES.get('domain', set()):
                        stats['domains'] += 1
                    elif rule_type in self.constants.RULE_TYPES.get('ipcidr', set()):
                        stats['ip_cidrs'] += 1
            else:
                stats['invalid_rules'] += 1
        
        return stats

    def _extract_rule_type(self, rule: str) -> str:
        """
        提取规则类型
        
        Args:
            rule: 规则字符串
            
        Returns:
            str: 规则类型
        """
        try:
            if ',' in rule:
                return rule.split(',')[0].strip()
            return 'UNKNOWN'
        except Exception:
            return 'UNKNOWN'

    def print_analysis_report(self, stats: Dict, title: str = "规则分析报告"):
        """
        打印分析报告
        
        Args:
            stats: 分析统计结果
            title: 报告标题
        """
        print(f"{'='*50}")
        print(f"{title:^50}")
        print(f"{'='*50}")
        
        print(f"总规则数: {stats['total_rules']}")
        print(f"有效规则: {stats['valid_rules']}")
        print(f"无效规则: {stats['invalid_rules']}")
        print(f"空行/注释: {stats['empty_or_comments']}")
        print(f"域名规则: {stats['domains']}")
        print(f"IP规则: {stats['ip_cidrs']}")
        
        if stats['rule_types']:
            print()
            print("规则类型分布:")
            for rule_type, count in stats['rule_types'].most_common():
                print(f"  {rule_type}: {count}")


class ConfigValidator:
    """
    配置文件验证器
    """
    
    def __init__(self):
        """初始化验证器"""
        self.logger = logging.getLogger(__name__)

    def validate_config(self, config_path: str) -> Tuple[bool, List[str]]:
        """
        验证配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误信息列表)
        """
        errors = []
        
        try:
            # 检查文件是否存在
            if not Path(config_path).exists():
                errors.append(f"配置文件不存在: {config_path}")
                return False, errors
            
            # 加载配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 验证配置结构
            if not isinstance(config, list):
                errors.append("配置文件必须是一个列表")
                return False, errors
            
            # 验证每个配置项
            for i, item in enumerate(config):
                item_errors = self._validate_config_item(item, i)
                errors.extend(item_errors)
            
        except yaml.YAMLError as e:
            errors.append(f"YAML解析错误: {e}")
        except Exception as e:
            errors.append(f"配置验证出错: {e}")
        
        return len(errors) == 0, errors

    def _validate_config_item(self, item: Dict, index: int) -> List[str]:
        """
        验证单个配置项
        
        Args:
            item: 配置项字典
            index: 配置项索引
            
        Returns:
            List[str]: 错误信息列表
        """
        errors = []
        prefix = f"配置项 {index + 1}"
        
        # 检查必需字段
        required_fields = ['path', 'upstream']
        for field in required_fields:
            if field not in item:
                errors.append(f"{prefix}: 缺少必需字段 '{field}'")
        
        # 验证behavior字段
        if 'behavior' in item:
            valid_behaviors = ['classical', 'domain', 'ipcidr']
            if item['behavior'] not in valid_behaviors:
                errors.append(f"{prefix}: 无效的behavior值 '{item['behavior']}'，"
                             f"有效值为: {valid_behaviors}")
        
        # 验证upstream配置
        if 'upstream' in item:
            upstream_errors = self._validate_upstream_config(item['upstream'], prefix)
            errors.extend(upstream_errors)
        
        return errors

    def _validate_upstream_config(self, upstream: Dict, prefix: str) -> List[str]:
        """
        验证upstream配置
        
        Args:
            upstream: upstream配置字典
            prefix: 错误消息前缀
            
        Returns:
            List[str]: 错误信息列表
        """
        errors = []
        
        if not isinstance(upstream, dict):
            errors.append(f"{prefix}: upstream必须是一个字典")
            return errors
        
        for source_name, source_config in upstream.items():
            source_errors = self._validate_source_config(source_config, f"{prefix}.{source_name}")
            errors.extend(source_errors)
        
        return errors

    def _validate_source_config(self, source: Dict, prefix: str) -> List[str]:
        """
        验证源配置
        
        Args:
            source: 源配置字典
            prefix: 错误消息前缀
            
        Returns:
            List[str]: 错误信息列表
        """
        errors = []
        
        # 检查type字段
        if 'type' not in source:
            errors.append(f"{prefix}: 缺少必需字段 'type'")
        elif source['type'] not in ['http', 'file']:
            errors.append(f"{prefix}: 无效的type值 '{source['type']}'，有效值为: ['http', 'file']")
        
        # 根据type验证相关字段
        if source.get('type') == 'http' and 'url' not in source:
            errors.append(f"{prefix}: http类型源缺少url字段")
        elif source.get('type') == 'file' and 'path' not in source:
            errors.append(f"{prefix}: file类型源缺少path字段")
        
        # 验证behavior字段
        if 'behavior' in source:
            valid_behaviors = ['classical', 'domain', 'ipcidr']
            if source['behavior'] not in valid_behaviors:
                errors.append(f"{prefix}: 无效的behavior值 '{source['behavior']}'")
        
        return errors


def analyze_rule_file(file_path: str):
    """
    分析规则文件的工具函数
    
    Args:
        file_path: 规则文件路径
    """
    analyzer = RuleAnalyzer()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if file_path.endswith(('.yml', '.yaml')):
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict) and 'payload' in data:
                        rules = data['payload'] if isinstance(data['payload'], list) else []
                    elif isinstance(data, list):
                        rules = data
                    else:
                        # 如果YAML解析失败，尝试按行分割
                        rules = content.splitlines()
                except yaml.YAMLError:
                    rules = content.splitlines()
            else:
                rules = content.splitlines()
        
        stats = analyzer.analyze_rules(rules)
        analyzer.print_analysis_report(stats, f"文件分析: {file_path}")
        
    except Exception as e:
        print(f"分析文件失败 {file_path}: {e}")


def validate_config_file(config_path: str):
    """
    验证配置文件的工具函数
    
    Args:
        config_path: 配置文件路径
    """
    validator = ConfigValidator()
    is_valid, errors = validator.validate_config(config_path)
    
    if is_valid:
        print(f"✅ 配置文件 {config_path} 验证通过")
    else:
        print(f"❌ 配置文件 {config_path} 验证失败:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python utils.py analyze <rule_file>  # 分析规则文件")
        print("  python utils.py validate <config_file>  # 验证配置文件")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze" and len(sys.argv) >= 3:
        analyze_rule_file(sys.argv[2])
    elif command == "validate" and len(sys.argv) >= 3:
        validate_config_file(sys.argv[2])
    else:
        print("无效的命令或参数")
