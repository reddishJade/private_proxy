# Private Proxy Rules

自用基于 mihomo 内核的代理规则集合与规则合并工具。
规则合并工具借鉴 xndeye 的 [rule-merger](https://github.com/xndeye/rule-merger) 项目。
规则内容使用 GitHub Actions 实现自动更新。

## 配置文件示例

### 1. moe.yaml
- 查看链接：[moe.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Full_Config/moe.yaml)
- 基于 Sukka(skk.moe) 的配置
- 参考：[我有特别的 Surge 配置和使用技巧](https://blog.skk.moe/post/i-have-my-unique-surge-setup/)

### 2. win.yaml
- 查看链接：[win.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Full_Config/win.yaml)
- 基于 DustinWin 的配置
- 参考：[ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)

### 3. mihomo.yaml（推荐）
- 查看链接：[mihomo.yaml](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Full_Config/mihomo.yaml)
- 基于本项目规则合并工具生成的配置
- 融合 Sukka 和 DustinWin 及其他优质规则提供者的规则

## 使用教程？
[配置文件语法](https://wiki.metacubex.one/handbook/syntax/)   

[配置文件说明](https://wiki.metacubex.one/config/)   

项目内配置文件及规则的使用说明[点这里](https://github.com/reddishJade/private_proxy/blob/main/GUIDE.md)   

## 规则列表

| 规则          | 上游规则来源 | 订阅链接 |
| ------------- | ------------ | -------- |
| ai            | • dler_ai | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/ai.yaml) |
| apple@cn      | • skk_apple_services<br>• skk_apple_cn<br>• skk_apple_cdn<br>• skk_apple_cdn_non_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/apple@cn.yaml) |
| cdn           | • skk_cdn_domainset<br>• skk_cdn_non_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn.yaml) |
| cdn@ip        | • skk_cdn_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/cdn@ip.yaml) |
| direct        | • Loyalsoldier_applications<br>• skk_direct| [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/direct.yaml) |
| domestic      | • skk_domestic | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic.yaml) |
| domestic@ip   | • skk_domestic_ip<br>• skk_china_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/domestic@ip.yaml) |
| download      | • skk_download_domainset<br>• skk_download_non_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download.yaml) |
| download@ip   | • skk_download_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/download@ip.yaml) |
| fakeip-filter | • fakeip-filter | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/fakeip-filter.yaml) |
| games@cn      | • DustinWin_games_cn | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/games@cn.yaml) |
| microsoft@cn  | • DustinWin_microsoft_cn | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/microsoft@cn.yaml) |
| private       | • DustinWin_private | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private.yaml) |
| private@ip    | • DustinWin_privateip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/private@ip.yaml) |
| proxy         | • skk_global | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/proxy.yaml) |
| reject        | • AWAvenue<br>• d3ward | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject.yaml) |
| reject@ip     | • skk_reject_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/reject@ip.yaml) |
| stream        | • skk_stream<br>• bilibili_hmt | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream.yaml) |
| stream@ip     | • skk_stream_ip<br>• bilibili_hmt | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/stream@ip.yaml) |
| telegram      | • skk_telegram | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram.yaml) |
| telegram@ip   | • skk_telegram_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/Mihomo/Provider/telegram@ip.yaml) |

## 鸣谢

感谢以下项目和个人提供的规则：

-   **Sukka**
-   **DustinWin**
-   **dler-io**
-   **xndeye**
-   **Loyalsoldier**
-   **juewuy**
