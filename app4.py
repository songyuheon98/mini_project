from flask import Flask, render_template
import requests
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb://1sparta:test@ac-j2cpxd6-shard-00-00.pyhzwix.mongodb.net:27017,ac-j2cpxd6-shard-00-01.pyhzwix.mongodb.net:27017,ac-j2cpxd6-shard-00-02.pyhzwix.mongodb.net:27017/?ssl=true&replicaSet=atlas-2769jq-shard-0&authSource=admin&retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def review_page():
    # 서울시 도서관 API로부터 데이터 가져오기
    api_url = "http://openapi.seoul.go.kr:8088/4a7869566f73656138317157546a58/json/SeoulLibraryBookRentNumInfo/1/20/"
    response = requests.get(api_url)
    data = response.json()
    rows = data['SeoulLibraryBookRentNumInfo']['row']

    # 책 정보를 가져와서 book_info 에
    book_info = {
        'imageUrl': 'URL_OF_YOUR_BOOK_IMAGE',
        'author': rows[0]['AUTHOR']}
    
    
    # MongoDB에 데이터 저장
    review_data = {
        'username': '사용자닉네임',
        'review': '사용자 리뷰 내용'
    }
    db.reviews.insert_one(review_data)
    
    return render_template('index.html', book_info=book_info)

if __name__ == '__main__':
    app.run(debug=True)
