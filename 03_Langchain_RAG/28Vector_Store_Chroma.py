from langchain_chroma import Chroma # chroma外部向量存储
from langchain_community.embeddings import DashScopeEmbeddings # 导入嵌入模型
from langchain_community.document_loaders import CSVLoader # 文档加载器

"""
# 外部chroma向量存储的使用
vector_store = Chroma(
    collection_name="my_collection", # 指定集合名称
    embedding_function=DashScopeEmbeddings(), # 指定嵌入模型
    persist_directory="./data/chroma_langchain_db" # 指定存储路径，用于存储向量数据库
)
"""
vector_store = Chroma(
    collection_name="chromadb_test", 
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_langchain_db"
)

loader = CSVLoader(
    file_path="./data/document1.csv",
    encoding="utf-8",
    source_column="title" # 指定本条文档的来源列，即指定 CSV 中哪一列作为每个 Document 的 metadata["source"]
)

documents = loader.load() # 10行csv文件，所以这里有10个Document对象，结构为[Document, Document...]
# 新增文档
vector_store.add_documents(
    documents=documents,
    ids=["id"+ str(i) for i in range(1, len(documents)+1)]
)
# 删除文档
vector_store.delete(ids=["id1", "id8"])
# 文档相似性搜索
results = vector_store.similarity_search(
    "机器学习是什么？",
    3,
    filter={"source": "机器学习概念"}, # 指定过滤条件,按照 metadata["source"] 进行过滤
)

for result in results:
    print(result)