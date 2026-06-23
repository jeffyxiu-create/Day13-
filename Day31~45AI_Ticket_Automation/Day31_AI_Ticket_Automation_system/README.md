# Day30 — 企业自动化中枢（Project1 毕业项目）

## 工作流结构
Webhook（外部入口）
→ HTTP Request（AI 分类）
→ Edit Fields（提取 category）
→ Switch（分流）
  → 物流 → HTTP Request（AI回复）→ Edit Fields（格式化）
  → 售后 → HTTP Request（AI回复）→ Edit Fields（格式化）
  → 财务 → HTTP Request（AI回复）→ Edit Fields（格式化）

## Webhook 配置
- Method：POST
- Path：enterprise-service
- Test URL：https://jeffyxiu.app.n8n.cloud/webhook-test/enterprise-service

## 标准输出格式
{
  "reply": "AI 生成的专业回复",
  "category": "物流 / 售后 / 财务",
  "status": "success"
}

## Project1 完整技术栈总结

| 技术 | 用途 | 从哪天开始用 |
|------|------|-------------|
| Manual Trigger | 手动启动工作流 | Day25 |
| Edit Fields | 设置和提取字段 | Day25 |
| HTTP Request | 调用外部 API | Day26 |
| SiliconFlow API | AI 模型服务 | Day26 |
| Switch | 条件分流 | Day27 |
| Webhook | 接收外部请求 | Day29 |
| system prompt | 定义 AI 角色 | Day28 |

## 核心表达式总结

| 用途 | 写法 |
|------|------|
| 取 Webhook 数据 | {{ $json.bady.message }} |
| 取 AI 回复内容 | {{ $json.choices[0].message.content.trim() }} |
| 跨节点取数据 | {{ $('Edit Fields').first().json.original_message }} |
| 取 Webhook 原始数据 | {{ $('Webhook').first().json.body.message }} |