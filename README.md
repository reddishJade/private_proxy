# Private Proxy Rules

<div align="center">

🛡️ **基于 Mihomo 内核的代理规则集合与规则合并工具 -- 造了一个新轮子**

[![GitHub Stars](https://img.shields.io/github/stars/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/issues)
[![Last Commit](https://img.shields.io/github/last-commit/reddishJade/private_proxy?style=flat-square)](https://github.com/reddishJade/private_proxy/commits/main)
[![Auto Update](https://img.shields.io/badge/Auto%20Update-Every%2012h-green?style=flat-square)](https://github.com/reddishJade/private_proxy/actions)

</div>

## 🚀 快速开始

### 📥 方式一：使用完整配置

适合想要开箱即用的用户：

1. **下载配置文件**：

- [mihomo.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Full_Config/mihomo.yaml)

2. **修改代理订阅**：将配置文件中的 `your-subscription-url` 替换为您的代理订阅链接
3. **导入客户端**：将配置文件导入到您的 Mihomo 客户端

### 🔧 方式二：仅使用规则集

适合已有配置文件，仅需要添加规则的用户：

```yaml
rule-providers:
  # 广告拦截规则
  reject:
    type: http
    behavior: classical  
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml
    path: ./rules/reject.yaml
  
  # 代理规则
  proxy:
    type: http
    behavior: classical
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.yaml
    path: ./rules/proxy.yaml

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,proxy,PROXY
  # 更多规则...
```

### 📚 相关文档

- [Mihomo 配置语法](https://wiki.metacubex.one/handbook/syntax/)
- [配置文件说明](https://wiki.metacubex.one/config/)

## 📋 规则列表

| 规则名称     | 订阅链接                                                     |
| ------------ | ------------------------------------------------------------ |
| ai           | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai.yaml) |
| ai@cn        | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai@cn.yaml) |
| apple        | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple.yaml) |
| apple@cn     | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple@cn.yaml) |
| cdn          | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn.yaml) |
| cdn@ip       | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn@ip.yaml) |
| direct       | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/direct.yaml) |
| domestic     | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic.yaml) |
| domestic@ip  | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic@ip.yaml) |
| download     | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download.yaml) |
| download@ip  | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download@ip.yaml) |
| games        | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games.yaml) |
| games@cn     | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games@cn.yaml) |
| games@ip     | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games@ip.yaml) |
| microsoft    | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft.yaml) |
| microsoft@cn | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft@cn.yaml) |
| private      | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private.yaml) |
| private@ip   | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private@ip.yaml) |
| proxy        | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.yaml) |
| reject       | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml) |
| reject@ip    | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject@ip.yaml) |
| streaming    | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream.yaml) |
| streaming@ip | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream@ip.yaml) |
| telegram@ip  | [📥](raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram@ip.yaml) |

## 🔄 自动更新机制

### ⏰ 更新时间表

- **定时更新**: 每天 08:00 和 20:00 (UTC+8) 自动运行
- **触发条件**: GitHub Actions 自动触发

### 📊 规则源监控

项目自动监控以下优质上游规则源的变化：

- [**Sukka's Surge Ruleset**](https://github.com/SukkaW/Surge)
- [**DustinWin's Ruleset**](https://github.com/DustinWin/ruleset_geodata)
- [**Meta rules**](https://github.com/MetaCubeX/meta-rules-dat)
- [**dler-io Rules**](https://github.com/dler-io/Rules)
- [**Loyalsoldier's Rules**](https://github.com/Loyalsoldier/clash-rules)
- [**ios_rule_script**](https://github.com/blackmatrix7/ios_rule_script)
- [**ACL4SSR**](https://github.com/ACL4SSR/ACL4SSR/tree/master)

## 🙏 致谢

感谢以下开源项目和个人贡献者，本项目的规则内容基于他们的优秀工作：

### 📚 参考项目

- **[Sukka](https://github.com/SukkaW)** - [Surge Ruleset](https://github.com/SukkaW/Surge)
- **[DustinWin](https://github.com/DustinWin)** - [ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)
- **[xndeye](https://github.com/xndeye)** - [rule-merger](https://github.com/xndeye/rule-merger)

感谢所有为开源社区贡献力量的开发者们！🎉

## ⚠️ 免责声明

本项目仅供学习交流使用，请遵守当地法律法规。使用本项目配置文件时，请确保：

1. 您有合法的代理服务订阅
2. 遵守相关法律法规和服务条款
3. 不用于任何违法违规活动

项目作者不对使用本项目导致的任何问题承担责任。

---

<p align="center">
  <strong>🌟 如果这个项目对您有帮助，请考虑给它一个 Star ⭐</strong><br>
  <a href="https://github.com/reddishJade/private_proxy">https://github.com/reddishJade/private_proxy</a>
