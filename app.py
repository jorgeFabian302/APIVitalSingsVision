from flask import Flask, jsonify, request
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


# Ruta para seleccionar un paciente
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

@app.route('/user/Insert', methods=['POST'])
def create_user():
    s_sesion = session()
    data = request.json
    user = User(
        IdUser=data['IdUser'],
        Nombre=data['Nombre'],
        Apellidos=data['Apellidos'],
        Correo=data['Correo'],
        Password=data['Password'],  
        FechaNacimiento=data['FechaNacimiento'],
        FotoPerfil=data['FotoPErfil']# hash 
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

if __name__ == '__main__':
    app.run(debug=True)

