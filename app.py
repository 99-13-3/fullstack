
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.phw7iou.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import jwt

app = Flask(__name__)



@app.route('/')
def home():
   return render_template('index.html')


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
    db.comment.insert_one(doc);
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

@app.route('/review/delete', methods=["POST"])
def post_comment_delete():
    member_id = request.form['member_id']
    db.comment.delete_one({'_id': member_id})
    return jsonify({'msg': '댓글 삭제'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)