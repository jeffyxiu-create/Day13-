# Day29 — 第一个 Webhook 接入系统

## 工作流结构
Webhook（接收外部请求）
→ HTTP Request（SiliconFlow AI 回复）

## Webhook 配置
- Method：POST
- Path：customer-service
- Test URL：https://jeffyxiu.app.n8n.cloud/webhook-test/customer-service
- Production URL：https://jeffyxiu.app.n8n.cloud/webhook/customer-service

## 接收的 JSON 格式
{
  "user": "用户名",
  "message": "用户问题"
}

## Day28 vs Day29 核心区别

| | Day28 | Day29 |
|--|-------|-------|
| 触发方式 | 手动点按钮 | 外部发 HTTP 请求 |
| 启动节点 | Manual Trigger | Webhook |
| 数据来源 | Edit Fields 里写死 | 外部 JSON 动态传入 |
| 适用场景 | 测试调试 | 真实生产环境 |

## 核心新知识

### Webhook 两种 URL
- Test URL：开发调试用，需要点 Listen for test event 激活
- Production URL：正式上线用，Workflow 发布后自动生效

### 取 Webhook 数据的写法
外部发来的 JSON 字段直接用 $json 取：
={{ $json.message }}
={{ $json.user }}
不需要跨节点写法，因为 Webhook 本身就是数据入口

## 测试结果
| 输入问题 | AI 回复质量 |
|---------|------------|
| 订单发货问题 | 专业物流口吻 ✅ |
| 申请退款 | 专业售后口吻 ✅ |
| 需要发票 | 专业财务口吻 ✅ |