"""
基于 LangChain 的向量存储，存储嵌入数据，并执行相似性搜索。
查询阶段(检索):
Query text(查询文本) -> Embedding model(嵌入模型) -转换-> Query vector(查询向量) -匹配-> "Vector stores(向量数据库)" -结果-> Top-k results(Top-k 结果)
索引阶段(存储):
Documents(文档) -> Embedding model(嵌入模型) -转换-> Embedding vectors(嵌入向量) -存入-> "Vector stores(向量数据库)"
"""

"""
LangChain 为向量存储提供了统一接口：
• add_documents
• delete
• similarity_search
"""

from langchain_core.vectorstores import InMemoryVectorStore # 内置的向量存储
from langchain_chroma import Chroma # chroma外部向量存储
from langchain_community.embeddings import DashScopeEmbeddings # 导入嵌入模型
from langchain_community.document_loaders import CSVLoader # 文档加载器

"""
# 内置向量存储的使用
vector_store  = InMemoryVectorStore(embedding=DashScopeEmbeddings()) # 定义时只需传入一个嵌入模型对象即可
# 可以使用InMEmoryVectorStore的add_documents方法添加文档
vector_store.add_documents(documents=[doc1, doc2],ids=["id1", "id2"])
# 用delete方法删除文档，指定添加文档时的id
vector_store.delete(ids=["id1", "id2"])
# 用similarity_search方法进行相似性搜索，指定查询文本和返回结果数量
vector_store.similarity_search("我喜欢你", 2)

# 外部chroma向量存储的使用
vector_store = Chroma(
    collection_name="my_collection", # 指定集合名称
    embedding_function=DashScopeEmbeddings(), # 指定嵌入模型
    persist_directory="./data/chroma_langchain_db" # 指定存储路径，用于存储向量数据库
)
"""
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())

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
results = vector_store.similarity_search("机器学习是什么？", 3)

for result in results:
    print(result)