# Enterprise Ticket Platform V2.0
## Assignment Engine — 自动派单引擎

### 本次更新 V1.5 → V2.0
新增企业模块：Assignment Engine
新增节点：
✓ Assignment Engine（Department/Owner/Queue/Priority Builder）
✓ Message Builder（派单通知模板）
✓ Gmail Send（通知负责人）
✓ Log Engine（记录assignment_completed）
✓ Ticket Engine（唯一更新入口：status=Assigned）

### Assignment规则（V1，写死版）

| priority | department | owner | queue |
|----------|-----------|-------|-------|
| 紧急 | Customer Service | Alice | VIP Queue |
| 高 | Support | Tom | Priority Queue |
| 低/中 | General | David | General Queue |

> Day40升级为规则引擎，支持动态配置

### Ticket生命周期（当前）

| 状态 | 触发时机 |
|------|---------|
| Pending | 工单创建时 |
| Pending Approval | 高优先级进入审批 |
| Approved | 审批通过 |
| Rejected | 审批拒绝 |
| Assigned | 自动派单完成 |

### Ticket Engine原则
所有对主表的更新只经过Ticket Engine这一个节点，Assignment Engine不直接写主表。

### Release Notes
Enterprise Ticket Platform V2.0
新增：
✓ Assignment Engine
✓ 自动派单（部门/负责人/队列）
✓ 派单通知邮件
✓ Assignment Log
✓ Ticket Engine统一更新
预留：
→ Day40：规则引擎（动态配置派单规则）
→ Day40：Status Flow Engine（完整生命周期）