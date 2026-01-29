"""
规则获取器模块

提供从HTTP源和本地文件获取规则的功能
"""

import logging
from typing import List

import requests
import yaml

from .constants import RuleSource


class RuleFetcher:
    """
    规则获取器类

    负责从不同来源（HTTP和本地文件）获取规则数据
    """

    def __init__(self):
        """初始化获取器"""
        self.logger = logging.getLogger(__name__)

    def fetch_rules(self, source: RuleSource) -> List[str]:
        """
        根据源类型获取规则

        Args:
            source: 规则源配置

        Returns:
            List[str]: 获取到的规则列表
        """
        if source.type == "http":
            return self._fetch_http_rules(source.url, source.format)
        elif source.type == "file":
            return self._read_local_rules(source.path, source.format)
        return []

    def _fetch_http_rules(self, url: str, file_format: str) -> List[str]:
        """
        从HTTP源获取规则

        Args:
            url: 规则文件的URL
            format: 文件格式（yaml或text）

        Returns:
            List[str]: 获取到的规则列表
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")

            # 判断是否为YAML格式
            is_yaml = self._is_yaml_format(
                file_format, content_type, url, response.text
            )

            if is_yaml:
                return self._parse_yaml_content(response.text, url)
            else:
                # 文本格式，按行分割
                return response.text.splitlines()

        except requests.RequestException as e:
            self.logger.error("获取规则失败 %s: %s", url, str(e))
            return []
        except (yaml.YAMLError, UnicodeDecodeError, ValueError) as e:
            self.logger.error("处理规则失败 %s: %s", url, str(e), exc_info=True)
            return []

    def _is_yaml_format(
        self, file_format: str, content_type: str, url: str, text: str
    ) -> bool:
        """
        判断是否为YAML格式

        Args:
            format: 指定的格式
            content_type: HTTP响应的Content-Type
            url: 文件URL
            text: 响应文本

        Returns:
            bool: 是否为YAML格式
        """
        return (
            file_format == "yaml"
            or "yaml" in content_type
            or url.endswith((".yml", ".yaml"))
            or text.strip().startswith("payload:")
        )

    def _parse_yaml_content(self, content: str, url: str) -> List[str]:
        """
        解析YAML内容

        Args:
            content: YAML内容字符串
            url: 源URL（用于日志）

        Returns:
            List[str]: 解析后的规则列表
        """
        try:
            data = yaml.safe_load(content)
            if isinstance(data, dict) and "payload" in data:
                return data["payload"] if isinstance(data["payload"], list) else []
            elif isinstance(data, list):
                return data
            else:
                self.logger.warning("YAML格式不正确，回退到文本处理: %s", url)
                return content.splitlines()
        except yaml.YAMLError as e:
            self.logger.warning(
                "YAML解析失败，回退到文本处理: %s, 错误: %s", url, str(e)
            )
            return content.splitlines()

    def _read_local_rules(self, path: str, file_format: str) -> List[str]:
        """
        从本地文件读取规则

        Args:
            path: 本地文件路径
            format: 文件格式

        Returns:
            List[str]: 读取到的规则列表
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

                if self._is_local_yaml_format(file_format, path):
                    return self._parse_yaml_content(content, path)
                else:
                    return content.splitlines()

        except (IOError, OSError, yaml.YAMLError, UnicodeDecodeError) as e:
            self.logger.error("读取本地规则失败 %s: %s", path, str(e))
            return []

    def _is_local_yaml_format(self, file_format: str, path: str) -> bool:
        """
        判断本地文件是否为YAML格式

        Args:
            format: 指定的格式
            path: 文件路径

        Returns:
            bool: 是否为YAML格式
        """
        return file_format == "yaml" or path.endswith((".yml", ".yaml"))
