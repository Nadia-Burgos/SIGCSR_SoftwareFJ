"""
helpers/log_helper.py
Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Módulo de registro de eventos y errores para Software FJ.
Gestiona la escritura de logs en archivo con formato profesional,
garantizando trazabilidad de todas las operaciones del sistema.
"""

import os
import traceback
from datetime import datetime


class LogHelper:
    """
    Clase utilitaria para el registro de eventos del sistema.
    Todos sus métodos son estáticos para facilitar su uso sin instanciar.
    """

    # Nombre del archivo de log con la fecha actual
    NOMBRE_LOG = datetime.now().strftime("%Y-%m-%d") + ".log"

    # Ruta donde se guarda el archivo de log (carpeta logs/ en la raíz del proyecto)
    RUTA_LOG = os.path.join(os.path.dirname(__file__), "..", "logs", NOMBRE_LOG)

    @staticmethod
    def _asegurar_directorio() -> None:
        """
        Verifica que la carpeta logs/ exista.
        Si no existe, la crea automáticamente.
        """
        directorio = os.path.dirname(LogHelper.RUTA_LOG)
        os.makedirs(directorio, exist_ok=True)

    @staticmethod
    def _timestamp() -> str:
        """
        Retorna la fecha y hora actual con formato legible.
        Ejemplo: 10/05/2026 03:26:31 AM
        """
        return datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    @staticmethod
    def _escribir(nivel: str, mensaje: str) -> None:
        """
        Escribe una línea en el archivo de log con nivel y timestamp.

        Parámetros:
            nivel   (str): Nivel del mensaje (INFO, WARNING, ERROR).
            mensaje (str): Contenido del mensaje a registrar.
        """
        LogHelper._asegurar_directorio()
        # Formatear la línea con timestamp y nivel alineado
        linea = f"{LogHelper._timestamp()}  [{nivel:<7}]  {mensaje}\n"
        # Abrir en modo append para no sobreescribir logs anteriores
        with open(LogHelper.RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
        # También mostrar en consola para seguimiento en tiempo real
        print(linea.strip())

    @staticmethod
    def log(mensaje: str) -> None:
        """
        Registra un mensaje sin nivel (usado para separadores y encabezados).
        """
        LogHelper._asegurar_directorio()
        linea = f"{mensaje}\n"
        with open(LogHelper.RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
        print(linea.strip())

    @staticmethod
    def info(mensaje: str) -> None:
        """Registra un evento informativo normal."""
        LogHelper._escribir("INFO", mensaje)

    @staticmethod
    def advertencia(mensaje: str) -> None:
        """Registra una advertencia — situación anormal pero no crítica."""
        LogHelper._escribir("WARNING", mensaje)

    @staticmethod
    def error(mensaje: str) -> None:
        """Registra un error — situación que impidió completar una operación."""
        LogHelper._escribir("ERROR", mensaje)

    @staticmethod
    def error_excepcion(excepcion: Exception, contexto: str = "") -> None:
        """
        Registra un error junto con la traza completa de la excepción.
        Útil para diagnóstico detallado de fallos.

        Parámetros:
            excepcion (Exception): La excepción capturada.
            contexto  (str)      : Descripción opcional del contexto donde ocurrió.
        """
        tipo = type(excepcion).__name__
        mensaje = str(excepcion)
        ctx = f" | Contexto: {contexto}" if contexto else ""
        traza = traceback.format_exc()
        LogHelper._escribir("ERROR", f"{tipo}: {mensaje}{ctx}")
        # Registrar la traza completa solo en el archivo, no en consola
        LogHelper._asegurar_directorio()
        with open(LogHelper.RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"  Traza:\n{traza}\n")

    @staticmethod
    def inicio_modulo(nombre: str) -> None:
        """Registra el inicio de un módulo de simulación."""
        LogHelper.log(f"\n{'─' * 50}")
        LogHelper.info(f"START: Módulo [{nombre}]")
        LogHelper.log(f"{'─' * 50}")

    @staticmethod
    def fin_modulo(nombre: str) -> None:
        """Registra el fin de un módulo de simulación."""
        LogHelper.log(f"{'─' * 50}")
        LogHelper.info(f"END: Módulo [{nombre}]")
        LogHelper.log(f"{'─' * 50}\n")