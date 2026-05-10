"""
main.py
Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Punto de entrada principal del sistema Software FJ.
Inicializa y ejecuta todas las simulaciones del sistema
de gestión de clientes, servicios y reservas.

Uso:
    python main.py
"""

import sys
from datetime import datetime
from helpers.log_helper import LogHelper
from simulaciones.simulador_sistema import SimuladorSistema


def main():
    """
    Función principal del sistema Software FJ.
    Gestiona el inicio, ejecución y cierre ordenado del sistema.
    """

    # Registrar el momento de inicio para calcular tiempo total
    inicio = datetime.now()

    try:
        # Mostrar encabezado del sistema en log y consola
        LogHelper.log("=" * 60)
        LogHelper.log("   SISTEMA: Software FJ — Gestión Integral")
        LogHelper.log("   Clientes, Servicios y Reservas")
        LogHelper.log("=" * 60)
        LogHelper.info(f"Sistema iniciado: {inicio.strftime('%d/%m/%Y %H:%M:%S')}")

        # Crear instancia del simulador e iniciar simulaciones
        simulador = SimuladorSistema()
        simulador.ejecutar_todas()

    except Exception as error_critico:
        # Capturar cualquier error crítico que no fue manejado antes
        LogHelper.error(f"ERROR CRÍTICO inesperado: {error_critico}")

    finally:
        # Este bloque siempre se ejecuta, haya o no error
        fin = datetime.now()
        tiempo = (fin - inicio).total_seconds()
        LogHelper.log("=" * 60)
        LogHelper.info(f"Sistema finalizado en {tiempo:.4f} segundos.")
        LogHelper.log("=" * 60)


# Punto de entrada cuando se ejecuta directamente
if __name__ == "__main__":
    main()
    