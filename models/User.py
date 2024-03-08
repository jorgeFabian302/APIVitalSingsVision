from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    IdUser =  Column(Integer, primary_key=True)
    Nombre = Column(String)
    Apellidos = Column(String)
    Correo = Column(String)
    Password = Column(String)
    Tipo = Column(String)
    FechaNacimiento = Column(Date)
    FotoPerfil = Column(String)
    
    def to_dict(self):
        fec_nac = self.FechaNacimiento.strftime("%Y-%m-%d") if self.FechaNacimiento else None
        return {
            "IdUser": self.IdUser,
            "Nombre": self.Nombre,
            "Apellidos": self.Apellidos,
            "Correo": self.Correo,
            "Tipo": self.Tipo,
            "FechaNacimiento": fec_nac,
            "FotoPerfil": self.FotoPerfil
        }