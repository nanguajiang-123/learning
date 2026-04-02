import re
lst = re.findall(r"\d+","我的电话号是1234567890，我朋友的电话号是0987654321")
print(lst)


# finditer:匹配字符串中的所有内容，返回迭代器

it=re.finditer(r"\d+","我的电话号是1234567890，我朋友的电话号是0987654321")
for i in it:
    print(i.group())  # 使用 group() 方法获取匹配的字符串

# search:从字符串中搜索符合规则的第一个内容，返回匹配对象
s=re.search(r"\d+","我的电话号是1234567890，我朋友的电话号是0987654321")
print(s.group())  # 使用 group() 方法获取匹配的字符串

#match:从字符串的开头开始匹配，返回匹配对象
s1=re.match(r"\d+","1234567890，我朋友的电话号是0987654321")
print(s1.group())  # 使用 group() 方法获取匹配的字符串