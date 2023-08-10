from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient('mongodb+srv://songyuheon2750:2028sus300djr@cluster0.mcsffwd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;

import hashlib



@app.route('/')
def home():
    return render_template('main_login_fail.html')
    


@app.route('/join', methods=['GET'])
def register():
    print('join')
    return render_template('join.html')

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/join', methods=['POST'])
def api_register():
    print('api_register')
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print(pw_hash)

    db.mini_project.insert_one({
        'id': id_receive,
        'pw': pw_hash, 
        'nick': nickname_receive
        })

    return jsonify({'result': 'success'})


@app.route("/login", methods=["POST"])
def guestbook_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    print(id_receive,pw_receive)

    #pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    all_users = list(db.mini_project.find({},{'_id':False}))

    print(all_users)

    id_existence=0
    for i in (all_users):
        if(i['id']==id_receive):
            if(i['pw']==int(pw_receive)):
                id_existence=1


    print(all_users)
    return jsonify({'msg': id_existence})



@app.route("/reviews", methods=["GET"])
def reviews():
    print('reviews')
    return render_template('./reviews.html')

@app.route("/main_login_fail", methods=["GET"])
def main_login_fail():
    print('main_login_fail')
    return render_template('./main_login_fail.html')


@app.route("/login_success", methods=["GET"])
def login_success():
    print('login_success')
    return render_template('./main_login_success.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://sparta:test@cluster0.pggigqp.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dbsparta_plus_week4

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


@app.route('/')
def home():
    return render_template('main.html')

    


@app.route('/register')
def register():
    return render_template('join.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
            'nickname': result['nick']
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token })
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    