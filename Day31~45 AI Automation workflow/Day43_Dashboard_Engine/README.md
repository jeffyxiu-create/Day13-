# Enterprise Ticket Platform V2.4
## Dashboard Workflow — 企业运营看板

### 本次更新 V2.3 → V2.4
新增独立工作流：Workflow 4 - Dashboard Workflow（Schedule Trigger驱动，只读）
新增节点：
✓ Schedule Trigger（定时统计，间隔比Escalation Engine更长）
✓ Statistics Builder（Code节点⭐首次引入，Run Once for All Items汇总N条工单为1条统计结果）
✓ KPI Calculator（计算sla_rate达成率）
✓ Dashboard Builder（补充report_time，组装最终看板数据）
✓ Dashboard_Table（独立Sheet，记录每次统计的时间序列快照）

### 四个工作流的分工（截至Day43）

| Workflow | 触发方式 | 关注点 | 写入列 |
|----------|---------|--------|--------|
| Workflow 1 Ticket Processing | Webhook | 工单创建/审批/派单 | status/department/owner/queue/sla_* |
| Workflow 2 Reminder Engine | Schedule（1分钟） | 快超时，提醒原负责人 | reminder_* |
| Workflow 3 Escalation Engine | Schedule（10分钟） | 真超时，通知主管 | escalation_* |
| Workflow 4 Dashboard Workflow | Schedule（30分钟） | 全局统计，只读呈现 | 不写Ticket_Main，写入Dashboard_Table |

### Dashboard统计口径（V1）

| 指标 | 计算方式 |
|------|---------|
| total_ticket | Ticket_Main总行数 |
| closed_ticket | status=Closed的数量 |
| open_ticket | total_ticket - closed_ticket |
| overdue_ticket | status≠Closed 且 due_time已早于当前时间 |
| reminder_count | 全部工单reminder_count字段求和 |
| escalation_count | escalation_status=escalated的数量 |
| sla_rate | (total_ticket - overdue_ticket) / total_ticket × 100 |

### Release Notes
Enterprise Ticket Platform V2.4
新增：
✓ Dashboard Workflow（独立Schedule工作流，只读）
✓ Code节点首次引入，解决跨工单汇总统计问题
✓ Dashboard_Table时间序列快照
预留：
→ Day44：Statistics（日/周报统计，在Dashboard基础上做时间维度切片）
→ Day45：Project 2收尾