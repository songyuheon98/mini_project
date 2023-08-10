from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

import certifi

ca=certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.f7rylqz.mongodb.net/?retryWrites=true&w=majority')
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
    return render_template('join.html')

@app.route('/api/join', methods=['POST'])
def api_register():
    print('api_register')
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    if(id_receive == "" or pw_receive == "" or nickname_receive == ""):
        return jsonify({'result': '항목이 누락되었습니다.'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    print('+++++++++++++++++++++')
    print(id_receive,pw_receive,nickname_receive)

    db.mini_project.insert_one({
        'id': id_receive,
        'pw': pw_hash, 
        'nick': nickname_receive
    })

    return jsonify({'result': 'success'})


@app.route('/save_comment', methods=['POST'])
def save_comment():
    print('save_commnet')
    title_receive=request.form['book_title']
    nick_name_receive = request.form['nick_name']
    user_comment_receive = request.form['user_comment']

    print(title_receive,nick_name_receive,user_comment_receive)
    if(nick_name_receive == "" or user_comment_receive == "" ):
        return jsonify({'result': '항목이 누락되었습니다.'})
    
    db.mini_project.insert_one({
        'title': title_receive,
        'nick_name': nick_name_receive,
        'user_comment_receive':user_comment_receive
    })

    return jsonify({'result': 'success'})

@app.route("/comments_show", methods=["GET"])
def comments_show():
    print(comments_show)
    all_comments_data = list(db.mini_project.find({},{'_id':False}))
    return jsonify({'result': all_comments_data})

@app.route("/reviews", methods=["GET"])
def reviews():
    print('reviews')
    return render_template('./reviews.html')

@app.route("/main_login_fail", methods=["GET"])
def main_login_fail():
    print('main_login_fail')
    return render_template('./main_login_fail.html')


@app.route("/main_login_success", methods=["GET"])
def login_success():
    print('login_success')
    return render_template('./main_login_success.html')

@app.route('/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']    
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.mini_project.find_one({'id': id_receive, 'pw': pw_hash})
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
            'nickname': result['nick']
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token })
        
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    