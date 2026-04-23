from langchain_community.embeddings import DashScopeEmbeddings

# 初始化嵌入模型对象，其默认使用的模型为：text-embedding-v1
embed = DashScopeEmbeddings()

# 测试
# embed_query：字符串转向量
print(embed.embed_query("我喜欢你"))
# embed_documents：多个字符串(批量)转向量
print(embed.embed_documents(["我喜欢你", "i like you", "ich liebe dich"]))