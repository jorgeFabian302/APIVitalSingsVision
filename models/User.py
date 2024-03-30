from sqlalchemy import Column, String, Date, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
class User(Base):
    __tablename__ = 'User'

    IdUser =  Column(String, primary_key=True)
    Nombre = Column(String)
    Apellidos = Column(String)
    Correo = Column(String)
    Password = Column(String)
    FechaNacimiento = Column(Date)
    FotoPerfil = Column(String)

    
    def to_dict(self):
        fec_nac = self.FechaNacimiento.strftime("%Y-%m-%d") if self.FechaNacimiento else None
        return {
            "IdUser": self.IdUser,
            "Nombre": self.Nombre,
            "Apellidos": self.Apellidos,
            "Correo": self.Correo,
            "FechaNacimiento": fec_nac,
            "FotoPerfil": self.FotoPerfil,
        }
    
class Paciente(Base):
    __tablename__ = 'Paciente'

    IdPaciente =  Column(String, ForeignKey('User.IdUser'), primary_key=True)
    NumeroSeguroSocial = Column(String, nullable=False)
    user = relationship("User")

    
    def to_dict(self):

        return {
            "IdPaciente": self.IdPaciente,
            "NumeroSeguroSocial": self.NumeroSeguroSocial,
            "data": self.user.to_dict()
        }

class Familiar(Base):
    __tablename__ = 'Familiar'

    IdFamiliar =  Column(String,ForeignKey('User.IdUser') , primary_key=True)
    NumeroTelefono = Column(String)
    user = relationship("User")
    
    def to_dict(self):

        return {
            "IdFamiliar": self.IdFamiliar,
            "NumeroTelefono": self.NumeroTelefono,
            "data": self.user.to_dict()
        }

class Pariente(Base):
    __tablename__ = 'Pariente'

    IdPariente =  Column(String, primary_key=True)
    IDFFamiliar = Column(String, ForeignKey('Familiar.IdFamiliar'))
    IDFPaciente = Column(String, ForeignKey('Paciente.IdPaciente'))
    familiar = relationship("Familiar")
    paciente = relationship("Paciente")

    
    def to_dict(self):

        return {
            "IdPariente": self.IdPariente,
            "IdFFamiliar": self.IDFFamiliar,
            "IdFPaciente": self.IDFPaciente,
            "familiar": self.familiar.to_dict(),
            "paciente": self.paciente.to_dict()
        }

class Roles(Base):
    __tablename__ = 'Roles'

    IdUser =  Column(String, ForeignKey('User.IdUser'), primary_key=True)
    RolPaciente = Column(Boolean)
    RolDoctor = Column(Boolean)
    RolFamiliar = Column(Boolean)

    user = relationship("User")

    def to_dict(self):

        return {
            "IdUser" : self.IdUser,
            "RolPaciente" : self.RolPaciente,
            "RolDoctor" : self.RolDoctor,
            "RolFamiliar" : self.RolFamiliar,
            "data": self.user.to_dict()
        }
    

class Doctor(Base):
    __tablename__ = 'Doctor'

    IdDoctor =  Column(String, ForeignKey('User.IdUser'), primary_key=True)
    Cedula = Column(String)
    Especialidad = Column(String)

    user = relationship("User")

    def to_dict(self):

        return {
            "IdDoctor" : self.IdDoctor,
            "Cedula" : self.Cedula,
            "Especialidad" : self.Especialidad,
            "data": self.user.to_dict()
        }
    
class RevisionCardiaca(Base):
    __tablename__ = 'RevisionCardiaca'

    IdRevisionCa =  Column(String, primary_key=True)
    imgFrecuencia = Column(String)
    PrimerPuntoX = Column(Float)
    PrimerPuntoY = Column(Float)
    PuntoMasAltoX = Column(Float)
    PuntoMasAltoY = Column(Float)
    PuntoFinalX = Column(Float)	
    PuntoFinalY	= Column(Float)
    QSignalX = Column(Float) 
    QSignalY = Column(Float)
    SSignalX = Column(Float)
    SSignalY = Column(Float)
    TSignalX = Column(Float)
    TSignalY = Column(Float)
    PSignalX = Column(Float)
    PSignalY = Column(Float)

    def to_dict(self):

        return {
            "IdRevisionCa" : self.IdRevisionCa,
            "imgFrecuencia" : self.imgFrecuencia, 
            "PrimerPuntoX" : self.PrimerPuntoX,
            "PrimerPuntoY" : self.PrimerPuntoY,
            "PuntoMasAltoX" : self.PuntoMasAltoX,
            "PuntoMasAltoY" : self.PuntoMasAltoY,
            "PuntoFinalX" : self.PuntoFinalX,
            "PuntoFinalY" : self.PuntoFinalY,
            "QSignalX" : self.QSignalX, 
            "QSignalY" : self.QSignalY,
            "SSignalX" : self.SSignalX,
            "SSignalY" : self.SSignalY,
            "TSignalX" : self.TSignalX,
            "TSignalY" : self.TSignalY,
            "PSignalX" : self.PSignalX,
            "PSignalY" : self.PSignalY,            
        }

class Consulta(Base):
    __tablename__ = 'Consulta'

    IdConsulta = Column(String, primary_key=True)
    FechaConsulta = Column(Date)
    HoraConsulta = Column(DateTime)
    IdFDoctor = Column(String, ForeignKey('Doctor.IdDoctor'))
    IdFPaciente = Column(String, ForeignKey('Paciente.IdPaciente'))
    IdFRevisionCa = Column(String, ForeignKey('RevisionCardiaca.IdRevisionCa'))
    Estado = Column(String)
    FrecuenciaCardiaca = Column(Float)
    
    #user = relationship("User")

    def to_dict(self):

        return {
            "IdConsulta" : self.IdConsulta,
            "FechaConsulta" : self.FechaConsulta,
            "HoraConsulta" : self.HoraConsulta,
            "IdFDoctor" : self.IdFDoctor,
            "IdFPaciente" : self.IdFPaciente,
            "IdFRevisionCa" : self.IdFRevisionCa,
            "Estado" : self.Estado,
            "FrecuenciaCardiaca" : self.FrecuenciaCardiaca,
            #"user": self.user.to_dict()
        }