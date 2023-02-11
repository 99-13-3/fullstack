
from flask import Flask, render_template, request, jsonify
import jwt

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.phw7iou.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta



app = Flask(__name__)



@app.route('/')
def home():
   return render_template('index.html')

@app.route('/posting')
def post_upload():

   title_receive = request.form['title_give']
   postdesc_receive = request.form['postdesc_give']
   postid_receive = request.form['postid_give']

   doc = {
      'title' : title_receive,
      'postdesc' : postdesc_receive,
      'postid' : postid_receive
   }

   db.fullstack.insert_one(doc)

   return jsonify({'msg': '게시글 등록 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=6000, debug=True)