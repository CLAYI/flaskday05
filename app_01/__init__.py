# 创建app程序对象 ..脚本from flask import Flaskfrom app_01.ext import init_extfrom app_01.settings import configfrom app_01.views import blue, init_bluedef create_app(env_name=None):  # 设置默认为None,则可以不穿环境参数    app = Flask(__name__)    # 配置数据库信息    app.config.from_object(config.get(env_name or 'default'))    # 数据库初始化    init_ext(app)    # 给app注册蓝图对象 ===改进===> 初始化蓝图    # app.register_blueprint(blueprint=blue)    # 蓝图初始化    init_blue(app)    return app