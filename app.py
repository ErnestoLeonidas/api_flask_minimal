# 0. ejecutamos pip install flask flask-sqlalchemy flask-migrate flask-cors
# 1. importamos la libreria flask
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Usuario
from flask_cors import CORS, cross_origin

# 2. Creamos la aplicacion
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False
app.config['DEBUG'] = False
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

Migrate(app, db)

# 6. Creamos una ruta para validar nuestra app
@app.route('/')
def index():
    return 'Hola mundo'

    # Consultar todos
@app.route('/usuarios', methods=['GET'])
@cross_origin()
def getUsuarios():
    user = Usuario.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200

# consulta solo un usuario según su id y me devuelve 1
@app.route('/usuarios/<id>', methods=['GET'])
def getUsuario(id):
    user = Usuario.query.get('id')
    return jsonify(user.serialize()),200

# borrar usuario segun id
@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuario.query.get('id')
    Usuario.delete(user)
    return jsonify(user.serialize()),200

# modificar usuario
@app.route('/usuarios/<id>', methods=['PUT'])
def updateUsuario(id):
    user = Usuario.query.get('id')

    primer_nombre = request.json.get('primer_nombre')
    segundo_nombre = request.json.get('segundo_nombre')
    apellido_paterno = request.json.get('apellido_paterno')
    apellido_materno = request.json.get('apellido_materno')
    direccion = request.json.get('direccion')

    user.primer_nombre = primer_nombre
    user.segundo_nombre = segundo_nombre
    user.apellido_paterno = apellido_paterno
    user.apellido_materno = apellido_materno
    user.direccion = direccion

    Usuario.save(user)

    return jsonify(user.serialize()),200

# agregar usuario
# Session = scoped_session(sessionmaker(bind=engine))
@app.route('/usuarios', methods=['POST'])
def addUsuario():
    user = Usuario()
    primer_nombre = request.json.get('primer_nombre')
    segundo_nombre = request.json.get('segundo_nombre')
    apellido_paterno = request.json.get('apellido_paterno')
    apellido_materno = request.json.get('apellido_materno')
    direccion = request.json.get('direccion')

    user.primer_nombre = primer_nombre
    user.segundo_nombre = segundo_nombre
    user.apellido_paterno = apellido_paterno
    user.apellido_materno = apellido_materno
    user.direccion = direccion
    
    Usuario.save(user)

    return jsonify(user.serialize()),200


# 3. Creamos una ruta y debug=true para que el servidor se reinicie ante los cambios
# 4. añadimos un validador para saber si estamos ejecutando nuestra aplicacion
# 5. ejecutamos python app.py o python3 app.py
# 6. ejecutamos el comando flask db init
# 7. ejecutamos el comando flask db migrate
# 8. ejecutamos el comando flask db upgrade
# 9. ejecutamos el comando flask run --host=0.0.0.0 en caso que tengamos problemas con el cors
if __name__ == '__main__':
    app.run(port=3000, debug=True)