import tkinter as tk
from tkinter import filedialog
from reply_engine import get_ai_reply
from file_loader import load_data
from result_save import save_result
root = tk.Tk()
root. title("企业客服系统v3完整版")
root.geometry("600x400")
title_label = tk.Label(
    root,
    text="企业客服批量处理系统Demo",
    font = ("微软雅黑",16)
    )
title_label.pack(pady=20)
file_path = ""
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(
    title="请选择投诉文件",
    filetypes = [("文本文件","* .txt")])
    show_text.delete(1.0,tk.END)
    show_text.insert(tk.END,f"已选中文件：{file_path}\n=====准备开始处理=====\n")

def run_process():
    if not file_path:
        show_text.insert(tk.END,"请先选择文件")
        return

    complaint_list = load_data(file_path)
    for idx, ques in enumerate(complaint_list,1) :
        reply = get_ai_reply(ques)  
        output = f"【问题{idx}】{ques}\n【回复】{reply}\n------------\n"   
        show_text.insert(tk.END,output) 
        save_result(output,reply)
    show_text.insert(tk.END,"\n所以内容处理完成,结果自动保存data/result.txt")
button = tk.Button(root, text="选择投诉文件",command = choose_file)
button.pack(pady = 20)
btn2 = tk.Button(root, text="2. 开始批量处理", command=run_process, font=("微软雅黑", 12), bg="#90EE90")
btn2.pack(pady=5)
show_text = tk.Text(root, width=70, height=15, font=("微软雅黑", 10))
show_text.pack(pady=10)
root.mainloop()