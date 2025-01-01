# 执行规则更新
Write-Host "Updating rules..."
python .\rule_merger.py

# 检查是否有更改
$hasChanges = git status --porcelain

if ($hasChanges) {
    # 有更改时提交并推送
    Write-Host "Changes detected, committing and pushing..."
    git add .
    git commit -m "update rules $(Get-Date -Format 'yyyy-MM-dd')"
    git push -u origin main
    Write-Host "Rules updated successfully!"
} else {
    Write-Host "No changes detected."
} 