import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
import Diccionarios

# Creamos el local host para para poder utilizar la API
app = Flask(__name__)


# Muestra del Route de la api
@app.route('/')
def ping():

    return jsonify('Welcome to Vital Sings Monitor')


# Ruta para insertar un paciente
@app.route('/Patient/Select')
def GetPSelect():
    # Tomamos la dirección de la DB
    S_db = 'C:' + chr(92) + 'Users' + chr(92) + 'Jorge Fabian RP' + chr(92) + 'Documents' + chr(92) + 'Modular' + chr(
        92) + 'DB Modular' + chr(92) + 'VitalSiggnsVisionDB_BackUp.db'
    #  Creamos la conexion hacia la DB
    ConnectionSQL = sqlite3.connect(S_db)
    # Creamos un Cursor para solicitar la peticiones a la DB
    C_Cursor = ConnectionSQL.cursor()
    # Mandamos la peticion sql a la DB
    C_Cursor.execute("SELECT * FROM Pacientes WHERE IdPaciente =?", ('09-PLaSo1899',))
    # Guardamos la tupla resultante en una variable
    Paciente = C_Cursor.fetchone()
    # Pacientes = C_Cursor.fetchall()
    # Cerramos la conxion hacia la db
    ConnectionSQL.close()
    print(Paciente[6])
    # Creamos una variable de tipo Paciente
    JSONPaciente = Diccionarios.Pacientes(Paciente[0], Paciente[1], Paciente[2], Paciente[3], Paciente[4],
                                          Paciente[5], Paciente[6], Paciente[7])

    print(JSONPaciente.FunDicJson())
    return jsonify(JSONPaciente.FunDicJson())


# Ruta para seleccionar un paciente


if __name__ == '__main__':
    app.run(debug=True)
