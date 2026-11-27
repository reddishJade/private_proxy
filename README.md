# Private Proxy

面向 Mihomo / Clash Meta、Shadowrocket 和 sing-box 的代理规则集合与规则生成工具。

本项目从多个公开规则源获取规则，按用途合并、去重、校验，并输出为不同客户端可以直接使用的格式。

## 特性

- 按 AI、Apple、CDN、国内服务、游戏、流媒体、广告拦截、私有地址等场景维护规则。
- 提供 Mihomo 和 sing-box 规则文件，以及直接引用 Sukka 规则的 Shadowrocket 配置。
- 提供 Mihomo 完整配置模板，也可以只引入单独的规则集。
- 通过 GitHub Actions 每 12 小时自动同步上游规则并更新生成物。
- 提供 Python 规则合并器，可扩展 HTTP 或本地规则源。

## 快速开始

### Mihomo / Clash Meta：使用完整配置

适合希望快速开始的用户：

1. 下载 [Mihomo/Full_Config/mihomo.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/main/Mihomo/Full_Config/mihomo.yaml)。
2. 编辑 `proxy-providers.provider1.url`，填入自己的代理订阅链接；也可以按需添加更多订阅。
3. 将配置导入 Mihomo 或兼容 Clash Meta 配置格式的客户端。
4. 在客户端中选择代理节点和策略组。

模板默认包含以下设置：

- `mixed-port: 7890`
- TUN 模式
- Fake-IP DNS
- 规则模式（`mode: rule`）
- 自动下载本项目的 MRS 规则集

如果客户端没有 TUN、DNS 监听或管理员权限，请根据客户端能力关闭或调整对应配置。

### Mihomo：只使用规则集

如果已经有自己的 Mihomo 配置，可以直接引用 `Mihomo/Provider` 中的 `.mrs` 或 `.yaml` 文件。例如：

```yaml
rule-providers:
  reject:
    type: http
    format: mrs
    behavior: domain
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/main/Mihomo/Provider/reject.mrs
    path: ./rules/reject.mrs

  proxy:
    type: http
    format: mrs
    behavior: domain
    interval: 43200
    url: https://raw.githubusercontent.com/reddishJade/private_proxy/main/Mihomo/Provider/proxy.mrs
    path: ./rules/proxy.mrs

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,proxy,PROXY
  - MATCH,DIRECT
```

也可以直接参考 [Mihomo/Rule.yaml](Mihomo/Rule.yaml) 中的完整 `rule-providers` 与 `rules` 示例。

### Shadowrocket

