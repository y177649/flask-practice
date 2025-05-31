from flask import Flask
from flask import render_template

app = Flask(__name__)


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

@app.route("/H")
def index():
    return render_template('index.html')

