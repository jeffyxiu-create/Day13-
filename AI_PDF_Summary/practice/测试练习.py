# from pathlib import Path
# base = Path(__file__).parent
# pdf_path = base/"input_file"/"test.pdf"
# from file_loader import read_pdf
# res = read_pdf(pdf_path)
# print(res[:100])

# from pathlib import Path
# base = Path(__file__).parent
# pdf_path = base/"input_file"/"test.pdf"
# from file_loader import read_pdf
# res = read_pdf(pdf_path)
# print(res[:200])

# from pathlib import Path
# base = Path(__file__).parent
# pdf_path = base/"input_file"/"test.pdf"
# from file_loader import read_pdf
# res = read_pdf(pdf_path)
# print(res[200:300])#冒号是python切片语法

# import os
# from file_loader import read_pdf
# base = os.path.dirname(__file__)
# paf_path = os.path.join(base,"input_file","test.pdf")
# res = read_pdf(paf_path)
# print(res[200:500])

# import os 
# from file_loader import read_pdf
# base = os.path.dirname(__file__)
# pdf_path = os.path.join(base,"input_file","test.pdf")
# res = read_pdf(pdf_path)
# print(res[:200])

from pathlib import Path
base = Path(__file__).parent
pdf_path = base/"input_file"/"test.pdf"
from file_loader import read_pdf
res = read_pdf(pdf_path)
print(res[:100])