# Enterprise Ticket Platform V2.1
## SLA Timer — 超时计时引擎

### 本次更新 V2.0 → V2.1
新增企业模块：SLA Timer
新增节点：
✓ SLA Builder（sla_hours/sla_level）
✓ Due Time Calculator（用Luxon的.plus()算截止时间）
✓ Remaining Time Calculator（用.diff()算剩余分钟）
✓ SLA Status IF（今日搭基础设施，Day41启用巡检）
✓ Notification Engine升级（通知加入SLA信息）
✓ Log Engine升级（记录sla_level/due_time）
✓ Ticket Engine升级（唯一更新入口新增sla_level/due_time/sla_status）

### SLA规则（V1，写死版）

| priority | SLA时长 | SLA Level |
|----------|---------|-----------|
| 紧急 | 1小时 | L1 |
| 高 | 4小时 | L2 |
| 低/中 | 24小时 | L3 |

> Day41会给这套规则加上定时巡检，真正抓出超时工单

### Ticket生命周期（当前）

| 状态 | 触发时机 |
|------|---------|
| Pending | 工单创建时 |
| Pending Approval | 高优先级进入审批 |
| Approved | 审批通过 |
| Rejected | 审批拒绝 |
| Assigned | 自动派单完成，同时算出SLA倒计时 |

### Ticket Engine原则
所有对主表的更新只经过Ticket Engine这一个节点，SLA Timer不直接写主表。

### Release Notes
Enterprise Ticket Platform V2.1
新增：
✓ SLA Timer
✓ 自动计算截止时间（due_time）
✓ SLA等级标签（sla_level）
✓ 剩余时间计算（remaining_minutes）
✓ 通知邮件包含SLA信息
预留：
→ Day41：Reminder Engine（定时巡检 + 自动催办）
→ Day42：Escalation Engine（超时自动升级）