
import tkinter as tk
from tkinter import filedialog,scrolledtext
import threading

from pdf_reader import read_pdf
from api_engine import generate_summary
from file_save import save_to_txt

class PdfSummaryApp:
    def __init__(self,root):
        self.root = root
        self.root.title("AI PDF 总结助手 V2.0")
        self.root.geometry("800x600")

        self.current_summary = ""

        self.status_label = tk.Label(root, text="就绪",fg = "#333")
        self.status_label.pack(fill=tk.X,padx=10,pady=5)

        #按钮框架:容器
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        # 按钮定义:两个按钮
        self.btn_select = tk.Button(btn_frame, text="选择PDF并总结",command=self.start_summary)
        self.btn_select.grid(row=0, column=0, padx=0)

        self.btn_save = tk.Button(btn_frame, text= "保存摘要",command=self.do_save, state=tk.DISABLED)
        self.btn_save.grid(row=0, column=1, padx=10)#第二个按钮,默认被禁用(state=tk.DISABLED)

        # 原文显示区
        tk.Label(root, text="PDF原文:").pack(anchor=tk.W, padx=10)
        self.txt_original = scrolledtext.ScrolledText(root,height=12)
        self.txt_original.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 摘要显示区
        tk.Label(root, text="AI 摘要:").pack(anchor=tk.W, padx=10)
        self.txt_summary = scrolledtext.ScrolledText(root,height=12)
        self.txt_summary.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    print("进入start_summary")
    def start_summary(self):
        """
        入口:选择PDF+启动子线程
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF文件","*.pdf"),("所有文件","*.*")]
        )
        if not file_path:
            return

        #界面状态:禁用按钮+变更提示
        self.btn_select.config(state=tk.DISABLED)
        self.btn_save.config(state=tk.DISABLED)
        self.status_label.config(text="正在读取PDF...")

        #读取PDF
        pdf_text, tip = read_pdf(file_path)
        self.txt_original.delete(1.0, tk.END)
        self.txt_original.insert(1.0, pdf_text)

        if tip:
            self.status_label.config(text=tip)
        if not pdf_text:
            self.btn_select.config(state=tk.NORMAL)
            return
        self.status_label.config(text="正在AI总结中,请稍候...")
        t = threading.Thread(target = self.run_ai_task, args= (pdf_text,))
        t.daemon = True
        t.start()


    print("进入run")
    def run_ai_task(self, text):
        """子线程执行AI调用"""
        summary = generate_summary(text)
        self.current_summary = summary

        # 回到主线程更新界面（Tkinter要求界面操作必须在主线程）
        self.root.after(0, self.update_result, summary)

    print("进入update")
    def update_result(self, summary):
        """更新摘要 + 恢复按钮"""
        self.txt_summary.delete(1.0, tk.END)
        self.txt_summary.insert(1.0, summary)
        self.status_label.config(text="总结完成")
        self.btn_select.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.NORMAL)

    print("进入do_save")
    def do_save(self):
        """执行保存"""
        res = save_to_txt(self.current_summary)
        self.status_label.config(text=res)

# 程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = PdfSummaryApp(root)
    root.mainloop()


