import tkinter as tk
from tkinter import filedialog, messagebox
from file_loader import load_data
from reply_engine import get_ai_reply
from result_save import save_result

# def run_all():
#     # 1. 获取文件路径
#     file_path = entry_path.get()
#     if not file_path:
#         messagebox.showwarning("警告", "请先选择文件！")
#         return
    
#     # 2. 调用加载器读取数据
#     complaints = file_loader.load_data(file_path)
    
#     # 3. 清空显示区域并逐个处理
#     text_display.delete(1.0, tk.END)
#     for c in complaints:
#         reply = reply_engine.get_ai_reply(c)
#         result_save.save_result(c, reply)
#         # 显示在界面上
#         text_display.insert(tk.END, f"问题: {c}\n{reply}\n{'-'*30}\n")

# # 创建界面
# root = tk.Tk()
# root.title("企业客服系统 V1")
# root.geometry("600x500")

# # 路径输入框
# entry_path = tk.Entry(root, width=50)
# entry_path.pack(pady=10)

# # 按钮
# btn_select = tk.Button(root, text="选择文件", command=lambda: entry_path.insert(0, filedialog.askopenfilename()))
# btn_select.pack()

# btn_run = tk.Button(root, text="开始批量处理", command=run_all, bg="lightblue")
# btn_run.pack(pady=10)

# # 结果显示框
# text_display = tk.Text(root, width=70, height=20)
# text_display.pack(pady=10)

# root.mainloop()
def run_all():
   path = filedialog.askopenfilename()
   if path:
    complaints = load_data(path)
    for item in complaints:
        reply = get_ai_reply(item)
        output = f"投诉：{item} | 回复 :{reply}"
        show_text.insert((tk.END),output + "\n")
        save_result(output,reply)

root = tk.Tk()
root.title("企业客服系统V3")
show_text = tk.Text(root, width =60 ,height=15)
show_text.pack()
tk.Button(root, text= "开始批量处理",command = run_all).pack()
root.mainloop()