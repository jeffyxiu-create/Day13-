# Enterprise Ticket Platform V2.5
## Statistics Workflow + Architecture Refactor

### 本次更新 V2.4 → V2.5

新增业务能力：
✓ Statistics Report（日报/周报/月报，Statistics_Report独立Sheet）

新增技术能力（本日核心）：
✓ Execute Workflow节点，首次引入"工作流复用"模式
✓ Shared_RemainingTimeCalculator（共享工作流，Reminder/Escalation共用，采用"整体传递"设计，避免下游大量改字段引用）
✓ Shared_StatisticsBuilder（共享工作流，按period参数复用，day/week/month三选一）
✓ Department_Mapping查表，替代硬编码三元表达式（Configuration over Code）
✓ Git提交，Project 2第一次正式版本控制实践

### 本次重构修复的历史Bug

| Bug | 位置 | 修复方式 |
|-----|------|---------|
| `deparment`拼写错字导致Support部门匹配不到 | Day42 Assign Manager | 改成Department_Mapping查表，department直接从配置数据取，不再靠拼字符串匹配 |
| Customer Service和Support共用同一邮箱 | Day42 Assign Manager | Department_Mapping表里为每个部门单独配置邮箱 |

### 五个工作流的分工（截至Day44）

| Workflow | 触发方式 | 关注点 | 写入位置 |
|----------|---------|--------|---------|
| Workflow 1 Ticket Processing | Webhook | 工单创建/审批/派单 | Ticket_Main: status/department/owner/queue/sla_* |
| Workflow 2 Reminder Engine | Schedule | 快超时，提醒原负责人 | Ticket_Main: reminder_* |
| Workflow 3 Escalation Engine | Schedule | 真超时，通知主管 | Ticket_Main: escalation_* |
| Workflow 4 Dashboard | Schedule | 实时快照，只读 | Dashboard_Table |
| Workflow 5 Statistics | Schedule（日/周/月三触发） | 周期性报表，只读 | Statistics_Report |

### 共享组件层（新增）

| 共享工作流 | 被谁调用 | 输入参数 | 输出 |
|-----------|---------|---------|------|
| Shared_RemainingTimeCalculator | Reminder Engine、Escalation Engine | ticket（完整工单对象） | 原始工单字段 + remaining_minutes |
| Shared_StatisticsBuilder | Day44_Statistics_Workflow（三个触发分支） | period(day/week/month) | 该周期内的统计汇总 |

### Release Notes
Enterprise Ticket Platform V2.5
新增：
✓ Statistics Report日/周/月报
✓ Execute Workflow子工作流复用机制
✓ Department_Mapping配置化查表
✓ 修复两处Day42历史遗留bug
预留：
→ Day45：Platform Release V3.0（正式发布/项目收尾）