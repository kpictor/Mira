# Market Briefing Loop

`market-briefing-loop` 用于生成固定频率或用户触发的市场观察产品：
daily brief、market close wrap、weekly market review、sector/theme weekly 和
risk/positioning watch。

它不是后台监控承诺，也不是完整 research package。它从 `market_scope` 出发，
把价格行为、宏观变量、事件日历、新闻流、行业/风格轮动和研究升级线索组织成
可刷新、可追溯的 market briefing。

## Objective

- 在盘前、盘中、收盘后或周度窗口内总结市场状态
- 区分事实、市场定价、推断和判断
- 识别主导变量、异常移动和高信息量事件
- 给出需要升级到 `quick_map`、`monitoring_update`、`earnings_event` 或
  `first_pass_research` 的 research escalation queue
- 写清 source freshness、quote/publish time、`stale_after` 和
  `must_refresh_if`

## Loop Input

- `briefing_type`: `daily_market_brief` / `market_close_wrap` /
  `weekly_market_review` / `sector_theme_weekly` / `risk_positioning_watch`
- `market_scope`: 例如 `US equities`、`A shares`、`HK equities`、`global macro`
  或特定行业/主题
- `time_boundary`: 盘前、收盘后、过去 1 个交易日、本周、下周预览等
- `source_boundary`: 公开来源、本地数据、指定链接、vendor export 或用户材料
- `watchlist_scope`: 可选；用户给定的 ticker、行业、主题、宏观变量或已有 thesis
- `output_depth`: `quick_map` / `standard` / `deep_dive`

## Briefing Types

### `daily_market_brief`

盘前或当天市场简报。默认问题：

- 隔夜或盘前哪些资产、行业、主题和宏观变量移动最大？
- 哪些移动有清晰催化剂，哪些只是噪音或流动性？
- 隔夜数据和财报相对公开预期（consensus / prior）是超预期还是低于预期？
  哪些已被定价、哪些还没有？
- 隔夜有哪些公司公告、评级/盈利预测变化或重点推荐变动需要 triage？
- 今天有哪些宏观数据、央行、财报、政策或公司事件可能改变判断？
- 哪些对象需要刷新 quote、source 或 thesis？

默认输出：

- `market snapshot`
- `key overnight / premarket moves`
- `driver map`
- `today calendar`
- `watchlist changes`
- `research escalation queue`
- `stale_after = next market session or next major scheduled release`

### `market_close_wrap`

收盘后复盘。默认问题：

- 当天涨跌、风格/行业/主题轮动和广度是否一致？
- 资金面和情绪结构怎么走：成交额、breadth、vol；A股加涨跌停家数、封板率、
  连板高度/梯队、两融余额、龙虎榜和北向盘后成交额？
- 市场叙事是否解释了价格行为，还是存在未解释的 divergence？
- 哪些 move 改变了短期 risk window 或已有 thesis 的刷新条件？

默认输出：

- `close snapshot`
- `move attribution`
- `sector / theme / factor rotation`
- `breadth and reaction quality`
- `flows and sentiment structure`
- `unexplained moves`
- `next-session watchpoints`

### `weekly_market_review`

周度市场复盘和下周预览。默认问题：

- 本周主导变量是什么：盈利、利率、通胀、政策、流动性、仓位、主题叙事还是事件？
- 哪些变化只是价格噪音，哪些进入 thesis / watchlist / risk register？
- 下周哪些事件最可能改变市场状态？

默认输出：

- `week in review`
- `dominant market variables`
- `asset / sector / theme rotation`
- `earnings / macro / policy calendar`
- `thesis impact queue`
- `next-week watchpoints`
- `stale_after = next weekly review or major intervening event`

### `sector_theme_weekly`

特定行业、主题或市场段周报。默认问题：

- 主题内谁在领涨/领跌，是否符合基本面或事件差异？
- 主题叙事、订单、价格、供需、政策、竞争和估值变量是否变化？
- 哪些公司需要进入单票 `quick_map` 或正式研究？

