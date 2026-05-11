'''
DocumentLoader：文档加载器提供了一套标准接口，用于将不同来源(如 CSV、PDF 或 JSON 等)的数据读取为 LangChain 的文档格式。
这确保了无论数据来源如何，都能对其进行一致性处理。
文档加载器（内置或自行实现）需实现 BaseLoader 接口。
'''

'''
Class Document，是 LangChain 内文档的统一载体，所有文档加载器最终返回此类的实例。
一个基础的 Document 类实例，基于如下代码创建：
from langchain_core.documents import Document

document = Document(
    page_content="Hello, world!",              # 文档的主要内容，字符串类型
    metadata={"source": "https://example.com"} # 文档的元数据，字典类型，可以包含任何与文档相关的附加信息，如来源、作者、日期等
)
'''

'''
不同的文档加载器可能定义了不同的参数，但是其都实现了统一的接口（方法）。
• load()：一次性加载全部文档
• lazy_load()：延迟流式传输文档，对大型数据集很有用，避免内存溢出。
一个简单的 CSVLoader 的使用示例如下：
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    ...  # 初始化参数
)

# 一次性加载全部文档
documents = loader.load() # 返回一个 Document 对象的列表

# 对于大数据集，分段返回文档
for document in loader.lazy_load():
    print(document)
'''

from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    csv_args={
        "delimiter": ",", # CSV文件的分隔符，默认为逗号，指定分隔符为逗号
        "quotechar": '"', # CSV文件的引用字符，默认为双引号，指定带有分隔符引号的字符为双引号
        "fieldnames": ["name", "age", "gender","hobby"] # CSV文件的列名，指定各列的名称
    }  
)
# # 一次性加载全部文档(批量加载)， -> Document 对象的列表
# documents = loader.load()
# for document in documents:
#     print(type(document), document)

# 对于大数据集，分段返回文档(流式加载)，每次返回一个 Document 对象
for document in loader.lazy_load():
    print(document)