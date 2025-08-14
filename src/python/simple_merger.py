#!/usr/bin/env python3
"""
简洁的规则合并器 - Linus式重构版本

去掉所有无用的抽象层，用最直接的方式解决问题。
核心原则：
1. 数据结构简单化 - 只有字符串列表的处理
2. 消除特殊情况 - 统一的处理流程
3. 代码清晰直接 - 不超过3层嵌套
"""

import os
import re
import sys
import yaml
import requests
import logging
from datetime import datetime
from typing import List, Dict, Set
from pathlib import Path


def setup_logging():
    """设置日志 - 简单直接"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def fetch_rules_from_url(url: str) -> List[str]:
    """
    从URL获取规则列表
    
    Args:
        url: 规则文件URL
        
    Returns:
        List[str]: 规则行列表
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 统一处理：不管是yaml还是txt，都按行分割
        content = response.text.strip()
        
        # 如果是yaml格式，尝试解析payload字段
        if content.startswith('payload:') or 'payload:' in content:
            try:
                data = yaml.safe_load(content)
                if isinstance(data, dict) and 'payload' in data:
                    return data['payload']
            except:
                pass  # 解析失败就按普通文本处理
        
        # 按行分割，过滤空行和注释
        lines = content.split('\n')
        return [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        
    except Exception as e:
        logging.error(f"获取规则失败 {url}: {e}")
        return []


def clean_rule(rule: str) -> str:
    """
    清理单条规则
    
    Args:
        rule: 原始规则
        
    Returns:
        str: 清理后的规则，如果无效返回空字符串
    """
    rule = rule.strip()
    
    # 跳过注释和空行
    if not rule or rule.startswith('#'):
        return ""
    
    # 移除常见的前缀标识符（如果有的话）
    prefixes = ['DOMAIN,', 'DOMAIN-SUFFIX,', 'DOMAIN-KEYWORD,', 'IP-CIDR,', 'GEOIP,']
    for prefix in prefixes:
        if rule.startswith(prefix):
            rule = rule[len(prefix):]
            break
    
    # 移除尾部的代理指令
    if ',' in rule:
        rule = rule.split(',')[0]
    
    return rule.strip()


def merge_rules(rule_lists: List[List[str]], target_type: str) -> List[str]:
    """
    合并多个规则列表
    
    Args:
        rule_lists: 多个规则列表
        target_type: 目标类型 (domain/ipcidr/classical)
        
    Returns:
        List[str]: 合并、去重、排序后的规则列表
    """
    all_rules: Set[str] = set()
    
    for rules in rule_lists:
        for rule in rules:
            cleaned = clean_rule(rule)
            if cleaned:
                # 根据目标类型进行基本验证
                if target_type == 'domain' and _is_valid_domain(cleaned):
                    all_rules.add(cleaned)
                elif target_type == 'ipcidr' and _is_valid_ip_cidr(cleaned):
                    all_rules.add(cleaned)
                elif target_type == 'classical':
                    all_rules.add(cleaned)
    
    return sorted(list(all_rules))


def _is_valid_domain(domain: str) -> bool:
    """检查是否为有效域名"""
    if not domain or len(domain) > 253:
        return False
    # 简单的域名格式检查
    return re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]*[a-zA-Z0-9])?$', domain) is not None


def _is_valid_ip_cidr(cidr: str) -> bool:
    """检查是否为有效IP/CIDR"""
    # 简单的IP/CIDR格式检查
    return re.match(r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$', cidr) is not None


def write_rules_file(output_path: str, rules: List[str]) -> None:
    """
    写入规则文件
    
    Args:
        output_path: 输出文件路径
        rules: 规则列表
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 更新时间: {timestamp}\n")
        f.write(f"# 规则数量: {len(rules)}\n")
        f.write("payload:\n")
        for rule in rules:
            f.write(f"  - {rule}\n")
    
    logging.info(f"生成规则文件: {output_path}, 共 {len(rules)} 条规则")


def load_config(config_path: str) -> List[Dict]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        List[Dict]: 配置列表
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def process_rule_group(config: Dict) -> None:
    """
    处理单个规则组
    
    Args:
        config: 规则组配置
    """
    if 'upstream' not in config or not config.get('path'):
        return
    
    target_type = config.get('behavior', 'classical')
    rule_lists = []
    
    # 获取所有上游规则
    for source_name, source_config in config['upstream'].items():
        if source_config.get('type') == 'http':
            url = source_config.get('url')
            if url:
                logging.info(f"获取规则: {source_name} from {url}")
                rules = fetch_rules_from_url(url)
                if rules:
                    rule_lists.append(rules)
    
    # 合并规则
    merged_rules = merge_rules(rule_lists, target_type)
    
    # 写入文件
    output_path = config['path']
    write_rules_file(output_path, merged_rules)


def move_output_to_provider():
    """
    将output目录的文件移动到Mihomo/Provider目录
    """
    # 简单直接的路径计算
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'output'
    provider_dir = script_dir.parent.parent / 'Mihomo' / 'Provider'
    
    if not output_dir.exists():
        logging.warning("output目录不存在")
        return
    
    provider_dir.mkdir(parents=True, exist_ok=True)
    
    # 移动所有yaml文件
    for yaml_file in output_dir.glob('*.yaml'):
        dest_file = provider_dir / yaml_file.name
        if dest_file.exists():
            dest_file.unlink()
        yaml_file.rename(dest_file)
        logging.info(f"移动文件: {yaml_file.name} -> Mihomo/Provider/")


def main():
    """主函数 - 简洁明了"""
    setup_logging()
    
    # 获取配置文件路径
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
    
    if not os.path.exists(config_path):
        logging.error(f"配置文件不存在: {config_path}")
        sys.exit(1)
    
    try:
        # 加载配置并处理
        config = load_config(config_path)
        
        logging.info("开始规则合并...")
        for rule_group in config:
            process_rule_group(rule_group)
        
        # 移动文件到最终位置
        move_output_to_provider()
        
        logging.info("规则合并完成！")
        
    except Exception as e:
        logging.error(f"执行失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
