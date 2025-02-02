from flask import session
import json
import os

USER_FILE = 'data/users.json'


# ユーザーデータをロード
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# ユーザーデータを保存
def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)


# ログインしているか確認
def is_login():
    return 'login' in session


# ログイン処理
def try_login(user, password):
    users = load_users()
    if user in users and users[user] == password:
        session['login'] = user
        return True
    return False


# ログアウト処理
def try_logout():
    session.pop('login', None)


# ユーザー登録処理
def add_user(user, password):
    users = load_users()
    if user in users:
        return False  # ユーザーがすでに存在する

    users[user] = password
    save_users(users)
    return True


# ログインユーザーを取得
def get_user():
    return session.get('login', 'not login')
