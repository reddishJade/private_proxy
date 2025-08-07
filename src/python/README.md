# 规则合并器 v2.0

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

## 🔧 模块说明

### 核心模块 (core/)

#### 1. constants.py - 常量定义

- `RuleConstants`: 规则类型和正则表达式常量
- `RuleSource`: 规则源配置数据类
- 脏数据过滤模式常量

#### 2. validators.py - 规则验证器

- `RuleValidator`: 提供各种规则格式的验证功能
- 支持经典、域名、IP CIDR三种规则类型的验证
- 内置脏数据过滤功能

#### 3. transformers.py - 规则转换器

- `RuleTransformer`: 在不同规则格式间转换
- 支持 classical ↔ domain ↔ ipcidr 的相互转换
- 智能规则类型识别和转换

#### 4. fetchers.py - 规则获取器

- `RuleFetcher`: 从HTTP和本地文件获取规则
- 支持YAML和纯文本格式
- 自动格式检测和解析

#### 5. processors.py - 规则处理器

- `RuleProcessor`: 规则清理和处理
- 去除注释、过滤脏数据
- 规则去重和排序

#### 6. merger.py - 规则合并器

- `RulesMerger`: 主要业务逻辑协调器
- 并行处理提高性能
- 配置管理和文件操作

### 工具模块

#### 1. rule_merger_main.py - 主入口

- 程序启动点
- 命令行参数处理
- 异常处理和日志配置

#### 2. utils.py - 实用工具

- `RuleAnalyzer`: 规则文件分析器
- `ConfigValidator`: 配置文件验证器
- 命令行工具功能

#### 3. config_docs.py - 配置文档

- 配置格式说明和示例
- 创建示例配置文件的工具

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

## ✨ 重构改进

### 1. 模块化设计

- 将623行的单文件拆分为多个专业模块
- 每个模块职责单一，便于维护
- 清晰的模块依赖关系

### 2. 代码质量提升

- 完善的类型注解
- 详细的文档字符串
- 一致的代码风格

### 3. 功能增强

- 新增配置验证功能
- 规则分析统计工具
- 更好的错误处理

### 4. 性能优化

- 保持并行处理能力
- 优化内存使用
- 更高效的规则处理

## 🐛 错误处理

程序具有完善的错误处理机制：

- 网络超时和重试
- 文件格式错误处理
- 配置验证和提示
- 详细的日志输出

## 📊 日志和监控

- 分级日志输出（INFO/WARNING/ERROR）
- 处理进度跟踪
- 规则统计信息
- 错误详情记录

---

**版本历史**

- v1.0: 原始单文件版本
- v2.0: 模块化重构版本，提升可维护性和扩展性
