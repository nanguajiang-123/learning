# 安装ubuntu22（子系统）
https://wardenxyz.github.io/posts/2025/install_wsl2_and_to_d_disk.html
# 在子系统里面安装postgre
https://zhuanlan.zhihu.com/p/1900465497427911910
# 安装数据库插件
在vscode左侧边栏找到插件，下载Datebase Client（推荐）
# 下载asyncpg
在终端输入

pip install asyncpg

如果下载了仍然不成功请检查是否是电脑中有多个版本的python
# 链接postgre数据库前首先需要先创建一个数据库（eg:mydatabase）
打开电脑命令提示符

进入wsl

>wsl

启动postgre

>sudo service postgresql status

使用 sudo 直接进入 psql（推荐）

>sudo -u postgres psql

创建数据库

>CREATE DATABASE mydatabase;

查看数据库

>\l

退出

>\q
# main.py连接数据库

```python
register_tortoise(
    app,
    db_url="postgres://postgres:1234567890@localhost:5432/mydatabase",  # 硬编码数据库配置,这里1234567890应写为你设置的postgres密码，这里是为了展示
    modules={"models": ["app.models"]},  # 注册模型
    generate_schemas=True,  # 自动生成表结构（开发环境使用）
    add_exception_handlers=True,  # 添加异常处理器1
)
```
# 最后一步 ！！！
点击这个小图标
![alt text](image.png)
看下方红色框框
![alt text](<屏幕截图 2025-12-05 154719.png>)
