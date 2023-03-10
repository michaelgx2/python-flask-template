# python-flask-template

#### 介绍
一个简单的python flask app模板

#### 软件架构
使用Flask库，并引入了pyYAML和jsonpickle备用


#### 安装教程

1.  clone这个repo
2.  创建虚拟环境并激活，然后安装依赖
##### Windows Powershell (不建议使用别的命令行工具)
``` Windows Powershell
python -m venv venv
venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
```
##### Linux Shell
``` Linux Shell
python -m venv venv
source venv/bin/acticate
python -m pip install -r requirements.txt
```
3.  修改 app.py 成你自己的逻辑
4.  修改start.bat和start.sh中的脚本路径和脚本名称并根据不同的系统运行不同的脚本(windows下运行bat，linux下运行sh)

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_pyflask 分支
3.  提交代码
4.  新建 Pull Request