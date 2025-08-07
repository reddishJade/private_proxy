# Mihomo 配置文件和规则

这个目录包含了完整的 Mihomo 代理客户端配置文件和规则集。

## 📁 目录结构

```
Mihomo/
├── Rule.yaml              # 规则配置文件（规则集引用）
├── Full_Config/           # 完整配置文件
│   ├── mihomo.yaml        # 标准配置文件
│   ├── mihomo_flag.yaml   # 带国旗图标的配置
│   ├── moe.yaml          # 萌化配置
│   └── win.yaml          # Windows 优化配置
└── Provider/             # 规则提供者文件
    ├── ai.yaml           # AI 相关规则
    ├── apple@cn.yaml     # Apple 中国区规则
    ├── cdn.yaml          # CDN 规则
    ├── direct.yaml       # 直连规则
    ├── domestic.yaml     # 国内规则
    ├── proxy.yaml        # 代理规则
    ├── reject.yaml       # 拒绝规则
    └── ...              # 其他规则文件
```

## 🚀 快速开始

### 1. 使用规则配置

如果您已有 Mihomo 客户端配置，只需要使用我们的规则集：

```yaml
# 在您的配置文件中添加
rule-providers:
  reject:
    type: http
    behavior: classical
    interval: 43200
    url: https://cdn.jsdelivr.net/gh/reddishJade/private_proxy@refs/heads/main/Mihomo/Provider/reject.yaml
    path: ./rules/reject.yaml

rules:
  - RULE-SET,reject,REJECT
```

### 2. 使用完整配置

选择适合您的配置文件：

- **标准用户**: [`mihomo.yaml`](./Full_Config/mihomo.yaml)
- **需要国旗显示**: [`mihomo_flag.yaml`](./Full_Config/mihomo_flag.yaml)  
- **Windows 用户**: [`win.yaml`](./Full_Config/win.yaml)
- **萌化主题**: [`moe.yaml`](./Full_Config/moe.yaml)

## 📋 规则说明

### 基础规则类型

| 规则类型 | 用途 | 示例文件 |
|---------|------|---------|
| `reject` | 广告拦截和恶意网站 | reject.yaml |
| `direct` | 直连访问（不走代理） | direct.yaml |
| `proxy` | 需要代理的网站 | proxy.yaml |
| `domestic` | 国内网站和服务 | domestic.yaml |

### 专用规则类型

| 规则类型 | 用途 | 说明 |
|---------|------|------|
| `ai` | AI 服务 | ChatGPT、Claude 等 |
| `stream` | 流媒体服务 | Netflix、YouTube 等 |
| `telegram` | Telegram 相关 | 包含域名和 IP |
| `apple@cn` | Apple 中国服务 | App Store、iCloud 等 |
| `microsoft@cn` | 微软中国服务 | Office、OneDrive 等 |
| `game@cn` | 游戏中国服务 | 游戏下载和更新 |

### IP 规则类型

以 `@ip` 结尾的规则文件包含 IP 地址段：

- `reject@ip.yaml` - 恶意 IP 段
- `domestic@ip.yaml` - 中国 IP 段  
- `private@ip.yaml` - 私有网络 IP
- `cdn@ip.yaml` - CDN IP 段

## ⚙️ 配置说明

### Rule.yaml

这是一个轻量级的规则配置文件，只包含规则引用。适合：
- 已有代理订阅的用户
- 只需要规则的用户
- 自定义代理配置的用户

### Full_Config 配置文件

包含完整的 Mihomo 配置，包括：
- 代理服务器配置
- 代理组配置  
- 规则配置
- DNS 配置
- 实验性功能

**使用步骤**：
1. 选择合适的配置文件
2. 修改其中的代理订阅链接
3. 根据需要调整代理组和规则

## 🔄 自动更新

所有规则文件通过 GitHub Actions 自动更新：
- **更新频率**: 每 12 小时
- **更新内容**: 从上游规则源同步最新规则
- **失效处理**: 自动清理失效域名和 IP

## 📊 规则统计

当前规则总数：**~30,000 条**

| 规则类型 | 规则数量 |
|---------|---------|
| 拒绝规则 | ~9,000 |
| 国内 IP | ~11,000 |  
| CDN 规则 | ~3,800 |
| 代理规则 | ~1,600 |
| 下载规则 | ~1,200 |

## 🛠️ 自定义配置

### 修改代理订阅

在配置文件中找到并修改：

```yaml
proxy-providers:
  provider1:
    type: http
    url: "你的订阅链接"
    interval: 3600
```

### 调整规则优先级

修改 `rules` 部分的顺序：

```yaml
rules:
  - RULE-SET,reject,REJECT      # 最高优先级
  - RULE-SET,direct,DIRECT      
  - RULE-SET,proxy,Proxy        # 最低优先级
  - MATCH,Final                 # 兜底规则
```

### 禁用特定规则

注释掉不需要的规则：

```yaml
rules:
  - RULE-SET,reject,REJECT
  # - RULE-SET,ai,AIGC         # 禁用 AI 规则
  - RULE-SET,proxy,Proxy
```

## 🔗 相关链接

- [Mihomo 官方文档](https://wiki.metacubex.one/)
- [配置文件语法](https://wiki.metacubex.one/handbook/syntax/)
- [使用教程](../GUIDE.md)
- [项目主页](https://github.com/reddishJade/private_proxy)

## ❓ 常见问题

### Q: 如何选择配置文件？
A: 新手推荐使用 `mihomo.yaml`，需要国旗显示选择 `mihomo_flag.yaml`

### Q: 规则更新频率是多少？
A: 每 12 小时自动更新一次，确保规则时效性

### Q: 如何添加自定义规则？
A: 可以在配置文件的 `rules` 部分添加自定义规则，建议放在现有规则之前

### Q: 配置文件中的订阅链接需要修改吗？
A: 是的，需要替换为您自己的代理订阅链接

---

💡 **提示**: 如果遇到问题，请查看 [项目 Issues](https://github.com/reddishJade/private_proxy/issues) 或提交新的问题。
