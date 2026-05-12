'''
TextLoader：文本加载器提供了一套标准接口，用于读取文本文件(如.txt)，并将全部内容放入一个Document对象中。[Document]
注意! 全部内容仅放入一个Document对象中，而不是像之前的[Document, Document]这样的多个Document对象。
'''

"""
若文本过大，放入一个Document对象中可能会导致内存溢出。
因此需要使用RecursiveCharacterTextSplitter(递归字符文本分割器)，用于按自然段落分割大文档。
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/python_basic_syntax_for_langchain.txt",
    encoding="utf-8"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 指定分段的最大允许字符数
    chunk_overlap=50, # 指定分段之间允许的重叠字符数，保证语义连贯性。
    separators=["\n\n","\n","。","！","？",".","!","?"," ",""], #指定文本分段依据
    length_function=len # 指定字符统计依据(函数)，即用什么函数统计比如最大允许字符数，重叠字符数。
)

split_documents = splitter.split_documents(documents)

print("="*30,len(split_documents),"="*30,"\n")

for document in split_documents:
    print("="*30)
    print(document)
    print("="*30)
