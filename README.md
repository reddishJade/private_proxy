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

## 📁 项目结构

```
private_proxy/
├── 📄 README.md              		# 项目说明文档
├── 📄 GUIDE.md               		# 详细使用教程
├── 📄 requirements.txt       		# Python 环境依赖
├── 📂 Mihomo/                		# Mihomo 配置和规则
│   ├── 📄 README.md          		# Mihomo 配置说明
│   ├── 📄 Rule.yaml          		# 纯规则配置文件
│   ├── 📂 Full_Config/       		# 完整配置文件模板
│   │   ├── mihomo.yaml       		# 标准配置模板
│   └── 📂 Provider/          		# 规则文件目录
│       ├── reject.yaml       		# 广告拦截规则
│       ├── proxy.yaml        		# 代理规则
│       └── ...               		# 其他规则文件
└── 📂 src/                   		# 源代码和工具
    ├── 📄 ads.txt            		# 广告域名数据源
    └── 📂 python/            		# Python 规则处理工具
        ├── 📄 config.yaml    		# 规则源配置文件
        ├── 📄 rule_merger_main.py  # 主程序入口
        ├── 📄 utils.py      		# 通用工具函数
        └── 📂 core/         		# 核心处理模块
            ├── constants.py  		# 规则常量定义
            ├── validators.py 		# 规则验证器
            ├── transformers.py 	# 格式转换器
            ├── fetchers.py   		# 规则获取器
            ├── processors.py 		# 规则处理器
            └── merger.py     		# 规则合并器
```

## 📋 规则列表

### 🌐 域名规则

| 规则名称               | 上游来源                              | 订阅链接                                                                                                         |
| ---------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **reject**       | AWAvenue, d3ward                      | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml)       |
| **proxy**        | skk_global, dler_proxy                | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.yaml)        |
| **domestic**     | skk_domestic                          | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic.yaml)     |
| **cdn**          | skk_cdn                               | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn.yaml)          |
| **streaming**    | skk_streaming                         | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream.yaml)       |
| **ai**           | dler_ai                               | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai.yaml)           |
| **telegram**     | skk_telegram                          | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram.yaml)     |
| **apple@cn**     | skk_apple                             | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple@cn.yaml)     |
| **microsoft@cn** | DustinWin_microsoft_cn                | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft@cn.yaml) |
| **game@cn**      | DustinWin_games_cn                    | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/game@cn.yaml)      |
| **download**     | skk_download                          | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download.yaml)     |
| **private**      | DustinWin_private                     | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private.yaml)      |
| **direct**       | Loyalsoldier_applications, skk_direct | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/direct.yaml)       |

### 🌍 IP 地址规则

| 规则名称              | 订阅链接                                                                                                        |
| --------------------- | --------------------------------------------------------------------------------------------------------------- |
| **reject@ip**   | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject@ip.yaml)   |
| **domestic@ip** | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic@ip.yaml) |
| **telegram@ip** | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram@ip.yaml) |
| **stream@ip**   | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream@ip.yaml)   |
| **cdn@ip**      | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn@ip.yaml)      |
| **download@ip** | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download@ip.yaml) |
| **private@ip**  | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private@ip.yaml)  |

### 🎭 FakeIP 过滤器

| 规则名称                | 订阅链接                                                                                                          |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **fakeip-filter** | [📥](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/fakeip-filter.yaml) |

## 🔄 自动更新机制

### ⏰ 更新时间表

- **定时更新**: 每天 08:00 和 20:00 (UTC+8) 自动运行
- **触发条件**: GitHub Actions 自动触发
- **更新频率**: 每 12 小时检查一次上游规则源变化

### 📊 规则源监控

项目自动监控以下优质上游规则源的变化：

- [**Sukka's Surge Ruleset**](https://github.com/SukkaW/Surge)
- [**DustinWin's Ruleset**](https://github.com/DustinWin/ruleset_geodata)
- [**dler-io AI Rules**](https://github.com/dler-io/Rules)
- [**Loyalsoldier's Rules**](https://github.com/Loyalsoldier/clash-rules)

## 🙏 致谢

感谢以下开源项目和个人贡献者，本项目的规则内容基于他们的优秀工作：

### 📚 参考项目
- **[Sukka](https://github.com/SukkaW)** - [Surge Ruleset](https://github.com/SukkaW/Surge)
- **[DustinWin](https://github.com/DustinWin)** - [ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)
- **[dler-io](https://github.com/dler-io)** - [Rules](https://github.com/dler-io/Rules)
- **[xndeye](https://github.com/xndeye)** - [rule-merger](https://github.com/xndeye/rule-merger)
- **[Loyalsoldier](https://github.com/Loyalsoldier)** - [clash-rules](https://github.com/Loyalsoldier/clash-rules)

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
