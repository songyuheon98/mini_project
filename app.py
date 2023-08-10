from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://test:test@cluster0.15fhovx.mongodb.net/test", tlsCAFile=ca)
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



@app.route('/join', methods=['GET'])
def register():
    return render_template('join.html')

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/join', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.mini_project.insert_one({
        'id': id_receive,
        'pw': pw_receive, 
        'nick': nickname_receive
        })

    return jsonify({'result': 'success'})

@app.route('/')
def home():
    return render_template('main.html')

@app.route("/login", methods=["POST"])
def guestbook_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    print(id_receive,pw_receive)

    # all_users = list(db.users.find({},{'_id':False}))

    # doc ={
    #     'name':name_receive,
    #     'comment':comment_receive
    # }
    # db.fan.insert_one(doc)
    # doc = {'id':'bobby','pw':21} 

    # db.mini_project.insert_one(doc)

    all_users = list(db.mini_project.find({},{'_id':False}))

    id_existence=0
    for i in (all_users):
        if(i['id']==id_receive):
            if(i['pw']==int(pw_receive)):
                id_existence=1


    print(all_users)
    return jsonify({'msg': id_existence})

@app.route("/login", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({},{'_id':False}))

    return jsonify({'result': all_comments})

@app.route("/reviews", methods=["GET"])
def reviews():
    

    return 


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
