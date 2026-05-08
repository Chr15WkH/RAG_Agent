from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
'''
Chain链，将组件串联起来，形成一个完整的流程。上一个组件的输出作为下一个组件的输入，是Langchain链(尤其是 | 管道链)的核心工作原理。
也是链式调用的核心价值：实现数据的自动化流转与组件的协同工作，如下：
chain = prompt_template | model
！注意！：核心前提为Runnable子类对象才能入链(Fewshot/chat/PromptTemplate,Tongyi,ChatTongyi等)，以及Callable，Mapping接口子类对象也可加入。
'''

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个被贬，但心怀大业，恨自己才华横溢却被人埋没的边塞诗人"),
        MessagesPlaceholder("history"),
        ("human", "按照上面这首回答的诗的格式，再给我写一首唐诗")
    ]
)

history_data = [
    ("human", "给我写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "再给我写一首唐诗"),
    ("ai", "窗前明月光，疑是地上霜，举头望明月，低头思故乡。")
]

# 调用模型进行回复
chat = ChatTongyi(model="qwen3-max")

# 形成的链是RunnableSerializable对象（Runnable接口子类）
chain = chat_template | chat
print(type(chain))
'''
response = chain.invoke(input={"history": history_data})
print(response.content)
'''
# 可以通过链调用invoke或stream方法触发整个链条的执行。
for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end = " ", flush = True)