默认输出：

- `theme snapshot`
- `leader / laggard map`
- `fundamental signal map`
- `narrative and positioning change`
- `company handoff queue`

### `risk_positioning_watch`

PM 或交易台风格的风险观察。默认问题：

- 哪些 crowded trades、vol、rates、FX、credit、liquidity、earnings 或 policy
  variables 可能改变风险承受度？
- 风险是 price-only、positioning、fundamental、macro 还是 liquidity driven？
- 哪些风险需要升级为 `position_review`、`portfolio_construction_review` 或
  `actionability` 检查？

默认输出：

- `risk dashboard`
- `positioning and crowding notes`
- `macro and liquidity stress map`
- `portfolio relevance`
- `escalation triggers`

## States

### `define-brief`

确认 `briefing_type`、`market_scope`、`time_boundary`、source boundary 和
用户指定 watchlist。没有指定市场时，先用用户上下文推断一个最小市场范围；不确定
时声明假设。

### `run-live-data-gate`

日报、盘前、盘中、收盘复盘和“最新/今天/本周”问题默认触发
[../data/live-data-source-policy.md](../data/live-data-source-policy.md)。
必须记录 quote time、publish time、as-of time 或明确 source gap。

### `collect-snapshot`

按市场范围收集最小可用 source pack：

- broad index / benchmark
- rates / FX / commodities / credit proxy when relevant
- sector / theme / factor movers
- flows / positioning / sentiment structure（公开免费口径）:
  - A股: 成交额、涨跌停家数与连板梯队、封板率、两融余额、龙虎榜、
    北向盘后成交额（无盘中实时口径）
  - US / global: breadth、vol（VIX 等）、CFTC COT、公开 ETF 流向；
    prime brokerage / CTA / gamma 数据只能以带 publish time 的媒体转引进入
- overnight announcements / rating and estimate changes for watchlist names
- macro / policy / earnings calendar，关键条目带 consensus_or_prior
- company or theme watchlist items
- official / primary source for material claims where practical

`quick_map` 只取其中与本次问题直接相关的最小子集；缺哪类数据就标 source gap，
不为凑齐快照而降低来源质量。

### `classify-moves-and-claims`

把输入分为以下桶；写入 evidence log 时映射到
[../data/claim-taxonomy.md](../data/claim-taxonomy.md) 的规范 token：

| briefing 桶 | claim-taxonomy 映射 |
| --- | --- |
| `reported_fact` | `fact` / `reported_metric` |
| `market_pricing` | `market_pricing` |
| `company_or_policy_claim` | `company_claim` / `guidance`（speaker=`company`/`regulator`） |
| `macro_release` | `reported_metric`（speaker=`official_agency`） |
| `sellside_or_expert_view` | `opinion` / `forecast`（speaker=`sellside`/`buyside`） |
| `weak_signal` | `rumor_signal` / `sentiment` |
| `mira_inference` | `interpretation` / `derived_calculation`（speaker=`mira`） |

不得把价格反应直接写成基本面验证。对 `macro_release` 和财报类条目，记录
consensus_or_prior vs actual：超预期/低于预期才是信息，复述已定价结果不是。

### `build-driver-map`

对主要移动给出 driver attribution：

- `confirmed_driver`: 有明确事件、数据或披露支持
- `plausible_driver`: 与价格行为和来源一致，但缺少直接证明
- `contested_driver`: 存在多个解释或来源冲突
- `unexplained_move`: 暂无高质量解释，只能进入 watchlist

### `separate-signal-from-noise`

按信息价值排序：

- 影响多资产或多行业的变量优先
- 相对公开预期有 surprise 的结果优先于已被定价的好坏消息
- 改变预期、贴现率、盈利、流动性或风险溢价的变量优先
- 与用户 watchlist / 已有 thesis / 持仓直接相关的条目优先给出
  so-what 和建议动作
