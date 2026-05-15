# Overlay: Strategic Catalyst

这个 overlay 用于研究小盘股、事件驱动股票和弱估值锚股票中，可能由巨头合作、投资、并购、客户认证、独家授权、平台接入或供应链导入触发的重估路径。

它的目标不是确认传闻，而是防止 alpha 研究过度过滤低置信度早期线索，同时确保输出不会把传闻写成事实。

## Use When

- 标的可能因单一战略关系重写收入确定性、融资能力、生存性或估值锚。
- 市场正在交易“谁会合作、谁会投资、谁会收购、谁会成为大客户”。
- 早期线索来自社交平台、论坛、交易员讨论、行业聊天、招聘、专利、供应链导入、会议纪要或异常量价。
- 用户明确要求不要漏掉社交传闻或非正式催化剂线索。

## Signal Status

每条催化剂线索必须标记为以下之一：

- `confirmed`: 公司公告、监管文件、交易所公告、合同、财报、官方新闻稿或高可信媒体已经确认。
- `reported`: 有署名媒体、行业媒体或可追溯消息源报道，但公司尚未确认。
- `social_signal`: 社交平台、论坛、社区、播客、长文、交易员讨论或行业聊天形成的线索。
- `unverified_rumor`: 来源不透明、无法复核、只有单点传播或高度依赖匿名说法。

## Required Fields

启用本 overlay 后，memo 或 case notes 必须记录：

- `catalyst_status`
- `counterparty_quality`
- `economic_materiality`
- `expected_timeline`
- `market_pricing_status`
- `verification_path`
- `what_would_confirm`
- `what_would_disconfirm`
- `next_refresh_trigger`

## Catalyst Quality

判断催化剂质量时，优先看：

- 交易对手是否是巨头、核心客户、产业链关键节点、潜在收购方或资金提供方。
- 是否有正式披露、合同金额、排他条款、付款、收入确认、认证进展或监管文件。
- 是否改变融资能力、现金 runway、客户可信度、估值锚或控制权预期。
- 时间窗口是否足够近，通常小盘股重点看未来 1 到 2 个季度。
- 市场是否已经充分 price in，还是仍处于扩散早期。

## Output Rules

- `confirmed` 和高质量 `reported` 可以进入催化剂分析，但仍要注明确认状态。
- `social_signal` 和 `unverified_rumor` 只能进入 `Alpha Signals / Rumor Watch`，不能支撑 `Core Conclusion`。
- 多个账号重复传播同一说法不构成独立验证。
- 如果传闻与公司披露、监管文件或已知事实冲突，必须显式降级或剔除。

## Refresh Conditions

默认 `stale_after`：

- `confirmed`: 下一个公司公告、财报或事件节点后刷新。
- `reported`: 14 到 30 天后刷新。
- `social_signal`: 7 到 14 天后刷新。
- `unverified_rumor`: 3 到 7 天后刷新，或一旦出现反向证据立即刷新。

必须刷新如果：

- 公司、交易所、监管文件、交易对手或高可信媒体确认或否认。
- 股价、成交量、期权隐波或借券成本出现异常变化。
- 出现融资、增发、债务重组、管理层变动或重大客户披露。
- 传闻的时间窗口过去但未出现验证证据。
