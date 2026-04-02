import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
request=requests.get("https://movie.douban.com/top250",headers=headers)
if request.ok:
    print("Connection successful")
    print(request.text)
    soup = BeautifulSoup(request.text, "html.parser")
    # 使用正确的方法名 find_all，避免返回 None
    alltitles = soup.find_all("span", attrs={"class": "title"})
    for title in alltitles:
        # 使用 get_text 保证返回字符串并去除首尾空白
        title_string = title.get_text(strip=True)
        if title_string and "/" not in title_string:
            print(title_string)
else:
    print("Connection failed with status code:", request.status_code) 