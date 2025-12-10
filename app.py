from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
import dicttoxml

app = Flask(__name__)

# DB CONFIG
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'game'

mysql = MySQL(app)

#  HELPER FUNCTIONS 

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
    """
    Converts response to JSON or XML based on ?format=
    Default: JSON
    """
    output_format = request.args.get('format', 'json').lower()

    if output_format == "xml":
        xml_data = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml_data, status)
        response.headers['Content-Type'] = 'application/xml'
        return response

    # JSON response
    return make_response(jsonify(data), status)

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
    cursor.execute("SELECT * FROM champions WHERE championid=%s", (champion_id,))
    champion = dict_fetchone(cursor)
    cursor.close()

    if champion:
        return format_response(champion)

    return format_response({"error": "Champion not found"}, 404)


# CREATE
@app.route('/champions', methods=['POST'])
def add_champion():
    data = request.get_json()
    name = data.get('champion_name')
    roleid = data.get('roleid')
    difficulty = data.get('difficulty_level')

    if not name or not roleid or not difficulty:
        return format_response({"error": "Missing required fields"}, 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO champions (champion_name, roleid, difficulty_level) VALUES (%s, %s, %s)",
        (name, roleid, difficulty)
    )
    mysql.connection.commit()
    cursor.close()

    return format_response({"message": "Champion added successfully"}, 201)


# UPDATE
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
        return format_response({"error": "Champion not found"}, 404)

    cursor.execute(
        "UPDATE champions SET champion_name=%s, roleid=%s, difficulty_level=%s WHERE championid=%s",
        (name, roleid, difficulty, champion_id)
    )
    mysql.connection.commit()
    cursor.close()

    return format_response({"message": "Champion updated successfully"})


# DELETE
@app.route('/champions/<int:champion_id>', methods=['DELETE'])
def delete_champion(champion_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM champions WHERE championid=%s", (champion_id,))
    existing = dict_fetchone(cursor)

    if not existing:
        cursor.close()
        return format_response({"error": "Champion not found"}, 404)

    try:
        cursor.execute("DELETE FROM champions WHERE championid=%s", (champion_id,))
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
    # Get query parameters
    name = request.args.get('name')
    roleid = request.args.get('roleid')
    difficulty = request.args.get('difficulty_level')
    output_format = request.args.get('format', 'json').lower()

    # Build dynamic query
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

    # Return XML if requested
    if output_format == 'xml':
        from dicttoxml import dicttoxml
        from flask import Response
        xml_data = dicttoxml(champions, custom_root='champions', attr_type=False)
        return Response(xml_data, mimetype='application/xml')

    # Default JSON output
    return jsonify({"champions": champions}), 200

#  RUN 
if __name__ == '__main__':
    app.run(debug=True)
