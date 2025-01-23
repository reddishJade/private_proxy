# Private Proxy 规则使用指南

## 目录
1. [使用完整配置](#使用完整配置)
2. [单独使用规则文件](#单独使用规则文件)

## 使用完整配置

### 方式一：使用 Gist 自定义

1. 创建自己的 GitHub Gist：
   - 访问 [GitHub Gist](https://gist.github.com/)
   - 创建新的 Gist
   - 复制完整的配置文件内容（如 `merger.yaml`）
   - [修改配置文件中的订阅信息](#1-修改订阅链接)
   - 保存 Gist

2. 获取 Raw 链接：
   - 点击 Gist 右上角的 "Raw" 按钮
   - 复制获得的链接，格式类似：`https://gist.githubusercontent.com/你的用户名/xxx/raw/xxx/xxx.yaml`
   - 删除第二串神秘数字，使链接的形式变为 `https://gist.githubusercontent.com/你的用户名/xxx/raw/xxx.yaml`

3. 在 Mihomo Party 中使用：
   - 打开 Mihomo Party
   - 点击左侧 "订阅管理" 选项
   - 在 `url` 栏输入你的 Gist 链接
   - 保存并使用

### 方式二：本地订阅

#### 在 Mihomo Party 中使用：

1. 打开 Mihomo Party
2. 点击 "订阅管理"
3. 选择 "本地文件" -> "+号" -> "新建"
4. 复制粘贴完整的配置文件内容
5. [修改配置文件中的订阅信息](#1-修改订阅链接)
6. 保存并使用

## 单独使用规则文件

在 `Mihomo/Provider` 目录下提供了多个独立的规则文件，可根据需要选择使用：

### 规则文件列表及用途

- `ai.yaml`: AI 相关服务规则
- `proxy.yaml`: 代理规则
- `direct.yaml`: 直连规则
- `reject.yaml`: 广告拦截规则
- `stream.yaml`: 流媒体规则
- 更多规则见 [规则列表](https://github.com/reddishJade/private_proxy#规则列表)

### 在配置中引用单个规则

1. 复制规则文件的 Raw 链接，例如：
   ```
   https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai.yaml
   ```

2. 在你的配置文件中添加规则：
   ```yaml
   rule-providers:
     ai:
       type: http
       behavior: classical
       url: "你复制的规则文件链接"
       path: ./providers/ai.yaml
       interval: 43200

   rules:
     - RULE-SET,ai,🤖 AI
   ```

### 本地使用规则文件

1. 下载需要的规则文件到本地
2. 在配置文件中使用本地路径：
   ```yaml
   rule-providers:
     ai:
       type: file
       behavior: classical
       path: ./providers/ai.yaml

   rules:
     - RULE-SET,ai,🤖 AI
   ```

## 配置文件修改说明

### 1. 修改订阅链接

在配置文件中找到 `proxies` 或 `proxy-providers` 部分：
```yaml
proxy-providers:
  your-subscription:
    type: http
    url: "将这里替换为你的订阅链接"
    interval: 43200
    path: ./providers/your-subscription.yaml
```

### 2. 修改规则

你可以根据需要：
- 添加或删除规则集
- 修改规则优先级
- 自定义规则分组

## 注意事项

1. 确保订阅链接可以正常访问
2. 规则文件会定期更新，建议设置合适的更新间隔
3. 如果使用本地文件，需要手动更新规则
4. 某些规则可能需要配合特定的代理分组使用

## 获取帮助

如果遇到问题：
1. 检查配置文件格式是否正确
2. 查看客户端的日志输出
3. 在 [GitHub Issues](https://github.com/reddishJade/private_proxy/issues) 提交问题
