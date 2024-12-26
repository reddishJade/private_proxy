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



- 新增借鉴xndeye的[rule-merger](https://github.com/xndeye/rule-merger)的自用规则集文件以及配置文件[merger.yaml](https://github.com/reddishJade/private_proxy/blob/main/merger.yaml)，merger用法详见[用法](https://github.com/xndeye/rule-merger?tab=readme-ov-file#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)

| reject@ip     | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/c.yaml) |
| ------------- | ------------------------------------------------------------ |
| reject@ip     | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/reject@ip.yaml) |
| direct        | [link](https://raw.githubusercontent.com/reddishJade/private_proxy/refs/heads/main/output/direct.yaml) |
| apple@cn      | [link](https://github.com/reddishJade/private_proxy/blob/main/output/apple@cn.yaml) |
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

