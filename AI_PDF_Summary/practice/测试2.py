from pathlib import Path
#1.项目根目录
root_path = Path(__file__).parent
import os
from 练习 import read_pdf
res = read_pdf(root_path/"input_file"/"test.pdf")
print(res[:500])