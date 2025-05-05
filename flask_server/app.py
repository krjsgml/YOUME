from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
from db_config import db_info


app = Flask(__name__)
CORS(app)

# --------------------
# ItemLocation API
# --------------------

@app.route('/api/item_locations', methods=['GET'])
def get_item_locations():
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ItemLocation")
            locations = cur.fetchall()
    return jsonify(locations)

@app.route('/api/item_locations', methods=['POST'])
def add_item_location():
    data = request.get_json()
    item_name = data['item_name']
    location = data['location']
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO ItemLocation (item_name, location) VALUES (%s, %s)", 
                        (item_name, location))
            conn.commit()
    return jsonify({'message': 'Item location added successfully'})

@app.route('/api/item_locations/<int:id>', methods=['DELETE'])
def delete_item_location(id):
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ItemLocation WHERE id = %s", (id,))
            conn.commit()
    return jsonify({'message': 'Item location deleted successfully'})

# --------------------
# TeamMember API
# --------------------

@app.route('/api/team_members', methods=['GET'])
def get_members():
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM TeamMember")
            members = cur.fetchall()
    return jsonify(members)

@app.route('/api/team_members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data['name']
    phone = data.get('phone_number', '')
    position = data.get('position', '')
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO TeamMember (name, phone_number, position) VALUES (%s, %s, %s)", 
                        (name, phone, position))
            conn.commit()
    return jsonify({'message': 'Member added successfully'})

@app.route('/api/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM TeamMember WHERE id = %s", (id,))
            conn.commit()
    return jsonify({'message': 'Member deleted successfully'})

# --------------------
# UsageHistory API
# --------------------

@app.route('/api/usage_histories', methods=['GET'])
def get_usage():
    id = request.args.get('id')
    date = request.args.get('date')

    query = "SELECT * FROM UsageHistory"
    params = []

    if id and date:
        query += " WHERE id = %s AND usage_date = %s"
        params = [id, date]
    elif id:
        query += " WHERE id = %s"
        params = [id]
    elif date:
        query += " WHERE usage_date = %s"
        params = [date]

    conn = pymysql.connect(**db_info)
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            usage = cur.fetchall()
    return jsonify(usage)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
