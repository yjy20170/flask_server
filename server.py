from flask import Flask,request,render_template,url_for,session,flash
from Manage import manage
from urllib.parse import quote
app = Flask(__name__)
app.secret_key='1232353141353241'
@app.route('/', methods=['GET', 'POST'])#山寨版Google首页
def home():
    if request.method=='GET':
        return render_template('index.html')
    else:
        print(quote(request.form['search']))
        return '<script>window.location.href=\'\
            https://www.google.com.hk/search?q='+quote(request.form['search'])+'\'</script>'

@app.route('/signin', methods=['GET'])#表单，模拟登录
def signin_form():
    if 'user' in session:
        print(session['user'])
        return '<h3>Hello, '+session['user']+'!</h3>'
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''
@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['password']=='password':
        session['user']=request.form['username']
        return '<h3>Hello, '+request.form['username']+'!</h3>'
    return '<h3>Bad username or password.</h3>'

@app.route('/hello')
@app.route('/hello/')
@app.route('/hello/<name>')
def ind(name='ERROR'):
    return render_template('hello.html',cont=manage(name))#jinja2生成网页

if __name__ == '__main__':
    app.run()
