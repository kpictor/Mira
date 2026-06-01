# Methodology Card: Long-Term Multibagger Research

- status: trial
- role: framework-lens + portfolio-discipline
- last_updated: 2026-06-01
- source_bucket: mixed (`institutional`, `practitioner`, `first_principles`, `derived_internal`)
- source_quality: medium-high
- credibility_score: medium-high
- credibility_basis: 核心逻辑来自长期个股收益右偏分布、Baillie Gifford LTGG 的长期右尾研究流程、长期资产配置/分散原则、实践派 tenbagger 思维和 Mira 现有 thesis horizon / framework routing；但能否稳定提前识别 10x/100x 候选，需要更多历史 case backtest 和 forward watch 验证。
- search_coverage: medium-high
- search_gaps: 还缺系统的失败样本库、A 股/港股长期倍数股样本、不同利率 regime 下高成长股估值容忍度对比、Baillie Gifford 历史持仓退出案例的可复现 source trail、以及真实组合层面的 sizing / trimming 复盘。
- comparison_baseline: `ordinary long_term_thesis research` + `variant-perception without return-path math`
- empirical_validation_mode: trial -> case backtest + forward watch + live case trial
- follow_through_plan: 先用 2-3 个历史 10x/100x 案例和 2 个当前候选标的试跑；每个 case 必须记录初始 target_return_path、evidence_ladder、kill_criteria 和后续刷新触发。

## Core Idea

`long-term-multibagger research` 的核心不是寻找“好公司”，而是寻找在足够长时间里可能让收入、利润、现金流和市场定价共同复利的结构，同时用组合纪律处理极度右偏分布带来的高失败率。

这个 lens 要先把目标收益路径数学化，再判断公司是否真的有足够长的再投资 runway、足够强的 right to win、足够稳的生存能力，以及足够清楚的证据阶梯来逐步提高或降低仓位信心。

## Reverse-Engineered From

- Hendrik Bessembinder 关于个股长期财富创造极度集中于少数赢家的研究。
- Baillie Gifford Long Term Global Growth 的公开 philosophy and process：长期、非基准、集中、寻找 outlier companies，用 10-question framework 评估长期机会、组织适应性、资本回报、5x upside 和市场误解。
- SEC / Investor.gov 对长期投资、风险承受、资产配置、分散和再平衡的投资者教育材料。
- Peter Lynch `tenbagger` 思维中“长期赢家往往来自被低估的小中型成长机会”的实践传统。
- Mira 现有 `thesis-horizon-routing`、`framework-routing`、`variant-perception` 和 `channel-check-scuttlebutt` 的内部方法沉淀。

## Search Paths Used

- 方法名搜索
  `tenbagger`, `multibagger stock`, `100 bagger`, `long term compounder`, `power law stock returns`
- 学术 / 实证搜索
  `Do stocks outperform Treasury bills`, `Bessembinder stock returns skewness`, `wealth creation listed companies`
- 投资者教育搜索
  `asset allocation diversification rebalancing long term investing`, `risk tolerance time horizon stocks`
- 实践派搜索
  `Peter Lynch tenbagger`, `100 baggers investing`, `long term growth stock checklist`
- 反面问题搜索
  `survivorship bias multibagger`, `why growth stocks fail`, `dilution risk high growth stocks`, `story stocks valuation risk`
- 机构流程搜索
  `Baillie Gifford Long Term Global Growth philosophy process`, `10 question stock research framework`, `outlier stocks five times upside market realise`

## Use When

- 用户明确寻找 `10x`、`100x`、`multibagger`、长期成长股、长期复利股或早期大机会。
- 单票研究的 `horizon_bucket = long_term_thesis`，且投资问题不是下个季度业绩，而是 3-10 年的经营和估值复利。
- 公司仍处于大市场渗透、商业模式升级、利润率爬坡、份额提升或平台化扩张阶段。
- 研究者需要把“长期好故事”压缩成可证伪、可刷新、可跟踪的投资路径。
- 研究问题需要判断市场是否低估了 5-10 年以后公司的规模、利润池、文化适应性或平台化能力。

