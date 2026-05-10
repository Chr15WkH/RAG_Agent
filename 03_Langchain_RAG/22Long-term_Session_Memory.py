import os, json
# message_to_dict:单个消息对象(BaseMessage类实例) -> 字典； AI/Human/SystemMessage等消息对象都是BaseMessage类的子类，所以都可以使用这个函数转换为字典。
# messages_from_dict:[字典,字典...] -> [消息，消息...]
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import Sequence, List
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi

'''
os库是python自带的标准库，用来和操作系统交互。常见用途包括：
os.getcwd()          # 获取当前工作目录
os.listdir()         # 查看目录下的文件
 os.makedirs()        # 创建文件夹，exist_ok=True表示如果文件夹已存在则不报错
os.remove()          # 删除文件
 os.path.join()       # 拼接路径
 os.path.dirname()    # 获取上一级目录路径
os.path.exists()     # 判断路径是否存在
'''
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id # 会话ID，字符串类型，用于区分不同的会话记录
        self.storage_path = storage_path   # 不同会话ID对应的历史记录存储文件路径，字符串类型
        # 完整的文件路径。文件路径可以根据会话ID动态生成，以确保每个会话的历史记录存储在不同的文件中。
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 确保文件存在，如果不存在则创建一个空文件
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequencep[BaseMessage]:变量类型标注，表示输入参数messages是一个BaseMessage对象的序列（列表、元组等）。
        all_messages = list(self.messages) # 已有的消息列表
        all_messages.extend(messages) # 将新消息添加到已有消息列表中,合并成一个list

        # 将数据同步写入到本地文件中，但是类对象写入文件中为一堆二进制，为了方便查看和调试，可以先将消息对象[BaseMessage类实例]转换为字典，再将字典写入文件中。
        # new_messages = []
        # for msg in messages:
        #     msg_dict = message_to_dict(msg) # 将消息对象转换为字典
        #     new_messages.append(msg_dict)
        new_messages = [message_to_dict(msg) for msg in all_messages] # 上面注释部分的列表推导式写法，功能相同
        
        # 将数据写入文件中，覆盖原有内容，写入模式为"w"，覆盖写入模式。
        '''
        这里的f是一个变量名(即file)，代表被打开的文件对象。
        with open(...) as f 是 Python 中的一种上下文管理器语法，用于处理文件操作。它的作用是确保在代码块执行完毕后，文件能够正确地关闭，即使在代码块中发生异常也能保证文件被关闭。
        用 UTF-8 编码写入文件。UTF-8 可以很好地支持中文、英文、德语特殊字符等内容。
        '''
        with open(self.file_path, "w", encoding="utf-8") as f:
            '''
            json.dump(data, f) 将 Python 对象 data 转换为 JSON 格式，并将其写入到文件对象 f 中。
            这一步叫做序列化（serialization），即将 Python 内存对象(dict)转换为可存储的格式(这里是JSON 字符串)的过程。
            注意！和jason.dumps()不同，json.dumps()只做数据类型转换的操作。json.dump()则是在转换的基础上，还将结果写入文件中。
            '''
            json.dump(new_messages, f)
    
    @property # @property装饰器将messages方法转换为属性，使得调用时不需要加括号，直接通过对象.属性的方式访问。
    def messages(self) -> List[BaseMessage]: # 返回值类型标注，表示返回值是一个BaseMessage对象的列表（列表、元组等）。
        # json.load(f)读取当前文件后，数据类型为list[字典]，需要将其转换为list[消息对象(即BaseMessage类实例)]，才能符合BaseChatMessageHistory类的要求。
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                '''
                json.load(f)读取json，并将json转换成python对象，这里是将json字符串转换为字典或列表，具体取决于json字符串的结构。
                '''
                messages_dict = json.load(f) # 从文件中读取数据，得到一个list[字典]
                messages = messages_from_dict(messages_dict) # 将list[字典]转换为list[消息对象(即BaseMessage类实例)]
                return messages
        except FileNotFoundError: # 如果文件不存在，则返回一个空列表，表示没有历史消息记录。
            return []
        
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)




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
    # FileChatMessageHistory是上面定义的基于文件存储历史记录的类，程序停止后历史记录依然存在。
    return FileChatMessageHistory(session_id, storage_path="./chat_history/") 
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
    # print(conversation_chain.invoke(
    #     {"question": "小明有一只猫"},
    #       session_config
    # ))
    # print(conversation_chain.invoke({"question": "小刚有两只狗"},
    #     session_config
    # ))
    print(conversation_chain.invoke({"question": "小明和小刚谁的宠物更多？"},
        session_config
    ))
