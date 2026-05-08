from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# 定义一个函数，将 prompt 打印出来方便查看，同时不改变它本身，最后原样返回。
def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

chatmodel = ChatTongyi(model="qwen3-max")

# prompt_template = PromptTemplate.from_template(
#     "你需要根据对话历史回应用户的问题。历史对话如下：{chat_history}，请根据历史对话内容回答用户的问题：{question}给出回应"
# )

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据对话历史回应用户的问题。对话历史如下："),
        MessagesPlaceholder("chat_history"),
        ("human", "请根据历史对话内容回答用户的问题：{question}给出回应")
    ]
)

# 定义一个不带有历史对话功能的链，作为基础链，后续会在它的基础上添加历史对话功能。
base_chain = chat_template | print_prompt | chatmodel | StrOutputParser()
# 定义一个字典用于存放多个会话ID所对应的历史会话记录，key是会话ID，value是InMemoryChatMessageHistory对象。
chat_history_store = {}
# 定义一个获取指定会话id的历史会话记录的函数，如果该会话id不存在，则创建一个新的InMemoryChatMessageHistory对象并存入字典中。
def get_history(session_id):
    '''
    函数传入为会话ID(字符串类型)
    函数要求返回BaseChatMessageHistory的子类
    BaserChatMessageHistory类专用于存放某个会话的历史记录
    InMemoryChatMessageHistory是官方自带的基于内存存放历史记录的类
    '''
    if session_id not in chat_history_store:
        # InMemoryChatMessageHistory是用于临时存储会话历史的类，程序一旦停止便会丢失。
        chat_history_store[session_id] = InMemoryChatMessageHistory() 
    return chat_history_store[session_id]
# 通过RunnableWithMessageHistory类获取一个新的带有历史记录功能的chain，该类有如下四个参数：
conversation_chain = RunnableWithMessageHistory(
    base_chain,                         # 被附加历史消息的Runnable对象，这里是上面定义的基础链，通常是chain
    get_history,                        # 获取指定会话ID的历史会话的函数，输入为会话ID，输出为BaseChatMessageHistory的子类对象
    input_messages_key="question",      # 声明用户输入的消息在模版中的占位符key
    history_messages_key="chat_history" # 声明历史消息在模版中的占位符key
)

if __name__ == "__main__":
    # configurable是LangChain RunnableConfig中预定义的一种配置格式，表示该配置项是可配置的，可以在调用链时动态传入不同的值。
    # LangChain内部允许session_id,user_id,thread_id,memory_key,checkpoint等预定义的配置项，也允许用户自定义配置项，只要在链调用时传入即可。
    session_config = {"configurable":{"session_id": "test_session_1"}} # 定义一个会话配置字典，包含一个可配置项session_id，值为字符串"test_session_1"
    # invoke有两个参数：input和config，input是链的输入，config是链的配置项。
    # 链在运行时会根据config中的session_id来获取对应的历史会话记录，并将其注入到模版中，构建完整的提示词文本。
    print(conversation_chain.invoke(
        {"question": "小明有一只猫"},
          session_config
    ))
    print(conversation_chain.invoke({"question": "小刚有两只狗"},
        session_config
    ))
    print(conversation_chain.invoke({"question": "小明和小刚谁的宠物更多？"},
        session_config
    ))
