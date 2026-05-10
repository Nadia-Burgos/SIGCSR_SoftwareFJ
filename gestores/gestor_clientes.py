"""
gestores/gestor_clientes.py

Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Gestiona el registro, búsqueda y administración de clientes
en memoria, sin uso de base de datos.
"""

import re
from helpers.log_helper import LogHelper
from excepciones.excepciones_personalizadas import (
    ClienteInvalidoException,
    ClienteDuplicadoException,
    ClienteNoEncontradoException,
)


# =============================================================
# CLASE BASE ABSTRACTA
# =============================================================

class EntidadBase:
    """
    Clase abstracta base para todas las entidades del sistema.
    Define atributos y comportamientos comunes.
    """

    # Contador global para generar IDs únicos automáticamente
    _contador_ids: int = 0

    def __init__(self, nombre: str):
        # Incrementar contador y asignar ID único
        EntidadBase._contador_ids += 1
        self._id = EntidadBase._contador_ids
        self._nombre = nombre.strip()

    @property
    def id(self) -> int:
        """Retorna el ID único de la entidad."""
        return self._id

    @property
    def nombre(self) -> str:
        """Retorna el nombre de la entidad."""
        return self._nombre

    def describir(self) -> str:
        """Retorna descripción de la entidad. Debe sobrescribirse."""
        raise NotImplementedError("El método describir() debe implementarse.")

    def validar(self) -> bool:
        """Valida los datos de la entidad. Debe sobrescribirse."""
        raise NotImplementedError("El método validar() debe implementarse.")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id}, nombre='{self._nombre}')"


# =============================================================
# CLASE CLIENTE
# =============================================================

class Cliente(EntidadBase):
    """
    Representa un cliente registrado en Software FJ.
    Encapsula datos personales con validaciones estrictas
    y acceso controlado mediante propiedades.
    """

    def __init__(self, nombre: str, email: str, telefono: str, identificacion: str):
        # Validar nombre antes de llamar al constructor base
        if not nombre or not nombre.strip():
            raise ClienteInvalidoException("El nombre no puede estar vacío.", campo="nombre")

        super().__init__(nombre)

        # Validar y asignar cada campo con sus reglas específicas
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)
        self._identificacion = self._validar_identificacion(identificacion)
        self._activo = True  # Todo cliente inicia activo

    # ── Validaciones privadas ──────────────────────────────

    @staticmethod
    def _validar_email(email: str) -> str:
        """Valida que el email tenga formato correcto (usuario@dominio.ext)."""
        if not email or not re.match(r"^[\w.\-+]+@[\w\-]+\.\w{2,}$", str(email).strip()):
            raise ClienteInvalidoException(
                f"'{email}' no tiene formato válido (ej: usuario@dominio.com).",
                campo="email"
            )
        return email.strip().lower()

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        """Valida que el teléfono tenga entre 7 y 15 dígitos."""
        limpio = re.sub(r"[\s\-()]", "", str(telefono))
        if not limpio.lstrip("+").isdigit() or not (7 <= len(limpio.lstrip("+")) <= 15):
            raise ClienteInvalidoException(
                f"'{telefono}' no es válido. Debe tener entre 7 y 15 dígitos.",
                campo="telefono"
            )
        return limpio

    @staticmethod
    def _validar_identificacion(identificacion: str) -> str:
        """Valida que la identificación tenga al menos 5 caracteres."""
        limpia = str(identificacion).strip()
        if not limpia or len(limpia) < 5:
            raise ClienteInvalidoException(
                f"'{identificacion}' debe tener al menos 5 caracteres.",
                campo="identificacion"
            )
        return limpia

    # ── Propiedades (encapsulación) ────────────────────────

    @property
    def email(self) -> str:
        """Retorna el email del cliente."""
        return self._email

    @property
    def telefono(self) -> str:
        """Retorna el teléfono del cliente."""
        return self._telefono

    @property
    def identificacion(self) -> str:
        """Retorna la identificación del cliente."""
        return self._identificacion

    @property
    def activo(self) -> bool:
        """Retorna True si el cliente está activo."""
        return self._activo

    def desactivar(self):
        """Desactiva el cliente, impidiendo nuevas reservas."""
        self._activo = False

    # ── Métodos de EntidadBase ─────────────────────────────

    def describir(self) -> str:
        """Retorna descripción completa del cliente."""
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente #{self._id}\n"
            f"  Nombre        : {self._nombre}\n"
            f"  Identificación: {self._identificacion}\n"
            f"  Email         : {self._email}\n"
            f"  Teléfono      : {self._telefono}\n"
            f"  Estado        : {estado}"
        )

    def validar(self) -> bool:
        """Verifica que todos los campos obligatorios estén presentes."""
        return bool(self._nombre and self._email and self._telefono and self._identificacion)

    def __str__(self):
        return f"Cliente('{self._nombre}', {self._email})"


# =============================================================
# GESTOR DE CLIENTES
# =============================================================

class GestorClientes:
    """
    Administra la colección de clientes en memoria.
    Permite registrar, buscar, listar y desactivar clientes.
    """

    def __init__(self):
        # Diccionario que almacena clientes con identificación como clave
        self._clientes: dict[str, Cliente] = {}

    def registrar(self, nombre: str, email: str, telefono: str, identificacion: str) -> Cliente:
        """
        Registra un nuevo cliente en el sistema.

        Parámetros:
            nombre        (str): Nombre completo del cliente.
            email         (str): Correo electrónico.
            telefono      (str): Número de teléfono.
            identificacion(str): Cédula o identificación única.

        Retorna:
            Cliente: El objeto cliente registrado exitosamente.

        Lanza:
            ClienteInvalidoException  : Si los datos no son válidos.
            ClienteDuplicadoException : Si ya existe un cliente con esa identificación.
        """
        try:
            # Verificar duplicado antes de crear el objeto
            if identificacion.strip() in self._clientes:
                raise ClienteDuplicadoException(identificacion)

            # Crear cliente (las validaciones ocurren en el constructor)
            cliente = Cliente(nombre, email, telefono, identificacion)

            # Guardar en el diccionario usando identificación como clave
            self._clientes[cliente.identificacion] = cliente

            LogHelper.info(f"FINISH: Operación --- Registrar cliente: Cliente registrado exitosamente.")
            return cliente

        except (ClienteInvalidoException, ClienteDuplicadoException):
            # Re-lanzar excepciones conocidas sin modificarlas
            raise
        except Exception as e:
            # Encadenar cualquier error inesperado
            raise ClienteInvalidoException(f"Error inesperado al registrar cliente: {e}") from e

    def buscar(self, identificacion: str) -> Cliente:
        """
        Busca un cliente por su identificación.

        Lanza:
            ClienteNoEncontradoException: Si no existe el cliente.
        """
        cliente = self._clientes.get(identificacion.strip())
        if not cliente:
            raise ClienteNoEncontradoException(identificacion)
        return cliente

    def listar(self) -> list[Cliente]:
        """Retorna la lista de todos los clientes registrados."""
        return list(self._clientes.values())

    def total(self) -> int:
        """Retorna el número total de clientes registrados."""
        return len(self._clientes)