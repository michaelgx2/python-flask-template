import argparse
from datetime import datetime
import os
import jsonpickle
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, Response, request, jsonify
from waitress import serve
from logging import info, error
import logging, logging.handlers

port = 10010 #端口号
app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask Api Server'

# get接口示例
@app.route("/getMe", methods=["GET"])
def get_me():
    return ok()

@app.route("/postMe", methods=["POST"])
def post_me():
    paras = get_validated_json(["required_para1", "required_para2"], {"default_val_para1":59, "default_val_para2":"omg"})
    info(f"paras['default_val_para2] is: {paras['default_val_para2']}")
    return ok("读取成功", paras)


# ----------------------------------------------------------
# 接口都在这上面
# 下面的不用管
# ----------------------------------------------------------    
def ok(msg = "操作成功", data = None):
    return jsonpickle.encode({"msg": msg, "errcode": 0, "data": data})

def fail(msg = "操作失败", data = None, error_code = -1):
    return jsonpickle.encode({"msg": msg, "errcode": error_code, "data": data})

def get_validated_json(required_params=None, default_params=None):
    """
    遍历验证字典中每个键值对的值是否为空，如果指定了默认值，则使用默认值。
    
    :param param_dict: 需要验证的字典
    :param required_params: 必填参数列表，如果指定，则该列表中的每个参数必须在param_dict中存在且不为空，否则会抛出异常。
    :param default_params: 默认参数字典，如果指定，则param_dict中不存在的参数会从该字典中获取默认值。
    :return: 验证通过的字典
    :raises: ValueError: 如果required_params中指定的某个参数不存在或为空时，会抛出该异常。
    """
    validated_dict = {}
    param_dict = request.get_json(True)

    # 检查必填参数
    if required_params:
        for param_name in required_params:
            if param_name not in param_dict or param_dict[param_name] == '':
                raise ValueError(f"{param_name}不能为空。")

    # 遍历验证参数
    for param_name, param_value in param_dict.items():
        if param_value == '' and default_params and param_name in default_params:
            validated_dict[param_name] = default_params[param_name]
        elif param_value != '':
            validated_dict[param_name] = param_value

    # 加入默认参数
    if default_params:
        for param_name, param_value in default_params.items():
            if param_name not in validated_dict:
                validated_dict[param_name] = param_value

    return validated_dict

def config_logging():  
    #设置log日志的标准输出打印
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(filename)s:%(lineno)d - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console) 
    #设置每天保存一个log文件，以日期为后缀，保留7个旧文件。
    myapp = logging.getLogger()
    myapp.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(filename)s:%(lineno)d - %(message)s')
    filehandler = logging.handlers.TimedRotatingFileHandler(os.path.join(os.path.dirname(__file__), "server.log"), when='d', interval=1, backupCount=7, encoding='utf-8')#每 1(interval) 天(when) 重写1个文件,保留7(backupCount) 个旧文件；when还可以是Y/m/H/M/S
    filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"#设置历史文件 后缀
    filehandler.setFormatter(formatter)
    myapp.addHandler(filehandler)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=10010, type=int, help="port number")
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':    
    config_logging()    
    parser = argparse.ArgumentParser(description="XXX Server")
    opt = parse_opt()
    port = opt.port
    app.wsgi_app = ProxyFix(app.wsgi_app)
    serve(app, port = port)