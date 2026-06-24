### Day28
- 完成内容：企业 AI 自动化工作流升级，Switch 三分支各接独立 HTTP Request 节点，AI 动态生成专业回复
- 核心收获：每个分支用独立 system prompt 定义角色，回复质量比固定文字高很多
- 遇到的坑：（做完填）

---

## Day28 升级对比

| | Day27 | Day28 |
|--|-------|-------|
| 分支处理方式 | Edit Fields 固定回复 | HTTP Request AI 动态回复 |
| 回复内容 | 写死的文字 | AI 根据问题实时生成 |
| system prompt | 无 | 每个部门独立角色定义 |
| 灵活性 | 低 | 高 |

---

## Day28 工作流结构

Manual Trigger
→ Edit Fields（customer_message）
→ HTTP Request（DeepSeek 分类）
→ Edit Fields1（提取 department）
→ Switch
  → Output 0 → HTTP Request（物流 AI 回复）
  → Output 1 → HTTP Request（售后 AI 回复）
  → Output 2 → HTTP Request（财务 AI 回复）

---

## Day28 核心新知识

### system prompt 是什么
在 messages 里加一个 role: system 的消息
作用是给 AI 定义角色和行为规范
user 的问题发过去之前，AI 已经知道自己是谁了

```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一名专业的物流客服..."
    },
    {
      "role": "user",
      "content": "用户的问题"
    }
  ]
}
```

### 跨节点取数据
分支里的 HTTP Request 需要取最开始 Edit Fields 的数据
不能用 $json（因为上一个节点是 Switch，没有 customer_message）
要用跨节点写法：

={{ $('Edit Fields').first().json.customer_message }}

---

## 测试结果

| 输入 | 分类结果 | AI 回复风格 |
|------|---------|------------|
| 快递三天没到 | 物流 | 物流客服专业口吻 |
| 申请退款 | 售后 | 售后客服专业口吻 |
| 需要发票 | 财务 | 财务客服专业口吻 |