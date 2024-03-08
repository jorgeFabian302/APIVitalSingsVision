import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
import Diccionarios
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import User

# Creamos el local host para para poder utilizar la API

app = Flask(__name__)
engine = create_engine('sqlite:///NewDB.db')
session = sessionmaker(bind=engine)
session.configure(bind=engine)


# Muestra del Route de la api
@app.route('/')
def ping():

    return jsonify('Welcome to Vital Sings Monitor')

# Ruta para insertar un paciente
@app.route('/Patient/Select')
def get_pselect():
    # Tomamos la dirección de la DB
    s_db = './VitalSiggnsVisionDB.db'
    #  Creamos la conexion hacia la DB
    connection_sql = sqlite3.connect(s_db)
    # Creamos un Cursor para solicitar la peticiones a la DB
    c_cursor = connection_sql.cursor()
    # Mandamos la peticion sql a la DB

    c_cursor.execute("SELECT * FROM Pacientes WHERE IdPaciente = ?", ('09-PLaSo1899',))
    # Guardamos la tupla resultante en una variable
    paciente = c_cursor.fetchone() 
    # Pacientes = C_Cursor.fetchall()
    # Cerramos la conxion hacia la db
    connection_sql.close()
    print(paciente[6])
    # Creamos una variable de tipo Paciente
    json_paciente = Diccionarios.Pacientes(paciente[0], paciente[1], paciente[2], paciente[3], paciente[4],
                                          paciente[5], paciente[6], paciente[7])

    print(json_paciente.FunDicJson())


# Ruta para seleccionar un paciente
@app.route('/users', methods=['GET'])
def users():
    s = session()
    users = s.query(User).all()
    
    result_list = []
    for user in users:
        result_list.append(user.to_dict())

    result_users = {
        'usuarios' : result_list,
        'total' : len(users),
    }

    result = {
        'error' : None, 
        'data' : result_users,
        'status' : 'success',
        'message' : 'Pacientes recuperados con exito', 
        'code' : 200
    }

    return jsonify(result)

# @app.route('/pacientes/<id>', methods=['GET'])
# def paciente(id):
#     s = session()
#     paciente = s.query(Paciente).filter(Paciente.IdPaciente == id).first()
#     result = {
#         'error' : None, 
#         'data' : paciente.to_dict(),
#         'status' : 'success',
#         'message' : 'Paciente recuperado con exito', 
#         'code' : 200
#     }
#     return jsonify(result)

@app.route('/user', methods=['POST'])
def create_user():
    s = session()
    data = request.json
    user = User(
        IdUser = data['IdUser'],
        Nombre = data['Nombre'],
        ApellidoPaterno = data['ApellidoPaterno'],
        ApellidoMaterno = data['ApellidoMaterno'],
        FechaNacimiento = data['FechaNacimiento'],
        Password = data['Password'] # hash
    )
    s.add(user)
    s.commit()
    result = {
        'error' : None, 
        'data' : user.to_dict(),
        'status' : 'success',
        'message' : 'Paciente creado con exito', 
        'code' : 201
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
