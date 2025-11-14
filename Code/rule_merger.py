#!/usr/bin/env python3
"""
规则合并器 - 主入口模块

这是一个用于合并和处理各种格式规则文件的工具。
支持从HTTP源和本地文件获取规则，并进行格式转换、验证和合并。

主要功能：
- 支持多种规则格式（classical、ipcidr、domain）
- 支持HTTP和本地文件源
- 自动规则验证和清理
- 并行处理提高性能
- 自动去重和排序

使用方法：
    python rule_merger_main.py [config_file]

配置文件格式请参考 config.yaml 示例文件。
"""

import sys
import logging
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent))

from core import RulesMerger


def setup_logging():
    """
    设置日志配置
    
    配置日志格式和级别，确保在整个应用程序中有一致的日志输出
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_config_path() -> str:
    """
    获取配置文件路径
    
    从命令行参数获取配置文件路径，如果未提供则使用默认的 config.yaml
    
    Returns:
        str: 配置文件路径
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        # 处理帮助参数
        if arg in ['-h', '--help', 'help']:
            print_help()
            sys.exit(0)
        return arg
    else:
        return 'config.yaml'


def print_help():
    """打印帮助信息"""
    help_text = """
规则合并器 v2.0

用法:
    python rule_merger_main.py [配置文件路径]
    python rule_merger_main.py -h/--help

参数:
    配置文件路径    可选，默认使用 config.yaml
    -h, --help     显示此帮助信息

示例:
    python rule_merger_main.py                    # 使用默认配置
    python rule_merger_main.py my_config.yaml     # 使用指定配置

工具命令:
    python utils.py analyze <规则文件>             # 分析规则文件
    python utils.py validate <配置文件>            # 验证配置文件
    python config_docs.py                         # 创建示例配置

    """
    print(help_text)


def validate_config_file(config_path: str) -> bool:
    """
    验证配置文件是否存在
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        bool: 配置文件是否存在且可读
    """
    config_file = Path(config_path)
    if not config_file.exists():
        logging.error(f"配置文件不存在: {config_path}")
        return False
    
    if not config_file.is_file():
        logging.error(f"指定的路径不是文件: {config_path}")
        return False
        
    return True


def main():
    """
    主函数
    
    程序的入口点，负责：
    1. 设置日志
    2. 获取和验证配置文件
    3. 创建并运行规则合并器
    4. 处理异常情况
    """
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 获取配置文件路径
        config_path = get_config_path()
        logger.info(f"使用配置文件: {config_path}")
        
        # 验证配置文件
        if not validate_config_file(config_path):
            sys.exit(1)
        
        # 创建合并器并执行合并
        logger.info("开始规则合并流程...")
        merger = RulesMerger(config_path)
        merger.merge_rules()
        logger.info("规则合并完成！")
        # 输出实际迁移目标路径
        try:
            target_dir = merger.get_target_provider_dir()
            logger.info("所有规则文件已迁移到 %s 目录下。", target_dir)
        except Exception:
            # 如果因某种原因无法获取，回退到以前的静态提示
            config_basename = Path(config_path).name.lower()
            if config_basename == 'rocket.yaml':
                logger.info("所有规则文件已迁移到 Shadowrocket/ruleset 目录下。")
            else:
                logger.info("所有规则文件已迁移到 Mihomo/Provider 目录下。")
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
