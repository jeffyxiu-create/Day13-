import tkinter as tk

root = tk.Tk()
root.geometry("400x200")

# 1.普通字符串
normal_str = "初始"
lab1 = tk.Label(root, text=normal_str, fg="red", font=12)
lab1.pack(pady=10)
# 重新赋值，界面不会变
normal_str = "普通变量更新了"

# 2.StringVar绑定变量
var_str = tk.StringVar(value="初始空白")
lab2 = tk.Label(root, textvariable=var_str, fg="blue", font=12)
lab2.pack(pady=10)
# set赋值，界面立刻刷新
var_str.set("StringVar刷新界面")

root.mainloop()