- 有 follow-through 可能的异常移动优先
- 单日 price-only 且无来源支持的解释降级为 `watch_only`

### `write-briefing`

使用匹配模板输出 brief。`quick_map` 可只输出简版；`standard` 和 `deep_dive`
必须写清 source notes、refresh boundary 和 escalation queue。

### `escalate-or-close`

把高信息量条目路由到下一步：

- 单票新问题 -> `first_pass_research` 或 `quick_map`
- 已有 thesis 增量 -> `monitoring_update`
- 财报/指引/业绩会 -> `earnings_event`
- 研报或 rating/target change -> `research_report_interpretation`
- 宏观数据发布 -> macro data release triage / macro overlay
- 真实持仓或组合风险 -> `position_review` / `portfolio_construction_review`
- 仅价格异动且来源弱 -> `watch_only`

escalation queue 是跨期累积的工作队列，不是单次输出表格：

- 同一 briefing package 内维护一份累积 `escalation-queue.csv`，每条带
  `status`（`open` / `escalated` / `expired` / `dismissed`）、`escalated_to`
  和 `status_updated`。
- 每次新 brief 先复核上一次的 `open` 条目：仍有效保留，已升级标
  `escalated` 并写明去向，过了 refresh_condition 标 `expired`，证伪标
  `dismissed`。
- 升级条目优先承载预期差信息；连续多期 `open` 而无人升级的条目要么给出
  升级理由，要么显式 `expired`，不允许无限挂账。

## Source Handling Rules

- 日报和收盘复盘必须优先使用带时间戳的市场数据、官方日历、公司 IR、监管、交易所、
  央行、统计机构或高质量市场媒体。
- 周报可以使用机构周度评论、策略 note、公开研究和图表，但必须标注 publish date。
- 使用付费研报、vendor export、用户文件或截图时，先走
  [../data/ingestion-layer.md](../data/ingestion-layer.md)。
- 弱信号、社媒和传闻只能进入 `weak_signal` 或 `watch_only`，不能支撑 durable
  conclusion。
- 仓位/资金面数据只用公开免费口径：A股两融、涨跌停、龙虎榜为每日公开；北向资金
  无盘中实时披露，只能引用盘后口径，不得出现"实时北向流入"类表述。prime
  brokerage、CTA 模型、dealer gamma 等台内数据只能以带 publish time 的媒体转引
  进入，标 `sellside_or_expert_view`，不得当作可复现数据。
- 任何实时或接近实时的结论都必须写清 `stale_after`；盘前简报通常在开盘后失效，
  收盘复盘通常在下一交易日前或重大隔夜事件后失效。

## Output Location

briefing 输出按市场范围 + 月份归档，brief 文件按日期命名，escalation queue
在 package 内跨期累积：

```text
cases/<market_scope>-briefing-<YYYY-MM>/
├── README.md
├── daily-brief-<YYYY-MM-DD>.md
├── close-wrap-<YYYY-MM-DD>.md
├── weekly-review-<YYYY>-W<ww>.md
├── sector-theme-weekly-<YYYY>-W<ww>.md
└── escalation-queue.csv   # 累积队列，带 status 生命周期
```

`market_scope` 用短 slug（如 `us-equities`、`a-shares`、`ai-semis`）。用户私有
watchlist/持仓相关的 brief 增量写入 `private/research/<OBJECT>/`，不进公共 cases。

## Output

- `briefing header`
- `market snapshot`
- `key moves`
- `driver map`
- `calendar / catalyst watch`
- `facts / inferences / judgments`
- `research escalation queue`
- `source notes`
- `stale_after`
- `must_refresh_if`

## Boundaries

- 不输出交易指令、仓位大小或自动执行建议。
- 不声称 Mira 在后台持续盯盘；除非用户显式创建 automation，否则 brief 只在用户触发
  或当前任务内运行。
- 不把日报/周报替代完整 thesis research；brief 的核心价值是 triage、refresh 和
  escalation。
