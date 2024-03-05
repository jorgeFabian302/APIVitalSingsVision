# Creamos las clases correposndientes para mandar
class Pacientes:
    # Construtor
    def __init__(self, idpaciente, name,  apellidos, correo, password, tipo, fechanaciemiento, fotoperfil):
        self.IdPaciente = idpaciente
        self.Nombre = name
        self.Apellidos = apellidos
        self.Correo = correo
        self.Password = password
        self.Tipo = tipo
        self.FechaNaciemiento = fechanaciemiento
        self.FotoPerfil = fotoperfil

    # Fun que regresa un diccionario
    def FunDicJson(self):
        DicTemp = {'IdPaciente': self.IdPaciente, 'Nombre': self.Nombre, 'Apellidos': self.Apellidos,
                   'Correo': self.Correo, 'Password': self.Password, 'Tipo': self.Tipo,
                   'FechaNacimiento': self.FechaNaciemiento,
                   'FotoPerfil': self.FotoPerfil}

        return DicTemp


class Doctor:
    # Construtor
    def __init__(self, idpaciente, name, apellidos, correo, password, tipo, fechanaciemiento, fotoperfil, cedula,
                 especialidad):
        self.IdPaciente = idpaciente
        self.Nombre = name
        self.Apellidos = apellidos
        self.Correo = correo
        self.Password = password
        self.Tipo = tipo
        self.FechaNaciemiento = fechanaciemiento
        self.FotoPerfil = fotoperfil
        self.Cedula = cedula
        self.Especialidad = especialidad

        # Fun que regresa un diccionario

    def FunDicJson(self):
        DicTemp = {'IdPciente': self.IdPaciente, 'Nombre': self.Nombre, 'Apellidos': self.Apellidos,
                   'Correo': self.Correo, 'Password': self.Password, 'Tipo': self.Tipo,
                   'FechaNacimiento': self.FechaNaciemiento,
                   'FotoPerfil': self.FotoPerfil, 'Cedula': self.Cedula, 'Especialidad': self.Especialidad}

        return DicTemp


class Familiar:
    # Construtor
    def __init__(self, idpaciente, name,  apellidos, correo, password, tipo, fechanaciemiento, fotoperfil):
        self.IdPaciente = idpaciente
        self.Nombre = name
        self.Apellidos = apellidos
        self.Correo = correo
        self.Password = password
        self.Tipo = tipo
        self.FechaNaciemiento = fechanaciemiento
        self.FotoPerfil = fotoperfil

    # Fun que regresa un diccionario
    def FunDicJson(self):
        DicTemp = {'IdPciente': self.IdPaciente, 'Nombre': self.Nombre, 'Apellidos': self.Apellidos,
                   'Correo': self.Correo, 'Password': self.Password, 'Tipo': self.Tipo,
                   'FechaNacimiento':  self.FechaNaciemiento,
                   'FotoPerfil': self.FotoPerfil}

        return DicTemp
