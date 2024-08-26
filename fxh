proxy-providers:
  iKuuu:
    url: "https://y2n00.no-mad-world.club/link/MngYxPypRGEjDTwW?clash=3"
    type: http
    exclude-filter: "免费"
    interval: 86400
    health-check:
      {
        enable: true,
        url: "https://www.gstatic.com/generate_204",
        interval: 600,
      }

ipv6: true
allow-lan: true
mixed-port: 7890
unified-delay: true
tcp-concurrent: true
keep-alive-interval: 30
find-process-mode: strict
global-client-fingerprint: chrome
external-controller: 127.0.0.1:9090
external-ui: ui
external-ui-url: "https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip"

profile:
  store-selected: true
  store-fake-ip: true

dns:
  enable: true
  ipv6: true
  enhanced-mode: fake-ip
  fake-ip-filter:
    - "*"
    - "+.lan"
    - "+.local"
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query

hosts:
  "mtalk.google.com": 142.250.157.188
  "alt1-mtalk.google.com": 142.250.157.188
  "alt2-mtalk.google.com": 142.250.115.188
  "alt3-mtalk.google.com": 108.177.97.188
  "alt4-mtalk.google.com": 173.194.202.188
  "alt5-mtalk.google.com": 142.250.141.188
  "alt6-mtalk.google.com": 142.250.115.188
  "alt7-mtalk.google.com": 142.250.141.188
  "alt8-mtalk.google.com": 142.250.152.188
  "dl.google.com": 180.163.151.161
  "dl.l.google.com": 180.163.150.33

sniffer:
  enable: true
  sniff:
    HTTP:
      ports: [80, 8080-8880]
      override-destination: true
    TLS:
      ports: [443, 8443]
    QUIC:
      ports: [443, 8443]

tun:
  enable: true
  stack: mixed
  dns-hijack:
    - "any:53"
    - "tcp://any:53"
  auto-route: true
  auto-redirect: true
  auto-detect-interface: true

# proxies:

proxy-groups:
  - {
      name: 节点选择,
      type: select,
      proxies:
        [
          自动回退,
          手动选择,
          香港节点,
          台湾节点,
          日本节点,
          新加坡节点,
          美国节点,
          DIRECT,
        ],
    }

  - { name: 手动选择, type: select, include-all-providers: true }
  - {
      name: 自动回退,
      type: fallback,
      include-all-providers: true,
      filter: "(?i)IEPL",
      tolerance: 10,
      lazy: true,
    }

  - { name: AI, type: select, proxies: [日本节点, 香港节点] }
  - { name: Apple, type: select, proxies: [节点选择, DIRECT] }
  - { name: CDN, type: select, proxies: [Download, DIRECT] }
  - { name: Domestic, type: select, proxies: [DIRECT, 节点选择] }
  - { name: Global, type: select, proxies: [节点选择, DIRECT] }
  - { name: Microsoft, type: select, proxies: [节点选择, DIRECT] }
  - { name: NetEase Music, type: select, proxies: [DIRECT] }
  - {
      name: Streaming,
      type: select,
      proxies: [节点选择, DIRECT, 香港节点, 美国节点],
    }
  - { name: Telegram, type: select, proxies: [节点选择, 手动选择] }
  - { name: Final, type: select, proxies: [节点选择, DIRECT] }

  # 地区分组
  # - { name: 🇭🇰 香港节点, <<: *use, filter: "(?i)港|hk|hongkong|hong kong" }
  - {
      name: 香港节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)港|hk",
      lazy: true,
    }
  - {
      name: 台湾节点,
      type: select,
      include-all-providers: true,
      filter: "(?i)台|tw",
      disable-udp: true,
    }
  - {
      name: 日本节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)日|jp",
      exclude-filter: "下载",
      lazy: true,
    }
  - {
      name: 新加坡节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)(新|sg)",
      lazy: true,
    }
  - {
      name: 美国节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)美|us",
      lazy: true,
    }
  - {
      name: Download,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)下载",
      lazy: true,
    }

