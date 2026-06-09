
---

### 第一步：把整个流程拆成「4块固定积木」
你现在的PDF工具，核心就4大块，每一块都是Python多线程+Tkinter的通用模板，背下来就能套所有类似项目：

| 积木编号 | 功能 | 一句话模板 |
| :--- | :--- | :--- |
| 1️⃣ | 界面初始化（`__init__`） | 建窗口、放按钮、放文本框、初始化变量 |
| 2️⃣ | 按钮点击触发（`start_summary`） | 选文件 → 锁界面 → 开线程跑AI |
| 3️⃣ | 子线程干活（`run_ai_task`） | 调用AI → 存结果 → 通知主线程更新 |
| 4️⃣ | 主线程更新界面（`update_result`） | 填文本框 → 解锁按钮 → 改状态文字 |

---

### 第二步：给每块积木写「极简记忆版」
我帮你把每一块的代码，缩成3-5行的“骨架”，先记骨架，再填细节，比背整段代码轻松10倍。

#### 积木1：`__init__` 初始化（只记关键变量）
```python
def __init__(self, root):
    self.root = root
    self.current_summary = ""  # 存AI结果的“仓库”
    # 界面控件：状态标签、两个按钮、两个文本框（PDF原文/AI摘要）
    self.status_label = tk.Label(...)
    self.btn_select = tk.Button(..., command=self.start_summary)
    self.btn_save = tk.Button(..., command=self.do_save, state=tk.DISABLED)
    self.txt_original = scrolledtext.ScrolledText(...)
    self.txt_summary = scrolledtext.ScrolledText(...)
```
**记忆点**：记住 `self.current_summary` 和所有控件变量名就行，布局代码不用死背，用的时候复制。

---

#### 积木2：`start_summary` 按钮触发（锁界面+开线程）
```python
def start_summary(self):
    # 1. 选文件
    file_path = filedialog.askopenfilename(...)
    if not file_path: return
    # 2. 锁界面（防止乱点）
    self.btn_select.config(state=tk.DISABLED)
    self.btn_save.config(state=tk.DISABLED)
    self.status_label.config(text="正在读取PDF...")
    # 3. 读取PDF（你已经写好的）
    pdf_text, tip = read_pdf(file_path)
    # 4. 异常处理（没读到文本就解锁退出）
    if not pdf_text:
        self.btn_select.config(state=tk.NORMAL)
        return
    # 5. 开线程跑AI（关键模板！）
    self.status_label.config(text="正在AI总结中...")
    t = threading.Thread(target=self.run_ai_task, args=(pdf_text,))
    t.daemon = True
    t.start()
```
**记忆点**：记住「选文件→锁界面→读文件→开线程」这个顺序，锁界面的3行是固定写法，线程的3行也是固定模板。

---

#### 积木3：`run_ai_task` 子线程干活（AI调用+通知主线程）
```python
def run_ai_task(self, text):
    # 1. 调用AI（耗时操作，放子线程）
    summary = generate_summary(text)
    # 2. 把结果存到“仓库”里
    self.current_summary = summary
    # 3. 通知主线程更新界面（固定模板！）
    self.root.after(0, self.update_result, summary)
```
**记忆点**：就3步：调用AI → 存结果 → `after` 通知主线程，`after` 这行是子线程和主线程的“安全通道”，必须写。

---

#### 积木4：`update_result` 主线程更新（填界面+解锁）
```python
def update_result(self, summary):
    # 1. 填AI摘要文本框
    self.txt_summary.delete(1.0, tk.END)
    self.txt_summary.insert(1.0, summary)
    # 2. 解锁按钮
    self.btn_select.config(state=tk.NORMAL)
    self.btn_save.config(state=tk.NORMAL)
    # 3. 改状态文字
    self.status_label.config(text="总结完成")
```
**记忆点**：记住「清空文本框→插入新内容→解锁按钮」这个顺序，`delete` 和 `insert` 是文本框的固定操作。

---

### 第三步：用「分步默写法」代替“一次性全写”
不要逼自己一次把整个文件写出来，用下面这个节奏练，3次就能记住：

1.  **第1次：只写骨架，不写细节**
    先把4个函数的框架搭好，比如：
    ```python
    class PdfSummaryApp:
        def __init__(self, root): pass
        def start_summary(self): pass
        def run_ai_task(self, text): pass
        def update_result(self, summary): pass
    ```

2.  **第2次：只填每个函数里的“关键3行”**
    比如 `run_ai_task` 里，先写 `summary = generate_summary(text)`、`self.current_summary = summary`、`self.root.after(...)` 这三行，其他细节空着。

3.  **第3次：补全细节+对照检查**
    把读取PDF、异常处理这些细节补进去，再和你原来的代码对照，看哪里漏了，改完就记牢了。

---

