from flask import Flask, request, jsonify
import pymysql
from db_config import db_info
from datetime import datetime, timedelta

app = Flask(__name__)

# 기본 테스트 라우터
@app.route('/')
def home():
    return "Flask 서버 작동 중!"


# ----------------------------------------
# 📦 ITEMLOCATION 관련 API
# ----------------------------------------

@app.route('/items', methods=['GET'])
def get_items():
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ITEMLOCATION")
            items = cursor.fetchall()
        return jsonify(items)
    finally:
        conn.close()


@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = data.get('item')
    location = data.get('location')
    if not item or not location:
        return jsonify({'status': 'fail', 'message': '필수 정보 누락'}), 400
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO ITEMLOCATION (item, location) VALUES (%s, %s)"
            cursor.execute(sql, (item, location))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


@app.route('/items/<string:item>', methods=['PUT'])
def update_item(item):
    data = request.get_json()
    new_location = data.get('location')
    if not new_location:
        return jsonify({'status': 'fail', 'message': '위치 정보 누락'}), 400
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE ITEMLOCATION SET location=%s WHERE item=%s"
            cursor.execute(sql, (new_location, item))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


@app.route('/items/<string:item>', methods=['DELETE'])
def delete_item(item):
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM ITEMLOCATION WHERE item=%s"
            cursor.execute(sql, (item,))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


# ----------------------------------------
# 👤 TeamMember 관련 API
# ----------------------------------------

@app.route('/members', methods=['GET'])
def get_members():
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM TeamMember")
            members = cursor.fetchall()
        return jsonify(members)
    finally:
        conn.close()


@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone_number')
    position = data.get('position')
    if not name or not phone or not position:
        return jsonify({'status': 'fail', 'message': '정보 누락'}), 400
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO TeamMember (name, phone_number, 직급) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, phone, position))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone_number')
    position = data.get('position')
    if not name or not phone or not position:
        return jsonify({'status': 'fail', 'message': '정보 누락'}), 400
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE TeamMember SET name=%s, phone_number=%s, 직급=%s WHERE id=%s"
            cursor.execute(sql, (name, phone, position, id))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM TeamMember WHERE id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
        return jsonify({'status': 'success'})
    finally:
        conn.close()


# ----------------------------------------
# 🕒 UsageHistory 최근 7일 조회 API
# ----------------------------------------

@app.route('/usage/recent', methods=['GET'])
def get_recent_usage():
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            sql = "SELECT * FROM UsageHistory WHERE usage_date >= %s ORDER BY usage_date DESC"
            cursor.execute(sql, (seven_days_ago,))
            result = cursor.fetchall()
        return jsonify(result)
    finally:
        conn.close()


# ----------------------------------------
# 서버 실행
# ----------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
