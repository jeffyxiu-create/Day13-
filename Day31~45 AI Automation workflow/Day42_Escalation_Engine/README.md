# Enterprise Ticket Platform V2.3
## Escalation Engine — 自动升级引擎

### 本次更新 V2.2 → V2.3
新增独立工作流：Workflow 3 - Escalation Engine（Schedule Trigger驱动）
新增节点：
✓ Schedule Trigger（定时巡检，比Reminder Engine间隔更长）
✓ Filter（status=Assigned 且 due_time不为空）
✓ Remaining Time Calculator（复用Day41的Luxon计算）
✓ Escalation Rule（remaining<0 且 未升级过）
✓ Escalation Level Builder（按sla_level算升级等级）
✓ Assign Manager（按部门分配主管）
✓ Send Manager Notification（Gmail升级通知）
✓ Escalation_Log（独立Sheet记录每次升级）

### 三个工作流的分工（截至Day42）

| Workflow | 触发方式 | 关注点 | 写入列 |
|----------|---------|--------|--------|
| Workflow 1 Ticket Processing | Webhook | 工单创建/审批/派单 | status/department/owner/queue/sla_* |
| Workflow 2 Reminder Engine | Schedule（1分钟） | 快超时，提醒原负责人 | reminder_* |
| Workflow 3 Escalation Engine | Schedule（10分钟） | 真超时，通知主管 | escalation_* |

### Escalation规则（V1）

| 条件 | 结果 |
|------|------|
| remaining_minutes < 0 且 escalation_status未升级过 | 通知主管，标记已升级 |
| remaining_minutes >= 0 | 不升级 |
| escalation_status已经是escalated | 不重复通知 |

### Release Notes
Enterprise Ticket Platform V2.3
新增：
✓ Escalation Engine（独立Schedule工作流）
✓ 自动升级通知主管
✓ 升级等级标签
✓ Escalation_Log独立追踪
预留：
→ Day43：Dashboard（运营看板，呈现方式待定）
→ Day44：Statistics（日/周报统计）