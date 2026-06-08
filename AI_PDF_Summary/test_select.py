import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    filetypes=[("PDF Files","*.pdf")]
)
print("PDF路径",file_path)
root.destroy()