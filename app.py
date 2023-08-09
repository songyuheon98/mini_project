from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://songyuheon2750:2028sus300djr@cluster0.mcsffwd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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


#==================================================================================
