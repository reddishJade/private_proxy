import yaml
import requests
import os
import logging
import sys
from typing import List, Dict, Optional, Literal, Set
import re
from dataclasses import dataclass
from datetime import datetime
import pytz  # 导入时区支持
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

# 配置日志输出格式和级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class RuleConstants:
    """规则相关的常量定义类"""
    RULE_TYPES: Dict[str, Set[str]] = None  # 存储不同类型规则的集合
    DOMAIN_PATTERN: str = r'^[a-zA-Z0-9_]([a-zA-Z0-9_-]*[a-zA-Z0-9_])?(\.[a-zA-Z0-9_]([a-zA-Z0-9_-]*[a-zA-Z0-9_])?)*$'  # 域名正则表达式（支持下划线）
    IPV4_CIDR_PATTERN: str = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'  # IPv4 CIDR正则表达式
    IPV6_CIDR_PATTERN: str = r'^([0-9a-fA-F:]+)/\d{1,3}$'  # IPv6 CIDR正则表达式

    def __post_init__(self):
        # 域名相关规则类型
        domain_rules = {
            'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 
            'DOMAIN-WILDCARD', 'DOMAIN-REGEX'
        }
        
        # IP相关规则类型
        ip_rules = {
            'IP-CIDR', 'IP-CIDR6', 'IP-SUFFIX', 'IP-ASN', 'GEOIP'
        }
        
        # 端口相关规则类型
        port_rules = {
            'DST-PORT', 'SRC-PORT', 'IN-PORT'
        }
        
        # 进程相关规则类型
        process_rules = {
            'PROCESS-PATH', 'PROCESS-NAME', 'PROCESS-PATH-REGEX', 'PROCESS-NAME-REGEX'
        }
        
        # 其他规则类型
        other_rules = {
            'IN-TYPE', 'IN-USER', 'IN-NAME', 'UID', 'NETWORK', 'DSCP'
        }

        # 初始化规则类型集合
        self.RULE_TYPES = {
            'domain': domain_rules,  # 域名规则类型
            'ipcidr': ip_rules,  # IP相关规则类型
            'classical': domain_rules | ip_rules | port_rules | process_rules | other_rules,  # 经典规则类型（包含所有）
        }

@dataclass
class RuleSource:
    """规则源配置数据类，定义规则来源的属性"""
    type: Literal['http', 'file']  # 规则源类型：http或文件
    url: str = ''  # HTTP URL
    path: str = ''  # 本地文件路径
    behavior: Literal['classical', 'ipcidr', 'domain'] = 'classical'  # 规则行为类型
    format: str = 'yaml'  # 规则文件格式

