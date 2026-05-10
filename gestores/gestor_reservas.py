"""
gestores/gestor_reservas.py
Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Gestiona el ciclo de vida completo de las reservas en Software FJ:
creación, confirmación, procesamiento y cancelación.
Implementa manejo robusto de excepciones en cada operación.
"""

from enum import Enum
from datetime import datetime
from helpers.log_helper import LogHelper
from excepciones.excepciones_personalizadas import (
    ReservaInvalidaException,
    ReservaNoEncontradaException,
    ReservaDuplicadaException,
    ServicioNoDisponibleException,
    ClienteInvalidoException,
)


# =============================================================
# ENUMERACIÓN DE ESTADOS DE RESERVA
# =============================================================

class EstadoReserva(Enum):
    """
    Define los posibles estados del ciclo de vida de una reserva.
    Usar Enum garantiza que solo se usen valores válidos.
    """
    PENDIENTE   = "Pendiente"    # Reserva creada pero no confirmada
    CONFIRMADA  = "Confirmada"   # Reserva confirmada por el sistema
    EN_PROCESO  = "En proceso"   # Servicio siendo usado actualmente
    COMPLETADA  = "Completada"   # Servicio finalizado exitosamente
    CANCELADA   = "Cancelada"    # Reserva cancelada antes de usarse


# =============================================================
# CLASE RESERVA
# =============================================================

class Reserva:
    """
    Representa una reserva de servicio hecha por un cliente.
    Integra cliente, servicio, duración y estado con manejo de excepciones.
    """

    # Contador para generar IDs únicos de reserva
    _contador: int = 0

    def __init__(self, cliente, servicio, duracion_horas: float):
        # Validar que el cliente exista y esté activo
        if cliente is None:
            raise ReservaInvalidaException("El cliente no puede ser nulo.")
        if not cliente.activo:
            raise ClienteInvalidoException(
                f"El cliente '{cliente.nombre}' está inactivo y no puede hacer reservas.",
                campo="cliente"
            )

        # Validar que el servicio exista y esté disponible
        if servicio is None:
            raise ReservaInvalidaException("El servicio no puede ser nulo.")
        if not servicio.disponible:
            raise ServicioNoDisponibleException(
                servicio.nombre, "El servicio no está disponible para reservar."
            )

        # Validar parámetros específicos del servicio (duración, etc.)
        servicio.validar_parametros(duracion_horas)

        # Generar ID único para la reserva
        Reserva._contador += 1
        self._id = f"RES-{Reserva._contador:04d}"
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = EstadoReserva.PENDIENTE        # Estado inicial siempre es PENDIENTE
        self._fecha_creacion = datetime.now()          # Fecha y hora de creación
        self._costo_total = servicio.calcular_costo(duracion_horas)  # Costo calculado

    # ── Propiedades ───────────────────────────────────────

    @property
    def id(self) -> str:
        """Retorna el ID único de la reserva."""
        return self._id

    @property
    def cliente(self):
        """Retorna el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Retorna el servicio reservado."""
        return self._servicio

    @property
    def duracion_horas(self) -> float:
        """Retorna la duración en horas de la reserva."""
        return self._duracion_horas

    @property
    def estado(self) -> EstadoReserva:
        """Retorna el estado actual de la reserva."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        return self._costo_total

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora en que se creó la reserva."""
        return self._fecha_creacion

    # ── Operaciones del ciclo de vida ─────────────────────

    def confirmar(self) -> None:
        """
        Confirma la reserva, pasando de PENDIENTE a CONFIRMADA.
        Usa try/except/else para manejar el flujo correctamente.

        Lanza:
            ReservaInvalidaException: Si la reserva no está en estado PENDIENTE.
        """
        try:
            # Verificar que esté en el estado correcto para confirmar
            if self._estado != EstadoReserva.PENDIENTE:
                raise ReservaInvalidaException(
                    f"Solo se pueden confirmar reservas en estado PENDIENTE. "
                    f"Estado actual: {self._estado.value}"
                )
        except ReservaInvalidaException:
            # Re-lanzar la excepción conocida
            raise
        else:
            # El bloque else se ejecuta solo si no hubo excepción
            self._estado = EstadoReserva.CONFIRMADA
            LogHelper.info(f"Reserva {self._id} confirmada para '{self._cliente.nombre}'.")

    def procesar(self) -> None:
        """
        Pone la reserva en proceso (servicio siendo usado).
        Usa try/except/finally para garantizar registro del intento.

        Lanza:
            ReservaInvalidaException: Si la reserva no está CONFIRMADA.
        """
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaException(
                    f"Solo se pueden procesar reservas CONFIRMADAS. "
                    f"Estado actual: {self._estado.value}"
                )
            self._estado = EstadoReserva.EN_PROCESO
            LogHelper.info(f"Reserva {self._id} en proceso.")
        except ReservaInvalidaException:
            raise
        finally:
            # El bloque finally siempre se ejecuta, haya o no error
            LogHelper.info(f"Intento de procesamiento registrado para reserva {self._id}.")

    def completar(self) -> None:
        """
        Marca la reserva como completada.

        Lanza:
            ReservaInvalidaException: Si la reserva no está EN_PROCESO.
        """
        try:
            if self._estado != EstadoReserva.EN_PROCESO:
                raise ReservaInvalidaException(
                    f"Solo se pueden completar reservas EN PROCESO. "
                    f"Estado actual: {self._estado.value}"
                )
        except ReservaInvalidaException:
            raise
        else:
            self._estado = EstadoReserva.COMPLETADA
            LogHelper.info(f"Reserva {self._id} completada. Costo: ${self._costo_total:,.0f}")

    def cancelar(self, motivo: str = "") -> None:
        """
        Cancela la reserva si está en estado PENDIENTE o CONFIRMADA.

        Parámetros:
            motivo (str): Razón opcional de la cancelación.

        Lanza:
            ReservaInvalidaException: Si la reserva no puede cancelarse.
        """
        estados_cancelables = {EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA}
        try:
            if self._estado not in estados_cancelables:
                raise ReservaInvalidaException(
                    f"No se puede cancelar una reserva en estado '{self._estado.value}'."
                )
        except ReservaInvalidaException:
            raise
        else:
            self._estado = EstadoReserva.CANCELADA
            razon = f" Motivo: {motivo}" if motivo else ""
            LogHelper.info(f"Reserva {self._id} cancelada.{razon}")

    def describir(self) -> str:
        """Retorna descripción completa del estado actual de la reserva."""
        return (
            f"Reserva {self._id}\n"
            f"  Cliente     : {self._cliente.nombre}\n"
            f"  Servicio    : {self._servicio.nombre}\n"
            f"  Duración    : {self._duracion_horas} horas\n"
            f"  Costo total : ${self._costo_total:,.0f}\n"
            f"  Estado      : {self._estado.value}\n"
            f"  Creada      : {self._fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
        )

    def __str__(self):
        return f"Reserva({self._id}, {self._cliente.nombre}, {self._estado.value})"


