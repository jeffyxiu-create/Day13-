# Day33 — AI工单多部门分配系统

## 工作流结构
Webhook（外部入口）
→ HTTP Request（DeepSeek分析）
→ Edit Fields（解析JSON，6个字段）
→ IF串联（按score路由）
  → score=1 → Edit Fields（普通队列）
  → score=2 → Edit Fields（售后队列）
  → score=3 → Edit Fields（高级客服队列）
  → score=4 → Edit Fields（主管处理队列）
→ Switch（按department分流）
  → 客服部      → Edit Fields（customer_service_flow）
  → 售后部      → Edit Fields（refund_flow）
  → 财务部      → Edit Fields（invoice_flow）
  → 技术支持部  → Edit Fields（tech_support_flow）
→ Respond to Webhook

## Webhook 配置
- Method：POST
- Path：ticket-department

## 标准输出格式
{
  "category": "退款",
  "priority": "中",
  "score": "2",
  "queue": "售后队列",
  "department": "售后部",
  "suggestion": "引导用户提交退款申请",
  "workflow": "refund_flow"
}

## 部门分配规则

| 问题类型 | 部门 | workflow |
|----------|------|----------|
| 物流/发货 | 客服部 | customer_service_flow |
| 退款/换货 | 售后部 | refund_flow |
| 发票/账单 | 财务部 | invoice_flow |
| 系统/登录 | 技术支持部 | tech_support_flow |

## 队列路由规则

| score | priority | queue |
|-------|----------|-------|
| 1 | 低 | 普通队列 |
| 2 | 中 | 售后队列 |
| 3 | 高 | 高级客服队列 |
| 4 | 紧急 | 主管处理队列 |

## IF vs Switch 对比

| 节点 | 匹配方式 | 出口数量 | 本项目用途 |
|------|----------|----------|------------|
| IF | 数字判断 | 只有2个 | 按score路由队列 |
| Switch | 文字精确匹配 | 多个 | 按department路由部门 |

## 核心表达式总结

| 用途 | 写法 |
|------|------|
| 取 Webhook 数据 | `{{ $json.body.message }}` |
| 解析AI返回JSON | `={{ JSON.parse($json.choices[0].message.content.replace(/\`\`\`json/g,'').replace(/\`\`\`/g,'').trim()).字段名 }}` |
| IF条件取score | `={{ $json.score }}` |
| Switch取department | `={{ $json.department }}` |

## Day31~33 升级对比

| 天数 | 新增节点 | 新增能力 |
|------|----------|----------|
| Day31 | Webhook + HTTP Request + Edit Fields + Respond | 基础工单JSON |
| Day32 | IF串联 | 按score数字路由队列 |
| Day33 | Switch | 按department文字路由部门 |