import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import threading
import pyperclip
from ai_helper import generate_email
import os

root = tk.Tk()
root.title("AI 邮件助手 V1.0")
root.geometry("900x640")
root.resizable(True,True)
root.configure(bg="#F5F6FA")

FONT_TITLE = ("微软雅黑",11, "bold")
FONT_NORMAL = ("微软雅黑",10)
COLOR_BG    = "#F5F6FA"
COLOR_BTN   = "#4682B4"
COLOR_BTN_FG= "#FFFFFF"
COLOR_GRAY_BTN = "#9E9E9E"

# 网格布局：两列自适应拉伸
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

tk.Label(root, text="邮件需求", font=FONT_TITLE, bg=COLOR_BG).grid(
    row=0, column=0, sticky="w", padx=20, pady=(16, 4)
)

# 输入框容器
input_frame = tk.Frame(root, bg=COLOR_BG)
input_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 10))
input_frame.columnconfigure(0, weight=1)
input_frame.rowconfigure(0, weight=1)

# 文本框 + 垂直滚动条
prompt_box = tk.Text(
    input_frame, font=FONT_NORMAL, wrap="word",
    relief="solid", bd=1
)
prompt_box.grid(row=0, column=0, sticky="nsew")

input_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=prompt_box.yview)
input_scroll.grid(row=0, column=1, sticky="ns")
prompt_box.configure(yscrollcommand=input_scroll.set)

# ====================== 右侧：结果展示区域 + 滚动条 ======================
tk.Label(root, text="生成结果", font=FONT_TITLE, bg=COLOR_BG).grid(
    row=0, column=1, sticky="w", padx=20, pady=(16, 4)
)
# 结果框容器
result_frame = tk.Frame(root, bg=COLOR_BG)
result_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 10))
result_frame.columnconfigure(0, weight=1)
result_frame.rowconfigure(0, weight=1)

# 结果文本框（默认只读）
result_box = tk.Text(
    result_frame, font=FONT_NORMAL, wrap="word",
    relief="solid", bd=1, state="disabled"
)
result_box.grid(row=0, column=0, sticky="nsew")

result_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=result_box.yview)
result_scroll.grid(row=0, column=1, sticky="ns")
result_box.configure(yscrollcommand=result_scroll.set)

# ====================== 底部状态栏 ======================
status_var = tk.StringVar(value="就绪")
status_bar = tk.Label(
    root, textvariable=status_var, font=("微软雅黑", 9),
    bg="#E8EAF0", anchor="w", padx=10
)
status_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

# ====================== 按钮容器 & 按钮封装函数 ======================
btn_frame = tk.Frame(root, bg=COLOR_BG)
btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

def make_btn(parent, text, cmd, bg_color=COLOR_BTN):
    """统一创建样式按钮"""
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        font=FONT_NORMAL,
        bg=bg_color,
        fg=COLOR_BTN_FG,
        relief="flat",
        padx=18,
        pady=6,
        cursor="hand2",
        activebackground="#3A5CE0",
        activeforeground="#FFFFFF"
    )

def set_status(msg, color="black"):
    """更新状态栏文字和颜色"""
    status_var.set(msg)
    status_bar.configure(fg=color)

def _do_generate(user_text):
    """子线程执行AI调用,防止UI卡死"""
    try:
        email_text = generate_email(user_text)
        root.after(0,lambda: _show_result(email_text))
    except Exception as e :
        root.after(0, lambda: _show_error(str(e)))

def _show_result(email_text):
    """展示生成后的邮件内容"""
    result_box.configure(state="normal")
    result_box.delete("1.0",tk.END)
    result_box.insert(tk.END, email_text)
    result_box.configure(stat="disabled")
    btn_generate.configure(state="normal",text="生成邮件")
    set_status("生成完成","green")

def _show_error(err_msg):
    """捕获异常并提示"""
    btn_generate.configure(state="normal", text="生成邮件")
    set_status(f"生成失败:{err_msg}","red")
    messagebox.showerror("错误",f"生成失败:{err_msg}")

def create_email():
    user_text = prompt_box.get("1.0",tk.END).strip()
    if not user_text:
        messagebox.showwarning("提示","请先输入邮件需求!")
        return
    btn_generate.configure(state="disabled",text="生成中...")
    set_status("正在生成,请稍候...")
    threading.Thread(target= _do_generate, args=(user_text,), daemon=True).start()

def copy_email():
    content = result_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("提示", "暂无可复制的内容！")
        return
    pyperclip.copy(content)
    set_status("✅ 已复制到剪贴板", "green")
    messagebox.showinfo("成功", "邮件已复制到剪贴板！")

def save_email():
    content = result_box.get("1.0",tk.END).strip()
    if not content:
        messagebox.showwarning("提示","暂无内容可保存!")
        return
    if not os.path.exists("output"):
        os.mkdir("output")
    file_path = filedialog.asksaveasfilename(
        initialdir = "output",
        defaultextension=".txt",
        filetypes=[("文本文件","*.txt"),("所有文件","*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            set_status(f"已保存:{file_path}","green")
            messagebox.showinfo("成功","文件保存完成!")

def clear_all():
    prompt_box.delete("1.0",tk.END)
    result_box.configure(state="normal")
    result_box.delete("1.0",tk.END)
    result_box.configure(state="disabled")
    set_status("已清空")

btn_generate = make_btn(btn_frame,"生成邮件",create_email)
btn_generate.pack(side="left",padx=8)

make_btn(btn_frame,"🖨一键复制",copy_email).pack(side="left",padx=8)
make_btn(btn_frame,"💾保存TXT",save_email).pack(side="left",padx=8)
make_btn(btn_frame,"🗑清空",clear_all,COLOR_GRAY_BTN ).pack(side="left",padx=8)



if __name__ == "__main__":
    root.mainloop()