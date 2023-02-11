import hashlib
from flask import Flask, render_template, request, jsonify, session
import certifi
from pymongo import MongoClient
import jwt
import datetime

app = Flask(__name__)

ca=certifi.where()
client = MongoClient('',tlsCAFile=ca)
db=client.flow99

SECRET_KEY = 'FLOW'
# token = jwt.encode({"user_id":user_id},SECRET,algorithm="HS256")

# 메인 화면
@app.route('/')
def home():
   token_receive = request.cookies.get('mytoken')
   print(token_receive)
   
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.flow99.find_one({"member_id": payload['member_id']})
      return render_template('index.html', user_id=user_info["member_id"])
   except jwt.ExpiredSignatureError:
      return render_template('index.html')
   except jwt.exceptions.DecodeError:
      return render_template('index.html')

# 로그인      
@app.route('/login', methods=["POST"])
def login():
   member_key = request.form['id']
   pw_receive = request.form['pw']
   
   pw =hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
   
   result = db.flow99.find_one({'member_id': member_key, 'pw':pw})
   
   if result is not None:
      payload = {
         'member_id': member_key,
         'exp': datetime.datetime.utcnow()
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      return jsonify({'result':'success', 'token':token})
   else:
      return jsonify({'result':'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
   # request.args.get("msg")은 받은 내용을 json형식의 데이터로 리턴하기 위해 사용
   
# 회원가입 API    
@app.route('/sign_in', methods = ["POST"])
def sign_in(): 
      member_key = request.form['id_name']
      pw_receive = request.form['pw_set']

      user = db.flow99.find_one({'member_id': member_key})
      if user is None:
         pw = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
         db.user.insert_one({'member_id': member_key, 'pw': pw})
         return jsonify({'result': 'success'})
      else:
         return jsonify({'msg': '이미 존재하는 아이디 입니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=6000, debug=True)