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
        interval: 300,
      }

mode: rule
ipv6: true
log-level: error
allow-lan: true
mixed-port: 7890
socks-port: 7891
unified-delay: true
tcp-concurrent: true
external-controller: 127.0.0.1:9090
external-ui: ui
external-ui-url: "https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip"
geodata-mode: true
find-process-mode: strict
global-client-fingerprint: random

profile:
  store-selected: true
  store-fake-ip: true

sniffer:
  enable: true
  sniff:
    TLS:
      ports: [443, 8443]
    HTTP:
      ports: [80, 8080-8880]
      override-destination: true
    QUIC:
      ports: [443, 8443]
  skip-domain:
    - "Mijia Cloud"
    - "+.push.apple.com"

tun:
  enable: true
  stack: system
  # stack: system # or 'gvisor'
  dns-hijack:
    - "any:53"
    - "tcp://any:53"
  auto-route: true
  auto-redirect: true
  auto-detect-interface: true

dns:
  enable: true
  ipv6: true
  listen: :1053
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  use-hosts: true
  fake-ip-filter:
    - "*"
    - "+.lan"
    - "+.local"
  prefer-h3: true
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - https://dns.google/dns-query
    - https://cloudflare-dns.com/dns-query
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4

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
          其它地区,
          DIRECT,
        ],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Proxy.png,
    }
  - {
      name: 手动选择,
      type: select,
      include-all-providers: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Filter.png,
    }
  - {
      name: 自动回退,
      type: fallback,
      include-all-providers: true,
      filter: "(?i)IEPL",
      tolerance: 10,
      lazy: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Available.png,
    }
  - {
      name: AI,
      type: select,
      proxies: [日本节点, 香港节点],
      icon: https://clash-verge-rev.github.io/assets/icons/chatgpt.svg,
    }
  - {
      name: Apple,
      type: select,
      proxies: [DIRECT, 节点选择],
      icon: https://clash-verge-rev.github.io/assets/icons/apple.svg,
    }
  - {
      name: Google,
      type: select,
      proxies: [节点选择, DIRECT],
      icon: https://fastly.jsdelivr.net/gh/clash-verge-rev/clash-verge-rev.github.io@main/docs/assets/icons/google.svg,
    }
  - {
      name: Microsoft,
      type: select,
      proxies: [节点选择, DIRECT],
      icon: https://clash-verge-rev.github.io/assets/icons/microsoft.svg,
    }
  - {
      name: Telegram,
      type: select,
      proxies: [节点选择, 手动选择],
      icon: https://clash-verge-rev.github.io/assets/icons/telegram.svg,
    }
  - {
      name: Game,
      type: select,
      proxies: [DIRECT, 节点选择],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Game.png,
    }
  - {
      name: Streaming,
      type: select,
      proxies: [节点选择, DIRECT, 香港节点, 美国节点],
      icon: https://clash-verge-rev.github.io/assets/icons/youtube.svg,
    }
  - {
      name: Music,
      type: select,
      proxies: [节点选择, DIRECT, 香港节点, 美国节点],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Spotify.png,
    }
  - {
      name: Global,
      type: select,
      proxies: [节点选择, DIRECT],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Global.png,
    }
  - {
      name: Domestic,
      type: select,
      proxies: [DIRECT, 节点选择],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Domestic.png,
    }
  - {
      name: Private,
      type: select,
      proxies: [DIRECT, 节点选择],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Lock.png,
    }
  - {
      name: Final,
      type: select,
      proxies: [节点选择, DIRECT],
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Final.png,
    }
  # 地区分组
  # - { name: 🇭🇰 香港节点, <<: *use, filter: "(?i)港|hk|hongkong|hong kong" }
  - {
      name: 香港节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)港|hk",
      lazy: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Hong_Kong.png,
    }
  - {
      name: 台湾节点,
      type: select,
      include-all-providers: true,
      filter: "(?i)台|tw",
      disable-udp: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Taiwan.png,
    }
  - {
      name: 日本节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)日|jp",
      exclude-filter: "下载",
      lazy: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Japan.png,
    }
  - {
      name: 新加坡节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)(新|sg)",
      lazy: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Singapore.png,
    }
  - {
      name: 美国节点,
      type: url-test,
      include-all-providers: true,
      filter: "(?i)美|us",
      lazy: true,
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/United_States.png,
    }
  - {
      name: 其它地区,
      type: select,
      include-all-providers: true,
      filter: "(?i)^(?!.*(?:🇭🇰|🇯🇵|🇺🇸|🇸🇬|🇨🇳|港|hk|hongkong|台|tw|taiwan|日|jp|japan|新|sg|singapore|美|us|unitedstates)).*",
      icon: https://fastly.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Airport.png,
    }
  # - { name: 全部节点, <<: *use }

