from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://songyuheon2750:2028sus300djr@cluster0.mcsffwd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://test:test@cluster0.15fhovx.mongodb.net/test", tlsCAFile=ca)
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
    
    return render_template('main_login_fail.html')
    


@app.route("/login", methods=["POST"])
def guestbook_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    print(id_receive,pw_receive)

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    all_users = list(db.mini_project.find({},{'_id':False}))

    id_existence=0
    for i in (all_users):
        if(i['id']==id_receive):
            if(i['pw']==int(pw_hash)):
                id_existence=1


    print(all_users)
    return jsonify({'msg': id_existence})



@app.route("/reviews", methods=["GET"])
def reviews():
    print('reviews')
    return render_template('./reviews.html')


@app.route("/login_success", methods=["GET"])
def login_success():
    print('login_success')
    return render_template('./main_login_success.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)


#==================================================================================
