from flask import Flask, request, jsonify
import pymysql
from db_config import db_info

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask 서버 작동 중!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 외부 접속 가능