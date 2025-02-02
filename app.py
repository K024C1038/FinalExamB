from flask import Flask, redirect, url_for, session, render_template, request
import os, json, datetime
import bbs_login  # ログイン管理モジュール
import bbs_data  # データ入出力用モジュール

app = Flask(__name__)
app.secret_key = 'U1sNMeUkZSuuX2Zn'


# 掲示板のメイン画面
@app.route('/')
def index():
    if not bbs_login.is_login():
        return redirect('/login')
    return render_template('index.html',
                           user=bbs_login.get_user(),
                           data=bbs_data.load_data())


# ログイン画面
@app.route('/login')
def login():
    return render_template('login.html')


# サインアップ画面
@app.route('/signup')
def signup():
    return render_template('signup.html')


# ログイン処理
@app.route('/try_login', methods=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')
    if bbs_login.try_login(user, pw):
        return redirect('/')
    return show_msg('ログインに失敗しました')


# サインアップ処理
@app.route('/try_signup', methods=['POST'])
def try_signup():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')

    if not user or not pw:
        return show_msg("ユーザー名とパスワードを入力してください")

    if bbs_login.add_user(user, pw):
        return show_msg("サインアップ成功！ログインしてください")
    else:
        return show_msg("そのユーザー名はすでに存在します")


# ログアウト処理
@app.route('/logout')
def logout():
    bbs_login.try_logout()
    return show_msg('ログアウトしました')


# 書き込み処理
@app.route('/write', methods=['POST'])
def write():
    if not bbs_login.is_login():
        return redirect('/login')

    ta = request.form.get('ta', '')
    if ta == '':
        return show_msg('書込が空でした。')

    bbs_data.save_data_append(user=bbs_login.get_user(), text=ta)
    return redirect('/')


# メッセージを表示
def show_msg(msg):
    return render_template('msg.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
