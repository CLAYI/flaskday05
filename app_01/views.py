# 视图、路由脚本
from flask import Blueprint, render_template, request, url_for, redirect, make_response, session
from app_01.ext import db
from app_01.models import Student, Grade

# 创建蓝图对象
blue = Blueprint('blue', __name__)


# 注册蓝图
def init_blue(app):
    app.register_blueprint(blueprint=blue)


# 主页
@blue.route('/')
def home():
    id = session.get("stu_id")
    if id:
        id = int(id)
        stu = Student.query.get(id)

        return render_template('home.html',user=stu)

    return render_template('home.html',user='游客')


# 登录
@blue.route('/login/')
def login():
    return render_template('login.html')


# 登录成功
@blue.route('/success/')
def success():
    students = Student.query.all()
    return render_template('login_success.html',students=students)


# 验证
@blue.route('/verify/', methods=['POST', 'GET'])
def verify():

    id = request.form.get("userid")
    s_name = request.form.get("username")

    # 判断学生id是否在数据库中存在
    stu = Student.query.filter(id).first()

    if stu:
        session['stu_name'] = s_name
        session['stu_id'] = id
        print('------------------------')
        print(session['stu_name'])
        print(session['stu_id'])

        students = Student.query.all()
        return render_template('login_success.html', stu=stu, students=students)
      
    return render_template('login.html',msg='输入的学生id不存在')


# 添加学生
@blue.route('/adduser/')
def adduser():
    grades = Grade.query.all()
    return render_template('adduser.html',grades=grades)

# 学生存入数据库
@blue.route('/saveuser/', methods=['POST','GET'])
def saveuser():
    stu = Student()
    s_name = request.form.get("s_name")
    s_grade = request.form.get("grade")
    stu.s_name = s_name

    g_id = db.session.query(Grade).filter(Grade.g_name == s_grade).first().id

    # 给学生的外键添加 班级id
    stu.s_grade = g_id
    # print(g_id)
    db.session.add(stu)
    db.session.commit()

    return '学生:{}--年级{}添加完成'.format(s_name,s_grade)


# 显示学生
@blue.route('/studentlist/')
def studentlist():

    # 逻辑删除
    students = Student.query.filter(Student.isdelete == False)

    return render_template('login_success.html',students=students)


# 显示班级
@blue.route('/delstu/')
def delgrade():
    grade = Grade.query.all()


@blue.route('/quit/')
def quit():
    if request.method == 'POST':
        session.pop('stu_id')
        session.pop('stu_name')
        return redirect(url_for('blue.home'))
    else:
        return redirect(url_for('blue.home'))


@blue.route('/modify/<int:stuid>')
def modify(stuid):
    pass
