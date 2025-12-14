from flask import Flask, request, jsonify, make_response, Response
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
import dicttoxml

app = Flask(__name__)


# DB CONFIG
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'game'

# JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

mysql = MySQL(app)
jwt = JWTManager(app)


# HELPER FUNCTIONS
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    return None

def format_response(data, status=200):
    output_format = request.args.get('format', 'json').lower()

    if output_format == "xml":
        xml_data = dicttoxml.dicttoxml(
            data, custom_root='response', attr_type=False
        )
        return Response(xml_data, status=status, mimetype='application/xml')

    return make_response(jsonify(data), status)

# AUTH (JWT)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get('username')
    password = data.get('password')

    
    if username == 'admin' and password == 'admin123':
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200

    return jsonify({"error": "Invalid credentials"}), 401


# ROUTES


# READ ALL
@app.route('/champions', methods=['GET'])
def get_champions():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions")
    champions = dict_fetchall(cursor)
    cursor.close()
    return format_response({"champions": champions})

# READ ONE
@app.route('/champions/<int:champion_id>', methods=['GET'])
def get_champion(champion_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM champions WHERE championid=%s", (champion_id,)
    )
    champion = dict_fetchone(cursor)
    cursor.close()

    if champion:
        return format_response(champion)

    return format_response({"error": "Champion not found"}, 404)

# CREATE (PROTECTED)
@app.route('/champions', methods=['POST'])
@jwt_required()
def add_champion():
    data = request.get_json()

    if not data:
        return format_response({"error": "Missing JSON body"}, 400)

    name = data.get('champion_name')
    roleid = data.get('roleid')
    difficulty = data.get('difficulty_level')

    if not name or not roleid or not difficulty:
        return format_response({"error": "Missing required fields"}, 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO champions (champion_name, roleid, difficulty_level) "
        "VALUES (%s, %s, %s)",
        (name, roleid, difficulty)
    )
    mysql.connection.commit()
    cursor.close()

    return format_response({"message": "Champion added successfully"}, 201)

# UPDATE (PROTECTED)
@app.route('/champions/<int:champion_id>', methods=['PUT'])
@jwt_required()
def update_champion(champion_id):
    data = request.get_json()

    if not data:
        return format_response({"error": "Missing JSON body"}, 400)

    name = data.get('champion_name')
    roleid = data.get('roleid')
    difficulty = data.get('difficulty_level')

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM champions WHERE championid=%s", (champion_id,)
    )
    existing = dict_fetchone(cursor)

    if not existing:
        cursor.close()
        return format_response({"error": "Champion not found"}, 404)

    cursor.execute(
        "UPDATE champions SET champion_name=%s, roleid=%s, "
        "difficulty_level=%s WHERE championid=%s",
        (name, roleid, difficulty, champion_id)
    )
    mysql.connection.commit()
    cursor.close()

    return format_response({"message": "Champion updated successfully"})

# DELETE (PROTECTED)
@app.route('/champions/<int:champion_id>', methods=['DELETE'])
@jwt_required()
def delete_champion(champion_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM champions WHERE championid=%s", (champion_id,)
    )
    existing = dict_fetchone(cursor)

    if not existing:
        cursor.close()
        return format_response({"error": "Champion not found"}, 404)

    try:
        cursor.execute(
            "DELETE FROM champions WHERE championid=%s", (champion_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return format_response({"message": "Champion deleted successfully"})
    except IntegrityError:
        cursor.close()
        return format_response(
            {"error": "Cannot delete champion: still referenced in other tables"},
            400
        )

# SEARCH
@app.route('/champions/search', methods=['GET'])
def search_champions():
    name = request.args.get('name')
    roleid = request.args.get('roleid')
    difficulty = request.args.get('difficulty_level')

    query = "SELECT * FROM champions WHERE 1=1"
    params = []

    if name:
        query += " AND champion_name LIKE %s"
        params.append(f"%{name}%")
    if roleid:
        query += " AND roleid=%s"
        params.append(roleid)
    if difficulty:
        query += " AND difficulty_level=%s"
        params.append(difficulty)

    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    champions = dict_fetchall(cursor)
    cursor.close()

    return format_response({"champions": champions})


# RUN
if __name__ == '__main__':
    app.run(debug=True)
