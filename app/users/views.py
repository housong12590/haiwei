from . import users as app
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.where('username', username).first()
    if user is None:
        flash('当前用户不存在,请联系管理员!')
        return render_template('users/login.html', username=username, password=password)
    if user.password != password:
        flash('登录密码错误!')
        return render_template('users/login.html', username=username, password=password)
    login_user(user)
    return redirect(url_for('docker.index'))


@app.route('/index')
@login_required
def index():
    _users = User.all()
    return render_template('users/index.html', users=_users)


@app.route('/users/<user_id>', methods=['GET', 'POST'])
@app.route('/users', methods=['GET', 'POST'])
def users(user_id=None):
    if request.method == 'GET':
        user = None
        if user_id:
            user = User.find(user_id)
        return render_template('users/users.html', user=user)
    if user_id:
        user = User.find(user_id)
    else:
        user = User()
    user.username = request.form.get('username')
    user.nickname = request.form.get('nickname')
    user.password = request.form.get('password')
    user.mobile = request.form.get('mobile')
    user.save()
    return redirect(url_for('users.index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
