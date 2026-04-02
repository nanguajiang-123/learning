
import re

def demo():
    s = "我的电话号是1234567890，我朋友的电话号是0987654321"
    lst = re.findall(r"\d+", s)
    print(lst)

    it = re.finditer(r"\d+", s)
    for m in it:
        print(m.group())

    s2 = re.search(r"\d+", s)
    print(s2.group())

    s1 = re.match(r"\d+", "1234567890，我朋友的电话号是0987654321")
    print(s1.group())

if __name__ == "__main__":
    demo()
