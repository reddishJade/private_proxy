用于mihomo内核的配置文件参考：

- 基于Sukka(skk.moe)的配置文件示例[moe.yaml](https://github.com/reddishJade/private_proxy/blob/main/moe.yaml)
	- 参考链接：
		- [我有特别的 Surge 配置和使用技巧](https://blog.skk.moe/post/i-have-my-unique-surge-setup/)
		- [Sukka Ruleset](https://github.com/SukkaW/Surge)
- 基于DustinWin的配置文件示例[win.yaml](https://github.com/reddishJade/private_proxy/blob/main/win.yaml)
	- 参考链接：
		- [适用于clash的ruleset规则集文件](https://github.com/DustinWin/ruleset_geodata?tab=readme-ov-file#%E4%BA%8C-ruleset-%E8%A7%84%E5%88%99%E9%9B%86%E6%96%87%E4%BB%B6%E8%AF%B4%E6%98%8E)
	- 各流媒体分组聚合为ios_rule_script的[Global Media](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash/GlobalMedia)并重命名为Streaming
- 如无特殊需求只需调整proxy-providers内的内容



- 新增借鉴xndeye的[rule-merger](https://github.com/xndeye/rule-merger)的自用规则集文件以及配置文件[merger.yaml](https://github.com/reddishJade/private_proxy/blob/main/merger.yaml)，merger用法详见[用法](https://github.com/reddishJade/private_proxy?tab=readme-ov-file#%E8%A7%84%E5%88%99%E5%90%88%E5%B9%B6%E5%B7%A5%E5%85%B7%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)


| 规则          | 链接                                                         |
| ------------- | ------------------------------------------------------------ |
| reject        | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/reject.yaml) |
| reject@ip     | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/reject@ip.yaml) |
| direct        | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/direct.yaml) |
| apple@cn      | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/apple@cn.yaml) |
| microsoft@cn  | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/microsoft@cn.yaml) |
| ai            | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/ai.yaml) |
| proxy         | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/game@cn.yaml) |
| proxy         | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/proxy.yaml) |
| proxy@ip      | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/proxy@ip.yaml) |
| domestic      | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/domestic.yaml) |
| domestic@ip   | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/domestic@ip.yaml) |
| private       | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/private.yaml) |
| private@ip    | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/private@ip.yaml) |
| download      | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/download.yaml) |
| fakeip-filter | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/fakeip-filter.yaml) |


# 规则合并工具使用说明

## 功能介绍

- 支持多种规则格式：classical、ipcidr、domain
- 支持 HTTP 和本地文件两种规则源
- 支持 YAML 和文本格式的规则文件
- 支持并行处理多个规则源
- 自动去重和规则验证

## 配置文件说明

工具使用 YAML 格式的配置文件（默认为 `config.yaml`），配置示例：

```yaml
- path: output/reject.yaml     # 输出文件路径
  behavior: classical          # 输出规则格式
  upstream:                    # 上游规则源
    blackmatrix7:             # 规则源名称（自定义）
      type: http              # 规则源类型：http 或 file
      url: https://example.com/rules.yaml  # HTTP 规则源 URL
      format: yaml            # 规则格式：yaml 或 text
      behavior: classical     # 源规则格式
    local_rules:              # 本地规则源
      type: file
      path: rules/local.txt   # 本地规则文件路径
      format: text
      behavior: domain
```

### 配置项说明

- `path`: 输出文件路径
- `behavior`: 输出规则格式，可选值：
  - `classical`: 标准格式（DOMAIN,DOMAIN-SUFFIX,IP-CIDR,IP-CIDR6）
  - `ipcidr`: 仅 IP-CIDR/IP-CIDR6
  - `domain`: 仅域名规则
- `upstream`: 规则源配置
  - `type`: 规则源类型（http/file）
  - `url`: HTTP 规则源 URL（type=http 时必填）
  - `path`: 本地规则文件路径（type=file 时必填）
  - `format`: 规则文件格式（yaml/text）
  - `behavior`: 源规则格式

## 使用方法

1. 环境要求：
```bash
Python >= 3.7
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 准备配置文件 `config.yaml`

4. 运行工具：
```bash
python rule_merger.py
```

## 规则格式说明

### Classical 格式
```
DOMAIN,example.com
DOMAIN-SUFFIX,example.com
IP-CIDR,192.168.1.0/24
IP-CIDR6,2001:db8::/32
```

### IPCIDR 格式
```
192.168.1.0/24
2001:db8::/32
```

### Domain 格式
```
example.com
+.example.com  # 表示 DOMAIN-SUFFIX
```