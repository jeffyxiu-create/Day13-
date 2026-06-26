# AI Ticket Automation System

## 项目简介

企业工单自动化系统。

通过 n8n + SiliconFlow + DeepSeek 实现：

用户提交问题
↓
AI分析
↓
自动生成工单
↓
输出处理建议

---

## 技术栈

- n8n
- HTTP Request
- SiliconFlow API
- DeepSeek
- Webhook

---

## 项目结构

```text
Day31_AI_Ticket_Automation_System/

├── workflow.json
├── prompt_library.txt
├── test_data.json
├── README.md
└── screenshots/
```

---

## 工作流架构

```text
Webhook
↓
DeepSeek分析
↓
Edit Fields
↓
Respond To Webhook
```

---

## AI分析内容

自动生成：

- 分类
- 优先级
- 处理部门
- 处理建议

---

## 测试案例

### 案例1

输入：

我的订单已经10天没有发货了

输出：

```json
{
  "category": "物流",
  "priority": "高",
  "department": "客服部",
  "suggestion": "立即核查订单状态"
}
```

### 案例2

输入：

我要申请退款

输出：

```json
{
  "category": "售后",
  "priority": "中",
  "department": "售后部",
  "suggestion": "核实订单信息后处理退款"
}
```

---

## 项目亮点

- AI自动分析工单
- 自动判断优先级
- 自动推荐处理部门
- 标准JSON输出
- 企业自动化场景

---

