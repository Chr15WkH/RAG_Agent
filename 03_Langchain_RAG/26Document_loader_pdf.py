"""
PyPDFLoader加载器，依赖PyPDF库，需要额外安装 pip install pypdf
"""

from langchain_community.document_loaders import PyPDFLoader

loader1 = PyPDFLoader(
    file_path="./data/python_basic_syntax_for_langchain.pdf" ,# 指定文件路径
    mode='page', # 指定加载模式为'page',读取模式。可选page(按页面划分不同Document)和single(单个Document)
)


loader2 = PyPDFLoader(
    file_path="./data/python_basic_syntax_for_langchain_with_password.pdf" ,# 指定文件路径
    mode='page', # 指定加载模式为'page',读取模式。可选page(按页面划分不同Document)和single(单个Document)
    password='password' # 文件密码
)

i = 0
for document in loader2.lazy_load():
    i += 1
    print(document)
    print("="*30,i,"="*30)
