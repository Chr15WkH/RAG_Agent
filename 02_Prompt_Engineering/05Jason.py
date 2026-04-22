import json 
#json.dumps(字典或列表, ensure_ascii=False)将字典转换成json; ensure_ascii=False是防止中文乱码
#json.loads(json字符串)将json转换成字典
data = {
    "name": "max",
    "age": "22",
    "gender": "woman",
}

s = json.dumps(data, ensure_ascii=False)
print(s,type(s))

list = [
    {
    "name": "max",
    "age": "22",
    "gender": "woman",
    },
    {
    "name": "chris",
    "age": "26",
    "gender": "man",
    },
    {
    "name": "jane",
    "age": "24",
    "gender": "woman",
    }
]
l = json.dumps(list, ensure_ascii=False)
print(l,type(l))

json_str = '{"name": "max", "age": "22", "gender": "woman"}'
res_dict = json.loads(json_str)
print(res_dict,type(res_dict))

json_array_str = '[{"name": "max", "age": "22", "gender": "woman"}, {"name": "chris", "age": "26", "gender": "man"}, {"name": "jane", "age": "24", "gender": "woman"}]'
res_list = json.loads(json_array_str)
print(res_list,type(res_list))