#!/bin/bash

# Git 自动化提交清理 - 完整解决方案

echo "🧹 Git 提交清理工具"
echo "===================="

# 步骤1: 检查当前状态
check_repo_status() {
    echo "📊 检查仓库状态..."

    # 检查未跟踪文件
    untracked=$(git ls-files --others --exclude-standard)
    if [ ! -z "$untracked" ]; then
        echo "📁 发现未跟踪的文件:"
        echo "$untracked"
    fi

    # 检查未暂存的更改
    unstaged=$(git diff --name-only)
    if [ ! -z "$unstaged" ]; then
        echo "📝 发现未暂存的更改:"
        echo "$unstaged"
    fi

    # 检查已暂存的更改
    staged=$(git diff --cached --name-only)
    if [ ! -z "$staged" ]; then
        echo "📋 发现已暂存的更改:"
        echo "$staged"
    fi
}

# 步骤2: 配置Git用户信息
setup_git_identity() {
    # 检查git身份配置
    if ! git config user.name >/dev/null 2>&1 || ! git config user.email >/dev/null 2>&1; then
        echo "⚠️  Git身份信息未配置"

        current_name=$(git config user.name 2>/dev/null || echo "")
        current_email=$(git config user.email 2>/dev/null || echo "")

        echo "当前配置："
        echo "  姓名: ${current_name:-未设置}"
        echo "  邮箱: ${current_email:-未设置}"

        read -p "请输入您的姓名: " name
        read -p "请输入您的邮箱: " email

        git config user.name "$name"
        git config user.email "$email"

        echo "✅ Git身份配置完成"
    fi
}

# 步骤3: 清理工作目录
clean_working_directory() {
    echo "🧽 清理工作目录..."

    echo "选择清理方式:"
    echo "1. 暂存所有更改并提交"
    echo "2. 丢弃所有未跟踪文件和更改（危险！）"
    echo "3. 手动处理（退出脚本）"

    read -p "请选择 (1-3): " choice

    case $choice in
        1)
            echo "暂存并提交所有更改..."
            setup_git_identity  # 确保身份配置
            git add .
            git commit -m "临时提交：清理前保存工作"
            echo "✅ 已提交当前工作"
            ;;
        2)
            echo "⚠️  这将删除所有未跟踪文件和未提交的更改！"
            read -p "确认继续吗？(输入 'YES' 确认): " confirm
            if [ "$confirm" = "YES" ]; then
                git clean -fdx
                git reset --hard HEAD
                echo "✅ 工作目录已清理"
            else
                echo "❌ 已取消清理"
                exit 1
            fi
            ;;
        3)
            echo "请手动处理未提交的更改，然后重新运行脚本"
            exit 0
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
}

# 步骤3: 创建备份并使用 git-filter-repo
cleanup_with_filter_repo() {
    echo "🔄 使用 git-filter-repo 清理提交..."

    # 创建备份分支
    timestamp=$(date +%Y%m%d-%H%M%S)
    backup_branch="backup-before-cleanup-$timestamp"
    git branch "$backup_branch"
    echo "✅ 创建备份分支: $backup_branch"

    # 使用git-filter-repo清理提交
    echo "🚀 开始清理自动化提交..."

    # 方法1: 使用消息过滤（修复Unicode问题）
    git filter-repo --force --message-callback '
import re

# 将bytes转换为字符串进行处理
message_str = message.decode("utf-8", errors="ignore")

# 使用字符串正则表达式匹配
if re.search(r"🚀 Update at \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", message_str):
    return b""  # 删除这个提交

return message  # 保留原消息
'

    echo "✅ 清理完成！"
}

# 步骤4: 使用 git filter-branch 的替代方案（如果没有git-filter-repo）
cleanup_with_filter_branch() {
    echo "🔄 使用 git filter-branch 清理提交..."

    # 创建备份分支
    timestamp=$(date +%Y%m%d-%H%M%S)
    backup_branch="backup-before-cleanup-$timestamp"
    git branch "$backup_branch"
    echo "✅ 创建备份分支: $backup_branch"

    # 使用filter-branch删除自动化提交
    git filter-branch -f --commit-filter '
        commit_msg=$(git log --format=%s -n 1 $GIT_COMMIT)
        if echo "$commit_msg" | grep -q "🚀 Update at [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]"; then
            skip_commit "$@"
        else
            git commit-tree "$@"
        fi
    ' HEAD

    # 清理引用
    git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
    git reflog expire --expire=now --all
    git gc --prune=now

    echo "✅ 清理完成！"
}

# 步骤5: 推送到远程仓库
push_to_remote() {
    echo "📡 推送到远程仓库..."

    echo "⚠️  即将强制推送到远程仓库，这将："
    echo "   - 重写远程历史"
    echo "   - 影响所有协作者"
    echo "   - 要求其他人重新克隆仓库"

    read -p "确认强制推送吗？(y/N): " confirm

    if [[ $confirm == [yY] ]]; then
        current_branch=$(git branch --show-current)
        echo "🚀 强制推送分支: $current_branch"

        git push --force-with-lease origin "$current_branch"

        if [ $? -eq 0 ]; then
            echo "✅ 成功推送到远程仓库"
            echo "📢 请通知团队成员重新克隆仓库！"
        else
            echo "❌ 推送失败，请检查权限和网络连接"
        fi
    else
        echo "✅ 已跳过远程推送"
    fi
}

# 主执行流程
main() {
    # 检查git-filter-repo是否可用
    if command -v git-filter-repo >/dev/null 2>&1; then
        echo "✅ 检测到 git-filter-repo"
        USE_FILTER_REPO=true
    else
        echo "⚠️  未检测到 git-filter-repo，将使用 git filter-branch"
        echo "建议安装 git-filter-repo: pip install git-filter-repo"
        USE_FILTER_REPO=false
    fi

    # 检查仓库状态
    check_repo_status

    # 清理工作目录
    clean_working_directory

    # 执行清理
    if [ "$USE_FILTER_REPO" = true ]; then
        cleanup_with_filter_repo
    else
        cleanup_with_filter_branch
    fi

    # 显示结果
    echo ""
    echo "📊 清理结果统计:"
    total_commits=$(git rev-list --all --count)
    echo "   剩余提交数: $total_commits"

    # 询问是否推送
    push_to_remote

    echo ""
    echo "🎉 清理操作完成！"
    echo "📋 备份分支已创建，可用于恢复"
}

# 运行主程序
main