rule-providers:
  ads:
    type: http
    behavior: domain
    format: text
    path: ./rules/ads.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/ads.list"
    interval: 86400

  applications:
    type: http
    behavior: classical
    format: text
    path: ./rules/applications.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/applications.list"
    interval: 86400

  private:
    type: http
    behavior: domain
    format: text
    path: ./rules/private.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/private.list"
    interval: 86400

  microsoft-cn:
    type: http
    behavior: domain
    format: text
    path: ./rules/microsoft-cn.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/microsoft-cn.list"
    interval: 86400

  apple-cn:
    type: http
    behavior: domain
    format: text
    path: ./rules/apple-cn.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/apple-cn.list"
    interval: 86400

  google-cn:
    type: http
    behavior: domain
    format: text
    path: ./rules/google-cn.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/google-cn.list"
    interval: 86400

  games-cn:
    type: http
    behavior: domain
    format: text
    path: ./rules/games-cn.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/games-cn.list"
    interval: 86400

  ai:
    type: http
    behavior: domain
    format: text
    path: ./rules/ai.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/ai.list"
    interval: 86400

  Streaming:
    type: http
    behavior: classical
    path: ./rules/Streaming.yaml
    url: "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/GlobalMedia/GlobalMedia_Classical.yaml"
    interval: 86400

  Spotify:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Spotify/Spotify.yaml"
    path: ./rules/Spotify.yaml
    interval: 86400

  Tidal:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TIDAL/TIDAL.yaml"
    path: ./rules/Tidal.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    format: text
    path: ./rules/proxy.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/proxy.list"
    interval: 86400

  cn:
    type: http
    behavior: domain
    format: text
    path: ./rules/cn.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/cn.list"
    interval: 86400

  telegramip:
    type: http
    behavior: ipcidr
    format: text
    path: ./rules/telegramip.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/telegramip.list"
    interval: 86400

  privateip:
    type: http
    behavior: ipcidr
    format: text
    path: ./rules/privateip.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/privateip.list"
    interval: 86400

  cnip:
    type: http
    behavior: ipcidr
    format: text
    path: ./rules/cnip.list
    url: "https://raw.githubusercontent.com/DustinWin/ruleset_geodata/clash-ruleset/cnip.list"
    interval: 86400

rules:
  - RULE-SET,ads,REJECT
  - RULE-SET,private,Private
  - RULE-SET,applications,DIRECT
  - DOMAIN-SUFFIX,genspark.ai,AI
  - DOMAIN-SUFFIX,perplexity.ai,AI
  - RULE-SET,ai,AI
  - RULE-SET,apple-cn,Apple
  - RULE-SET,google-cn,Google
  - RULE-SET,microsoft-cn,Microsoft
  - RULE-SET,games-cn,Game
  - RULE-SET,Spotify,Music
  - RULE-SET,Tidal,Music
  - DOMAIN-SUFFIX,misakaf.org,Streaming
  - RULE-SET,Streaming,Streaming
  - RULE-SET,proxy,Global
  - RULE-SET,cn,Domestic
  - RULE-SET,telegramip,Telegram,no-resolve
  - RULE-SET,privateip,Private,no-resolve
  - RULE-SET,cnip,Domestic
  - MATCH,Final
