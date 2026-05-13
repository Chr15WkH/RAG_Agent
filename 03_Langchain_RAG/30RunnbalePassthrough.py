'''
让向量检索(query vector)加入chain中，可以使用RunnablePassthrough类来实现。
'''

from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document


model = ChatTongyi(model='qwen3-max')
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}"),
        ("user", "用户提问：{question}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备参考资料(向量库的数据)
# add_texts 传入一个list[str],转换成向量，存入向量库
vector_store.add_texts(["机器学习是一种让计算机从数据中自动学习规律的方法，而无需为每一种情况显式编写规则。",
                       "监督学习是一种利用“带标签数据”训练模型的方法。模型通过学习输入与正确输出之间的映射关系，从而对新的数据进行预测。",
                       "强化学习通过“奖励机制”让智能体学习如何行动。智能体在环境中不断试错，目标是获得长期最大的累计奖励。"]
)

input_text = "什么是机器学习中的监督学习？"

# langchain中向量存储对象(VectorStore),有一个方法：as_retriever,可以返回一个Runnable接口的子类实例对象

# vector_store.as_retriever() 本质上就是把向量数据库封装成一个会自动调用 similarity_search() 的 Runnable 检索器。
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 构建一个函数，将提示词打印出来供调试
def print_prompt(prompt):
    print("="*20, prompt.to_string(), "="*20)
    return prompt

# 构建一个函数，将检索后的内容格式化,将list[document]转换成str
def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str

# 构建嵌套链,第一个组件字典中还有一个嵌套链，调用invoke方法时输入内容会同时给retriever和字典传入。
# RunnablePassthrough 本质上就是一个“输入什么就原样返回什么”的 Runnable，常用于 LCEL 链中保留用户原始输入作为占位符继续传递。
chain = {"question": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
'''
retriever:
 - 输入为用户的提问,类型为str
 - 输出为检索后的内容,类型为listp[document]
prompt:
 - 输入为用户的提问+检索后的内容,类型为dict
 - 输出为完整的提示词,类型为Promptvalue

'''
response = chain.invoke(input_text)
print(response)