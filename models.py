from datetime import date
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    stock_disponible = Column(Integer, nullable=False, default=0)

    prestamos = relationship("Prestamo", back_populates="equipo")

    __table_args__ = (
        CheckConstraint(
            "stock_disponible >= 0", name="chk_stock_no_negativo"
        ),
    )


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)

    prestamos = relationship("Prestamo", back_populates="estudiante")

    __table_args__ = (
        CheckConstraint("length(nombre) > 0", name="chk_nombre_no_vacio"),
        CheckConstraint("length(correo) > 0", name="chk_correo_no_vacio"),
    )


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    estudiante_id = Column(
        Integer, ForeignKey("estudiantes.id"), nullable=False
    )
    fecha = Column(
        String, nullable=False, default=lambda: date.today().isoformat()
    )
    cantidad = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="ACTIVO")

    equipo = relationship("Equipo", back_populates="prestamos")
    estudiante = relationship("Estudiante", back_populates="prestamos")

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="chk_cantidad_positiva"),
        CheckConstraint(
            "estado IN ('ACTIVO', 'DEVUELTO')", name="chk_estado_valido"
        ),
    )