class RuleValidator:
    """规则验证器类"""
    def __init__(self):
        self.constants = RuleConstants()
        self.logger = logging.getLogger(__name__)

    def validate_classical_rule(self, rule: str) -> Optional[str]:
        """验证经典格式规则"""
        try:
            parts = rule.split(',')
            if len(parts) < 2:
                return None
                
            rule_type = parts[0]
            value = parts[1].strip()
                
            # 根据规则类型验证值的格式
            if rule_type in {'DOMAIN', 'DOMAIN-SUFFIX'}:
                return rule if self._is_valid_domain(value) else None
            elif rule_type == 'IP-CIDR':
                return rule if re.match(self.constants.IPV4_CIDR_PATTERN, value) else None
            elif rule_type == 'IP-CIDR6':
                return rule if re.match(self.constants.IPV6_CIDR_PATTERN, value) else None
            else:
                # 对于其他类型的规则，进行基本验证
                return rule if value else None
        except Exception as e:
            self.logger.debug(f"规则验证失败: {rule}, 错误: {str(e)}")
            return None

    def _is_valid_domain(self, domain: str) -> bool:
        """验证是否为有效域名，过滤脏数据"""
        if not re.match(self.constants.DOMAIN_PATTERN, domain):
            return False
            
        # 过滤明显的脏数据域名
        dirty_patterns = [
            r'.*_rul[e3]s[e3]t.*',  # 匹配 ruleset 变形
            r'.*_made_by_.*',       # 匹配 made_by 模式
            r'^[0-9][a-z0-9_]*_.*', # 匹配数字开头的混合字符串
            r'.*sukkaw.*',          # 匹配 sukkaw 相关
            r'.*5ukk4w.*'           # 匹配 5ukk4w 变形
        ]
        
        for pattern in dirty_patterns:
            if re.match(pattern, domain, re.IGNORECASE):
                return False
                
        return True

    def validate_ipcidr_rule(self, rule: str) -> Optional[str]:
        """验证IP CIDR规则"""
        try:
            # 如果是完整的规则格式（如 "IP-CIDR,192.168.1.0/24" 或 "IP-ASN,13335"）
            if ',' in rule:
                parts = rule.split(',')
                if len(parts) >= 2:
                    rule_type = parts[0]
                    value = parts[1].strip()
                    # 检查规则类型是否属于ipcidr类型
                    if rule_type in self.constants.RULE_TYPES.get('ipcidr', set()):
                        return rule
                return None
            # 如果是纯IP CIDR格式
            else:
                if re.match(self.constants.IPV4_CIDR_PATTERN, rule) or re.match(self.constants.IPV6_CIDR_PATTERN, rule):
                    return rule
                return None
        except Exception as e:
            self.logger.debug(f"IP CIDR规则验证失败: {rule}, 错误: {str(e)}")
            return None

    def validate_domain_rule(self, rule: str) -> Optional[str]:
        """验证域名规则"""
        try:
            # 如果是完整的规则格式（如 "DOMAIN,example.com" 或 "GEOSITE,youtube"）
            if ',' in rule:
                parts = rule.split(',')
                if len(parts) >= 2:
                    rule_type = parts[0]
                    value = parts[1].strip()
                    # 检查规则类型是否属于domain类型
                    if rule_type in self.constants.RULE_TYPES.get('domain', set()):
                        # 对于DOMAIN和DOMAIN-SUFFIX类型，验证域名有效性
                        if rule_type in {'DOMAIN', 'DOMAIN-SUFFIX'}:
                            validator = RuleValidator()
                            return rule if validator._is_valid_domain(value) else None
                        # 其他类型直接通过
                        return rule
                return None
            # 如果是纯域名格式
            else:
                # 处理域名格式：+.example.com 或 example.com
                if rule.startswith('+.'):
                    domain = rule[2:]
                    validator = RuleValidator()
                    return rule if validator._is_valid_domain(domain) else None
                else:
                    validator = RuleValidator()
                    return rule if validator._is_valid_domain(rule) else None
        except Exception as e:
            self.logger.debug(f"域名规则验证失败: {rule}, 错误: {str(e)}")
            return None

