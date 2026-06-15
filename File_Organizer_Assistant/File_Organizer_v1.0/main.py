import tkinter as tk
from tkinter import filedialog, scrolledtext
from organizer import organize_files

#----------定义设计图-----
class FileOrganizerGUI:
    def __init__(self, root):
        self.root=root
        self.root.title("文件自动归档助手V1.0")
        self.root.geometry("500x400")
        self.select_path = tk.StringVar()
        tk.Label(root, text="文件自动归档助手", font=("微软雅黑",16)).pack(pady=10)

        frame_path=tk.Frame(root)
        frame_path.pack(fill="x", padx=20)

        tk.Button(frame_path, text="选择文件夹", command=self.choose_folder, width=12).grid(row=0, column=0)
        tk.Label(frame_path, textvariable=self.select_path, fg="#333").grid(row=0, column=1, padx=10)

        tk.Button(root, text="开始整理", command=self.start_organize, bg="#409EFF", fg="white", width=15, height=1).pack(pady=15)

        tk.Label(root, text="运行日志 & 统计结果:").pack()
        self.result_text= scrolledtext.ScrolledText(root, width=65, height=12)
        self.result_text.pack(padx=20, pady=5)

#----------------动作流------------------
    def choose_folder(self):
        """弹出窗口选择文件夹"""
        path = filedialog.askdirectory(title="请选择需要整理的文件夹")
        if path:
            self.select_path.set(path)
        self.result_text.insert(tk.END,f"已选中文件夹:{path}\n")
        self.result_text.see(tk.END)

    def start_organize(self):
        """执行文件整理"""
        source_path = self.select_path.get()
        if not source_path:
            self.result_text.insert(tk.END,"请先选择文件夹!\n")
            return
    
        output_path = "./File_Organizer_Assistant/File_Organizer_v1.0/output"
        count_data, msg = organize_files(source_path, output_path)

        show_text = f"\n===={msg}======\n"
        for cate, num in count_data.items():
            show_text += f"{cate}:{num}个文件\n"

        self.result_text.insert(tk.END, show_text)
        self.result_text.see(tk.END)

if __name__== "__main__":
    root=tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()