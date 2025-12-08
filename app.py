from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'game'

mysql = MySQL(app)

# Helper to convert MySQL rows to dict
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    return None

# ====== READ ALL ======
@app.route('/champions', methods=['GET'])
def get_champions():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions")
    champions = dict_fetchall(cursor)
    cursor.close()
    return jsonify({"champions": champions}), 200

# ====== READ ONE ======
@app.route('/champions/<int:champion_id>', methods=['GET'])
def get_champion(champion_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions WHERE championid=%s", (champion_id,))
    champion = dict_fetchone(cursor)
    cursor.close()
    if champion:
        return jsonify(champion), 200
    return jsonify({"error": "Champion not found"}), 404

# ====== CREATE ======
@app.route('/champions', methods=['POST'])
def add_champion():
    data = request.get_json()
    name = data.get('champion_name')
    roleid = data.get('roleid')
    difficulty = data.get('difficulty_level')

    if not name or not roleid or not difficulty:
        return jsonify({"error": "Missing required fields"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO champions (champion_name, roleid, difficulty_level) VALUES (%s, %s, %s)",
        (name, roleid, difficulty)
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Champion added successfully"}), 201

# ====== UPDATE ======
@app.route('/champions/<int:champion_id>', methods=['PUT'])
def update_champion(champion_id):
    data = request.get_json()
    name = data.get('champion_name')
    roleid = data.get('roleid')
    difficulty = data.get('difficulty_level')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions WHERE championid=%s", (champion_id,))
    existing = dict_fetchone(cursor)
    if not existing:
        cursor.close()
        return jsonify({"error": "Champion not found"}), 404

    cursor.execute(
        "UPDATE champions SET champion_name=%s, roleid=%s, difficulty_level=%s WHERE championid=%s",
        (name, roleid, difficulty, champion_id)
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Champion updated successfully"}), 200

# ====== DELETE ======
@app.route('/champions/<int:champion_id>', methods=['DELETE'])
def delete_champion(champion_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions WHERE championid=%s", (champion_id,))
    existing = dict_fetchone(cursor)
    if not existing:
        cursor.close()
        return jsonify({"error": "Champion not found"}), 404

    cursor.execute("DELETE FROM champions WHERE championid=%s", (champion_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Champion deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