class RuleTransformer:
    """规则转换器类，用于在不同规则格式之间转换"""
    def __init__(self):
        self.validator = RuleValidator()

    def transform(self, rule: str, source_behavior: str, target_behavior: str) -> Optional[str]:
        """转换规则格式"""
        if not rule:
            return None
            
        # 如果源和目标behavior相同，直接验证
        if source_behavior == target_behavior:
            # 检查规则是否应该包含在目标behavior中
            if not self._should_include_rule(rule, target_behavior):
                return None

            validators = {
                'classical': self.validator.validate_classical_rule,
                'ipcidr': self.validator.validate_ipcidr_rule,
                'domain': self.validator.validate_domain_rule
            }
            validator = validators.get(source_behavior)
            return validator(rule) if validator else rule
            
        # 如果需要转换格式，先检查原始规则是否可以转换
        if not self._can_transform_rule(rule, source_behavior, target_behavior):
            return None
            
        transformer = self._get_transformer(source_behavior, target_behavior)
        if not transformer:
            return None
            
        transformed_rule = transformer(rule)
        return transformed_rule
        
    def _can_transform_rule(self, rule: str, source_behavior: str, target_behavior: str) -> bool:
        """检查规则是否可以从源behavior转换到目标behavior"""
        if not rule:
            return False
            
        try:
            rule_type = rule.split(',')[0]
            
            # 从classical转换到具体类型时，检查规则类型是否匹配
            if source_behavior == 'classical':
                target_types = self.validator.constants.RULE_TYPES.get(target_behavior, set())
                return rule_type in target_types
            
            return True
        except Exception:
            return False

    def _should_include_rule(self, rule: str, target_behavior: str) -> bool:
        """判断规则是否应该包含在目标behavior中"""
        if not rule:
            return False
            
        try:
            rule_type = rule.split(',')[0]
            allowed_types = self.validator.constants.RULE_TYPES.get(target_behavior, set())
            return rule_type in allowed_types
        except Exception:
            return False

    def _get_transformer(self, source_behavior: str, target_behavior: str):
        """获取对应的转换函数"""
        transformers = {
            ('classical', 'ipcidr'): self._classical_to_ipcidr,
            ('classical', 'domain'): self._classical_to_domain,
            ('ipcidr', 'classical'): self._ipcidr_to_classical,
            ('domain', 'classical'): self._domain_to_classical
        }
        return transformers.get((source_behavior, target_behavior))

    def _classical_to_ipcidr(self, rule: str) -> Optional[str]:
        """将经典格式转换为IP CIDR格式"""
        try:
            parts = rule.split(',')
            if len(parts) < 2:
                return None
            
            rule_type = parts[0]
            value = parts[1].strip()
            
            # 对于IP-CIDR和IP-CIDR6，提取IP地址部分
            if rule_type in {'IP-CIDR', 'IP-CIDR6'}:
                return value
            # 对于其他IP相关规则，保持完整格式（因为ipcidr behavior实际上可以包含各种IP相关规则）
            elif rule_type in self.validator.constants.RULE_TYPES.get('ipcidr', set()):
                return rule
            
            return None
        except Exception:
            return None
    
    def _classical_to_domain(self, rule: str) -> Optional[str]:
        """将经典格式转换为域名格式"""
        try:
            parts = rule.split(',')
            if len(parts) < 2:
                return None
                
            rule_type = parts[0]
            value = parts[1].strip()
            
            # 对于DOMAIN和DOMAIN-SUFFIX，转换为域名格式
            if rule_type == 'DOMAIN':
                if self.validator._is_valid_domain(value):
                    return value
            elif rule_type == 'DOMAIN-SUFFIX':
                if self.validator._is_valid_domain(value):
                    return '+.' + value
            # 对于其他域名相关规则，保持完整格式（因为domain behavior实际上可以包含各种域名相关规则）
            elif rule_type in self.validator.constants.RULE_TYPES.get('domain', set()):
                return rule
                
            return None
        except Exception:
            return None
    
    def _ipcidr_to_classical(self, rule: str) -> Optional[str]:
        """将IP CIDR格式转换为经典格式"""
        return "IP-CIDR6," + rule if ':' in rule else "IP-CIDR," + rule
    
    def _domain_to_classical(self, rule: str) -> Optional[str]:
        """将域名格式转换为经典格式"""
        if rule.startswith('+.'):
            suffix = rule[2:]
            if not re.match(self.validator.constants.DOMAIN_PATTERN, suffix):
                return None
            return f"DOMAIN-SUFFIX,{suffix}"
        
        if not re.match(self.validator.constants.DOMAIN_PATTERN, rule):
            return None
        return f"DOMAIN,{rule}"

