"""Mihomo规则文件变更检测模块。"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def get_git_file_content(file_path: str) -> Optional[str]:
    """获取 Git 中最新提交的单个文件内容"""
    try:
        # 使用'/'作为路径分隔符，以兼容不同系统
        git_path = file_path.replace("\\", "/")
        content = subprocess.check_output(
            ["git", "show", f"HEAD:{git_path}"],
            encoding="utf-8",
            stderr=subprocess.PIPE,
        )
        return content
    except subprocess.CalledProcessError:
        # 如果文件是新增的，git show会失败
        return None


def get_payload(content: str) -> Optional[List[str]]:
    """从文件内容中解析并提取 payload"""
    try:
        data: Dict[str, Any] = yaml.safe_load(content)
        if data and "payload" in data:
            return data["payload"]
    except yaml.YAMLError:
        return None
    return None


def compare_rules(base_path: Path) -> bool:
    """
    比较指定路径下所有.yaml规则文件的payload是否发生变化。

    :param base_path: 规则文件所在的根目录。
    :return: 如果有任何文件的payload发生变化，则返回True，否则返回False。
    """
    rule_files = list(base_path.glob("**/*.yaml"))
    if not rule_files:
        print("未找到任何.yaml规则文件。")
        return False

    print(f"开始检测 {len(rule_files)} 个规则文件...")

    for file_path in rule_files:
        relative_path = str(file_path)
        print(f"  - 正在处理: {relative_path}")

        # 获取当前文件内容
        try:
            current_content = file_path.read_text(encoding="utf-8")
        except IOError as e:
            print(f"    - 错误: 无法读取当前文件: {e}")
            continue

        current_payload = get_payload(current_content)

        # 获取 Git 中的文件内容
        git_content = get_git_file_content(relative_path)

        if git_content is None:
            # 新增文件，且包含有效payload，视为有变更
            if current_payload:
                print(f"    - 发现新增规则文件: {relative_path}")
                return True
            else:
                # 新增文件但无payload，跳过
                continue

        git_payload = get_payload(git_content)

        # 如果任一版本无法解析出payload，但另一个可以，则视为变更
        if (current_payload is None) != (git_payload is None):
            print(f"    - 发现payload结构变更: {relative_path}")
            return True

        # 如果两个版本都无法解析，或者内容相同，则无变更
        if current_payload is None and git_payload is None:
            continue

        # 比较 payload 内容
        if current_payload is not None and git_payload is not None:
            if set(current_payload) != set(git_payload):
                print(f"    - 发现规则内容变更: {relative_path}")
                return True

    print("所有规则文件均未检测到实质性变更。")
    return False


def main():
    """主函数：解析命令行参数并执行规则检测。"""
    parser = argparse.ArgumentParser(
        description="检测Mihomo规则文件的payload是否发生变化。"
    )
    parser.add_argument(
        "check_path", type=str, help="需要检测的规则文件所在的目录路径。"
    )
    args = parser.parse_args()

    rules_path = Path(args.check_path)
    if not rules_path.is_dir():
        print(f"错误: 路径 '{args.check_path}' 不是一个有效的目录。")
        sys.exit(1)

    has_changed = compare_rules(rules_path)

    if has_changed:
        print("检测到规则变更。")
        # 在GitHub Actions中设置输出变量
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
                f.write("has_changed=true\n")
    else:
        print("未检测到规则变更。")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
                f.write("has_changed=false\n")


if __name__ == "__main__":
    main()
