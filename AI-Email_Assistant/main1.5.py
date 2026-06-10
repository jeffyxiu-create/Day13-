#==============================模块1:导入工具========================
import os
import tkinter as tk
from tkinter import ttk,messagebox
import threading
from turtle import up, update
import pyperclip

from prompts import PROMPTS
from ai_helper import get_ai_email
from export_docx import export_to_word

#================模块2：创建主窗口======================
root = tk.Tk()
root.title("AI 邮件助手 V1.5 企业版")
root.geometry("700x500")

#=======================模块3:绘制界面控件===============
tk.Label(root, text="选择类型:", font=("微软雅黑",11)).place(x=20, y=20)
mail_type = ttk.Combobox(root, width=30, font=("微软雅黑",10))
mail_type["values"] = tuple(PROMPTS.keys())
mail_type.current(0)
mail_type.place(x=130, y=22)
#----------输入文本框-------------
tk.Label(root, text="输入内容:", font=("微软雅黑",11)).place(x=20, y=70)
input_text = tk.Text(root, width=80, height=8, font=("微软雅黑",10))
input_text.place(x=20 , y=95)
#----------输出文本框-------------
tk.Label(root, text="AI生成结果:", font=("微软雅黑",11)).place(x=20, y=230)
output_text = tk.Text(root, width=80, height=12, font=("微软雅黑",10))
output_text.place(x=20 , y=255)

#==================模块4:功能函数=========================
def generate_email():
    user_content = input_text.get(1.0, tk.END).strip()
    if not user_content:
        messagebox.showwarning("提示","请输入内容")
        return
    btn_generate.config(text="生成中....",state = tk.DISABLED)
    output_text.delete(1.0, tk.END)

    def task():
        prompt = PROMPTS[mail_type.get()].format(content=user_content)
        result = get_ai_email(prompt)

        def update_ui():
            if result.startswith("ERROR:"):
                messagebox.showerror("失败","AIP/网络错误")
            else:
                output_text.insert(tk.END, result)
            btn_generate.config(text="生成邮件",state = tk.NORMAL)
        root.after(0, update_ui)
    threading.Thread(target = task, daemon= True).start()

#函数2:一键复制结果 
def copy_email():
    content = output_text.get(1.0, tk.END).strip()
    if content:
        pyperclip.copy(content)
        messagebox.showinfo("成功","已复制")

#函数3:导出为TXT文件
def export_txt():
    content = output_text.get(1.0, tk.END).strip()
    if content:
        os.makedirs("output",exist_ok=True)
        with open("output/email.txt","w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("成功","TXT 已保存")

#函数4:导出为Markdown
def export_md():
    content = output_text.get(1.0, tk.END).strip()
    if content:
        os.makedirs("output",exist_ok=True)
        with open("output/email.md","w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("成功","MD 已保存")

#函数5:导出为Word文件
def export_word():
    content = output_text.get(1.0, tk.END).strip()
    if content:
        export_to_word(content, mail_type.get())
        messagebox.showingfo("成功", "Word 已保存")

#函数6:清空输入和输出所有内容
def clear_all():
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)

#==================================模块5:摆放按钮+启动程序=========================
btn_generate=tk.Button(root, text="生成邮件",command=generate_email, width=12)
btn_generate.place(x=20 , y=450)

tk.Button(root, text="一键复制", command=copy_email, width=10).place(x=120, y=450)
tk.Button(root, text="导出TXT", command=export_txt, width=10).place(x=210, y=450)
tk.Button(root, text="导出MD", command=export_md, width=10).place(x=300, y=450)
tk.Button(root, text="导出Word", command=export_word, width=10).place(x=390, y=450)
tk.Button(root, text="清空", command=clear_all, width=8).place(x=480, y=450)



























if __name__ == "__main__":
    root.mainloop()