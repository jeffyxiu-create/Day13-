import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# --- 1. 不用StringVar的标签（手动改，各改各的） ---
label1 = tk.Label(root, text="未更新", bg="lightblue", width=30)
label1.pack(pady=10)

def update_label1():
    label1.config(text="我被手动更新了！")

btn1 = tk.Button(root, text="更新标签1（不用StringVar）", command=update_label1)
btn1.pack(pady=5)

# --- 2. 用StringVar的标签（一个变量绑定两个标签，自动同步） ---
# 定义1个变量，准备给2个标签共用
var = tk.StringVar(value="未更新")

# 第一个标签绑定var
label2 = tk.Label(root, textvariable=var, bg="lightgreen", width=30)
label2.pack(pady=10)

# 第二个标签也绑定同一个var！
label3 = tk.Label(root, textvariable=var, bg="lightyellow", width=30)
label3.pack(pady=10)

def update_label2():
    # 只需要改一次var.set，两个标签会一起变！
    var.set("我被自动更新了！")

btn2 = tk.Button(root, text="更新标签2&3（用StringVar）", command=update_label2)
btn2.pack(pady=5)

root.mainloop()