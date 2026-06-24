# Day27 — 企业 AI 分流系统（DeepSeek HTTP 版）

## 工作流结构
Manual Trigger
→ Edit Fields（客户问题）
→ HTTP Request（DeepSeek 分类）
→ Edit Fields（提取 department）
→ Switch（分流）
  → 物流部门
  → 售后部门
  → 财务部门

## 为什么用 HTTP Request 而不是 OpenAI 节点
n8n 内置 OpenAI 节点需要直连 api.openai.com，国内网络无法访问。
改用 HTTP Request 节点直接调用 DeepSeek API，国内可以直连，效果相同。

## HTTP Request 关键配置
- Method：POST
- URL：https://api.siliconflow.cn/v1/chat/completions
- Header：Authorization: Bearer {API Key}
- Body：JSON 格式，model 用 deepseek-chat

## 核心表达式速查
| 用途 | 表达式 |
|------|--------|
| 取 DeepSeek 回答 | {{ $json.choices[0].message.content }} |
| 清洗输出 | .trim().toLowerCase() |
| 取当前节点数据 | {{ $json.字段名 }} |
| 跨节点取数据 | {{ $('节点名').first().json.字段名 }} |

## 测试结果
| 输入 | AI 分类 | 分流结果 |
|------|---------|---------|
| 快递没到 | logistics | 物流部门 |
| 申请退款 | aftersales | 售后部门 |
| 需要发票 | finance | 财务部门 |