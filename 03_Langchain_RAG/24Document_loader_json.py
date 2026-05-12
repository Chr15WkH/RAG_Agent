"""
JSON(JavaScript Object Notation)是一种用于表示和交换结构化数据的轻量级文本格式。
其核心结构为object(类似Python的dict)和array(类似list)。
JSON的优势是清晰易读、跨语言兼容且非常适合存储与传输层级化数据(适合表达结构化信息)。
"""
"""
使用JSONLoader将JSON数据加载为Document类型对象需要额外安装：pip install jq!
jq是一个跨平台的json解析工具，LangChain底层对JSON的解析就是基于jq工具实现的。
将JSON数据的信息抽取出来，封装为Document对象，抽取的时候依赖 jq_schema 语法。
对于JSON对象，有如下几种常见的jq_schema语法：(见stu.json文件)
• . 表示整个 JSON 对象（根）
• [] 表示数组
• .name 表示抽取小明
• .hobby 表示抽取爱好数组
• .hobby[1] 或 .hobby.[1] 表示抽取篮球
• .other.addr 表示抽取地址北京市海淀区
对于JSON数组，有如下几种常见的jq_schema语法：(见stus.json文件)
• .[]. 得到 3 个字典
• .[].name 表示抽取全部的 name，即得到 3 个 name 信息
"""
from langchain_community.document_loaders import JSONLoader

'''
loader = JSONLoader(
    file_path="./data/stu.json", # 定义JSON文件路径
    jq_schema=".",               # jq_schema参数是一个jq表达式，用于从JSON数据中提取特定的部分。这里的"."表示提取整个JSON对象。
    text_content=False,          # 默认为True，指示抽取的是否是字符串，
    # 上一行抽取的是整个json对象(对应python中的字典)，因此需要将text_content设置为False，表示抽取的内容不是字符串，而是一个结构化的数据对象。
    json_lines=True,             # 默认为False，指示是否是JsonLines文件(即，每一行都是独立的JSON的文件)
)
'''
loader1 = JSONLoader(
    file_path="./data/stu.json",
    jq_schema=".",
    text_content=False,
)
print(loader1.load()) # 输出一个Document对象，内容为整个JSON对象(对应python中的字典)

loader2 = JSONLoader(
    file_path="./data/stus.json",
    jq_schema=".[].name", 
)
print(loader2.load()) # 输出一个Document对象，内容为3个name

loader3 = JSONLoader(
    file_path="./data/stus_json_lines.jsonl",
    jq_schema=".name",
    text_content=False,
    json_lines=True,
)
print(loader3.load()) # 输出一个Document对象，内容为3个name