"""
ALQUILAPC - versión de consola (proyecto1.py).
Usa las mismas reglas de negocio que la aplicación web (liquidacion/calculos.py).

Ejecutar:  python proyecto1.py
"""
from liquidacion.calculos import MODALIDADES, ErrorValidacion, calcular_valores

OPCIONES = {"1": "CIUDAD", "2": "FUERA", "3": "ESTABLECIMIENTO"}


def pesos(valor):
    return "$" + f"{int(valor):,}".replace(",", ".")


def imprimir_recibo(l):
    print("\n========== RECIBO ALQUILAPC ==========")
    print(f"Cliente ................ {l.nombre}")
    print(f"Opción de alquiler ..... {l.modalidad_texto}")
    print(f"Equipos alquilados ..... {l.equipos}")
    print(f"Días iniciales ......... {l.dias_iniciales}")
    print(f"Días adicionales ....... {l.dias_adicionales}")
    print(f"Valor alquiler ......... {pesos(l.valor_alquiler)}")
    print(f"Valor adicionales ...... {pesos(l.valor_adicional_bruto)}")
    print(f"Descuentos ............. {pesos(l.total_descuentos)}")
    print(f"Incremento domicilio ... {pesos(l.incremento_domicilio)}")
    print(f"TOTAL A PAGAR .......... {pesos(l.total)}")
    print("======================================\n")


def main():
    print("ALQUILAPC - Liquidación de servicio")
    nombre = input("Nombre del cliente: ")
    equipos = input("Número de equipos (mínimo 2): ")
    dias = input("Días iniciales: ")
    adicionales = input("Días adicionales (0 si no hay): ")
    for clave, codigo in OPCIONES.items():
        print(f"  {clave}. {MODALIDADES[codigo]}")
    opcion = input("Tipo de servicio: ").strip()
    try:
        l = calcular_valores(nombre, equipos, dias, adicionales, OPCIONES.get(opcion, opcion))
    except ErrorValidacion as exc:
        print("\nNo se puede generar el recibo:")
        for mensaje in exc.errores.values():
            print(f"  - {mensaje}")
        return 1
    imprimir_recibo(l)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
