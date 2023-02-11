
from flask import Flask, render_template, request, jsonify

# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.phw7iou.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta

import jwt

app = Flask(__name__)



@app.route('/')
def home():
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=6000, debug=True)