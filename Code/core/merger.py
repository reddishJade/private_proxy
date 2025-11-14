"""
规则合并器主模块

提供规则合并的核心逻辑和文件操作功能
"""

import os
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytz
import yaml

from .constants import RuleSource
from .fetchers import RuleFetcher
from .processors import RuleProcessor


class RulesMerger:
    """
    规则合并器类

    负责协调整个规则合并流程，包括配置加载、规则获取、处理和输出
    """

    def __init__(self, config_path: str):
        """
        初始化合并器

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.fetcher = RuleFetcher()
        self.processor = RuleProcessor()
        # store the config path and filename so we can choose target directories later
        self._config_path = config_path
        self._config_filename = Path(config_path).name.lower()

    def _load_config(self, path: str) -> dict:
        """
        加载配置文件

        Args:
            path: 配置文件路径

        Returns:
            dict: 配置字典

        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: 配置文件解析失败
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error("配置文件不存在: %s", path)
            raise
        except yaml.YAMLError as e:
            self.logger.error("配置文件解析失败: %s", e)
            raise

    def _process_source(self, source: Dict, target_behavior: str) -> List[str]:
        """
        处理单个规则源

        Args:
            source: 源配置字典
            target_behavior: 目标行为类型

        Returns:
            List[str]: 处理后的规则列表
        """
        source_obj = RuleSource(
            type=source["type"],
            url=source.get("url", ""),
            path=source.get("path", ""),
            behavior=source.get("behavior", "classical"),
            format=source.get("format", "yaml"),
        )

        # 获取原始规则
        rules = self.fetcher.fetch_rules(source_obj)

        # 处理规则
        processed_rules = self.processor.process_rules(
            rules, source_obj.behavior, target_behavior
        )

        return processed_rules

    def _write_rules(self, output_path: str, rules: List[str], format_type: str = "yaml") -> None:
        """
        将处理后的规则写入文件

        Args:
            output_path: 输出文件路径
            rules: 规则列表

        Raises:
            Exception: 文件写入失败
        """
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # 获取北京时间
            beijing_tz = pytz.timezone("Asia/Shanghai")
            current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

            # 写入文件（根据 format_type 决定输出是 YAML 还是 plain text）
            with open(output_path, "w", encoding="utf-8") as f:
                # 添加头部注释（纯文本格式下以 # 开头的注释通常也可以被接受）
                f.write(f"# 更新时间: {current_time}（北京时间）\n")
                f.write(f"# 规则数量: {len(rules)}\n")

                # 文本格式（txt/text/list等）
                if isinstance(format_type, str) and format_type.lower() in {"txt", "text", "list"}:
                    for rule in rules:
                        f.write(rule.rstrip() + "\n")
                else:
                    # 生成YAML格式
                    yaml_str = yaml.dump(
                        {"payload": rules},
                        allow_unicode=True,
                        indent=2,
                        default_flow_style=False,
                        sort_keys=False,
                    )

                    # 格式化YAML输出
                    formatted_yaml = yaml_str.replace("\n-", "\n  -")
                    f.write(formatted_yaml)

            self.logger.info(
                "已生成规则文件: %s, 共 %d 条规则", output_path, len(rules)
            )

        except (OSError, IOError, yaml.YAMLError) as e:
            self.logger.error("写入规则文件失败: %s", str(e), exc_info=True)
            raise

    def _move_rules_to_provider(self) -> None:
        """
        将output目录下的规则文件移动到Mihomo/Provider目录

        这个方法会将生成的规则文件从临时output目录移动到最终的Provider目录
        """
        try:
            # 计算目标目录路径，默认是Mihomo/Provider
            provider_dir = self._get_provider_directory()

            # 如果是 rocket.yaml，则把文件移动到 Shadowrocket/ruleset
            if self._config_filename == "rocket.yaml":
                provider_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "Shadowrocket",
                    "ruleset",
                )
            output_dir = self._get_output_directory()

            os.makedirs(provider_dir, exist_ok=True)

            # 检查output目录是否存在
            if not os.path.exists(output_dir):
                self.logger.warning("output目录不存在: %s", output_dir)
                return

            # 移动output目录中所有支持的文件（包括 .yaml/.yml/.txt/.list）
            self._move_output_files(output_dir, provider_dir)

        except (OSError, IOError) as e:
            self.logger.error("移动规则文件失败: %s", str(e))

    def _get_provider_directory(self) -> str:
        """
        获取Provider目录路径

        Returns:
            str: Provider目录的绝对路径
        """
        # 从 core/merger.py -> Code/core -> Code -> 根目录 -> Mihomo/Provider
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "Mihomo",
            "Provider",
        )

    def _get_output_directory(self) -> str:
        """
        获取output目录路径

        Returns:
            str: output目录的绝对路径
        """
        # 从当前文件位置计算output目录：core/../output
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

    def get_target_provider_dir(self) -> str:
        """
        返回将要把生成文件迁移到的目标目录（Mihomo/Provider 或 Shadowrocket/ruleset）
        """
        if self._config_filename == "rocket.yaml":
            return os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "Shadowrocket",
                "ruleset",
            )
        return self._get_provider_directory()

    def _move_output_files(self, output_dir: str, provider_dir: str) -> None:
        """
        移动YAML文件从output目录到provider目录

        Args:
            output_dir: 源目录
            provider_dir: 目标目录
        """
        supported_ext = (".yaml", ".yml", ".txt", ".list")
        for filename in os.listdir(output_dir):
            if any(filename.endswith(ext) for ext in supported_ext):
                src_path = os.path.join(output_dir, filename)
                dst_path = os.path.join(provider_dir, filename)
                try:
                    # 如果目标文件已存在，先删除
                    if os.path.exists(dst_path):
                        os.remove(dst_path)
                    os.rename(src_path, dst_path)
                    # 显示实际的目标目录
                    # provider_dir 可能是 Mihomo/Provider 或 Shadowrocket/ruleset
                    self.logger.info("已移动规则文件: %s 到 %s", filename, provider_dir)
                except (OSError, IOError) as e:
                    self.logger.error("移动文件 %s 失败: %s", filename, str(e))

    def merge_rules(self) -> None:
        """
        合并所有规则源的规则

        这是主要的入口方法，协调整个规则合并流程
        """
        with ThreadPoolExecutor() as executor:
            for config in self.config:
                if "upstream" not in config or not config.get("path"):
                    continue

                # 处理单个配置项
                self._process_config_item(config, executor)

        # 在所有规则处理完成后，移动文件到Provider目录
        self._move_rules_to_provider()

    def _process_config_item(self, config: Dict, executor: ThreadPoolExecutor) -> None:
        """
        处理单个配置项

        Args:
            config: 配置项字典
            executor: 线程池执行器
        """
        target_behavior = config.get("behavior", "classical")
        futures = []

        # 并行处理所有规则源
        for _, source_config in config["upstream"].items():
            future = executor.submit(
                self._process_source, source_config, target_behavior
            )
            futures.append(future)

        # 收集所有处理结果
        merged_rules = self._collect_processing_results(futures)

        # 去重并排序
        final_rules = self.processor.deduplicate_and_sort(merged_rules)

        # 写入文件，根据配置格式决定输出格式
        format_type = config.get("format", "yaml")
        self._write_rules(config["path"], final_rules, format_type)

    def _collect_processing_results(self, futures: List) -> List[str]:
        """
        收集并行处理的结果

        Args:
            futures: Future对象列表

        Returns:
            List[str]: 合并后的规则列表
        """
        merged_rules = []

        for future in as_completed(futures):
            try:
                rules = future.result()
                merged_rules.extend(rules)
            except (OSError, IOError, yaml.YAMLError, ValueError) as e:
                self.logger.error("处理规则源失败: %s", str(e))

        return merged_rules
