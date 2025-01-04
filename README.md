# Private Proxy Rules

自用基于 mihomo 内核的代理规则集合与规则合并工具。

## 目录

- [配置文件示例](#配置文件示例)
- [规则列表](#规则列表)

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

### 广告拦截类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| reject        | 广告域名拦截   | • skk_reject<br>• skk_reject_non_ip<br>• DustinWin_ads |
| reject@ip     | 广告IP拦截     | • skk_reject_ip |

### 应用分流类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| direct        | 直连规则       | • DustinWin_applications<br>• skk_direct<br>• dler_special |
| apple@cn      | 苹果服务分流   | • DustinWin_apple_cn<br>• skk_apple_services<br>• skk_apple_cn<br>• skk_apple_cdn<br>• skk_apple_cdn_non_ip |
| microsoft@cn  | 微软服务分流   | • DustinWin_microsoft_cn<br>• skk_microsoft_cdn |
| ai            | AI服务分流     | • skk_ai<br>• dler_ai |
| games@cn      | 游戏平台分流   | • skk_steam_cn<br>• DustinWin_games_cn |

### 基础分流类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| proxy         | 代理规则       | • DustinWin_proxy<br>• skk_stream<br>• skk_telegram |
| proxy@ip      | 代理IP规则     | • skk_stream_ip<br>• skk_telegram_ip |
| domestic      | 国内网站       | • DustinWin_domestic<br>• skk_domestic |
| domestic@ip   | 国内IP         | • DustinWin_domestic_ip<br>• skk_domestic_ip |
| private       | 私有网络       | • DustinWin_private |
| private@ip    | 私有网络IP     | • DustinWin_privateip |
| download      | 下载服务       | • skk_cdn_domainset<br>• skk_cdn_non_ip<br>• skk_download_domainset<br>• skk_download_non_ip<br>• DustinWin_download |
| download@ip   | 下载服务IP     | • skk_cdn_ip<br>• skk_download_ip |
| fakeip-filter | Fake-IP过滤    | • fake_ip_filter |
