# 规则合并器

本项目是一个用于合并和处理各种格式规则文件的工具，经过重构后具有更好的代码结构和可维护性。

## 📁 项目结构

```
src/python/
├── core/                         # 核心模块包
│   ├── __init__.py               # 模块初始化文件
│   ├── constants.py              # 常量定义模块
│   ├── validators.py             # 规则验证器模块
│   ├── transformers.py           # 规则转换器模块
│   ├── fetchers.py               # 规则获取器模块
│   ├── processors.py             # 规则处理器模块
│   └── merger.py                 # 规则合并器主模块
├── rule_merger_main.py           # 主入口文件
├── utils.py                      # 实用工具模块
├── config_docs.py                # 配置文档和示例
├── config.yaml                   # 配置文件
└── output/                       # 输出目录
```

## 🚀 使用方法

### 基本使用

```bash
# 使用默认配置文件 config.yaml
python rule_merger_main.py

# 使用指定配置文件
python rule_merger_main.py my_config.yaml
```

### 工具命令

```bash
# 分析规则文件
python utils.py analyze rules.yaml

# 验证配置文件
python utils.py validate config.yaml

# 创建示例配置
python config_docs.py
```

## 📝 配置文件格式

```yaml
- path: "output/ads.yaml"			# 输出文件路径
  behavior: "classical"				# 规则类型: classical/domain/ipcidr
  upstream:					# 上游规则源
    source1:
      type: "http"				# 源类型: http/file
      url: "https://example.com/rules.yaml"
      behavior: "classical"			# 源规则格式
      format: "yaml"				# 文件格式: yaml/text
```

## 🔍 规则类型说明

### Classical (经典格式)

包含所有类型的规则，如：

- `DOMAIN,example.com`
- `DOMAIN-SUFFIX,google.com`
- `IP-CIDR,192.168.1.0/24`
- `DST-PORT,80`

### Domain (域名格式)

只包含域名相关规则：

- `DOMAIN,example.com`
- `DOMAIN-SUFFIX,google.com`
- `DOMAIN-KEYWORD,ads`

### IP CIDR (IP格式)

只包含IP相关规则：

- `IP-CIDR,192.168.1.0/24`
- `IP-CIDR6,2001:db8::/32`
