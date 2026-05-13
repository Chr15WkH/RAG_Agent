from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
# 检索向量库
results = vector_store.similarity_search(input_text, k=2)
# 包装检索后的内容
reference_context = "["
for result in results:
    reference_context += result.page_content
reference_context += "]"
# 构建一个函数，将提示词打印出来供调试
def print_prompt(prompt):
    print("="*20, prompt.to_string(), "="*20)
    return prompt

# 构建链
chain = prompt | print_prompt | model | StrOutputParser()

response = chain.invoke(input={"context": reference_context, "question": input_text})

print(response)