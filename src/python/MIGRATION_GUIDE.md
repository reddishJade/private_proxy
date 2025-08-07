# 迁移指南：从 v1.0 到 v2.0

本指南帮助您从旧版本的单文件 `rule_merger.py` 迁移到新的模块化版本。

## 🚀 快速迁移

### 1. 立即开始使用新版本

```bash
# 旧版本（不推荐）
python rule_merger.py

# 新版本（推荐）
python rule_merger_main.py
```

### 2. 配置文件兼容性

✅ **好消息**：配置文件格式完全兼容！您的现有 `config.yaml` 无需修改即可使用。

```bash
# 验证现有配置
python utils.py validate config.yaml
```

## 📁 文件结构变化

### v1.0 结构

```
src/python/
├── rule_merger.py          # 单个文件（623行）
├── config.yaml            # 配置文件
└── output/                # 输出目录
```

### v2.0 结构

```
src/python/
├── core/                   # 📦 新增：核心模块包
│   ├── __init__.py
│   ├── constants.py       # 常量定义
│   ├── validators.py      # 规则验证
│   ├── transformers.py    # 规则转换
│   ├── fetchers.py        # 规则获取
│   ├── processors.py      # 规则处理
│   └── merger.py          # 主要逻辑
├── rule_merger_main.py    # 📦 新增：主入口文件
├── utils.py               # 📦 新增：实用工具
├── config_docs.py         # 📦 新增：配置文档
├── rule_merger.py         # ⚠️  已弃用（保留兼容）
├── config.yaml           # ✅ 保持不变
└── output/               # ✅ 保持不变
```

## 🔄 功能对比

| 功能         | v1.0 | v2.0 | 说明               |
| ------------ | ---- | ---- | ------------------ |
| 基本规则合并 | ✅   | ✅   | 功能保持一致       |
| 并行处理     | ✅   | ✅   | 性能保持           |
| 配置格式     | ✅   | ✅   | 完全兼容           |
| 错误处理     | ✅   | ✅   | 更加完善           |
| 配置验证     | ❌   | ✅   | **新增功能** |
| 规则分析     | ❌   | ✅   | **新增功能** |
| 帮助信息     | ❌   | ✅   | **新增功能** |
| 类型注解     | 部分 | ✅   | 更加完善           |
| 文档字符串   | 部分 | ✅   | 更加详细           |
| 模块化设计   | ❌   | ✅   | **重大改进** |

## 🛠️ 新增工具命令

### 配置验证

```bash
# 验证配置文件格式
python utils.py validate config.yaml
```

### 规则分析

```bash
# 分析规则文件统计信息
python utils.py analyze output/ads.yaml
```

### 创建示例配置

```bash
# 生成配置文件示例
python config_docs.py
```

### 帮助信息

```bash
# 查看使用帮助
python rule_merger_main.py --help
```

## 🔧 开发者迁移

### 1. 导入方式变化

```python
# v1.0 - 直接导入类
from rule_merger import RulesMerger, RuleValidator

# v2.0 - 从模块导入
from core import RulesMerger, RuleValidator
# 或者
from core.merger import RulesMerger
from core.validators import RuleValidator
```

### 2. 扩展开发

```python
# v2.0 - 更容易扩展
from core.validators import RuleValidator

class CustomValidator(RuleValidator):
    def validate_custom_rule(self, rule: str):
        # 自定义验证逻辑
        pass
```

## 📊 性能和质量提升

### 代码质量

- **行数减少**：单文件从 623 行拆分为多个小模块
- **职责分离**：每个模块职责单一
- **类型安全**：完整的类型注解
- **文档完善**：详细的文档字符串

### 维护性提升

- **模块化**：便于单独测试和维护
- **扩展性**：新功能易于添加
- **调试性**：错误定位更精确
- **复用性**：模块可独立使用

## ⚠️ 注意事项

1. **旧文件保留**：`rule_merger.py` 被标记为已弃用但仍可使用
2. **配置兼容**：现有配置文件无需修改
3. **输出格式**：生成的规则文件格式保持一致
4. **性能维持**：处理速度和内存使用保持相同水平

## 🎯 推荐迁移步骤

### 第一步：验证环境

```bash
cd src/python
python utils.py validate config.yaml
```

### 第二步：测试新版本

```bash
# 使用小配置测试
python rule_merger_main.py test_config.yaml
```

### 第三步：完整迁移

```bash
# 使用完整配置
python rule_merger_main.py config.yaml
```

### 第四步：验证结果

```bash
# 分析生成的规则
python utils.py analyze output/ads.yaml
```

## 🆘 问题排查

### 常见问题

**Q: 新版本运行报错怎么办？**
A: 首先验证配置文件：`python utils.py validate config.yaml`

**Q: 生成的规则数量不一致？**
A: 使用分析工具对比：`python utils.py analyze output/rules.yaml`

**Q: 想继续使用旧版本？**
A: 可以继续使用，但会显示弃用警告

**Q: 如何获得帮助？**
A: 运行 `python rule_merger_main.py --help`

### 回滚方案

如果需要回滚到旧版本：

```bash
# 使用旧版本（会显示警告）
python rule_merger.py config.yaml
```

## 📚 更多资源

- **详细文档**：`README.md`
- **配置说明**：`config_docs.py`
- **示例配置**：运行 `python config_docs.py`

---

**总结**：新版本在保持完全兼容的基础上，提供了更好的代码结构、更多实用功能和更强的扩展性。建议所有用户迁移到新版本以获得更好的使用体验。
