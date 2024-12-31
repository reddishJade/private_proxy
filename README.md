# Private Proxy Rules

基于 mihomo 内核的代理规则集合与规则合并工具。本项目致力于提供一个简单、高效的规则管理解决方案。

## 目录

- [功能特点](#功能特点)
- [规则列表](#规则列表)
- [快速开始](#快速开始)
- [配置文件说明](#配置文件说明)
- [规则格式说明](#规则格式说明)
- [配置文件示例](#配置文件示例)
- [常见问题](#常见问题)
- [更新日志](#更新日志)

## 功能特点

- 多源规则合并：支持从多个来源获取和合并规则
- 规则去重：自动去除重复规则
- 格式转换：支持多种规则格式之间的转换
- 并行处理：使用多线程提高规则处理效率
- 定期更新：规则每24小时自动更新一次
- 完整性验证：自动验证规则格式的正确性

## 规则列表

### 广告拦截类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| reject        | 广告域名拦截   | • skk_reject<br>• skk_reject_non_ip<br>• xndeye_reject<br>• anti-AD |
| reject@ip     | 广告IP拦截     | • skk_reject_ip |

### 应用分流类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| apple@cn      | 苹果服务分流   | • DustinWin_apple_cn<br>• skk_apple_services<br>• skk_apple_cn<br>• skk_apple_cdn<br>• skk_apple_cdn_non_ip |
| microsoft@cn  | 微软服务分流   | • DustinWin_microsoft_cn<br>• skk_microsoft_cdn |
| ai            | AI服务分流     | • skk_ai |
| games@cn      | 游戏平台分流   | • skk_steam_cn<br>• DustinWin_games_cn |

### 基础分流类
| 规则          | 用途           | 上游规则来源 |
| ------------- | -------------- | ------------ |
| direct        | 直连规则       | • DustinWin_applications<br>• skk_direct |
| proxy         | 代理规则       | • DustinWin_proxy<br>• skk_stream<br>• skk_telegram |
| proxy@ip      | 代理IP规则     | • skk_stream_ip<br>• skk_telegram_ip |
| domestic      | 国内网站       | • DustinWin_domestic<br>• skk_domestic |
| domestic@ip   | 国内IP         | • DustinWin_domestic_ip<br>• skk_domestic_ip |
| private       | 私有网络       | • DustinWin_private |
| private@ip    | 私有网络IP     | • DustinWin_privateip |
| download      | 下载服务       | • skk_cdn_domainset<br>• skk_cdn_non_ip<br>• skk_download_domainset<br>• skk_download_non_ip<br>• DustinWin_download |
| download@ip   | 下载服务IP     | • skk_cdn_ip<br>• skk_download_ip |
| fakeip-filter | Fake-IP过滤    | • fake_ip_filter |

## 快速开始

1. 环境要求：
```bash
Python >= 3.7
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 准备配置文件：
   - 下载示例配置文件 `config.yaml`
   - 根据需要修改规则源和输出设置

4. 运行工具：
```bash
python rule_merger.py
```

## 配置文件说明

配置文件使用 YAML 格式，主要包含以下部分：

### 基本结构
```yaml
- path: rules/example.yaml    # 输出文件路径
  behavior: classical         # 输出规则格式
  format: yaml               # 输出文件格式
  upstream:                  # 上游规则源配置
    source_name:            # 规则源名称（自定义）
      type: http           # 规则源类型
      url: "https://..."   # 规则源地址
      format: yaml         # 规则源格式
      behavior: classical  # 规则源格式类型
```

### 规则格式说明

#### Classical 格式
```
DOMAIN,example.com
DOMAIN-SUFFIX,example.com
IP-CIDR,192.168.1.0/24
IP-CIDR6,2001:db8::/32
```

#### IPCIDR 格式
```
192.168.1.0/24
2001:db8::/32
```

#### Domain 格式
```
example.com
+.example.com  # 表示 DOMAIN-SUFFIX
```

## 配置文件示例

本项目提供三个预配置的配置文件示例：

### 1. moe.yaml
- 基于 Sukka(skk.moe) 的配置
- 参考：[我有特别的 Surge 配置和使用技巧](https://blog.skk.moe/post/i-have-my-unique-surge-setup/)

### 2. win.yaml
- 基于 DustinWin 的配置
- 参考：[ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)

### 3. merger.yaml
- 基于本项目规则合并工具生成的配置
- 融合了 Sukka 和 DustinWin 的规则

## 常见问题

1. 如何选择配置文件？
   - win.yaml 适用于想使用DustinWin的规则
   - moe.yaml 适用于想使用Sukka的规则
   - merger.yaml 适用于想自定义融合规则

2. 规则更新频率是多少？
   - 所有规则默认每24小时更新一次
   - 可以通过修改配置文件中的 interval 参数调整

3. 如何处理规则冲突？
   - 规则按照在配置文件中的顺序优先级降序排列
   - 建议将更精确的规则放在前面

## 更新日志

- 2024-12-31：优化规则结构，添加规则说明
- 2024-11-29：添加并行处理功能
- 2024-09-29：首次发布