# AI PDF 总结助手 V2.0
## 环境要求
- Python >= 3.6
- 依赖库：pypdf、openai

## 技术栈
- Python
- Tkinter 桌面GUI
- pypdf PDF解析
- OpenAI 大模型API

## 功能列表
1. 本地选择PDF文件
2. 自动提取PDF文本
3. 大模型AI智能总结
4. 超长内容自动截断并提示
5. 图片PDF友好提示
6. 异步调用AI，界面不卡顿
7. 自定义路径保存摘要为TXT
8. 操作状态实时提示，防重复点击

## 使用说明
1. 打开程序，点击【选择PDF并总结】
2. 等待AI生成摘要
3. 查看原文与AI摘要
4. 点击【保存摘要】自定义位置保存文件

## 项目结构
- ui.py：主界面与交互逻辑
- pdf_reader.py：PDF文本解析
- api_engine.py：AI接口调用
- file_save.py：文件保存功能
- 
