import os
base_path = os.path.dirname(__file__)
full_path = os.path.join(base_path,"input_file","test.pdf")
from file_loader import read_pdf
res = read_pdf(full_path)
print(res[:500])