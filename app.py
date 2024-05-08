import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import User, Paciente, Familiar, Pariente, Roles, Doctor, RevisionCardiaca, Consulta
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


# Contar el total de usuarios de que contiene la tabla User
@app.route('/user/count', methods=['GET'])
def count_users():
    s_sesion = session()
    li_pacientes = s_sesion.query(Paciente).all()
    result= {
        'total': len(li_pacientes),
    }
    return jsonify(result)


# Crear un usuario
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
        'listpatient': result_pacientes,
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
@app.route('/Paciente/Insert', methods=['POST'])
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


# Muestra un doctor por ID
@app.route('/doctor/<id>', methods=['GET'])
def doctor(id):
    s = session()
    doctoru = s.query(Doctor).filter(Doctor.IdDoctor == id).first()
    result = {
        'error' : None, 
        'doctor' : doctoru.to_dict(),
        'status' : 'success',
        'message' : 'doctor recuperado con exito', 
        'code' : 200
    }
    return jsonify(result)


# Crea un usuario doctor
@app.route('/Doctor/Insert', methods=['POST'])
def create_doctor():
    s_sesion = session()
    data = request.json
    doctor = Doctor(
        IdDoctor = data['IdDoctor'],
        Cedula = data['Cedula'],
        Especialidad = data['Especialidad']
    )
    s_sesion.add(doctor)
    s_sesion.commit()
    result = {
        'error': None,
        'data': doctor.to_dict(),
        'status': 'success',
        'message': 'Doctor creado con exito',
        'code': 201
    }
    return jsonify(result)

# Crea un usuario familiar
@app.route('/familiar/Insert', methods=['POST'])
def create_familiar():
    s_sesion = session()
    data = request.json
    familiar = Familiar(
        IdFamiliar = data['IdFamiliar'],
        NumeroTelefono = data['NumeroTelefono'],
    )
    s_sesion.add(familiar)
    s_sesion.commit()
    result = {
        'error': None,
        'data': familiar.to_dict(),
        'status': 'success',
        'message': 'Familiar creado con exito',
        'code': 201
    }
    return jsonify(result)

# Agregamos el rol del usuario creado
@app.route('/Roles/Insert', methods=['POST'])
def create_roles():
    s_sesion = session()
    data = request.json
    roles = Roles(
        IdUser= data['IdUser'],
        RolPaciente = data['RolPaciente'],
        RolDoctor = data['RolDoctor'],
        RolFamiliar = data['RolFamiliar'],
    )
    s_sesion.add(roles)
    s_sesion.commit()
    result = {
        'error': None,
        'data': roles.to_dict(),
        'status': 'success',
        'message': 'roles asginados con exito',
        'code': 201
    }
    return jsonify(result)

#Login de los Usuarios
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


