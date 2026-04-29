from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
'''
类继承关系，(class inheritance, inherits from (parent/child class))
1.PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
2.FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
3.ChatPromptTemplate -> BaseChatPromptTemplate-> BasePromptTemplate -> RunnableSerializable -> Runnable
'''

example_template = PromptTemplate.from_template("我的邻居是{lastname}，最喜欢{hobby}。")

# format方法：1.功能：纯字符串替换，解析占位符生成提示词。2.返回值：字符串 
# 3.传参：.format(k=v, k=v, ...) 4.解析：占位符{变量}，将传入的参数k=v中的v替换占位符{变量}，生成提示词字符串。
response_format = example_template.format(lastname="qinglan", hobby="看书")
print(response_format, type(response_format))

# invoke方法：1.功能：Runnable接口标准方法，解析占位符生成提示词。2.返回值：PromptValue类对象 
# 3.传参：.invoke({"k": v, "k": v, ...}) 4.解析：占位符{变量}和MessagesPlaceholder结构化占位符。
response_invoke = example_template.invoke(input={"lastname":"qinglan", "hobby": "看书"})
print(response_invoke, type(response_invoke))