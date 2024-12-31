import yaml
import requests
import os
import logging
from typing import List, Dict, Optional, Literal, Set
import re
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class RuleConstants:
    """规则相关的常量定义"""
    RULE_TYPES: Dict[str, Set[str]] = None
    DOMAIN_PATTERN: str = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$'
    IPV4_CIDR_PATTERN: str = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    IPV6_CIDR_PATTERN: str = r'^([0-9a-fA-F:]+)/\d{1,3}$'

    def __post_init__(self):
        self.RULE_TYPES = {
            'classical': {'DOMAIN', 'DOMAIN-SUFFIX', 'IP-CIDR', 'IP-CIDR6'},
            'ipcidr': {'IP-CIDR', 'IP-CIDR6'},
            'domain': {'DOMAIN', 'DOMAIN-SUFFIX'}
        }

@dataclass
class RuleSource:
    """规则源配置数据类"""
    type: Literal['http', 'file']
    url: str = ''
    path: str = ''
    behavior: Literal['classical', 'ipcidr', 'domain'] = 'classical'
    format: str = 'yaml'

class RuleValidator:
    """规则验证器类"""
    def __init__(self):
        self.constants = RuleConstants()
        self.logger = logging.getLogger(__name__)

    def validate_classical_rule(self, rule: str) -> Optional[str]:
        try:
            parts = rule.split(',')
            if len(parts) < 2:
                return None
                
            rule_type = parts[0]
            value = parts[1].strip()
                
            if rule_type in {'DOMAIN', 'DOMAIN-SUFFIX'}:
                return rule if re.match(self.constants.DOMAIN_PATTERN, value) else None
            elif rule_type == 'IP-CIDR':
                return rule if re.match(self.constants.IPV4_CIDR_PATTERN, value) else None
            elif rule_type == 'IP-CIDR6':
                return rule if re.match(self.constants.IPV6_CIDR_PATTERN, value) else None
        except Exception as e:
            self.logger.debug(f"规则验证失败: {rule}, 错误: {str(e)}")
            return None
        return rule

    def validate_ipcidr_rule(self, rule: str) -> Optional[str]:
        return rule

    def validate_domain_rule(self, rule: str) -> Optional[str]:
        return rule

class RuleTransformer:
    """规则转换器类"""
    def __init__(self):
        self.validator = RuleValidator()

    def transform(self, rule: str, source_behavior: str, target_behavior: str) -> Optional[str]:
        if not rule:
            return None
            
        if source_behavior == target_behavior:
            validators = {
                'classical': self.validator.validate_classical_rule,
                'ipcidr': self.validator.validate_ipcidr_rule,
                'domain': self.validator.validate_domain_rule
            }
            validator = validators.get(source_behavior)
            return validator(rule) if validator else rule
            
        transformer = self._get_transformer(source_behavior, target_behavior)
        return transformer(rule) if transformer else None

    def _get_transformer(self, source_behavior: str, target_behavior: str):
        transformers = {
            ('classical', 'ipcidr'): self._classical_to_ipcidr,
            ('classical', 'domain'): self._classical_to_domain,
            ('ipcidr', 'classical'): self._ipcidr_to_classical,
            ('domain', 'classical'): self._domain_to_classical
        }
        return transformers.get((source_behavior, target_behavior))

    def _classical_to_ipcidr(self, rule: str) -> Optional[str]:
        if not (rule.startswith('IP-CIDR,') or rule.startswith('IP-CIDR6,')):
            return None
        parts = rule.split(',')
        return parts[1].strip() if len(parts) >= 2 else None
    
    def _classical_to_domain(self, rule: str) -> Optional[str]:
        parts = rule.split(',')
        if len(parts) < 2:
            return None
            
        domain = parts[1].strip()
        if not re.match(RuleConstants.DOMAIN_PATTERN, domain):
            return None
            
        if rule.startswith('DOMAIN,'):
            return domain
        elif rule.startswith('DOMAIN-SUFFIX,'):
            return '+.' + domain
        return None
    
    def _ipcidr_to_classical(self, rule: str) -> Optional[str]:
        return "IP-CIDR6," + rule if ':' in rule else "IP-CIDR," + rule
    
    def _domain_to_classical(self, rule: str) -> Optional[str]:
        if rule.startswith('+.'):
            suffix = rule[2:]
            if not re.match(RuleConstants.DOMAIN_PATTERN, suffix):
                return None
            return f"DOMAIN-SUFFIX,{suffix}"
        
        if not re.match(RuleConstants.DOMAIN_PATTERN, rule):
            return None
        return f"DOMAIN,{rule}"

class RuleFetcher:
    """规则获取器类"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_rules(self, source: RuleSource) -> List[str]:
        if source.type == 'http':
            return self._fetch_http_rules(source.url, source.format)
        elif source.type == 'file':
            return self._read_local_rules(source.path, source.format)
        return []

    def _fetch_http_rules(self, url: str, format: str) -> List[str]:
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
        rule = rule.strip()
        if rule.startswith('#'):
            return ''
        
        parts = re.split(r'\s+#', rule)
        return parts[0].strip() if len(parts) > 1 else rule.strip()

    def process_rules(self, rules: List[str], source_behavior: str, target_behavior: str) -> List[str]:
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
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.fetcher = RuleFetcher()
        self.processor = RuleProcessor()

    def _load_config(self, path: str) -> dict:
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
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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

    def merge_rules(self) -> None:
        with ThreadPoolExecutor() as executor:
            for config in self.config:
                if 'upstream' not in config or not config.get('path'):
                    continue
                
                target_behavior = config.get('behavior', 'classical')
                futures = []
                
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
                
                merged_rules = sorted(set(merged_rules))
                self._write_rules(config['path'], merged_rules)

def main():
    merger = RulesMerger('config.yaml')
    merger.merge_rules()

if __name__ == '__main__':
    main()