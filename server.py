from flask import Flask,request,render_template,url_for,session,flash,redirect
from urllib.parse import quote
import Manage
app = Flask(__name__)
app.secret_key='1232353141353241'

@app.route('/', methods=['GET','POST'])#山寨版Google首页
def home():
    if request.method=='GET':
        return render_template('index.html')
    else:
        print('wh')
        #return '<script>window.location.href=\'
        #https://www.google.com.hk/search?q='+quote(request.form['search'])+'\'</script>'
        if(request.form['s']=='search'):
            print('a')
            return redirect('http://www.google.com.hk/search?q='+quote(request.form['search']),302)
        else:
            print('b')
            return redirect('http://www.google.com.hk/search?newwindow=1&hl=zh-TW&source=hp&q='+quote(request.form['search'])+'&btnI=1',302)

@app.route('/login', methods=['GET'])#表单，模拟登录
def login_form():
    if 'user' in session:#好像没用
        return redirect('/userPage',302)
    return render_template('login.html',bad='n')
@app.route('/login', methods=['POST'])
def login():
    # 需要从request对象读取表单内容：
    if request.form['password']=='password':
        session['user']=request.form['username']
        return redirect('/userPage',302)
    else:
        return render_template('login.html',bad='y')

@app.route('/userPage')
def userPage():
    if 'user' in session:
        return render_template('userGoodbye.html',cont=session['user'])#jinja2生成网页
    else:
        return render_template('login.html',bad='u')

@app.route('/logout')
def logout():
    if session['user']:
        session.pop('user',None)
    return redirect('/',302)

if __name__ == '__main__':
    app.run()
