from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Equipo, Estudiante, Prestamo

#CRUD Equipos
def crear_equipo(db: Session, nombre: str, tipo: str, stock_disponible: int):
    if stock_disponible < 0:
        raise ValueError("El stock no puede ser negativo.")
    equipo = Equipo(
        nombre=nombre, tipo=tipo, stock_disponible=stock_disponible
    )
    db.add(equipo)
    db.commit()
    db.refresh(equipo)
    return equipo


def listar_equipos(db: Session):
    return db.scalars(select(Equipo)).all()


def buscar_equipo_por_id(db: Session, equipo_id: int):
    return db.get(Equipo, equipo_id)


def actualizar_equipo(
    db: Session,
    equipo_id: int,
    nombre: str = None,
    tipo: str = None,
    stock: int = None,
):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise ValueError("Equipo no encontrado.")
    if nombre:
        equipo.nombre = nombre
    if tipo:
        equipo.tipo = tipo
    if stock is not None:
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        equipo.stock_disponible = stock
    db.commit()
    db.refresh(equipo)
    return equipo


def eliminar_equipo(db: Session, equipo_id: int):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise ValueError("Equipo no encontrado.")
    if equipo.prestamos:
        raise ValueError(
            "No se puede eliminar: el equipo tiene préstamos asociados."
        )
    db.delete(equipo)
    db.commit()
    return True


# CRUD Estudiantes


def registrar_estudiante(db: Session, nombre: str, correo: str):
    if not nombre.strip() or not correo.strip():
        raise ValueError("El nombre y el correo no pueden estar vacíos.")

    existente = db.scalar(
        select(Estudiante).where(Estudiante.correo == correo.strip())
    )
    if existente:
        raise ValueError("Ya existe un estudiante registrado con este correo.")

    estudiante = Estudiante(nombre=nombre.strip(), correo=correo.strip())
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    return estudiante


def listar_estudiantes(db: Session):
    return db.scalars(select(Estudiante)).all()


# Prestamos y devoluciones

def registrar_prestamo(
    db: Session,
    equipo_id: int,
    estudiante_id: int,
    cantidad: int,
    fecha_str: str = None,
):
    if cantidad <= 0:
        raise ValueError("La cantidad prestada debe ser un entero positivo.")

    equipo = db.get(Equipo, equipo_id)
    estudiante = db.get(Estudiante, estudiante_id)

    if not equipo:
        raise ValueError("El equipo especificado no existe.")
    if not estudiante:
        raise ValueError("El estudiante especificado no existe.")
    if equipo.stock_disponible < cantidad:
        raise ValueError(
            f"Stock insuficiente. Disponibles: {equipo.stock_disponible}, Solicitados: {cantidad}"
        )

    if fecha_str is None:
        fecha_str = date.today().isoformat()

    equipo.stock_disponible -= cantidad
    prestamo = Prestamo(
        equipo_id=equipo_id,
        estudiante_id=estudiante_id,
        cantidad=cantidad,
        fecha=fecha_str,
        estado="ACTIVO",
    )
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def procesar_devolucion(db: Session, prestamo_id: int):
    prestamo = db.get(Prestamo, prestamo_id)
    if not prestamo:
        raise ValueError("El préstamo no existe.")
    if prestamo.estado == "DEVUELTO":
        raise ValueError("El préstamo ya fue devuelto previamente.")

    prestamo.equipo.stock_disponible += prestamo.cantidad
    prestamo.estado = "DEVUELTO"
    db.commit()
    return prestamo
