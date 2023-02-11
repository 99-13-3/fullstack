
from flask import Flask, render_template, request, jsonify
import jwt

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.phw7iou.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta



app = Flask(__name__)



# @app.route('/')
# def home():
#    return render_template('index.html')
#
# # -----글쓰기 페이지로 이동
# @app.route('/write', )
# def post_upload():
#    memberid = db.fullstack.find_one({'_id:False'})
#    return render_template('indedx.html', memberid = memberid)
#
# # -----글쓰기 완료 기능
# @app.route('/write/posting', method=["GET", "POST"])
def post_upload_done():

      title_receive = request.form['title_give']
      postdesc_receive = request.form['postdesc_give']
      memberid_receive = request.form['memberid_give']

      post_list = list(db.fullstack.find({}, {'_id' : False}))
      post_id = len(post_list) + 1

      doc = {
         'postid' : post_id,
         'title' : title_receive,
         'postdesc' : postdesc_receive,
         'memberid' : memberid_receive,
         'done' : 0
      }

      db.fullstack.insert_one(doc)

      return jsonify({'msg': '게시글 등록 완료!'})


# -----게시글 수정 기능
# @app.route("/posting", method =["PUT"])
# def post_update():
#    memberid = db.fullstack.find_one({'_id:False'})
#    postid = db.fullstack.find_one({'_id':False})
#    return render_template('index.html', memberid = memberid, postid = postid)


# -----게시글 삭제 기능
# @app.route("/posting", method=["DELETE"])
# def post_remove():
#
#    remove_receive = request.form['remove_give']
#    db.fullstack.delete_one({'postid' : int(remove_receive)})
#
#    return jsonify({'msg' : '게시글 삭제 완료!'})





if __name__ == '__main__':
   app.run('0.0.0.0', port=6000, debug=True)