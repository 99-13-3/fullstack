import hashlib

from bson import ObjectId
from flask import Flask, render_template, request, jsonify, session
# import certifi
from pymongo import MongoClient

import jwt
import datetime

app = Flask(__name__)
ca=certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.lreiodk.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db=client.info

SECRET_KEY = 'FLOW'

# 메인 화면
@app.route('/')
def home():
   token_receive = request.cookies.get('myToken')
   print(token_receive)

   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.info.find_one({"id": payload['id']})
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
   
   result = db.info.find_one({'id': id_receive, 'pw':pw_hash})
   
   if result is not None:
      payload = {
         'id': id_receive,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=18000)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      return jsonify({'result':'success', 'tokens':token})
   else:
      return jsonify({'result':'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입

@app.route('/register')
def register_after():
      return render_template('loginAfter.html')

@app.route('/register', methods = ["POST"])
def register():
      id_receive = request.form['id_give']
      pw_receive = request.form['pw_give']

      user = db.info.find_one({'id': id_receive})
      if user is None:
         pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
         db.info.insert_one({'id': id_receive, 'pw': pw_hash})
         return jsonify({'result': 'success', "msg":"회원가입이 완료됐습니다."})
      else:
         return jsonify({'msg': '이미 존재하는 아이디 입니다.'})

      
# @app.route('/content/post_id', methods=['GET'])
# def content_show():
#    titles=list(db.포스트.find_one({},{'_id':False}))
#    post_desc=list(db.포스트.find_one({},{'_id':False}))
#    post_key=list(db.포스트.find_one({},{'_id':False}))
#    comments=list(db.코멘트.find_one({},{'_id':False}))
#    member_key=list(db.유저정보.find_one({},{'_id':False}))
#    return jsonify({'comment_list':comments, 'post_desc':post_desc,
#                    'member_id': member_key, 'post_id': post_key,
#                    'post_title': titles})

# -----글쓰기 페이지로 이동
def post_write():

token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('editorTemplate.html')


    except jwt.ExpiredSignatureError:
        return render_template('index.html', result='fail', msg='만료된 토큰')
    except jwt.exceptions.DecodeError:
        return render_template('login.html', result='fail', msg='로그인 후 이용해 주십시오.')


# -----게시글 올리기
@app.route('/posting', methods=["POST"])
def post_done():

    post_title = request.form['제목']
    post_desc = request.form['내용']
    member_id = request.form['member_key']

    post_list = list(db.gugupost.find({}, {'_id': False}))
    post_id = post_list[len(post_list)-1]['num']

    doc = {
            'post_id': post_id,
            'post_title': post_title,
            'post_desc': post_desc,
            'member_id': member_id
        }

    db.gugupost.insert_one(doc)

    return jsonify({'posting_msg': '게시글 등록 완료!'})


# ----- 게시글리스트
@app.route("/posting/list", methods=["GET"])
def post_list():

    posting_list = list(db.gugupost.find({}, {'_id':False}))

    return jsonify({'posting_list': posting_list})

# ------ 게시글 좋아요/싫어요
@app.route("/posting/like", methods=["GET"])
def post_like():
token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        post_id = int(request.form['post_id'])
        user_info = flow99.find_one({"id":payload['id']})

        doc = {
        'post_id' : post_id,
        'member_id' : user_info['id']
        }
        like = db.gugulike.find_one(doc)
        if like is None:
            db.gugulike.insert_one(doc)
        else:
            db.gugulike.delete_one(doc)

        return jsonify({'post_like_msg':'게시글 좋아요 완료'})

    except jwt.ExpiredSignatureError:
        return render_template('lecture.html', result='fail', msg='만료된 토큰')

    except jwt.exceptions.DecodeError:
        return render_template('login.html', result='fail', msg='로그인 후 이용해 주세요.')

# -----게시글 수정 기능
@app.route("/posting/update", methods =["POST"])
def post_update():
    member_id = ['member_key']
    update_receive = ['update_give']
    db.gugupost.update_one({'memberid': member_id}, {'$set': {'post_desc': str(update_receive)}})

   return jsonify({'post_up_msg': '게시글 수정 완료'})

# -----게시글 삭제 기능
@app.route("/posting/delete", methods=["POST"])
def post_remove():

token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = member_db.find_one({"id": payload['id']})
    object_id_receive = request.form['object_id_give']
    writer = db.gugupost.find_one({'_id': ObjectId(object_id_receive)})['member_id']


    if user_info['member_id'] == writer:
        db.comment.delete_one({'_id': ObjectId(object_id_receive)})
        return jsonify({'post_rm_msg': '게시글 삭제 완료'})
    else:
        return jsonify({'msg': '다른 사람이 쓴 글은 삭제할 수 없습니다.'})

    except jwt.ExpiredSignatureError:

        return render_template('editorTemplate.html', result ='fail',msg='만료된 토큰')

    except jwt.exceptions.DecodeError:

        return render_template('login.html', result='fail', msg='로그인 후 이용해 주세요.')


@app.route('/comment', methods=["POST"])
def post_comment():
    token_receive = request.cookies.get('mytoken')
    try:
        comment_id = request.form['comment_id']
        comment_receive = request.form['comment']
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.info.find_one({'id': payload['id']}, {'_id': 0})
        lists = list(db.info.find({}, {'_id': False}))
        count = lists[len(lists)-1]['num']


        doc = {
            'id':count,
            'comment_id': comment_id,
            'member_id' : userinfo['id'],
            'comment' : comment_receive,
        }
        db.comment.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '댓글 등록 완료'})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})

    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route("/comment", methods=["GET"])
