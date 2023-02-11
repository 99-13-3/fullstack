
from flask import Flask, render_template, request, jsonify
import certifi
from pymongo import MongoClient
import jwt

app = Flask(__name__)

ca=certifi.where()
client = MongoClient('',tlsCAFile=ca)
db=client.db99

@app.route('/')
def home():
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=6000, debug=True)