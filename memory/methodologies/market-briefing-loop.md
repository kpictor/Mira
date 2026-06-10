# Methodology Card: market-briefing-loop

- status: trial
- role: market briefing, market triage, research escalation
- last_updated: 2026-06-10
- source_bucket: institutional; practitioner; first_principles; derived_internal
- source_quality: medium_high
- credibility_score: 4
- credibility_basis: Public institutional examples consistently show daily market updates, weekly market recaps, weekly commentary and market calendars as recurring products. Internal-grade structure (expectation delta, flows/positioning, announcement triage, morning-meeting action discipline) is reconstructed from public copies of Chinese sell-side 晨会纪要, sell-side practice literature, and media-documented desk notes. The method is operationally simple, but its investment value depends on freshness, attribution discipline and escalation quality.
- search_coverage: English retail/wealth public products; Chinese sell-side 晨会纪要 public PDF copies (aggregators); A股实战盘后复盘 practitioner material; sell-side morning call practice literature (Valentine); buy-side morning meeting day-in-the-life accounts; flows/positioning desk notes via media coverage (GS Prime Services, Nomura QIS); Bridgewater Daily Observations public description; Mira internal loop comparison
- search_gaps: Did not read full paid texts of live sell-side morning notes, Bloomberg terminal templates, or internal buy-side desk notes directly; internal-grade structure is reverse-engineered from public copies, practice literature and media citations rather than primary internal documents. Positioning data referenced in media (prime brokerage, CTA models) is not reproducible from free public sources and can only enter briefs as dated secondary citations.
- comparison_baseline: `monitoring-loop` for existing thesis updates
- empirical_validation_mode: live_trial
- follow_through_plan: Use on at least three market scopes: US equity daily brief, US equity weekly review, and one sector/theme weekly. Review whether the escalation queue produces useful follow-up research.

## Core Idea

机构常见的日报/周报不是完整研究包，而是固定节奏的 market triage product。它从市场范围和时间窗口出发，把价格行为、宏观变量、事件日历、新闻流、行业/风格轮动、风险信号和研究升级线索组织成可刷新输出。

Mira 应把它作为独立 loop，而不是塞进 `monitoring_update`。`monitoring_update` 的对象是已有 thesis；`market-briefing-loop` 的对象是市场窗口。

## Reverse-Engineered From

- Schwab Market Update: https://www.schwab.com/learn/schwab-market-update
- Schwab Weekly Trader's Outlook: https://www.schwab.com/learn/story/weekly-traders-outlook
- J.P. Morgan Asset Management Market Updates: https://am.jpmorgan.com/us/en/asset-management/adv/insights/market-insights/market-updates/
- BlackRock Weekly Market Commentary: https://www.blackrock.com/us/individual/insights/blackrock-investment-institute/weekly-commentary
- Morningstar Weekly Markets Planner: https://www.morningstar.com/markets/whats-happening-markets-this-week
- UBS Daily Outlook: https://www.ubs.com/global/en/wealthmanagement/insights/chief-investment-office/house-view/daily.html
- Fidelity Weekly Market Update: https://www.fidelity.com/learning-center/trading-investing/weekly-market-update

以上为零售/财富管理向公开评论。以下为 2026-06-10 补充的机构/台内级样本：

### 中文卖方与实战样本

- 券商晨会纪要公开副本（东方财富研报中心晨会纪要栏目，含国信、东海、财信等）:
  https://stock.eastmoney.com/a/cchjy.html
  共同结构：市场表现 + 市场情绪（涨跌停家数、封板率）+ 资金（两融余额）+
  宏观要闻点评 + 行业与公司快评 + 重点推荐 / 评级与盈利预测变化。
- 东海证券晨会纪要样例（新浪财经转载）:
  https://finance.sina.com.cn/wm/2026-05-13/doc-inhxtvfp4561315.shtml
- A股实战盘后复盘结构（涨停复盘、连板梯队、龙头晋级、涨停题材复盘、情绪周期）:
  https://img3.gelonghui.com/pdf/33dde-21366a86-9b23-48da-9d38-84bac6fcfefc.pdf
- A股情绪周期四阶段（冰点、复苏启动、主升高潮、衰退退潮）与连板高度/涨跌停比值
  作为情绪量化指标: https://caifuhao.eastmoney.com/news/20260425144232343083610

### 英文机构/台内级样本