## Avoid When

- 用户问题本质是财报事件、FY1/FY2 盈利修正、短线催化剂或交易节奏。
- 公司已经是成熟权重资产，未来主要由分红、回购、估值均值回归或宏观贴现率驱动，而不是经营复利驱动。
- 关键 thesis 只能依赖单一二手故事，缺少可跟踪的经营变量。
- 当前估值已经要求完美执行，但证据阶梯仍处于早期弱信号阶段。
- 公司需要持续融资才能活下去，而稀释风险可能吃掉普通股东的大部分 upside。
- 研究者无法给出市场误解的具体变量，只能说“市场短视”或“长期会好”。
- 右尾情景需要连续多个未验证假设同时成立，且没有中期证据阶梯可以刷新。

## Applies To

- `micro-small`
  重点验证生存性、融资稀释、单一产品/客户真实性、从事件资产转为经营资产的可能性。
- `mid-cap`
  重点验证公司能否从板块 beta 变成可持续 alpha，是否拥有长 runway、份额提升和利润池扩张。
- `large-mega`
  只在新平台、新利润池、重大技术周期或资本配置范式改变可能重写长期现金流曲线时启用。

## Core Question

这家公司是否有机会在可承受的失败率下，形成足够长、足够大、足够可验证的经营复利路径，让普通股东获得 10x/100x 级别的赔率？

## Required Inputs

- `target_return_path`
  目标倍数、目标年限、隐含 CAGR、需要的收入/利润/估值组合。
- `five_year_sales_test`
  未来五年收入是否至少有翻倍空间；如果没有，解释为什么仍值得进入长期右尾研究。
- `ten_year_outcome`
  十年以后公司可能变成什么，以及这个终局依赖哪些可证伪假设。
- `five_times_upside_question`
  公司如何可能值现在的 5 倍或更多；拆成收入、利润率、资本回报、估值倍数和资本结构路径。
- `market_misunderstanding`
  市场为什么没有充分理解；必须定位到具体变量、时间跨度、定价锚或行为偏差。
- `market_expansion`
  TAM 是否足够大且仍在扩张，当前渗透率是否低。
- `right_to_win`
  公司为什么能赢，而不是行业里所有公司一起赢。
- `culture_adaptability`
  创始人/管理层、组织学习能力、激励结构和长期资本配置是否支持穿越变化。
- `reinvestment_runway`
  高回报再投资还能持续多久，资本需求和边际回报如何变化。
- `operating_leverage`
  收入增长是否能转化为毛利率、营业利润率、FCF 或单位经济改善。
- `balance_sheet_survivability`
  现金、债务、融资窗口、周期压力和经营亏损能否撑到 thesis 兑现。
- `dilution_risk`
  股权融资、可转债、管理层激励和并购对普通股东回报的稀释。
- `valuation_tolerance`
  当前估值隐含了多少未来成功，允许哪些执行错误。
- `missed_winner_risk`
  如果 Mira 选择 watch/reject，哪些证据可能说明我们错过了真正的大赢家。
- `evidence_ladder`
  从弱信号到强确认的证据阶梯。
- `kill_criteria`
  哪些事实出现后必须降级、减仓或退出 thesis。

## Primary Signal

最重要的信号不是单季增长率，而是以下变量是否同向改善：

- 市场空间仍在扩张或被重新定义。
- 公司份额、留存、定价权或产品采用率持续改善。
- 单位经济、毛利率、现金转换或资本效率改善。
- 管理层持续把增量资本投向高回报机会，而不是靠融资维持叙事。
- 市场误解从叙事层逐渐被证据压缩：共识开始承认 TAM、份额、利润率、平台化或组织适应性高于原假设。
- 外部证据逐步从公司口径升级为客户、竞品、供应链、监管、财务和价格多方确认。

## Why It Works

长期个股回报不是均匀分布，而是由少数大赢家贡献大量财富创造。因此，研究流程既要能识别极少数可能复利很久的公司，也要承认大多数候选最终会失败或只成为普通赢家。