# Manda los roles del usuario que se consulta por medio del id
@app.route('/roles', methods=['POST'])
def roles():
    s = session()
    data = request.json
    roles = s.query(Roles).filter(Roles.IdUser == data['IdUser']).first()
    if roles:
        result  = {
            'error': None,
            'roles': roles.to_dict(),
            'status': 'success',
            'message': 'Roles enviados con exito',
            'code': 200
        }
    else:
        result = {
            'error': 'Usuario no encontrado',
            'roles': None,
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

#ultima Consulta reliazada al paciente de Revision Cardiaca
@app.route('/consulta/ultimasesion', methods=['POST'])
def revisioncardiacaUltimasesion():
    s = session()
    data = request.json
    revisionList = s.query(Consulta).filter(Consulta.IdFPaciente == data['IdFPaciente']).all()
    if revisionList:
        revision = revisionList[len(revisionList) - 1]
        result  = {
            'error': None,
            'consulta': revision.to_dict(),
            'status': 'success',
            'message': 'consulta enviada con exito',
            'code': 200
        }
    else:
        result = {
            'error': 'consulta no encontrada',
            'consulta': None,
            'status': 'error',
            'message': 'consulta no encontrada',
            'code': 404
        }
    return jsonify(result)
        
# ultima consulta realizada al paciente
@app.route('/consultas', methods=['POST'])
def consultas():
    s = session()
    data = request.json
    li_consultas = s.query(Consulta).filter(Consulta.IdFPaciente == data['IdFPaciente']).all()
    result_list = []
    for consulta in li_consultas:
        result_list.append(consulta.to_dict())
        
    result_pacientes = {
        'consultas': result_list,
        'total': len(li_consultas),
    }
    result = {
        'error': None,
        'listconsults': result_pacientes,
        'status': 'success',
        'message': 'consultas recuperadas con exito',
        'code': 200
    }
    return jsonify(result)

# Inserccion de una consulta
@app.route('/consulta/insert', methods=['POST'])
def insert_consult():
    s_sesion = session()
    data = request.json
    date_consult = data['FechaConsulta']
    date_consult = datetime.strptime(date_consult, '%Y-%m-%d')
    
    consulta = Consulta(
        IdConsulta = data['IdConsulta'],
        FechaConsulta = date_consult,
        HoraConsulta = data['HoraConsulta'],
        IdFDoctor = data['IdFDoctor'],
        IdFPaciente = data['IdFPaciente'],
        IdFRevisionCa = data['IdFRevisionCa'],
        Estado = data['Estado'],
        FrecuenciaCardiaca = data['FrecuenciaCardiaca']
    )
    s_sesion.add(consulta)
    s_sesion.commit()
    result = {
        'error': None,
        'status' : 'success',
        'message' : 'Consulta creada con exito',
    }
    
    return jsonify(result)

# Inserccion de revisioncardiaca
@app.route('/revisioncardiaca/insert', methods=['POST'])
def insert_revision_cardiaca():
    s_sesion = session()
    print(request)
    #data = request.json()
    # Directorio donde se contiene la imagen ECG
    IdPaciente =  request.form.get('IdPaciente', '')
    IdRevisionCa = request.form.get('IdRevisionCa', '')
    DirectoryECG =  "static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults' + chr(92) + IdRevisionCa
    app.config['UPLOAD_FOLDER'] = DirectoryECG
    # Lista de los nombres de las imagenes que se encuentran dentro del directorio
    image_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.png') or f.endswith('.jpg')]
    # Iteramos en la lista de imagenes obtenidas
    for image_file in image_files:
        # Cargamos la imagen del  ECG
        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
        # Convertimos la imagen a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Aplicamos umbralización para resaltar las líneas verdes
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        # Encontramos contornos en la imagen umbralizada
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filtramos  los contornos por el color verde
        green_contours = []
        # Iteramos dentro de la lista de los contornos obtenidos
        for contour in contours:
            # Obtenemos el promedio del color en el contorno
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
            mean_color = cv2.mean(img, mask=mask)[:3]  # Canal BGR
            # Comprovamos si el color esta dentro del rango verde
            if mean_color[1] > mean_color[0] and mean_color[1] > mean_color[2]:
                green_contours.append(contour)
        # Aproximamos los contornos para adelgazar las líneas
        approx_green_contours = [cv2.approxPolyDP(contour, epsilon=0.5, closed=True) for contour in green_contours]
        # Dibujamos los contornos en la imagen original
        cv2.drawContours(img, approx_green_contours, -1, (0, 255, 0), thickness=2)
        # Creamos una imagen con transparencia del mismo tamaño que la original
        contour_img = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
        # Dibujamos contornos en la imagen con transparencia
        cv2.drawContours(contour_img, approx_green_contours, -1, (0, 255, 0, 255), thickness=cv2.FILLED)
        # Guardamos la imagen del contorno en un archivo con canal alfa
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], image_file), contour_img)
        # Mostramos la imagen con contornos resaltados
        #cv2.imshow('Contornos verdes', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Mostramos la imagen contorno.png utilizando OpenCV
        #cv2.imshow('Contorno', contour_img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        # Leemos la imagen del contorno guardada
        contour_img = cv2.imread('static\images\RECORTE_3.png', cv2.IMREAD_UNCHANGED)

        # Convertir la imagen a RGB para ser compatible con Matplotlib
        contour_img_rgb = cv2.cvtColor(contour_img, cv2.COLOR_BGRA2RGBA)
        # Invertimos la imagen
        # contour_img_rgb = np.flipud(contour_img_rgb) #Invierte el eje Y de la imagen
        # Se aplica un filtro blur para quitar un poco el ruido
        filtered_mask = cv2.medianBlur(contour_img_rgb, 5)
        # Guardamos la imagen del contorno en un archivo con canal alfa
        cv2.imwrite('static\images\RECORTE_3.png', filtered_mask)
         # Leemos la imagen del contorno guardada
        contour_img = cv2.imread('static\images\electrocardiograms\JS_1_1.png', cv2.IMREAD_UNCHANGED)
        # definimos el color a buscar (verde)
        green = np.array([0, 255, 0, 255], dtype=np.uint8)
        # Encontramos la coordenadas de x y y en los pixeles verdes
        y_coords, x_coords = np.where(np.all(contour_img == green, axis=-1))
        # imprimimos las coordenadas
        # print("X values:", x_coords)
        # print("Y values:", y_coords)
        # Encontramos los valores minimo y maximo de y para cada valor de x
        min_y = {}
        max_y = {}
        for x, y in zip(x_coords, y_coords):
            if x not in min_y or y < min_y[x]:
                min_y[x] = y
            if x not in max_y or y > max_y[x]:
                max_y[x] = y
        # Encontramos la posicion de la coordenada inferior y en la matriz de y_coords
        # coordenada y mas baja
        lower_y = min(y_coords)  
        lower_y_pos = np.where(y_coords == lower_y)[0][0]
        # Encontramos la posicion de X de la corrdenada Y más baja
        lower_x_pos = x_coords[lower_y_pos]  # coordenada x de la coordenada y mas baja
        # Encontramos el punto inicial de ECG
        first_point = (min(x_coords), min_y[min(x_coords)])
        # Buscamos el ultimo punto del ECG
        final_point = (max(x_coords), max_y[max(x_coords)])
        # Buscamos el punto más alto entre el primer y punto más bajo
        QSignal = (lower_x_pos, max_y[lower_x_pos])
        # Obtenemos el numero de punto x entre el primer punto y el punto inferior
        x_between = np.where((x_coords > first_point[0]) & (x_coords < lower_x_pos))
         # iteramos en x_between hacia la derecha y obtenemos la coordenada del valor más alto de y
        for i in range(x_between[0].shape[0]):
            if y_coords[x_between[0][i]] > QSignal[1]:
                QSignal = (x_coords[x_between[0][i]], y_coords[x_between[0][i]])
        # Encontramos el punto más alto entre el punto inferior y el final
        QSignal2 = (lower_x_pos, max_y[lower_x_pos])
        # Obtenemos las x entre el punto inferior y el punto final
        x_between2 = np.where((x_coords > lower_x_pos) & (x_coords < final_point[0]))
        # Obtenemos el punto medio del rango X_between2
        midpoint = lower_x_pos + (final_point[0] - lower_x_pos) // 2
         # obtenemosel numero de x entre el punto inferior y el punto medio
        x_between2_first_half = np.where((x_coords > lower_x_pos) & (x_coords < midpoint))
        # Iteramos en x_between2_first_half recorriendo los puntos hacia la derecha para obtener la coordenada del valor superior de Y
        for i in range(x_between2_first_half[0].shape[0]):
            if y_coords[x_between2_first_half[0][i]] > QSignal2[1]:
                QSignal2 = (x_coords[x_between2_first_half[0][i]], y_coords[x_between2_first_half[0][i]])
        # Buscamos el punto más bajo ente Qsignal 2 y el punto final
        lower_point_startQ = (QSignal2[0], max_y[QSignal2[0]])
        # Obtenemos el numero de x ente QSignal2 y el punto final
        x_between2_second_half = np.where((x_coords > QSignal2[0]) & (x_coords < final_point[0]))
        # Iteramos en x_between2_second_half hacia la derecha y obtenemos el valor inferior de y
        for i in range(x_between2_second_half[0].shape[0]):
            if y_coords[x_between2_second_half[0][i]] < lower_point_startQ[1]:
                lower_point_startQ = (x_coords[x_between2_second_half[0][i]], y_coords[x_between2_second_half[0][i]])
        # Encontramos el punto inferior entre el punto inicial y las coordenas de QSignal
        lower_point_startP = (first_point[0], max_y[first_point[0]])
        # Obtenemos el numero de x entre el punto de inicio y QSignal dividido entre 2
        x_between3 = np.where((x_coords > first_point[0]) & (x_coords < QSignal[0]))
        midpoint2 = first_point[0] + (QSignal[0] - first_point[0]) // 2
        # Obtenemos el numero de x entre el punto inicial y el punto medio
        x_between3_first_half = np.where((x_coords > first_point[0]) & (x_coords < midpoint2))
        # Iteramos en x_between3_first_half hacia la derecha y obtenemos el valor inferior de y
        for i in range(x_between3_first_half[0].shape[0]):
            if y_coords[x_between3_first_half[0][i]] < lower_point_startP[1]:
                lower_point_startP = (x_coords[x_between3_first_half[0][i]], y_coords[x_between3_first_half[0][i]])
        # Crea un diagrama de dispersión de los valores x e y
        # plt.scatter(x_coords, y_coords, s=1)
        # Invertimos el eje de la y
        # plt.gca().invert_yaxis()
        #Traza los puntos primero, inferior y final
        # plt.plot(first_point[0], first_point[1], 'co', label='First')
        # plt.plot(lower_x_pos, lower_y, 'ko', label='R')
        # plt.plot(final_point[0], final_point[1], 'bo', label='Final')
        # plt.plot(QSignal[0], QSignal[1], 'ro', label='Q')
        # plt.plot(QSignal2[0], QSignal2[1], 'go', label='S')  # ONDA S
        # plt.plot(lower_point_startQ[0], lower_point_startQ[1], 'yo', label='T')
        # plt.plot(lower_point_startP[0], lower_point_startP[1], 'mo', label='P')
        # Mandamos los datos obtenidos a la db
        revisioncardiaca = RevisionCardiaca(
            IdRevisionCa = IdRevisionCa,
            imgFrecuencia = IdRevisionCa + '.png',
            PrimerPuntoX = float(int(first_point[0])),
            PrimerPuntoY = float(int(first_point[1])),
            PuntoMasAltoX = float(int(lower_x_pos)),
            PuntoMasAltoY = float(int(lower_y)),
            PuntoFinalX = float(int(final_point[0])),
            PuntoFinalY	= float(int(final_point[1])),
            QSignalX = float(int(QSignal[0])),
            QSignalY = float(int(QSignal[1])),
            SSignalX = float(int(QSignal2[0])),
            SSignalY = float(int(QSignal2[1])),
            TSignalX = float(int(lower_point_startQ[0])),
            TSignalY = float(int(lower_point_startQ[1])),
            PSignalX = float(int(lower_point_startP[0])),
            PSignalY = float(int(lower_point_startP[1])),
        )
        s_sesion.add(revisioncardiaca)
        s_sesion.commit()
        result = {
        'error': None,
        'data': revisioncardiaca.to_dict(),
        'status': 'success',
        'message': 'revision creada con exito',
        'code': 201
        }
        return jsonify(result)


