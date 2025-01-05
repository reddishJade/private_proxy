# Private Proxy Rules

自用基于 mihomo 内核的代理规则集合与规则合并工具。
规则合并工具借鉴 [xndeye](https://github.com/xndeye/rule-merger) 的rule-merger 项目。

## 配置文件示例

### 1. moe.yaml
- 基于 Sukka(skk.moe) 的配置
- 参考：[我有特别的 Surge 配置和使用技巧](https://blog.skk.moe/post/i-have-my-unique-surge-setup/)

### 2. win.yaml
- 基于 DustinWin 的配置
- 参考：[ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)

### 3. merger.yaml
- 基于本项目规则合并工具生成的配置
- 融合 Sukka 和 DustinWin 的规则

## 规则列表

| 规则          | 上游规则来源 | 订阅链接 |
| ------------- | ------------ | -------- |
| ai            | • skk_ai<br>• dler_ai | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/ai.yaml) |
| apple@cn      | • DustinWin_apple_cn<br>• skk_apple_services<br>• skk_apple_cn<br>• skk_apple_cdn<br>• skk_apple_cdn_non_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/apple@cn.yaml) |
| cdn           | • skk_cdn_domainset<br>• skk_cdn_non_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/cdn.yaml) |
| cdn@ip        | • skk_cdn_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/cdn@ip.yaml) |
| direct        | • Loyalsoldier_applications<br>• skk_direct<br>• dler_special | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/direct.yaml) |
| domestic      | • DustinWin_domestic<br>• skk_domestic | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/domestic.yaml) |
| domestic@ip   | • DustinWin_domestic_ip<br>• skk_domestic_ip<br>• skk_china_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/domestic@ip.yaml) |
| download      | • skk_download_domainset<br>• skk_download_non_ip<br>• ios_download | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/download.yaml) |
| download@ip   | • skk_download_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/download@ip.yaml) |
| fakeip-filter | • fakeip-filter | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/fakeip-filter.yaml) |
| games@cn      | • skk_steam_cn<br>• DustinWin_games_cn | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/games@cn.yaml) |
| microsoft@cn  | • DustinWin_microsoft_cn<br>• skk_microsoft_cdn | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/microsoft@cn.yaml) |
| private       | • DustinWin_private | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/private.yaml) |
| private@ip    | • DustinWin_privateip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/private@ip.yaml) |
| proxy         | • DustinWin_proxy<br>• skk_global<br>• skk_stream<br>• skk_telegram | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/proxy.yaml) |
| proxy@ip      | • skk_stream_ip<br>• skk_telegram_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/proxy@ip.yaml) |
| reject        | • skk_reject<br>• DustinWin_ads | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/reject.yaml) |
| reject@ip     | • skk_reject_ip | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/reject@ip.yaml) |
