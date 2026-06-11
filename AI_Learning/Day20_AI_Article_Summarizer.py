#=========================模块1：导入库===========================
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
from docx.shared import T
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

#=========================模块2：API 配置==========================
root_path = Path(__file__).resolve().parent.parent
env_path = root_path/".env"
load_dotenv(env_path)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
MODEL="deepseek-ai/DeepSeek-V3"
if not all([API_KEY, BASE_URL, MODEL]):
    raise Exception("环境变量读取失败，请检查.evn 文件配置")
client = OpenAI(api_key = API_KEY, base_url = BASE_URL)

#全局变量与常量
global_result = ""
BTN_NORMAL_TEXT = "生成摘要+关键词"
BTN_RUNNING_TEXT = "正在生成中......."
MAX_ARTICLE_LENGTH = 4000

#==============模块3:搭建窗口界面=====================
root = tk.Tk()
root.title("AI 长文章摘要工具 ")
root.geometry("900x700")

#--------标题文字标签----------
title_label = tk.Label(root, text= "AI 文章摘要 & 关键词提取工具",font = ("微软雅黑",16,"bold"))
title_label.pack(pady=10)

#---------输入区----------
input_label = tk.Label(root, text="请粘贴📄待处理长文章:", font=("微软雅黑", 11))
input_label.pack(anchor="w", padx=20)
input_text = scrolledtext.ScrolledText(root, width=100, height =15, font=("微软雅黑",10))
input_text.pack(padx=20, pady=5)

#---------按钮区---------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_summary = tk.Button(btn_frame, text=BTN_NORMAL_TEXT, width=15, bg="#409EFF", fg = "white")
btn_save_txt = tk.Button(btn_frame, text="导出为TXT",width=12)
btn_save_md = tk.Button(btn_frame, text="导出为Markdown",width=14)
btn_clear = tk.Button(btn_frame, text="清空内容",width=12, bg="#F56C6C", fg= "white")

btn_summary.grid(row=0, column=0, padx=8)
btn_save_txt.grid(row=0, column=1, padx=8)
btn_save_md.grid(row=0, column=2, padx=8)
btn_clear.grid(row=0, column=3, padx=8)

#-------------结果展示区----------------

result_label = tk.Label(root, text="AI 处理结果（摘要+关键词）：", font=("微软雅黑", 11))
result_label.pack(anchor="w", padx=20, pady=(10, 0))
result_text = scrolledtext.ScrolledText(root, width=100, height=18, font=("微软雅黑", 10))
result_text.pack(padx=20, pady=10)

#======================模块4:功能函数=========================
def clear_all():
    """清空所有文本内容与结果"""
    input_text.delete(1.0, tk.END)
    result_text.delete(1.0, tk.END)
    global global_result
    global_result = ""

def check_input():
    """输入内容校验:非空,长度限制"""
    content = input_text.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("提示:","请先粘贴需要处理的文章内容!")
        return False
    if len(content) > MAX_ARTICLE_LENGTH:
        messagebox.showwarning("提示",f"文章过长(最大{MAX_ARTICLE_LENGTH}字符),请精简后重试!")
        return False
    return True

def set_buttons_state(state):
    """统一控制按钮启用/禁用状态"""
    btn_summary.config(state=state)
    btn_save_txt.config(state=state)
    btn_save_md.config(state=state)
    btn_clear.config(state=state)

def on_api_success(ai_result):
    """API请求成功,更新界面"""
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ai_result)
    btn_summary.config(text=BTN_NORMAL_TEXT, bg="#409EEF")
    set_buttons_state("normal")

def on_api_error(error_msg):
    """API请求失败,弹出错误提示"""
    messagebox.showerror("API调用失败",f"错误信息:{error_msg}")
    btn_summary.config(text=BTN_NORMAL_TEXT,  bg="#409EEF")
    set_buttons_state("normal")

#=------------------------核心函数(子线程执行网络请求)----------------------
def call_api(article_content):
    """调用OpenAI接口生成摘要和关键词"""
    global global_result
    prompt = f"""
    请对下面的长文章完成两项工作:
    1. 生成一段通顺,精简的中文摘要,概括全文核心内容;
    2. 提取5-8个核心关键词.

    严格按照以下格式输出,不要额外解释:
    [文章摘要]
    这里放置摘要内容

    [核心关键词]
    关键词1、关键词2、 关键词3、 关键词4、 关键词5

    文章内容：
    {article_content}
    """
    try:
        response = client.chat.completions.create(
            model=  MODEL,
            messages = [{"role":"user","content":prompt}],
           temperature=0.3 
           )
        
        ai_result = response.choices[0].message.content.strip()
        global_result = ai_result
        root.after(0,lambda:on_api_success(ai_result)) # root.after（延迟毫秒，函数），在主线程的下一个时机执行这个函数，0是尽快处理（不等待）
    except Exception as e:
        root.after(0, lambda: on_api_error(str(e)))
 
#---------点击”生成摘要“-------------
def generate_summary():
    """生成摘要按钮主逻辑"""
    if not check_input():
        return
    article_content= input_text.get(1.0, tk.END).strip()
    set_buttons_state("disabled")
    btn_summary.config(text="正在生成中。。。。", bg="#909399")
    #---------开启子线程执行--------------------
    t = threading.Thread(target=call_api, args=(article_content,))
    t.daemon=True
    t.start()

    #============文件导出函数=============
def save_to_txt():
    global global_result
    if not global_result:
        messagebox.showwarning("提示","暂无可导出的内容,请先生成摘要!")
        return
        
    file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件","*.txt"),("所有文件","*.*")],
            title= "保存为TXT文件"
        )
    if file_path:
        with open(file_path,"w", encoding="utf-8")as f :
            f.write(global_result)
            messagebox.showinfo("成功","TXT 文件导出完成!")

def save_to_md():
    """导出为Markdown文件"""
    global global_result
    if not global_result:
        messagebox.showwarning("提示","暂无可导出的内容,请先生成摘要!")
        return
    md_content=f"""#文章摘要结果{global_result}"""
    file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown文本文件","*.md"),("所有文件","*.*")],
            title= "保存为Markdwon文件"
        )
    if file_path:
        with open(file_path,"w", encoding="utf-8")as f :
            f.write(global_result)
            messagebox.showinfo("成功","Markdown 文件导出完成!")

#===================模块5:绑定按钮================================
btn_summary.config(command=generate_summary)
btn_save_txt.config(command=save_to_txt)
btn_save_md.config(command=save_to_md)
btn_clear.config(command=clear_all)

#-------------启动窗口-------------
if __name__ == "__main__":
    root.mainloop()