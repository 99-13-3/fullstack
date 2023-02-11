from flask import Flask, render_template, request, jsonify
import certifi
from pymongo import MongoClient

app = Flask(__name__)

ca=certifi.where()
client = MongoClient('mongodb+srv://webuser:webuser@cluster0.whzzs4t.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db=client.db99

@app.route('/')
def home():
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)