# =============================================================
# GESTOR DE RESERVAS
# =============================================================

class GestorReservas:
    """
    Administra todas las reservas del sistema en memoria.
    Permite crear, buscar, listar y cancelar reservas.
    """

    def __init__(self):
        # Diccionario con ID de reserva como clave
        self._reservas: dict[str, Reserva] = {}

    def crear(self, cliente, servicio, duracion_horas: float) -> Reserva:
        """
        Crea una nueva reserva en el sistema.

        Parámetros:
            cliente        : Objeto Cliente válido y activo.
            servicio       : Objeto Servicio disponible.
            duracion_horas : Duración en horas del servicio.

        Retorna:
            Reserva: La reserva creada exitosamente.
        """
        try:
            # Crear la reserva (las validaciones ocurren en el constructor)
            reserva = Reserva(cliente, servicio, duracion_horas)

            # Verificar que no exista ya una reserva con el mismo ID
            if reserva.id in self._reservas:
                raise ReservaDuplicadaException(reserva.id)

            # Guardar la reserva en memoria
            self._reservas[reserva.id] = reserva
            LogHelper.info(
                f"FINISH: Reserva creada: {reserva.id} | "
                f"Cliente: {cliente.nombre} | Servicio: {servicio.nombre}"
            )
            return reserva

        except (ReservaInvalidaException, ReservaDuplicadaException,
                ServicioNoDisponibleException, ClienteInvalidoException):
            # Re-lanzar excepciones conocidas del dominio
            raise
        except Exception as e:
            # Encadenar errores inesperados con contexto
            raise ReservaInvalidaException(
                f"Error inesperado al crear reserva: {e}"
            ) from e

    def buscar(self, id_reserva: str) -> Reserva:
        """
        Busca una reserva por su ID.

        Lanza:
            ReservaNoEncontradaException: Si no existe la reserva.
        """
        reserva = self._reservas.get(id_reserva.strip())
        if not reserva:
            raise ReservaNoEncontradaException(id_reserva)
        return reserva

    def listar(self) -> list:
        """Retorna todas las reservas registradas."""
        return list(self._reservas.values())

    def listar_por_estado(self, estado: EstadoReserva) -> list:
        """Retorna solo las reservas que tienen el estado indicado."""
        return [r for r in self._reservas.values() if r.estado == estado]

    def total(self) -> int:
        """Retorna el número total de reservas registradas."""
        return len(self._reservas)