rule-providers:
  # 广告拦截 / 隐私保护 / Malware 拦截 / Phiishing 拦截
  reject_non_ip_no_drop:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/reject-no-drop.txt
    path: ./sukkaw_ruleset/reject_non_ip_no_drop.txt
  reject_non_ip_drop:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/reject-drop.txt
    path: ./sukkaw_ruleset/reject_non_ip_drop.txt
  reject_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/reject.txt
    path: ./sukkaw_ruleset/reject_non_ip.txt
  reject_domainset:
    type: http
    behavior: domain
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/domainset/reject.txt
    path: ./sukkaw_ruleset/reject_domainset.txt
  reject_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/reject.txt
    path: ./sukkaw_ruleset/reject_ip.txt
  # 包含所有常见静态资源 CDN 域名、对象存储域名
  cdn_domainset:
    type: http
    behavior: domain
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/domainset/cdn.txt
    path: ./sukkaw_ruleset/cdn_domainset.txt
  cdn_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/cdn.txt
    path: ./sukkaw_ruleset/cdn_non_ip.txt
  # 流媒体
  stream_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/stream.txt
    path: ./sukkaw_ruleset/stream_non_ip.txt
  stream_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/stream.txt
    path: ./sukkaw_ruleset/stream_ip.txt
  # AI服务
  ai_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/ai.txt
    path: ./sukkaw_ruleset/ai_non_ip.txt
  # 电报服务
  telegram_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/telegram.txt
    path: ./sukkaw_ruleset/telegram_non_ip.txt
  telegram_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/telegram.txt
    path: ./sukkaw_ruleset/telegram_ip.txt
  # 规则组包含 Apple, Inc. 在中华人民共和国完成工信部 ICP 备案和公安网备、且在中华人民共和国境内提供 HTTP 服务的域名
  apple_cdn:
    type: http
    behavior: domain
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/domainset/apple_cdn.txt
    path: ./sukkaw_ruleset/apple_cdn.txt
  # Apple服务
  apple_services:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/apple_services.txt
    path: ./sukkaw_ruleset/apple_services.txt
  # 云上贵州（icloud.com.cn）和 苹果地图大陆特供版 等服务的域名。
  apple_cn_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/apple_cn.txt
    path: ./sukkaw_ruleset/apple_cn_non_ip.txt
  # 规则组包含 Microsoft 在中华人民共和国完成工信部 ICP 备案和公安网备、且在中华人民共和国境内提供 HTTP 服务的域名
  microsoft_cdn_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/microsoft_cdn.txt
    path: ./sukkaw_ruleset/microsoft_cdn_non_ip.txt
  # 微软服务
  microsoft_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/microsoft.txt
    path: ./sukkaw_ruleset/microsoft_non_ip.txt
  # 网易云音乐
  neteasemusic_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/neteasemusic.txt
    path: ./sukkaw_ruleset/neteasemusic_non_ip.txt
  neteasemusic_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/neteasemusic.txt
    path: ./sukkaw_ruleset/neteasemusic_ip.txt
  # 软件更新、操作系统等大文件下载
  download_domainset:
    type: http
    behavior: domain
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/domainset/download.txt
    path: ./sukkaw_ruleset/download_domainset.txt
  download_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/download.txt
    path: ./sukkaw_ruleset/download_non_ip.txt
  # 内网域名和局域网 IP
  lan_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/lan.txt
    path: ./sukkaw_ruleset/lan_non_ip.txt
  lan_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/lan.txt
    path: ./sukkaw_ruleset/lan_ip.txt
  # 其他网站
  domestic_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/domestic.txt
    path: ./sukkaw_ruleset/domestic_non_ip.txt
  direct_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/direct.txt
    path: ./sukkaw_ruleset/direct_non_ip.txt
  global_non_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/non_ip/global.txt
    path: ./sukkaw_ruleset/global_non_ip.txt
  domestic_ip:
    type: http
    behavior: classical
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/domestic.txt
    path: ./sukkaw_ruleset/domestic_ip.txt
  # chnroute CIDR
  # 补充合并了 Misaka Network, Inc. 收不到 BGP 路由的部分国内段、排除了被 Misaka Network, Inc. 误收的在香港广播的 IP 段（通常由 中国移动国际 CMI 广播）
  china_ip:
    type: http
    behavior: ipcidr
    format: text
    interval: 43200
    url: https://ruleset.skk.moe/Clash/ip/china_ip.txt
    path: ./sukkaw_ruleset/china_ip.txt

rules:
  # Reject rules
  - RULE-SET,reject_domainset,REJECT
  - RULE-SET,reject_non_ip,REJECT
  - RULE-SET,reject_non_ip_drop,REJECT-DROP
  - RULE-SET,reject_non_ip_no_drop,REJECT
  - RULE-SET,reject_ip,REJECT
  # CDN rules
  - RULE-SET,cdn_domainset,CDN
  - RULE-SET,cdn_non_ip,CDN
  # Streaming services
  - DOMAIN-SUFFIX,misakaf.org,Streaming
  - RULE-SET,stream_non_ip,Streaming
  # AI services
  - RULE-SET,ai_non_ip,AI
  # Telegram
  - RULE-SET,telegram_non_ip,Telegram
  # Apple services
  - RULE-SET,apple_cdn,Domestic
  - RULE-SET,apple_services,Apple
  - RULE-SET,apple_cn_non_ip,Domestic
  # Microsoft services
  - RULE-SET,microsoft_cdn_non_ip,Domestic
  - RULE-SET,microsoft_non_ip,Microsoft
  # NetEase Music
  - RULE-SET,neteasemusic_non_ip,NetEase Music
  # Download
  - RULE-SET,download_domainset,CDN
  - RULE-SET,download_non_ip,CDN
  # LAN
  - RULE-SET,lan_non_ip,DIRECT
  # Misc rules
  - RULE-SET,domestic_non_ip,Domestic
  - RULE-SET,direct_non_ip,DIRECT
  - RULE-SET,global_non_ip,Global
  # IP rules
  - RULE-SET,stream_ip,Streaming
  - RULE-SET,telegram_ip,Telegram
  - RULE-SET,neteasemusic_ip,NetEase Music
  - RULE-SET,lan_ip,DIRECT
  - RULE-SET,domestic_ip,Domestic
  - RULE-SET,china_ip,Domestic
  # Final rules
  - GEOIP,CN,Domestic
  - MATCH,Final
