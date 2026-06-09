import os
from file_loader import read_pdf
res = read_pdf("input_file/test.pdf")
print(res[:500])