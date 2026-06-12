#=========================模块1：导入库===========================
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
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

#================模块3:函数=====================\
def get_summary_and_keywords(article_text):
    """纯业务逻辑:调用AI生成摘要+关键词
    职责单一,不操作UI,异常向上抛出
    """
    prompt= f"""
    请用中文完成以下两项工作:
    1. 撰写简洁通顺的内容摘要
    2. 提取3-8个核心关键词,用顿号分隔
    原文:
    {article_text}
    """
    res = client.chat.completions.create(
        model = MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    return res.choices[0].message.content
#---------------------子线程调用------------------------    
def run_analysis(input_content):
    """
    子线程执行AI调用
    通过 root.after 回到主线程更新UI
    """
    try:
        ai_result = get_summary_and_keywords(input_content)
        root.after(0, update_output, ai_result)
    except Exception as e:
        root.after(0, show_error, str(e))

#================UI交互回调函数=======================
def analyze_article():
    """开始分析按钮点击事件:校验内容+启动子线程"""
    input_content = input_text.get(1.0, tk.END)
    if not input_content.strip():
        messagebox.showwarning("提示","请先粘贴文章内容!")
        return
    #禁用按钮,防止重复点击
    btn_analyze.config(text="分析中....", state= tk.DISABLED)
    #启动后台线程
    thread = threading.Thread(target= run_analysis, args=(input_content,))
    thread.daemon = True
    thread.start()

def update_output(ai_result):
    """更新结果到文本框,并恢复按钮状态"""
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, ai_result)
    btn_analyze.config(text="开始分析",state=tk.NORMAL)

def show_error(msg):
    """异常弹窗提示,并恢复按钮状态"""
    btn_analyze.config (text="开始分析", state=tk.NORMAL)
    messagebox.showerror("调用失败",f"AI接口异常{msg}")

def save_result():
    """将结果保存为TXT,增加异常捕获"""
    content = output_text.get(1.0, tk.END)
    if not content.strip():
        messagebox.showwarning("提示","暂无结果可保存!")
        return
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文本文件","*.txt"),("所有文件","*.*")]
    )
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("成功","文件已保存!")
        except Exception as e:
            messagebox.showerror("保存失败",f"写入文件时出错:{str(e)}")

def clear_all():
    """一键清空输入,输出文本框"""
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)

#=====================GUI界面布局==============
root = tk.Tk()
root.title("文章摘要&关键词提取工具")
root.geometry("900x600")
root.minsize(700,450)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_analyze = tk.Button(btn_frame, text="开始分析", command=analyze_article, width=12, height=2)
btn_analyze.grid(row=0, column=0, padx=15)

btn_save = tk.Button(btn_frame, text="保存结果", command=save_result, width=12, height=2)
btn_save.grid(row=0, column=1, padx=15)

btn_clear = tk.Button(btn_frame, text="清空全部", command=clear_all, width=12, height=2)
btn_clear.grid(row=0, column=2, padx=15)

    # 主体分区：输入区 + 结果区
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=5)

    # 左侧：原文输入框
tk.Label(main_frame, text="粘贴原文：", font=("微软雅黑", 10)).grid(row=0, column=0, sticky="w")
input_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("微软雅黑", 10))
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # 右侧：摘要&关键词输出框
tk.Label(main_frame, text="摘要 & 关键词：", font=("微软雅黑", 10)).grid(row=0, column=1, sticky="w")
output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("微软雅黑", 10))
output_text.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

    # 网格自适应配置（窗口拉伸同步缩放）
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)

    # 启动主循环
if __name__ == "__main__":
    root.mainloop()









