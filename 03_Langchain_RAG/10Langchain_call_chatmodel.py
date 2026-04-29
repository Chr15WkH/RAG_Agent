from langchain_community.chat_models.tongyi import ChatTongyi
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

chat = ChatTongyi(model="qwen3-max")

'''
messages = [
    SystemMessage(content="你是一个被贬，但心怀大业，恨自己才华横溢却被人埋没的边塞诗人"),
    HumanMessage(content="给我写一首唐诗")
]
'''
# 消息的简写形式：通过二元元组的形式封装消息，第一个元素为角色(system,human,ai)，第二个元素为内容。
# 简写后的消息是动态的，需要在运行时由langchain内部机制转换为Message类对象。
# 简写形式支持内部填充{变量}占位，且可以避免导包。
messages = [
    ("system", "你是一个被贬，但心怀大业，恨自己才华横溢却被人埋没的边塞诗人"),
    ("human", "给我写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照上面这首回答的诗的格式，再给我写一首唐诗")
]

for chunk in chat.stream(input=messages):
    print(chunk.content, end = " ", flush = True)