这个 lens 的增量在于把“长期看好”拆成六个可审计问题：

- 需要多大的经营结果才配得上 10x/100x？
- 这条经营路径是否足够长、足够大、足够可验证？
- 当前价格给了多少容错率？
- 如果我们错了，哪些事实会最早暴露？
- 如果它真是 outlier，市场今天到底错在什么变量上？
- 如果 Mira 拒绝它，哪些后续证据会证明我们犯了 false negative 错误？

## Failure Mode

- 把热门主题或宏大 TAM 当成公司特定 upside。
- 忽视稀释、融资窗口和资产负债表，导致公司活到了故事里，股东没有活到回报里。
- 用后视镜挑历史赢家，形成幸存者偏差。
- 把估值扩张当成经营复利，忽略未来倍数压缩风险。
- 因为追求 100x 而拒绝承认 thesis 已经失效。
- 组合过度集中在早期弱证据公司，导致单票失败摧毁长期复利。
- 把 Baillie Gifford 式耐心资本误用到交易账户或短期 actionability，忽视技术破位、融资窗口和风格逆风。
- 把“市场没理解”写成空泛口号，没有 consensus proxy、估值锚或可迫使重定价的证据。

## Evidence Cost

high

这个 lens 需要比普通长期 thesis 更多的样本比较、长期财务路径建模、稀释检查、竞争跟踪和刷新纪律。它不适合所有股票默认启用。

## Speed Vs Depth

偏 `depth`。

可以用 30 分钟做初筛，但不能用初筛结果直接形成长期结论。正式结论至少需要完成 return path、evidence ladder、kill criteria 和 refresh triggers。

## Comparison To Existing Methods

相对 `thesis-horizon-routing`：

- `thesis-horizon-routing` 判断时间跨度。
- `long-term-multibagger research` 判断长期跨度内是否存在足够大的倍数股路径。

相对 `framework-routing`：

- `framework-routing` 选择 micro-small / mid-cap / large-mega 主框架。
- 本方法不替代主框架，只在长期倍数股问题上增加目标收益数学、生命周期判断和组合纪律。

相对 `variant-perception`：

- `variant-perception` 关注市场共识错在哪里。
- 本方法吸收 Baillie Gifford 的 `why doesn't the market realise this?`，但要求它通过 Mira 的 consensus proxy、expectation map 和 evidence ladder；它关注即使市场错了，经营路径是否足以产生 10x/100x，且普通股东能否真正拿到。

相对 Baillie Gifford LTGG：

- 本方法借鉴其 `outlier companies`、`5x upside`、`market misunderstanding`、文化适应性和概率加权 upside 思维。
- 本方法不照搬其组合集中度、持有期或波动忍耐度；Mira 仍保留估值预期、source trail、refresh trigger、kill criteria 和 actionability downgrade。

相对 `channel-check-scuttlebutt`：

- `channel-check` 是高成本验证路径。
- 本方法会决定哪些关键变量值得做 channel check。

## Follow-Through Criteria

- 是否能在 memo 里稳定写出目标倍数、时间、隐含 CAGR 和经营结果要求。
- 是否能区分 `TAM story`、`company right to win` 和 `shareholder return path`。
- 是否能把长期 thesis 拆成季度/年度可刷新的 evidence ladder。
- 是否能稳定写出市场误解变量和重定价证据，而不是只写“市场短视”。
- 是否能记录 `missed_winner_risk`，避免 Mira 只擅长防错而系统性错过右尾赢家。
- 是否减少“看起来很大但普通股东拿不到回报”的错误。
- 是否帮助组合层面控制早期候选的失败率和仓位风险。

## Trial Design

### Case Backtest

- 至少选 2-3 个历史案例：
  - 一个真实 10x/100x 长期赢家。
  - 一个中途失败的热门成长故事。
  - 一个经营不错但股东回报一般的估值/稀释失败案例。
