from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import os
import sys
import click

from flask import Flask

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

login_manager = LoginManager(app)  # 实例化扩展类

login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


@app.cli.command()  # 注册为命令
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'TTYY751'
    movies = [
        {'id': '1001', 'title': '战狼2', 'year': '2017/7/27', 'country': '中国', 'type': '战争'},
        {'id': '1002', 'title': '哪吒之魔童降世', 'year': '2019/7/26', 'country': '中国', 'type': '动画'},
        {'id': '1003', 'title': '流浪地球', 'year': '2019/2/5', 'country': '中国', 'type': '科幻'},
        {'id': '1004', 'title': '复仇者联盟4', 'year': '2019/4/24', 'country': '美国', 'type': '科幻'},
        {'id': '1005', 'title': '红海行动', 'year': '2018/2/16', 'country': '中国', 'type': '战争'},
        {'id': '1006', 'title': '唐人街探案2', 'year': '2018/2/16', 'country': '中国', 'type': '喜剧'},
        {'id': '1007', 'title': '我不是药神', 'year': '2018/7/5', 'country': '中国', 'type': '喜剧'},
        {'id': '1008', 'title': '中国机长', 'year': '2019/9/30', 'country': '中国', 'type': '剧情'},
        {'id': '1009', 'title': '速度与激情8', 'year': '2017/4/14', 'country': '美国', 'type': '动作'},
        {'id': '1010', 'title': '西虹市首富', 'year': '2018/7/27', 'country': '中国', 'type': '喜剧'},
        {'id': '1011', 'title': '复仇者联盟3', 'year': '2018/5/11', 'country': '美国', 'type': '科幻'},
        {'id': '1012', 'title': '捉妖记2', 'year': '2018/2/16', 'country': '中国', 'type': '喜剧'},
        {'id': '1013', 'title': '八佰', 'year': '2020/08/21', 'country': '中国', 'type': '战争'},
        {'id': '1014', 'title': '姜子牙', 'year': '2020/10/01', 'country': '中国', 'type': '动画'},
        {'id': '1015', 'title': '我和我的家乡', 'year': '2020/10/01', 'country': '中国', 'type': '剧情'},
        {'id': '1016', 'title': '你好，李焕英', 'year': '2021/02/12', 'country': '中国', 'type': '喜剧'},
        {'id': '1017', 'title': '长津湖', 'year': '2021/09/30', 'country': '中国', 'type': '战争'},
        {'id': '1018', 'title': '速度与激情9', 'year': '2021/05/21', 'country': '中国', 'type': '动作'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(id=m['id'], title=m['title'], year=m['year'], country=m['country'], type=m['type'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


from flask import request, url_for, redirect, flash


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))
        title = request.form.get('title')  # 传入表单对应输入字段的name 值
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
            # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form['title']  # 传入表单对应输入字段的name 值
        year = request.form['year']
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回主页
        # 保存表单数据到数据库
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/search', methods=['POST'])
def search_movies():
    movies = None
    if request.method == 'POST':
        # 获取用户输入的电影名
        title = request.form.get('title')
        year = request.form.get('year')

        # 在数据库中查询电影
        movies = Movie.query.filter_by(title=title, year=year).all()

        # 渲染模板并将查询结果传递给模板
        return render_template('search.html', movies=movies)

    # 如果是 GET 请求，直接渲染模板
    return render_template('404.html')