def get_comment():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


#     comment = request.form['comment_give']
#     # comment_id = list(포스트db.find{}, {'_id':False}))
#     # check = request.form['boolean']

#     # lists = list(db.comment.find({}, {'_id': False}))
#     # count = len(lists) + 1
#     doc = {
#        'comment' : comment,
#         # 'check': check,
#        # 'comment_id' : comment_id,
#        # 'Num' : count

#     }
#     db.comment.insert_one(doc)
#     return jsonify({'result': 'success', 'msg': '댓글 등록 완료'})


# @app.route("/comment", methods=["GET"])
# def get_comment():
#     comment_list = list(db.comment.find({}, {'_id': False}))
#     return jsonify({'comments': comment_list})

# @app.route('/comment/update', methods=["POST"])
# def post_comment_update():
#    member_id = request.form['member_id']
#    update_receive = request.form['update_give']
#    db.comment.update_one({'_id': member_id}, {'$set': {'comment': str(update_receive)}})
#    return jsonify({'msg': '댓글 수정'})

# @app.route('/review/delete', methods=["POST"])
# def post_comment_delete():
#     token_receive = request.cookies.get('mytoken')
#

# 댓글 수정
@app.route('/comment/update', methods=["POST"])
def post_comment_update():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.find_one({"id": payload['id']})

        object_id_receive = request.form['object_id_give']
        update_receive = request.form['update_give']
        writer = db.comment.find_one({'_id': ObjectId(object_id_receive)})['member_id']

        if user_info['member_id'] == writer:
            db.comment.update_one({'_id': ObjectId(object_id_receive)}, {'$set': {'comment': str(update_receive)}})
            return jsonify({'msg': '댓글 수정'})
        else:
            return jsonify({'msg': '다른 사람이 쓴 댓글은 수정할 수 없습니다.'})
    except jwt.ExpiredSignatureError:

        return render_template('lecture.html', result="fail", msg="만료된 토큰")
    except jwt.exceptions.DecodeError:
        return render_template('lecture.html', result="fail", msg="존재하지 않는 아이디")


# 댓글지우기
@app.route('/comment/delete', methods=["POST"])
def post_comment_delete():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.comment.find_one({"id": payload['id']})
        object_id_receive = request.form['object_id_give']
        writer = db.comment.find_one({'_id': ObjectId(object_id_receive)})['member_id']
        if user_info['member_id'] == writer:
            db.comment.delete_one({'_id': ObjectId(object_id_receive)})
            return jsonify({'msg': '댓글 삭제'})
        else:
            return jsonify({'msg': '다른 사람이 쓴 글은 삭제할 수 없습니다.'})
    except jwt.ExpiredSignatureError:
        return render_template('lecture.html', result="fail", msg="만료된 토큰")
    except jwt.exceptions.DecodeError:
        return render_template('lecture.html', result="fail", msg="존재하지 않는 아이디")

# 좋아요 싫어요

@app.route('/comment/like', methods=['GET'])
def show_comment_like():
    comment_list = list(db.comment.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'comments': comment_list})


@app.route('/comment/like', methods=['POST'])
def like_comment():
    comment_receive = request.form['comment_give']
    target_like = db.comment.find_one({'comment': comment_receive})
    current_like = target_like['check']
    new_like = current_like + 1
    db.comment.update_one({'comment': comment_receive}, {'$set': {'check': new_like}})
    return jsonify({'msg': '좋아요 완료!'})

@app.route('/comment/dislike', methods=['POST'])
def dislike_comment():
    comment = request.form['comment_give']
    target_dislike = db.comment.find_one({'comment': comment})
    current_like = target_dislike['check']
    new_like = current_like - 1
    db.comment.update_one({'comment': comment}, {'$set': {'check': new_like}})
    return jsonify({'msg': '싫어요 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)