- James Valentine, Best Practices for Equity Research Analysts（前 Morgan Stanley
  分析师；morning call 纪律与 FaVeS 框架——每个 call 必须在 Forecast / Valuation /
  Sentiment 至少一项上有 out-of-consensus 观点）: CFA Institute 公开样章
  https://www.cfainstitute.org/-/media/documents/support/research-challenge/challenge/best-practices-equity-sample.pdf
- Bridgewater Daily Observations（机构日度宏观笔记的标杆，"the wire"，面向客户与
  政策制定者的实时世界观处理）:
  https://www.bridgewater.com/50-years-of-the-bridgewater-daily-observations
- Goldman Sachs Prime Services 周度仓位数据（net leverage 分位、long/short ratio、
  行业买卖流向；经 Reuters 等媒体长期引用，结构稳定）: 例
  https://www.investing.com/news/economy-news/hedge-fund-tech-positions-hover-near-record-highs-goldman-sachs-says-4708371
- Nomura QIS / Charlie McElligott 日度跨资产笔记（CTA 仓位触发位、dealer gamma
  状态、vol 体制；经媒体公开转述）: 例
  https://www.macrovoices.com/podcast-transcripts/870-charlie-mcelligott-explains-the-upside-catalyst-for-equity-markets
- 买方晨会实践（隔夜新闻对持仓影响 -> 分析师 quick take -> 建议动作）:
  https://www.wallstreetoasis.com/forum/asset-management/day-in-the-life-of-an-investment-analyst

## Internal-Grade Increments

对照台内级样本，零售向公开评论缺少、且已编码进 loop v2 的五个结构差异：

1. **预期差纪律**：宏观数据与财报类 driver 必须记录 consensus/prior vs actual；
   escalation 条目优先承载 out-of-consensus 信息（Valentine FaVeS），而不是复述
   已被定价的新闻。
2. **资金面与仓位是 first-class 输入**：A股为两融余额、涨跌停/连板梯队、龙虎榜、
   北向盘后成交额（注意披露口径限制）；美股为 breadth、vol、CFTC COT、ETF 流向等
   公开免费口径，prime brokerage / CTA 数据只能以带 publish time 的媒体转引进入。
3. **隔夜公告与评级变化 triage**：晨会纪要的核心不是行情复述，而是公告点评、
   评级/盈利预测变化和重点推荐；daily brief 必须有对应扫描问题。
4. **A股情绪结构指标**：连板高度、涨跌停家数比、封板率、情绪周期阶段是 A股
   close wrap 的标准件，不是可选项。
5. **So-what-for-book 与队列生命周期**：买方晨会以"对持仓/watchlist 的影响 +
   建议动作"收尾；escalation queue 必须跨期累积、带状态流转（open / escalated /
   expired / dismissed），而不是一次性表格。

## Search Paths Used

- `daily market update`, `market open report`, `weekly market recap`
- `weekly market commentary`, `weekly trader outlook`, `markets this week`
- institutional public sites from Schwab, J.P. Morgan Asset Management, BlackRock, Morningstar, UBS and Fidelity
- `券商晨会纪要 结构 宏观要闻 评级变化 重点推荐`、`中金早班车 晨会纪要`
- `A股 盘后复盘 涨停板梯队 连板 情绪周期 北向资金 两融 龙虎榜`
- `Valentine best practices equity research morning call consensus`
- `Bridgewater Daily Observations`、`Goldman Sachs prime brokerage weekly positioning`
- `Nomura McElligott CTA positioning dealer gamma`、buy-side `morning meeting` accounts
- internal comparison against `loops/monitoring-loop.md`

## Use When

- 用户问“日报 / 周报 / 盘前简报 / 收盘复盘 / 本周市场回顾 / 下周市场怎么看”
- 用户指定某个市场、板块、主题或 watchlist，希望做固定窗口观察
- 用户想知道今天/本周哪些变量需要刷新或升级研究
- 需要把市场新闻流转成 research escalation queue，而不是完整 thesis

## Avoid When

- 用户要完整研究单票、财报、研报解读或组合复盘；应路由到对应 loop/skill
- 用户要求真实仓位、下单、仓位大小或交易执行；必须走 decision/actionability gates
- 数据无法建立 quote/publish time，而用户要求 live-use 判断
- 只有 price-only 叙事，无法做 attribution quality 标注

## Applies To