# inserccion de imagen corrspondiente a la lectura del electrocardiograma
@app.route('/consulta/insertimg', methods=['POST'])
def insert_consult_img():
    IdPaciente = request.form.get('IdPaciente', '')
    IdRevisionCa = request.form.get('IdRevisionCa', '')
    directory = "static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults' + chr(92) + IdRevisionCa
    app.config['UPLOAD_FOLDER'] = directory
    if 'image' not in request.files:
        return jsonify(
            {
                'error': 'No se ha proporcionado ninguna imagen',
                'message': 'No se ha proporcionado ninguna imagen',
                'code': 400
            }), 400
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify(
            {'error': 'Nombre de archivo vacío',
             'message': 'Nombre de archivo vacío',
             'code': 400
             }), 400
    new_filename = request.form.get('new_filename', '')
    if not new_filename:
         return jsonify(
                {
                    'error': 'Nombre de archivo nuevo no proporcionado',
                    'message': 'Nombre de archivo nuevo no proporcionado',
                    'code': 400
                }), 400
    new_filename = new_filename + '.png'
    # Verificamos si existe el directorio del usuario mandado, si no es asi la creamos
    if not os.path.exists("static" + chr(92) + "images" + chr(92) + IdPaciente):
        os.makedirs("static" + chr(92) + "images" + chr(92) + IdPaciente)
     # Verificamos si no se ha hecho el directorio correspondiente a la consulta si no es asi creamos el directorio
    if not os.path.exists("static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults'):
        os.makedirs("static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults')
    # Verificamos si no se ha hecho el directorio correspondiente a la consulta si no es asi creamos el directorio
    if not os.path.exists("static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults' + chr(92) + IdRevisionCa):
        os.makedirs("static" + chr(92) + "images" + chr(92) + IdPaciente + chr(92) + 'Consults' + chr(92) + IdRevisionCa)
    # Guardar la imagen en el directorio corresponddiente
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return jsonify({
            'error': None,
            'message': 'imagen anexada con exito',
            'code': 201
        }), 201


# Contar el total de usuarios de que contiene la tabla User
@app.route('/consult/count', methods=['GET'])
def count_consults():
    s_sesion = session()
    li_consulta = s_sesion.query(Consulta).all()
    result= {
        'error': None,
        'total': len(li_consulta),
        'code': 200
    }
    return jsonify(result)


# Contar el total de usuarios de que contiene la tabla User
@app.route('/revisionca/count', methods=['GET'])
def count_RevisionCardiac():
    s_sesion = session()
    li_revisionca = s_sesion.query(RevisionCardiaca).all()
    result= {
        'error': None,
        'total': len(li_revisionca),
        'code': 200
    }
    return jsonify(result)


# inserccion de foto de perfil al usuario
@app.route('/user/insertimg', methods=['POST'])
def insert_user_img():
    IdPaciente = request.form.get('IdPaciente', '')
    directory = "static" + chr(92) + "images"
    app.config['UPLOAD_FOLDER'] = directory
    if 'image' not in request.files:
        return jsonify(
            {
                'error': 'No se ha proporcionado ninguna imagen',
                'message': 'No se ha proporcionado ninguna imagen',
                'code': 400
            }), 400
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify(
            {'error': 'Nombre de archivo vacío',
             'message': 'Nombre de archivo vacío',
             'code': 400
             }), 400
    new_filename = request.form.get('new_filename', '')
    if not new_filename:
         return jsonify(
                {
                    'error': 'Nombre de archivo nuevo no proporcionado',
                    'message': 'Nombre de archivo nuevo no proporcionado',
                    'code': 400
                }), 400
    new_filename = new_filename + '.png'
    # Verificamos si existe el directorio del usuario mandado, si no es asi la creamos
    if not os.path.exists("static" + chr(92) + "images" + chr(92) + IdPaciente):
        os.makedirs("static" + chr(92) + "images" + chr(92) + IdPaciente)
    # Guardar la imagen en el directorio corresponddiente
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return jsonify({
            'error': None,
            'message': 'imagen anexada con exito',
            'code': 201
        }), 201


if __name__ == '__main__':
    app.run(debug=True, port=4000)
