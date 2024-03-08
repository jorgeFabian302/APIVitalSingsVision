from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import User, Paciente, Familiar, Pariente
from datetime import datetime
# Creamos el local host para para poder utilizar la API

app = Flask(__name__)
engine = create_engine('sqlite:///VitalSingSVisionDB.db')
session = sessionmaker(bind=engine)
session.configure(bind=engine)


# Muestra del Route de la api
@app.route('/')
def ping():
    return jsonify('Welcome to Vital Sings Monitor')


# Ruta para seleccionar todos los pacientes
@app.route('/users', methods=['GET'])
def users():
    s = session()
    li_users = s.query(User).all()

    result_list = []
    for user in li_users:
        result_list.append(user.to_dict())

    result_users = {
        'usuarios': result_list,
        'total': len(li_users),
    }

    result = {
        'error': None,
        'data': result_users,
        'status': 'success',
        'message': 'Pacientes recuperados con exito',
        'code': 200
    }

    return jsonify(result)

#selecciona un paciente por ID
@app.route('/users/<id>', methods=['GET'])
def users_by_id(id):
    s = session()
    paciente = s.query(User).filter(User.IdUser == id).first()
    result = {
        'error' : None, 
        'data' : paciente.to_dict(),
        'status' : 'success',
        'message' : 'Paciente recuperado con exito', 
        'code' : 200
    }
    return jsonify(result)

#Crear un usuario
@app.route('/user/Insert', methods=['POST'])
def create_user():
    s_sesion = session()
    data = request.json

    date_birth = data['FechaNacimiento']
    # year-month-day parse to datetime
    date_birth = datetime.strptime(date_birth, '%Y-%m-%d')

    user = User(
        IdUser = data['IdUser'],
        Nombre = data['Nombre'],
        Apellidos = data['Apellidos'],
        Correo = data['Correo'],
        Password = data['Password'],  
        FechaNacimiento = date_birth,
        FotoPerfil = data['FotoPerfil']
    )
    s_sesion.add(user)
    s_sesion.commit()
    result = {
        'error': None,
        'data': user.to_dict(),
        'status': 'success',
        'message': 'Usuario creado con exito',
        'code': 201
    }
    return jsonify(result)


#Muestra los pacientes
@app.route('/pacientes', methods=['GET'])
def pacientes():
    s = session()
    li_pacientes = s.query(Paciente).all()

    result_list = []
    for paciente in li_pacientes:
        result_list.append(paciente.to_dict())

    result_pacientes = {
        'pacientes': result_list,
        'total': len(li_pacientes),
    }

    result = {
        'error': None,
        'data': result_pacientes,
        'status': 'success',
        'message': 'Pacientes recuperados con exito',
        'code': 200
    }

    return jsonify(result)

#Muestra un Paciente por ID
@app.route('/pacientes/<id>', methods=['GET'])
def paciente(id):
    s = session()
    paciente = s.query(Paciente).filter(Paciente.IdPaciente == id).first()
    result = {
        'error' : None, 
        'data' : paciente.to_dict(),
        'status' : 'success',
        'message' : 'Paciente recuperado con exito', 
        'code' : 200
    }
    return jsonify(result)

#Crea un paciente
@app.route('/paciente/Insert', methods=['POST'])
def create_paciente():
    s_sesion = session()
    data = request.json

    paciente = Paciente(
        IdPaciente = data['IdPaciente'],
        NumeroSeguroSocial = data['NumeroSeguroSocial'],
    )
    s_sesion.add(paciente)
    s_sesion.commit()
    result = {
        'error': None,
        'data': paciente.to_dict(),
        'status': 'success',
        'message': 'Paciente creado con exito',
        'code': 201
    }
    return jsonify(result)

#Loguin de los Usuarios
@app.route('/login', methods=['POST'])
def login():
    s = session()
    data = request.json
    user = s.query(User).filter(User.Correo == data['Correo']).filter(User.Password == data['Password']).first()
    if user:
        result = {
            'error': None,
            'data': user.to_dict(),
            'status': 'success',
            'message': 'Usuario logeado con exito',
            'code': 200
        }
    else:
        result = {
            'error': 'Usuario no encontrado',
            'data': None,
            'status': 'error',
            'message': 'Usuario no encontrado',
            'code': 404
        }
    return jsonify(result)

#Enlista los pacientes de un Familiar
@app.route('/getPacientesByFamiliar/<id>', methods=['GET'])
def get_pacientes_by_familiar(id):
    s = session()
    parientes = s.query(Pariente).filter(Pariente.IDFFamiliar == id).all()
    result_list = []
    for pariente in parientes:
        result_list.append(pariente.paciente.to_dict())

    result_pacientes = {
        'pacientes': result_list,
        'total': len(parientes),
    }

    result = {
        'error': None,
        'data': result_pacientes,
        'status': 'success',
        'message': 'Pacientes recuperados con exito',
        'code': 200
    }

    return jsonify(result)

#Consulta a familiares
@app.route('/familiares', methods=['GET'])
def familiares():
    s = session()
    li_familiares = s.query(Familiar).all()

    result_list = []
    for familiar in li_familiares:
        result_list.append(familiar.to_dict())

    result_familiares = {
        'familiares': result_list,
        'total': len(li_familiares),
    }

    result = {
        'error': None,
        'data': result_familiares,
        'status': 'success',
        'message': 'Familiares recuperados con exito',
        'code': 200
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