- 对每个案例回到早期时间点，重建当时可见的 `target_return_path`、`evidence_ladder` 和 `kill_criteria`。
- 判断本方法是否能在事前提高筛选质量，而不是事后解释赢家。

### Forward Watch

- 选 2 个当前候选标的：
  - 一个 `micro-small` 或早期 `mid-cap`。
  - 一个更成熟但仍可能有长期平台化空间的 `mid/large`。
- 每次重大财报、融资、客户/产品、竞争或估值变化后刷新。
- 记录 thesis 是升级、降级、维持还是退出。

## Falsification Conditions

- 如果它只能把历史赢家解释得更漂亮，却不能在失败样本中提前暴露风险，应降级。
- 如果它无法形成比普通长期 thesis 更明确的 kill criteria，应降级。
- 如果它经常鼓励过度集中、过度乐观或忽视估值，应降级。
- 如果试跑中发现它只是 `variant-perception` 或 `framework-routing` 的重复包装，应合并或退休。

## Adoption Decision

当前判断：`trial`

原因：

- 用户目标明确指向 10x/100x 长期股票，本方法能补齐 Mira 现有框架中“目标倍数路径”和“组合失败率”两块。
- 逻辑基础较强，但还没有经过 Mira 真实 case 复盘。
- 先试用，避免把一个听起来正确的方法直接固化为 adopted。

## Output Add-On

启用本 lens 时，在 `investment memo` 或 `case notes` 中增加：

- `target_return_path`
- `return_path_math`
- `five_year_sales_test`
- `ten_year_outcome`
- `five_times_upside_question`
- `market_misunderstanding`
- `market_expansion`
- `right_to_win`
- `culture_adaptability`
- `reinvestment_runway`
- `operating_leverage`
- `balance_sheet_survivability`
- `dilution_risk`
- `valuation_tolerance`
- `missed_winner_risk`
- `evidence_ladder`
- `position_sizing_implication`
- `kill_criteria`
- `must_refresh_if`

## Source Notes

- Hendrik Bessembinder, `Do stocks outperform Treasury bills?`, Journal of Financial Economics, 2018. ASU summary: https://asu.elsevierpure.com/en/publications/do-stocks-outperform-treasury-bills
- ASU W. P. Carey feature on Bessembinder's stock-market wealth creation findings: https://wpcarey.asu.edu/index.php/department-finance/faculty-research/do-stocks-outperform-treasury-bills
- SEC Investor.gov, `Asset Allocation, Diversification, and Rebalancing 101`: https://www.investor.gov/index.php/introduction-investing/getting-started/asset-allocation
- SEC, `Beginners' Guide to Asset Allocation, Diversification, and Rebalancing`: https://www.sec.gov/investor/pubs/assetallocation.htm
- Corporate Finance Institute plain-language tenbagger overview, used only as a terminology/practitioner reference: https://corporatefinanceinstitute.com/resources/career-map/sell-side/capital-markets/10-ten-bagger/
- Baillie Gifford, `Long Term Global Growth Philosophy and Process`, published page current as of 2026-03-31: https://www.bailliegifford.com/literature-library/institutional-only-literature/philosophy-and-process/long-term-global-growth-philosophy-and-process/
- Baillie Gifford, `Long Term Global Growth` strategy page, holdings and strategy description accessed 2026-06-01: https://www.bailliegifford.com/en/uk/institutional-investor/investment-strategies/long-term-global-growth/
- lufei X article summarizing Baillie Gifford growth stock system, posted 2026-05-28, used as practitioner prompt and not as standalone evidence: https://x.com/lufeieth/status/2060005022147256645

## Refresh Conditions

- stale_after: 2026-09-01 or after first two live cases are completed, whichever comes first.
- must_refresh_if:
  - a trial case produces materially different conclusions from ordinary `long_term_thesis` research;
  - a candidate company issues equity/debt financing that changes dilution or survivability;
  - a major customer, competitor, regulation, technology path or market-size assumption changes;
  - valuation expands enough that the original target return path no longer offers adequate upside;
  - evidence ladder remains stuck at weak-signal level for two consecutive refresh cycles.