导入 [Shadowrocket/config.conf](Shadowrocket/config.conf)，再选择自己的代理节点。配置直接引用 [Sukka 的 Surge 规则](https://ruleset.skk.moe/)，下载和 CDN 流量使用 `PROXY`。

### sing-box

- Source JSON：[SingBox/Source](SingBox/Source)
- 二进制规则集：[SingBox/RuleSet](SingBox/RuleSet)

`.json` 适合查看和进一步编辑，`.srs` 适合在 sing-box 中作为本地二进制规则集使用。仓库不提供完整的 sing-box 出站配置，节点、DNS、路由和策略组需要在自己的 sing-box 配置中定义。

## 规则目录

规则文件都位于 `Mihomo/Provider`，并通常同时提供以下格式：

| 名称 | 用途 |
| --- | --- |
| `ai` / `ai@cn` | AI 服务；`@cn` 为国内直连或国内服务拆分 |
| `apple` / `apple@cn` | Apple 服务 |
| `cdn` / `cdn@ip` | CDN 域名与 IP-CIDR |
| `direct` | 适合直连的规则 |
| `domestic` / `domestic@ip` | 国内域名与 IP-CIDR |
| `download` / `download@ip` | 下载相关服务与地址 |
| `games` / `games@cn` / `games@ip` | 游戏服务 |
| `google` | Google 服务 |
| `microsoft` / `microsoft@cn` | Microsoft 服务 |
| `private` / `private@ip` | 私有域名与私有地址 |
| `proxy` | 通常需要代理的域名 |
| `reject` / `reject@ip` | 广告、跟踪、恶意地址等拦截规则 |
| `streaming` / `streaming@ip` | 流媒体服务 |
| `telegram@ip` | Telegram IP-CIDR |

命名约定：

- `@cn`：面向中国大陆网络环境的域名拆分，通常用于直连。
- `@ip`：IP-CIDR 规则，使用时需要将 `behavior` 设置为 `ipcidr`。
- `.yaml`：可读的 Mihomo YAML 规则集。
- `.mrs`：Mihomo 二进制规则集，体积更小、加载更快。
- `skk-*`、`dler-*`：从对应上游规则目录生成的细分规则，适合需要更细粒度控制的用户。

也可以浏览 [全部 Mihomo 规则文件](https://github.com/reddishJade/private_proxy/tree/main/Mihomo/Provider)。

## 目录结构

```text
.
├── Mihomo/
│   ├── Full_Config/mihomo.yaml  # Mihomo / Clash Meta 完整配置模板
│   ├── Rule.yaml                # 可嵌入已有配置的规则示例
│   └── Provider/                # Mihomo YAML 与 MRS 规则集
├── Shadowrocket/
│   ├── config.conf              # Shadowrocket 配置模板
│   └── ruleset/                 # 历史规则文件
├── SingBox/
│   ├── Source/                  # sing-box source JSON
│   └── RuleSet/                 # sing-box .srs 规则集
├── Code/
│   ├── config.yaml              # Mihomo 规则合并配置
│   ├── rule_merger.py           # Mihomo 规则合并入口
│   ├── skk_ruleset.py           # 生成 ruleset.skk.moe 规则
│   ├── dler_ruleset.py          # 生成 dler-io/Rules 规则
│   └── singbox_converter.py     # Mihomo YAML → sing-box Source JSON
└── .github/workflows/
    └── update-rules.yml         # 自动同步与构建流程
```

## 本地生成

需要 Python 3.10 或更高版本：

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r Code/requirements.txt
```

规则合并器的输出路径是相对于 `Code` 目录解析的，因此运行时请先进入该目录：

```bash
cd Code

# 生成并更新 Mihomo Provider
python rule_merger.py config.yaml

# 生成 SKK 与 Dler 的细分规则
python skk_ruleset.py
python dler_ruleset.py
```

将 Mihomo YAML 转换为 sing-box Source JSON：

```bash
# 回到项目根目录后执行
cd ..
python Code/singbox_converter.py \
  Mihomo/Provider/proxy.yaml \
  SingBox/Source/proxy.json \
  --behavior domain
```

MRS 和 SRS 属于客户端使用的二进制格式。本地生成时请使用对应平台的 Mihomo / sing-box 命令行工具；GitHub Actions 会在自动更新流程中完成 Mihomo YAML 到 MRS 的转换。

## 自动更新

`.github/workflows/update-rules.yml`：

- 每 12 小时运行一次（UTC 00:00 与 12:00，即北京时间 08:00 与 20:00）。
- 同步多个公开上游规则源。
- 合并并校验 Mihomo YAML 规则。
- 使用 Mihomo 转换生成对应的 MRS 文件。
- 只有规则发生变化时才提交更新。

主要上游包括：

- [ruleset.skk.moe](https://ruleset.skk.moe/)
- [SukkaW/Surge](https://github.com/SukkaW/Surge)
- [DustinWin/ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)
- [appshubcc/bett-rules](https://github.com/appshubcc/bett-rules)
- [dler-io/Rules](https://github.com/dler-io/Rules)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
- [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR)

## 免责声明

本项目只提供规则整理、转换和配置示例，不提供代理节点或代理服务。使用前请确认：

1. 你拥有合法有效的代理服务订阅。
2. 你的使用行为符合所在地法律法规和相关服务条款。
3. 你理解规则匹配、DNS、TUN 和 Fake-IP 设置可能影响网络访问。

使用本项目产生的配置、网络行为及相关风险由使用者自行承担。

## 致谢

感谢所有上游规则项目及开源社区贡献者：

- [SukkaW/Surge](https://github.com/SukkaW/Surge)
- [DustinWin/ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)
- [appshubcc/bett-rules](https://github.com/appshubcc/bett-rules)
- [dler-io/Rules](https://github.com/dler-io/Rules)
- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
- [xndeye/rule-merger](https://github.com/xndeye/rule-merger)

如果这个项目对你有帮助，欢迎点亮 [Star](https://github.com/reddishJade/private_proxy)。
