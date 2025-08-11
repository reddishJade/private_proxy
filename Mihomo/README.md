# Mihomo 配置文件和规则

这个目录包含了完整的 Mihomo 代理客户端配置文件和规则集。

## 📁 目录结构

```
Mihomo/
├── Rule.yaml              # 规则配置文件（规则集引用）
├── Full_Config/           # 完整配置文件
│   ├── mihomo.yaml        # 标准配置文件
└── Provider/              # 规则提供者文件
    ├── proxy.yaml         # 代理规则
    ├── reject.yaml        # 拒绝规则
    └── ...                # 其他规则文件
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

- [`mihomo.yaml`](./Full_Config/mihomo.yaml)

## 📋 规则说明

### 基础规则类型

| 规则类型     | 用途                 | 示例文件      |
| ------------ | -------------------- | ------------- |
| `reject`   | 广告拦截和恶意网站   | reject.yaml   |
| `direct`   | 直连访问（不走代理） | direct.yaml   |
| `proxy`    | 需要代理的网站       | proxy.yaml    |
| `domestic` | 国内网站和服务       | domestic.yaml |

### 专用规则类型

| 规则类型         | 用途           | 说明                 |
| ---------------- | -------------- | -------------------- |
| `ai`           | AI 服务        | ChatGPT、Claude 等   |
| `stream`       | 流媒体服务     | Netflix、YouTube 等  |
| `telegram`     | Telegram 相关  | 包含域名和 IP        |
| `apple@cn`     | Apple 中国服务 | App Store、iCloud 等 |
| `microsoft@cn` | 微软中国服务   | Office、OneDrive 等  |
| `game@cn`      | 游戏中国服务   | 游戏下载和更新       |

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
  - RULE-SET,proxy,Proxy
  - MATCH,Final                 # 兜底规则
```

## 🔗 相关链接

- [Mihomo 官方文档](https://wiki.metacubex.one/)
- [配置文件语法](https://wiki.metacubex.one/handbook/syntax/)