- US equities, A-shares, HK equities, global macro, commodities, rates-sensitive assets
- sector/theme windows such as AI semiconductors, China internet, power equipment, robotics
- PM/trader risk watch when holdings are provided or when only research-only risk triage is needed

## Core Question

在给定市场范围和时间窗口内，哪些价格行为、事件、宏观变量、行业/主题变化和风险信号具有足够信息量，值得进入 watchlist、刷新已有 thesis 或升级为正式研究？

## Required Inputs

- `briefing_type`
- `market_scope`
- `time_boundary`
- quote/publish/as-of time for live or near-live inputs
- macro/earnings/policy calendar when relevant
- source notes for material claims
- optional watchlist or portfolio context

## Primary Signal

- confirmed or plausible drivers behind major moves
- sector/theme/factor rotation and breadth
- dated catalysts and next checks
- divergence between market pricing and available evidence
- escalation queue quality

## Why It Works

固定频率 brief 的价值不是预测市场，而是压缩信息流、识别主导变量、暴露需要刷新的旧判断，并把“市场发生了什么”转成可执行的研究下一步。机构公开产品普遍包含每日市场更新、周度回顾、下周预览、市场日历和策略评论，说明这种工作流是常见投研表面。

## Failure Mode

- 把日报写成新闻摘要，没有 research escalation
- 用事后叙事解释所有价格波动，缺少 attribution quality
- 忽略数据时间戳，导致 stale market view 被复用
- 把 price reaction 当成基本面验证
- 在没有持仓、mandate 和风险预算时输出仓位或交易建议

## Evidence Cost

中等。`quick_map` 需要少量高质量、带时间戳的市场和事件来源；`standard` 需要补充 calendar、sector/theme rotation、source notes 和 escalation queue；`deep_dive` 才需要更完整的跨资产、仓位、流动性和历史对比。

## Speed Vs Depth

- daily brief: speed > depth，默认短生命周期
- close wrap: speed and attribution balance
- weekly review: depth > daily，强调主导变量和下周事件
- sector/theme weekly: depth depends on theme complexity
- risk/positioning watch: depth depends on portfolio context and data availability

## Comparison To Existing Methods

相对 `monitoring-loop`，本方法不要求已有 thesis，也不从单个研究对象出发。它先观察市场窗口，再决定是否把某个对象送入 `quick_map`、`monitoring_update`、`earnings_event` 或 `first_pass_research`。

相对 `macro-regime-analysis`，本方法不尝试建立宏观 regime，只在 briefing 窗口内识别宏观变量对市场的短期信息价值。

## Follow-Through Criteria

- brief 是否写清了 `stale_after` 和 `must_refresh_if`
- source notes 是否包含 quote/publish/as-of time
- major moves 是否有 attribution quality，而不是单一叙事
- 宏观/财报类 driver 是否记录了 consensus_or_prior vs actual 的预期差
- escalation queue 是否能产生后续有效研究，open 条目是否在下一次 brief 被复核
- 被升级对象是否真的改善了 thesis freshness 或 source coverage

## Trial Design

- target_case_1: `US equities daily_market_brief`
- target_case_2: `US equities weekly_market_review`
- target_case_3: `AI semiconductors sector_theme_weekly`
- target_case_4: optional `HK equities weekly_market_review`
- target_case_5: `A shares market_close_wrap`（检验情绪结构指标：连板梯队、
  涨跌停比、两融、龙虎榜）
- target_case_6: `US equities risk_positioning_watch`（research-only，检验与
  position/portfolio loops 的边界是否清晰、是否漂移成仓位建议）

每个 case 都要检查：source freshness、driver attribution、expectation delta、facts/inferences/judgments 分离、escalation queue 命中率与状态流转，以及下一轮 follow-through。close wrap 和 risk watch 两类必须至少各跑一次才能进入 adoption decision。

## Falsification Conditions

- 连续三次 brief 只产出泛泛新闻摘要，不能产生有用 escalation
- 多数 driver attribution 无法被来源支持，或经常把 price-only 移动写成事实判断
- 用户复用 brief 时经常越过 `stale_after` 造成错误结论
- brief 明显重复 `monitoring-loop` 或 `macro-regime-analysis`，没有独立价值

## Adoption Decision

进入 `trial`。理由：机构样本和 Mira 内部缺口都支持新增独立 loop；但还需要真实日报/周报 case 验证是否改善研究升级、刷新边界和用户使用效率，不能直接标记 `adopted`。
