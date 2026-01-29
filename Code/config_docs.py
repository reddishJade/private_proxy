"""
配置文件示例和说明

这个文件展示了规则合并器的配置格式和选项说明
"""

# 配置文件格式说明（YAML格式）

EXAMPLE_CONFIG = """
# 规则合并器配置示例
# 每个配置项代表一个输出文件的规则合并任务

- # 第一个规则集：广告拦截规则
  path: "output/ads.yaml"           # 输出文件路径
  behavior: "classical"             # 规则行为类型：classical、domain、ipcidr
  upstream:                         # 上游规则源配置
    source1:                        # 规则源名称（可自定义）
      type: "http"                  # 源类型：http 或 file
      url: "https://example.com/ads.yaml"  # HTTP源的URL
      behavior: "classical"         # 源规则的格式类型
      format: "yaml"               # 文件格式：yaml 或 text
    source2:
      type: "file"                 # 本地文件源
      path: "../ads.txt"           # 本地文件路径
      behavior: "classical"
      format: "text"

- # 第二个规则集：域名规则
  path: "output/domains.yaml"
  behavior: "domain"               # 只包含域名相关规则
  upstream:
    domain_source:
      type: "http"
      url: "https://example.com/domains.yaml"
      behavior: "classical"        # 从classical格式转换为domain格式
      format: "yaml"

- # 第三个规则集：IP CIDR规则
  path: "output/ipcidr.yaml"
  behavior: "ipcidr"               # 只包含IP相关规则
  upstream:
    ip_source:
      type: "http"
      url: "https://example.com/ips.yaml"
      behavior: "classical"
      format: "yaml"
"""

# 规则行为类型说明
BEHAVIOR_TYPES = {
    "classical": {
        "description": "经典格式，包含所有类型的规则",
        "supported_rules": [
            "DOMAIN,example.com",
            "DOMAIN-SUFFIX,example.com", 
            "IP-CIDR,192.168.1.0/24",
            "DST-PORT,80",
            "PROCESS-NAME,chrome.exe"
        ]
    },
    "domain": {
        "description": "域名格式，只包含域名相关规则",
        "supported_rules": [
            "DOMAIN,example.com",
            "DOMAIN-SUFFIX,example.com",
            "DOMAIN-KEYWORD,google",
            "DOMAIN-WILDCARD,*.example.com"
        ]
    },
    "ipcidr": {
        "description": "IP CIDR格式，只包含IP相关规则", 
        "supported_rules": [
            "IP-CIDR,192.168.1.0/24",
            "IP-CIDR6,2001:db8::/32",
            "GEOIP,CN",
            "IP-ASN,13335"
        ]
    }
}

# 源类型说明
SOURCE_TYPES = {
    "http": {
        "description": "从HTTP URL获取规则",
        "required_fields": ["url"],
        "optional_fields": ["behavior", "format"]
    },
    "file": {
        "description": "从本地文件获取规则",
        "required_fields": ["path"],
        "optional_fields": ["behavior", "format"]
    }
}

# 文件格式说明
FILE_FORMATS = {
    "yaml": {
        "description": "YAML格式，支持payload结构",
        "example": """
payload:
  - DOMAIN,example.com
  - DOMAIN-SUFFIX,google.com
        """
    },
    "text": {
        "description": "纯文本格式，每行一个规则",
        "example": """
DOMAIN,example.com
DOMAIN-SUFFIX,google.com
# 这是注释
        """
    }
}

def create_sample_config(output_path: str = "config_sample.yaml"):
    """
    创建示例配置文件
    
    Args:
        output_path: 输出文件路径
    """
    import yaml
    
    config_data = [
        {
            "path": "output/ads.yaml",
            "behavior": "classical",
            "upstream": {
                "easylist": {
                    "type": "http",
                    "url": "https://easylist-downloads.adblockplus.org/easylist.txt",
                    "behavior": "classical",
                    "format": "text"
                }
            }
        }
    ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 规则合并器配置文件示例\\n")
        f.write("# 详细说明请参考文档\\n\\n")
        yaml.dump(config_data, f, allow_unicode=True, indent=2, default_flow_style=False)
    
    print(f"示例配置文件已创建: {output_path}")


if __name__ == "__main__":
    # 如果直接运行此文件，创建示例配置
    create_sample_config()
