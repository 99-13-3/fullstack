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
   token_receive = request.cookies.get('mytoken')
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
@app.route('/login', methods=["POST"])
def login():
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
@app.route('/signin', methods = ["POST"])
def sign_in(): 
      id_receive = request.form['id_give']
      pw_receive = request.form['pw_give']
      email_receive = request.form['email_give']

      user = db.flow99.find_one({'id': id_receive})
      print(user)
      if user is None:
         pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
         db.flow99.insert_one({'id': id_receive, 'pw': pw_hash, 'email': email_receive})
         return jsonify({'result': 'success'})
      else:
         return jsonify({'msg': '이미 존재하는 아이디 입니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)