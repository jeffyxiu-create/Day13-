# Day32 — AI工单优先级路由系统

## 工作流结构
Webhook（外部入口）
→ HTTP Request（DeepSeek分析+评分）
→ Edit Fields（解析JSON）
→ IF_1（score=1）→ Edit Fields（普通队列）
→ IF_2（score=2）→ Edit Fields（售后队列）
→ IF_3（score=3）→ Edit Fields（高级客服队列）
→ false → Edit Fields（主管处理队列）
→ Respond to Webhook

## Webhook 配置
- Method：POST
- Path：ticket-priority

## 标准输出格式
{
  "category": "物流",
  "priority": "高",
  "score": "3",
  "queue": "高级客服队列",
  "department": "客服部",
  "suggestion": "立即核查订单状态"
}

## 核心表达式总结

| 用途 | 写法 |
|------|------|
| 取 Webhook 数据 | `{{ $json.body.message }}` |
| 解析AI返回JSON | `={{ JSON.parse($json.choices[0].message.content.replace(/\`\`\`json/g,'').replace(/\`\`\`/g,'').trim()).字段名 }}` |
| IF条件取score | `={{ $json.score }}` |

## 队列路由规则

| score | priority | 队列 |
|-------|----------|------|
| 1 | 低 | 普通队列 |
| 2 | 中 | 售后队列 |
| 3 | 高 | 高级客服队列 |
| 4 | 紧急 | 主管处理队列 |