class RuleFetcher:
    """规则获取器类"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_rules(self, source: RuleSource) -> List[str]:
        """根据源类型获取规则"""
        if source.type == 'http':
            return self._fetch_http_rules(source.url, source.format)
        elif source.type == 'file':
            return self._read_local_rules(source.path, source.format)
        return []

    def _fetch_http_rules(self, url: str, format: str) -> List[str]:
        """从HTTP源获取规则"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if format == 'yaml' or 'yaml' in content_type or url.endswith(('.yml', '.yaml')):
                data = yaml.safe_load(response.text)
                return data['payload'] if isinstance(data, dict) and 'payload' in data else data
            return response.text.splitlines()
        except Exception as e:
            self.logger.error(f"获取规则失败 {url}: {str(e)}", exc_info=True)
            return []

    def _read_local_rules(self, path: str, format: str) -> List[str]:
        """从本地文件读取规则"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if format == 'yaml':
                    data = yaml.safe_load(f)
                    return data['payload'] if isinstance(data, dict) and 'payload' in data else data
                return f.read().splitlines()
        except Exception as e:
            self.logger.error(f"读取本地规则失败 {path}: {str(e)}")
            return []

class RuleProcessor:
    """规则处理器类"""
    def __init__(self):
        self.transformer = RuleTransformer()
        self.logger = logging.getLogger(__name__)

    def clean_rule(self, rule: str) -> str:
        """清理规则，去除注释和空白"""
        rule = rule.strip()
        if rule.startswith('#'):
            return ''
        
        parts = re.split(r'\s+#', rule)
        return parts[0].strip() if len(parts) > 1 else rule.strip()

    def process_rules(self, rules: List[str], source_behavior: str, target_behavior: str) -> List[str]:
        """处理规则列表"""
        processed_rules = []
        for rule in rules:
            cleaned_rule = self.clean_rule(rule)
            if not cleaned_rule:
                continue
            transformed_rule = self.transformer.transform(cleaned_rule, source_behavior, target_behavior)
            if transformed_rule:
                processed_rules.append(transformed_rule)
        return processed_rules

class RulesMerger:
    """规则合并器类"""
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.fetcher = RuleFetcher()
        self.processor = RuleProcessor()

    def _load_config(self, path: str) -> dict:
        """加载配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"配置文件不存在: {path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"配置文件解析失败: {e}")
            raise

    def _process_source(self, source: Dict, target_behavior: str) -> List[str]:
        """处理单个规则源"""
        source_obj = RuleSource(
            type=source['type'],
            url=source.get('url', ''),
            path=source.get('path', ''),
            behavior=source.get('behavior', 'classical'),
            format=source.get('format', 'yaml')
        )
        rules = self.fetcher.fetch_rules(source_obj)
        return self.processor.process_rules(rules, source_obj.behavior, target_behavior)

    def _write_rules(self, output_path: str, rules: List[str]) -> None:
        """将处理后的规则写入文件"""
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 获取北京时间
            beijing_tz = pytz.timezone('Asia/Shanghai')
            current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# 更新时间: {current_time}（北京时间）\n")
                f.write(f"# 规则数量: {len(rules)}\n")
                yaml_str = yaml.dump(
                    {'payload': rules}, 
                    allow_unicode=True, 
                    indent=2,
                    default_flow_style=False,
                    sort_keys=False
                )
                formatted_yaml = yaml_str.replace('\n-', '\n  -')
                f.write(formatted_yaml)
            
            self.logger.info(f"已生成规则文件: {output_path}, 共 {len(rules)} 条规则")
        except Exception as e:
            self.logger.error(f"写入规则文件失败: {str(e)}", exc_info=True)
            raise

    def _move_rules_to_provider(self) -> None:
        """将output目录下的规则文件移动到Mihomo/Provider目录"""
        try:
            # 确保目标目录存在
            provider_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Mihomo', 'Provider')
            os.makedirs(provider_dir, exist_ok=True)
            
            # 获取output目录路径
            output_dir = os.path.join(os.path.dirname(__file__), 'output')
            
            # 确保output目录存在
            if not os.path.exists(output_dir):
                self.logger.warning("output目录不存在")
                return
                
            # 移动所有yaml文件
            for filename in os.listdir(output_dir):
                if filename.endswith('.yaml'):
                    src_path = os.path.join(output_dir, filename)
                    dst_path = os.path.join(provider_dir, filename)
                    try:
                        # 如果目标文件已存在，先删除
                        if os.path.exists(dst_path):
                            os.remove(dst_path)
                        os.rename(src_path, dst_path)
                        self.logger.info(f"已移动规则文件: {filename} 到 Mihomo/Provider/")
                    except Exception as e:
                        self.logger.error(f"移动文件 {filename} 失败: {str(e)}")
                        
        except Exception as e:
            self.logger.error(f"移动规则文件失败: {str(e)}")

    def merge_rules(self) -> None:
        """合并所有规则源的规则"""
        with ThreadPoolExecutor() as executor:
            for config in self.config:
                if 'upstream' not in config or not config.get('path'):
                    continue
                
                target_behavior = config.get('behavior', 'classical')
                futures = []
                
                # 并行处理所有规则源
                for source_name, source_config in config['upstream'].items():
                    future = executor.submit(self._process_source, source_config, target_behavior)
                    futures.append(future)
                
                merged_rules = []
                for future in as_completed(futures):
                    try:
                        rules = future.result()
                        merged_rules.extend(rules)
                    except Exception as e:
                        self.logger.error(f"处理规则源失败: {str(e)}")
                
                # 去重并排序
                merged_rules = sorted(set(merged_rules))
                self._write_rules(config['path'], merged_rules)
        
        # 在所有规则处理完成后，移动文件到Provider目录
        self._move_rules_to_provider()

def main():
    """主函数"""
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = 'config.yaml'
    
    merger = RulesMerger(config_path)
    merger.merge_rules()

if __name__ == '__main__':
    main()