from models import Base
from crud import (
    actualizar_equipo,
    buscar_equipo_por_id,
    crear_equipo,
    eliminar_equipo,
    listar_equipos,
    listar_estudiantes,
    procesar_devolucion,
    registrar_estudiante,
    registrar_prestamo,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///sistema_prestamos.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def menu():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    while True:
        print("\n--- SISTEMA DE PRÉSTAMOS DE EQUIPAMIENTO TECNOLÓGICO ---")
        print("1. Registrar nuevo equipo")
        print("2. Listar equipos")
        print("3. Buscar equipo por ID")
        print("4. Actualizar equipo")
        print("5. Eliminar equipo")
        print("6. Registrar estudiante")
        print("7. Listar estudiantes")
        print("8. Registrar préstamo")
        print("9. Procesar devolución")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                nombre = input("Nombre del equipo: ")
                tipo = input("Tipo (ej. Notebook, Proyector): ")
                stock = int(input("Stock inicial: "))
                eq = crear_equipo(db, nombre, tipo, stock)
                print(f"-> Equipo registrado exitosamente (ID: {eq.id})")

            elif opcion == "2":
                equipos = listar_equipos(db)
                print("\nLISTADO DE EQUIPOS:")
                for e in equipos:
                    print(
                        f"ID: {e.id} | Nombre: {e.nombre} | Tipo: {e.tipo} | Stock Disponible: {e.stock_disponible}"
                    )

            elif opcion == "3":
                eq_id = int(input("ID del equipo: "))
                eq = buscar_equipo_por_id(db, eq_id)
                if eq:
                    print(
                        f"ID: {eq.id} | Nombre: {eq.nombre} | Tipo: {eq.tipo} | Stock: {eq.stock_disponible}"
                    )
                else:
                    print("-> Equipo no encontrado.")

            elif opcion == "4":
                eq_id = int(input("ID del equipo a actualizar: "))
                nombre = input("Nuevo nombre (Enter para omitir): ")
                tipo = input("Nuevo tipo (Enter para omitir): ")
                stock_input = input("Nuevo stock (Enter para omitir): ")
                stock = int(stock_input) if stock_input.strip() else None
                actualizar_equipo(
                    db,
                    eq_id,
                    nombre or None,
                    tipo or None,
                    stock,
                )
                print("-> Equipo actualizado correctamente.")

            elif opcion == "5":
                eq_id = int(input("ID del equipo a eliminar: "))
                eliminar_equipo(db, eq_id)
                print("-> Equipo eliminado correctamente.")

            elif opcion == "6":
                nombre = input("Nombre del estudiante: ")
                correo = input("Correo electrónico: ")
                est = registrar_estudiante(db, nombre, correo)
                print(f"-> Estudiante registrado exitosamente (ID: {est.id})")

            elif opcion == "7":
                estudiantes = listar_estudiantes(db)
                print("\nLISTADO DE ESTUDIANTES:")
                for e in estudiantes:
                    print(f"ID: {e.id} | Nombre: {e.nombre} | Correo: {e.correo}")

            elif opcion == "8":
                eq_id = int(input("ID del equipo: "))
                est_id = int(input("ID del estudiante: "))
                cant = int(input("Cantidad a prestar: "))
                p = registrar_prestamo(db, eq_id, est_id, cant)
                print(
                    f"-> Préstamo registrado exitosamente (ID Préstamo: {p.id})"
                )

            elif opcion == "9":
                p_id = int(input("ID del préstamo a devolver: "))
                procesar_devolucion(db, p_id)
                print("-> Devolución procesada correctamente.")

            elif opcion == "0":
                print("Cerrando programa...")
                break

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError as err:
            print(f"[ERROR DE VALIDACIÓN] {err}")
        except Exception as err:
            print(f"[ERROR INESPERADO] {err}")

    db.close()


if __name__ == "__main__":
    menu()
