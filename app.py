import hashlib
from flask import Flask, render_template, request, jsonify, session
import certifi
from pymongo import MongoClient
import jwt
import datetime

app = Flask(__name__)
ca=certifi.where()
client = MongoClient('mongodb+srv://ryu:junyeong@cluster0.mr8szun.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db=client.flow99

SECRET_KEY = 'FLOW'

# 메인 화면
@app.route('/')
def home():
   token_receive = request.cookies.get('myToken')
   print(token_receive)
   
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"id": payload['id']})
      return render_template('index.html', user_id=user_info["id"])
   except jwt.ExpiredSignatureError:
      return render_template('index.html')
   except jwt.exceptions.DecodeError:
      return render_template('index.html')

# 로그인      
@app.route('/login')
def login_get():
   return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
   id_receive = request.form['id_check']
   pw_receive = request.form['pw_check']
   
   pw_hash =hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
   
   result = db.flow99.find_one({'id': id_receive, 'pw':pw_hash})
   
   if result is not None:
      payload = {
         'id': id_receive,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=18000)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      return jsonify({'result':'success', 'tokens':token})
   else:
      return jsonify({'result':'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
   # request.args.get("msg")은 받은 내용을 json형식의 데이터로 리턴하기 위해 사용
   
# 회원가입 API
@app.route('/register')
def register_after():
      return render_template('loginAfter.html')
    
@app.route('/register', methods = ["POST"])
def register(): 
      id_receive = request.form['id_give']
      pw_receive = request.form['pw_give']
      # email_receive = request.form['email_give']

      user = db.flow99.find_one({'id': id_receive})
      print(user)
      if user is None:
         pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
         db.flow99.insert_one({'id': id_receive, 'pw': pw_hash})
         return jsonify({'result': 'success', "msg":"회원가입이 완료됐습니다."})
      else:
         return jsonify({'msg': '이미 존재하는 아이디 입니다.'})

@app.route('/comment', methods=["POST"])
def post_comment():
    member_id = request.form['member_key']
    comment_receive = request.form['comment_give']
    # comment_id = request.form['comment_key']

    lists = list(db.comment.find({}, {'_id': False}))
    count = len(lists) + 1
    doc = {
       'member_id' : member_id,
       'comment' : comment_receive,
       # 'comment_id' : comment_id,
       'Num' : count
    }
    db.comment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글 등록 완료'})

@app.route("/comment", methods=["GET"])
def get_comment():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route('/comment/update', methods=["POST"])
def post_comment_update():
   member_id = request.form['member_id']
   update_receive = request.form['update_give']
   db.comment.update_one({'_id': member_id}, {'$set': {'comment': str(update_receive)}})
   return jsonify({'msg': '댓글 수정'})

# @app.route('/review/delete', methods=["POST"])
# def post_comment_delete():
#     token_receive = request.cookies.get('mytoken')
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = member_db.find_one({"id": payload['id']})
#     object_id_receive = request.form['object_id_give']
#     writer = db.comment.find_one({'_id': ObjectId(object_id_receive)})['member_id']
#     if user_info['member_id'] == writer:
#         db.comment.delete_one({'_id': ObjectId(object_id_receive)})
#         return jsonify({'msg': '리뷰 삭제'})
#     else:
#         return jsonify({'msg': '다른 사람이 쓴 글은 삭제할 수 없습니다.'})
#     except jwt.ExpiredSignatureError:
#         return render_template('댓글.html', result="fail", msg="만료된 토큰")
#     except jwt.exceptions.DecodeError:
#         return render_template('댓글.html', result="fail", msg="존재하지 않는 아이디")



if __name__ == '__main__':
   app.run('0.0.0.0', port=8000, debug=True)