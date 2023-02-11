
from flask import Flask, render_template, request, jsonify
import jwt

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:<password>@cluster0.qdjzhnz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta




app = Flask(__name__)



@app.route('/')
def home():
   return render_template('index.html')

# -----글쓰기 페이지로 이동
def post_write():

    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = flow99.find_one({"id": payload['id']})
        object_id_receive = request.form['object_id_give']

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

    게시글묶음 = list(db.gugupost.find({}, {'_id':False}))

    return jsonify({'poting_list': 게시글묶음})

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


#
# @app.route('/comment', methods=["POST"])
# def post_comment():
#     member_id = request.form['member_key']
#     comment_receive = request.form['comment_give']
#     # comment_id = request.form['comment_key']
#
#     lists = list(db.comment.find({}, {'_id': False}))
#     count = len(lists) + 1
#     doc = {
#        'member_id' : member_id,
#        'comment' : comment_receive,
#        # 'comment_id' : comment_id,
#        'Num' : count
#
#     }
#     db.comment.insert_one(doc);
#     return jsonify({'result': 'success', 'msg': '댓글 등록 완료'})
#
# @app.route("/comment", methods=["GET"])
# def get_comment():
#     comment_list = list(db.comment.find({}, {'_id': False}))
#     return jsonify({'comments': comment_list})
#
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
   app.run('0.0.0.0', port=5000, debug=True)