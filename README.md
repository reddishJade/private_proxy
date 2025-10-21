# Private Proxy Rules

<div align="center">

🛡️ **基于 Mihomo 内核的代理规则集合与规则合并工具**

[![GitHub Stars](https://img.shields.io/github/stars/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/issues)
[![Last Commit](https://img.shields.io/github/last-commit/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/commits/main)
[![Auto Update](https://img.shields.io/badge/Auto%20Update-Every%2012h-green?style=flat-square)](https://github.com/reddishJade/private_proxy/actions)

</div>

## 🚀 快速开始

### 📥 方式一：使用完整配置

适合想要开箱即用的用户：

1. 下载配置文件：[mihomo.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Full_Config/mihomo.yaml)
2. 将 `your-subscription-url` 替换成自己的代理订阅链接
3. 导入 Mihomo / Clash Meta 客户端并启用

### 🔧 方式二：仅订阅规则集

适合已有配置文件，仅需增补规则集的用户：

```yaml
rule-providers:
  reject:
    type: http
    behavior: domain
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml
    path: ./rules/reject.yaml

  proxy:
    type: http
    behavior: mrs
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.mrs
    path: ./rules/proxy.mrs

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,proxy,PROXY
  # 添加更多规则...
```

> 温馨提示：更多规则组合方式请查阅 [Mihomo 配置语法](https://wiki.metacubex.one/handbook/syntax/) 与 [官方配置手册](https://wiki.metacubex.one/config/)。

## 📋 规则订阅目录

| 规则名称     | 订阅链接                                                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| ai           | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai.yaml)           |
| ai@cn        | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai@cn.yaml)        |
| apple        | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple.yaml)        |
| apple@cn     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple@cn.yaml)     |
| cdn          | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn.yaml)          |
| cdn@ip       | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn@ip.yaml)       |
| direct       | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/direct.yaml)       |
| domestic     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic.yaml)     |
| domestic@ip  | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic@ip.yaml)  |
| download     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download.yaml)     |
| download@ip  | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download@ip.yaml)  |
| games        | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games.yaml)        |
| games@cn     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games@cn.yaml)     |
| games@ip     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games@ip.yaml)     |
| microsoft    | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft.yaml)    |
| microsoft@cn | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft@cn.yaml) |
| private      | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private.yaml)      |
| private@ip   | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private@ip.yaml)   |
| proxy        | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.yaml)        |
| reject       | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml)       |
| reject@ip    | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject@ip.yaml)    |
| streaming    | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/streaming.yaml)    |
| streaming@ip | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/streaming@ip.yaml) |
| telegram@ip  | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram@ip.yaml)  |

> 同时提供的还有对应的 `mrs`文件

## 🤖 自动构建与上游同步

- GitHub Actions 在每天 08:00 / 20:00 (UTC+8) 自动运行合并流程
- 自动抓取并跟踪以下上游规则仓库：
  - [SukkaW/Surge](https://github.com/SukkaW/Surge)
  - [DustinWin/ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)
  - [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)
  - [dler-io/Rules](https://github.com/dler-io/Rules)
  - [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
  - [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
  - [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR/tree/master)
- 合并结果发布到 `Mihomo/Provider`

## 🙏 致谢

- [SukkaW](https://github.com/SukkaW/Surge)
- [DustinWin](https://github.com/DustinWin/ruleset_geodata)
- [MetaCubeX](https://github.com/MetaCubeX/meta-rules-dat)
- [dler-io](https://github.com/dler-io/Rules)
- [Loyalsoldier](https://github.com/Loyalsoldier/clash-rules)
- [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script)
- [xndeye](https://github.com/xndeye/rule-merger)

感谢所有为开源社区贡献力量的开发者！

## ⚠️ 免责声明

本项目仅供学习交流，使用时请确保：

1. 拥有合法的代理服务订阅
2. 遵守所在地法律法规及服务条款
3. 不将配置用于任何违法违规用途

作者不对使用本项目产生的任何风险或损失负责。

---

<p align="center">
  <strong>🌟 如果这个项目对您有帮助，请考虑点亮一个 Star ⭐</strong><br>
  <a href="https://github.com/reddishJade/private_proxy">https://github.com/reddishJade/private_proxy</a>
