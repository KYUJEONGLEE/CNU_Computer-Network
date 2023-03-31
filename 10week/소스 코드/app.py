import json
import urllib
from flask import Flask, Blueprint, render_template, request, redirect

endpoint = 'http://localhost:8080/pastebin/api'

app = Flask(__name__)

bp = Blueprint('mybp', __name__,
               static_folder='static',
               static_url_path='/pastebin/static',
               template_folder='templates',
               url_prefix='/pastebin')

@bp.route(f'/', methods=['GET'])
@bp.route('/index.html', methods=['GET'])
def get_index():
    count_users = 0
    paste_list = {}

    url = f'{endpoint}/users/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_users = len(data)

    count_pastes = 0
    url = f'{endpoint}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)

    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('index.html',
                           count_users=count_users,
                           count_pastes=count_pastes)

@bp.route('/createuser', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        url = f'{endpoint}/users/'
        data = {'username': request.form['username'],
                'password': request.form['password']}
        headers = {'Accept': 'application/json',
                   'Content-type':'application/json'}
        method = 'POST'
        data = json.dumps(data).encode('utf-8')

        req = urllib.request.Request(url=url,
                                     data=data,
                                     headers=headers,
                                     method=method)


        urllib.request.urlopen(req)

        return redirect('/pastebin/')

    if request.method == 'GET':
        return render_template('createuser.html')

@bp.route('/createpaste', methods=['POST', 'GET'])
def create_paste():
    if request.method == 'POST':
        user_data = {'username': request.form['username'],
                     'password': request.form['password']}

        paste_data = {'title': request.form['title'],
                      'content': request.form['content']}

        url = f'{endpoint}/users/{user_data["username"]}/pastes/?password={user_data["password"]}'

        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}
        method = 'POST'
        data = json.dumps(paste_data).encode('utf-8')

        req = urllib.request.Request(url=url,
                                     data=data,
                                     headers=headers,
                                     method=method)

        urllib.request.urlopen(req)

        return redirect('/pastebin/')

    if request.method == 'GET':
        return render_template('createpaste.html')
from markupsafe import escape

@bp.route('/getpaste/<username>/', methods=['GET'])
def get_paste(username):
    count_pastes = 0
    paste_list = {}

    username = escape(username)
    url = f'{endpoint}/users/{username}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)

    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)
        for i in range(count_pastes):
            title = data[i]['title']
            content = data[i]['content']
            paste_list[title] = content

    return render_template('getpaste.html',
                            count_pastes=count_pastes,
                            username=username,
                            paste_list=paste_list)

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host="localhost", port="8890", debug=True)
