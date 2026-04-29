from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

'''
ChatPromptTemplate是专门为对话模型设计的提示词模版类，支持多轮对话场景，支持系统消息、用户消息、AI消息等角色区分。
输入是一个消息列表（通过from_messages方法），消息可以是系统消息(system)，用户消息(human)，AI消息(ai)，每条消息都可以包含占位符，支持动态注入信息。
输出是一个结构化的消息列表，包含系统消息、用户消息、AI消息等角色区分，适用于对话模型的输入格式
'''

# 用MessagesPlaceholder占位符定义一个消息列表的占位符，表示在运行时会注入一个消息列表。提供history变量作为占位符的key。
# 必须使用invoke方法注入消息列表，不能使用format方法注入，因为format方法只能处理字符串占位符，无法处理结构化的消息列表占位符。
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
prompt_text = chat_template.invoke(input={"history": history_data}).to_string()
# print(prompt_text)

chat = ChatTongyi(model="qwen3-max")
'''
for chunk in chat.stream(input=prompt_text):
    print(chunk.content, end = " ", flush = True)
'''
response = chat.invoke(input=prompt_text)
print(response.content)