import select
import tkinter as tk
from tkinter import filedialog
from pdf_reader import read_pdf

root = tk.Tk()
root.title("PDF总结助手 v1.5")
root.geometry("700x500")

select_pdf_path = tk.StringVar()

def select_file():
    path = filedialog.askopenfilename(
    filetypes = [("PDF Files","*.pdf")]
    )
    if not path :
        return
    select_pdf_path.set(path)
    pdf_content = read_pdf(path)
    content_text.delete("1.0",tk.END)
    content_text.insert("1.0",pdf_content)

tk.Label(root, text="PDF总结助手",font = ("黑体",16)).pack(pady=8)
tk.Button(root,text = "选择PDF",command = select_file).pack(pady=4)

tk.Label(root, text="文件路径:").pack()
tk.Label(root,textvariable=select_pdf_path, wraplength = 650).pack(pady=2)
tk.Frame(root,height=2,bg="black").pack(fill=tk.X,padx=20,pady=5)

content_text = tk.Text(root)
content_text.pack(fill=tk.BOTH, expand = True, padx=10, pady=5)
root.mainloop()


    
        

