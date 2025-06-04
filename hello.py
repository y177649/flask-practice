#環境変数設定と起動コマンド
#export FLASK_APP=hello.py
#flask run --debug

from flask import Flask
from flask import render_template , request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_bootstrap import Bootstrap 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    body = db.Column(db.String(300),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(128))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#最も標準的なルーティング
@app.route("/")
def hello():
    return "Hello"


#returnの中にHTMLのタグを指定して表示する
@app.route("/A")
def hello_A():
    return "<h1>Hello, A</h1>"


#htmlという変数に文字列をHTML形式で入力、htmlをreturnに渡すとHTMLの形式で出力される
html="""
<h1>サンプルHTML</h1>
<ul>
    <li>リスト１</li>
    <li>リスト２</li>
    <li>リスト３</li>
</ul>
"""

@app.route("/B")
def hello_B():
    return html


#URLを変数として入力して、入力に応じて出力を変化させる
@app.route("/C/<city>")
def hello_C_city(city):
    return f"Hello, C ,{ city }"


#render_template関数を使ってhello.htmlの内容を出力
@app.route("/D")
def hello_D():
    return render_template('hello.html')


#render_template関数で指定したファイルにURLで取得したpyの変数を渡す
@app.route("/E/<count>")
def hello_E(count):
    return render_template('hello2.html',count=count)



#render_template関数で指定したファイルにpyのリストを渡す
bullets = [
    '箇条書き1',
    '箇条書き2',
    '箇条書き3',
    '箇条書き4',
    '箇条書き5',
    '箇条書き6',
]

@app.route("/F") #今回は入力を受け取らないのでここは無し
def hello_F(): #今回は入力を受け取らないのでここも無し
    return render_template('hello3.html',bullets=bullets)


@app.route("/G")
def original():
    return render_template('original.html')

@app.route("/H",methods=['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html',posts=posts)


@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password =request.form.get('password')

        user = User(username=username,password=generate_password_hash(password,method='pbkdf2:sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password =request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password,password):
            login_user(user)
            return redirect('/H')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/create",methods=['GET','POST'])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get('title')
        body =request.form.get('body')

        post = Post(title=title,body=body)

        db.session.add(post)
        db.session.commit()
        return redirect('/H')
    else:
        return render_template('create.html')

@app.route("/<int:id>/edit",methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get(id)
    if request.method == "GET":
        return render_template('edit.html',post=post)

    else:
        post.title = request.form.get('title')
        post.body =request.form.get('body')

        db.session.commit()
        return redirect('/H')

@app.route("/<int:id>/delete",methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/H')