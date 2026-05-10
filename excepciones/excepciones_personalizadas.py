"""
Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Define todas las excepciones personalizadas del sistema Software FJ.
Implementa una jerarquía clara de errores para manejar situaciones
específicas del dominio: clientes, servicios, reservas y cálculos.
"""


# =============================================================
# EXCEPCIÓN BASE DEL SISTEMA
# =============================================================

class SoftwareFJException(Exception):
    """
    Excepción base de la que heredan todas las excepciones del sistema.
    Permite capturar cualquier error del dominio con un solo bloque except.

    Atributos:
        mensaje (str): Descripción del error.
        codigo  (str): Código identificador del error (opcional).
    """

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Guardar el mensaje y código como atributos accesibles
        self.mensaje = mensaje
        self.codigo = codigo
        # Llamar al constructor de Exception para que str(excepción) funcione bien
        super().__init__(f"[{codigo}] {mensaje}")

    def __str__(self) -> str:
        # Representación legible del error con código y mensaje
        return f"[{self.codigo}] {self.mensaje}"

    def __repr__(self) -> str:
        # Representación técnica útil para depuración
        return f"{self.__class__.__name__}(codigo='{self.codigo}', mensaje='{self.mensaje}')"


# =============================================================
# EXCEPCIONES DE CLIENTE
# =============================================================

class ClienteException(SoftwareFJException):
    """Excepción base para errores relacionados con clientes."""

    def __init__(self, mensaje: str, codigo: str = "ERR_CLIENTE"):
        super().__init__(mensaje, codigo)


class ClienteInvalidoException(ClienteException):
    """
    Se lanza cuando los datos de un cliente no cumplen las validaciones.
    Ejemplo: nombre vacío, email con formato incorrecto, identificación inválida.
    """

    def __init__(self, mensaje: str, campo: str = ""):
        # Agregar el campo específico que falló al mensaje de error
        detalle = f" (Campo: '{campo}')" if campo else ""
        super().__init__(
            f"Datos del cliente inválidos{detalle}: {mensaje}",
            codigo="ERR_CLIENTE_INVALIDO"
        )
        self.campo = campo  # Guardar el campo para uso posterior


class ClienteDuplicadoException(ClienteException):
    """
    Se lanza cuando se intenta registrar un cliente que ya existe
    (misma identificación).
    """

    def __init__(self, identificacion: str):
        super().__init__(
            f"Ya existe un cliente registrado con la identificación '{identificacion}'.",
            codigo="ERR_CLIENTE_DUPLICADO"
        )
        self.identificacion = identificacion


class ClienteNoEncontradoException(ClienteException):
    """
    Se lanza cuando se busca un cliente que no existe en el sistema.
    """

    def __init__(self, identificacion: str):
        super().__init__(
            f"No se encontró ningún cliente con la identificación '{identificacion}'.",
            codigo="ERR_CLIENTE_NO_ENCONTRADO"
        )
        self.identificacion = identificacion


# =============================================================
# EXCEPCIONES DE SERVICIO
# =============================================================

class ServicioException(SoftwareFJException):
    """Excepción base para errores relacionados con servicios."""

    def __init__(self, mensaje: str, codigo: str = "ERR_SERVICIO"):
        super().__init__(mensaje, codigo)


class ServicioInvalidoException(ServicioException):
    """
    Se lanza cuando los parámetros de un servicio no son válidos.
    Ejemplo: tarifa negativa, capacidad cero, nombre vacío.
    """

    def __init__(self, mensaje: str, campo: str = ""):
        detalle = f" (Campo: '{campo}')" if campo else ""
        super().__init__(
            f"Parámetros del servicio inválidos{detalle}: {mensaje}",
            codigo="ERR_SERVICIO_INVALIDO"
        )
        self.campo = campo


class ServicioNoDisponibleException(ServicioException):
    """
    Se lanza cuando un servicio no está disponible para ser reservado.
    Ejemplo: sala ya reservada, equipo fuera de servicio.
    """

    def __init__(self, nombre_servicio: str, motivo: str = ""):
        razon = f" Motivo: {motivo}" if motivo else ""
        super().__init__(
            f"El servicio '{nombre_servicio}' no está disponible.{razon}",
            codigo="ERR_SERVICIO_NO_DISPONIBLE"
        )
        self.nombre_servicio = nombre_servicio


class ServicioNoEncontradoException(ServicioException):
    """
    Se lanza cuando se busca un servicio que no existe en el sistema.
    """

    def __init__(self, codigo_servicio: str):
        super().__init__(
            f"No se encontró ningún servicio con el código '{codigo_servicio}'.",
            codigo="ERR_SERVICIO_NO_ENCONTRADO"
        )
        self.codigo_servicio = codigo_servicio


# =============================================================
# EXCEPCIONES DE RESERVA
# =============================================================

class ReservaException(SoftwareFJException):
    """Excepción base para errores relacionados con reservas."""

    def __init__(self, mensaje: str, codigo: str = "ERR_RESERVA"):
        super().__init__(mensaje, codigo)


class ReservaInvalidaException(ReservaException):
    """
    Se lanza cuando los datos de una reserva no son válidos.
    Ejemplo: duración negativa, cliente nulo, servicio nulo.
    """

    def __init__(self, mensaje: str):
        super().__init__(
            f"Reserva inválida: {mensaje}",
            codigo="ERR_RESERVA_INVALIDA"
        )


class ReservaNoEncontradaException(ReservaException):
    """
    Se lanza cuando se busca una reserva que no existe.
    """

    def __init__(self, id_reserva: str):
        super().__init__(
            f"No se encontró la reserva con ID '{id_reserva}'.",
            codigo="ERR_RESERVA_NO_ENCONTRADA"
        )
        self.id_reserva = id_reserva


class ReservaDuplicadaException(ReservaException):
    """
    Se lanza cuando se intenta crear una reserva que ya existe
    o que entra en conflicto con otra existente.
    """

    def __init__(self, id_reserva: str):
        super().__init__(
            f"Ya existe una reserva activa con ID '{id_reserva}'.",
            codigo="ERR_RESERVA_DUPLICADA"
        )
        self.id_reserva = id_reserva


# =============================================================
# EXCEPCIONES DE CÁLCULO
# =============================================================

class CalculoException(SoftwareFJException):
    """Excepción base para errores en cálculos financieros."""

    def __init__(self, mensaje: str, codigo: str = "ERR_CALCULO"):
        super().__init__(mensaje, codigo)


class DescuentoInvalidoException(CalculoException):
    """
    Se lanza cuando el porcentaje de descuento no está en el rango válido (0-100%).
    """

    def __init__(self, porcentaje: float):
        super().__init__(
            f"El porcentaje de descuento '{porcentaje}' no es válido. "
            f"Debe estar entre 0.0 y 1.0 (0% a 100%).",
            codigo="ERR_DESCUENTO_INVALIDO"
        )
        self.porcentaje = porcentaje