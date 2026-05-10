"""
gestores/gestor_servicios.py

Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Define la clase abstracta Servicio y tres servicios especializados:
  - ReservaSala      : Reserva de salas de reuniones.
  - AlquilerEquipo   : Alquiler de equipos tecnológicos.
  - AsesoriaEspecializada: Asesorías profesionales por horas.

Implementa polimorfismo mediante métodos sobrescritos en cada servicio.
"""

from abc import ABC, abstractmethod
from helpers.log_helper import LogHelper
from excepciones.excepciones_personalizadas import (
    ServicioInvalidoException,
    ServicioNoDisponibleException,
    ServicioNoEncontradoException,
    DescuentoInvalidoException,
)


# =============================================================
# CLASE ABSTRACTA SERVICIO
# =============================================================

class Servicio(ABC):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Define la interfaz común que cada servicio especializado debe implementar.
    """

    # Tasa de IVA aplicada en Colombia
    IVA = 0.19

    # Contador para generar códigos únicos de servicio
    _contador: int = 0

    def __init__(self, nombre: str, tarifa_hora: float, disponible: bool = True):
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ServicioInvalidoException("El nombre no puede estar vacío.", campo="nombre")
        # Validar que la tarifa no sea negativa
        if tarifa_hora < 0:
            raise ServicioInvalidoException(
                f"La tarifa no puede ser negativa: {tarifa_hora}", campo="tarifa_hora"
            )

        # Generar código único para el servicio
        Servicio._contador += 1
        self._codigo = f"SRV-{Servicio._contador:03d}"
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible

    # ── Propiedades ───────────────────────────────────────

    @property
    def codigo(self) -> str:
        """Retorna el código único del servicio."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        """Retorna la tarifa por hora del servicio."""
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        """Retorna True si el servicio está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        """Permite cambiar la disponibilidad del servicio."""
        self._disponible = valor

    # ── Métodos abstractos (polimorfismo) ─────────────────

    @abstractmethod
    def calcular_costo(self, duracion_horas: float) -> float:
        """Calcula el costo base del servicio para la duración indicada."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna descripción detallada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion_horas: float) -> bool:
        """Valida que la duración y parámetros sean correctos para este servicio."""
        pass

    # ── Métodos sobrecargados (parámetros opcionales) ─────

    def calcular_costo_con_impuestos(self, duracion_horas: float, tasa_iva: float = None) -> float:
        """
        Sobrecarga 1: Calcula el costo incluyendo IVA.
        Si no se especifica tasa, usa el IVA estándar del 19%.

        Parámetros:
            duracion_horas (float): Horas de uso del servicio.
            tasa_iva       (float): Tasa de IVA opcional (0.0 a 1.0).
        """
        # Usar IVA por defecto si no se especifica
        if tasa_iva is None:
            tasa_iva = self.IVA
        # Validar rango del IVA
        if not (0 <= tasa_iva <= 1):
            raise ServicioInvalidoException(
                f"La tasa de IVA debe estar entre 0 y 1, recibido: {tasa_iva}",
                campo="tasa_iva"
            )
        costo_base = self.calcular_costo(duracion_horas)
        return round(costo_base * (1 + tasa_iva), 2)

    def calcular_costo_con_descuento(
        self, duracion_horas: float, descuento: float = 0.0, aplicar_iva: bool = False
    ) -> float:
        """
        Sobrecarga 2: Calcula el costo con descuento e IVA opcionales.

        Parámetros:
            duracion_horas (float): Horas de uso del servicio.
            descuento      (float): Porcentaje de descuento (0.0 a 1.0).
            aplicar_iva    (bool) : Si True, agrega IVA al resultado.
        """
        # Validar rango del descuento
        if not (0 <= descuento < 1):
            raise DescuentoInvalidoException(descuento)
        costo_base = self.calcular_costo(duracion_horas)
        # Aplicar descuento al costo base
        costo_con_descuento = costo_base * (1 - descuento)
        # Aplicar IVA si se solicita
        if aplicar_iva:
            costo_con_descuento *= (1 + self.IVA)
        return round(costo_con_descuento, 2)

    def calcular_costo_paquete(self, horas_list: list, descuento_paquete: float = 0.0) -> float:
        """
        Sobrecarga 3: Calcula el costo total de múltiples sesiones (paquete).

        Parámetros:
            horas_list        (list ): Lista de duraciones en horas por sesión.
            descuento_paquete (float): Descuento global para el paquete (0.0 a 1.0).
        """
        if not horas_list:
            raise ServicioInvalidoException("La lista de horas no puede estar vacía.", campo="horas_list")
        if not (0 <= descuento_paquete < 1):
            raise DescuentoInvalidoException(descuento_paquete)
        # Sumar el costo de cada sesión
        total = sum(self.calcular_costo(h) for h in horas_list)
        # Aplicar descuento de paquete
        return round(total * (1 - descuento_paquete), 2)

    def __str__(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"[{self._codigo}] {self._nombre} — ${self._tarifa_hora:,.0f}/hora — {estado}"


# =============================================================
# SERVICIO 1: RESERVA DE SALA
# =============================================================

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reuniones.
    Cobra tarifa por hora con recargo si se requiere proyector.
    """

    RECARGO_PROYECTOR = 0.15  # 15% de recargo por uso de proyector

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = False):
        super().__init__(nombre, tarifa_hora)
        # Validar que la capacidad sea positiva
        if capacidad <= 0:
            raise ServicioInvalidoException(
                f"La capacidad debe ser mayor a 0, recibido: {capacidad}", campo="capacidad"
            )
        self._capacidad = capacidad
        self._tiene_proyector = tiene_proyector

    @property
    def capacidad(self) -> int:
        """Retorna la capacidad máxima de personas de la sala."""
        return self._capacidad

    @property
    def tiene_proyector(self) -> bool:
        """Retorna True si la sala tiene proyector."""
        return self._tiene_proyector

    def calcular_costo(self, duracion_horas: float) -> float:
        """
        Calcula el costo de la sala por horas.
        Agrega recargo del 15% si tiene proyector.
        """
        costo = self._tarifa_hora * duracion_horas
        # Aplicar recargo por proyector si aplica
        if self._tiene_proyector:
            costo *= (1 + self.RECARGO_PROYECTOR)
        return round(costo, 2)

    def describir(self) -> str:
        """Describe la sala con todas sus características."""
        proyector = "Sí" if self._tiene_proyector else "No"
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Sala de Reuniones [{self._codigo}]\n"
            f"  Nombre      : {self._nombre}\n"
            f"  Capacidad   : {self._capacidad} personas\n"
            f"  Proyector   : {proyector}\n"
            f"  Tarifa/hora : ${self._tarifa_hora:,.0f}\n"
            f"  Estado      : {estado}"
        )

    def validar_parametros(self, duracion_horas: float) -> bool:
        """Valida que la duración esté entre 1 y 12 horas."""
        if duracion_horas <= 0:
            raise ServicioInvalidoException(
                f"La duración debe ser mayor a 0 horas, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if duracion_horas > 12:
            raise ServicioInvalidoException(
                f"Una sala no puede reservarse por más de 12 horas, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if not self._disponible:
            raise ServicioNoDisponibleException(self._nombre, "Sala no disponible actualmente.")
        return True


# =============================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# =============================================================

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Cobra tarifa por hora más depósito de garantía opcional.
    """

    def __init__(self, nombre: str, tarifa_hora: float, tipo_equipo: str, deposito_garantia: float = 0.0):
        super().__init__(nombre, tarifa_hora)
        # Validar que el tipo de equipo no esté vacío
        if not tipo_equipo or not tipo_equipo.strip():
            raise ServicioInvalidoException("El tipo de equipo no puede estar vacío.", campo="tipo_equipo")
        # Validar que el depósito no sea negativo
        if deposito_garantia < 0:
            raise ServicioInvalidoException(
                f"El depósito no puede ser negativo: {deposito_garantia}", campo="deposito_garantia"
            )
        self._tipo_equipo = tipo_equipo.strip()
        self._deposito_garantia = deposito_garantia

    @property
    def tipo_equipo(self) -> str:
        """Retorna el tipo de equipo."""
        return self._tipo_equipo

    @property
    def deposito_garantia(self) -> float:
        """Retorna el depósito de garantía requerido."""
        return self._deposito_garantia

    def calcular_costo(self, duracion_horas: float) -> float:
        """
        Calcula el costo del alquiler por horas.
        No incluye el depósito (se cobra aparte y se devuelve).
        """
        return round(self._tarifa_hora * duracion_horas, 2)

    def calcular_costo_total_con_deposito(self, duracion_horas: float) -> float:
        """Calcula el costo incluyendo el depósito de garantía."""
        return round(self.calcular_costo(duracion_horas) + self._deposito_garantia, 2)

    def describir(self) -> str:
        """Describe el equipo con todas sus características."""
        estado = "Disponible" if self._disponible else "No disponible"
        deposito = f"${self._deposito_garantia:,.0f}" if self._deposito_garantia > 0 else "No requerido"
        return (
            f"Alquiler de Equipo [{self._codigo}]\n"
            f"  Nombre      : {self._nombre}\n"
            f"  Tipo        : {self._tipo_equipo}\n"
            f"  Tarifa/hora : ${self._tarifa_hora:,.0f}\n"
            f"  Depósito    : {deposito}\n"
            f"  Estado      : {estado}"
        )

    def validar_parametros(self, duracion_horas: float) -> bool:
        """Valida que la duración esté entre 1 y 72 horas (3 días máximo)."""
        if duracion_horas <= 0:
            raise ServicioInvalidoException(
                f"La duración debe ser mayor a 0 horas, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if duracion_horas > 72:
            raise ServicioInvalidoException(
                f"El alquiler no puede superar 72 horas, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if not self._disponible:
            raise ServicioNoDisponibleException(self._nombre, "Equipo no disponible actualmente.")
        return True


# =============================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# =============================================================

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría profesional por horas.
    La tarifa varía según el nivel de especialización del asesor.
    """

    # Niveles válidos y sus multiplicadores de tarifa
    NIVELES = {
        "basico": 1.0,
        "intermedio": 1.5,
        "avanzado": 2.0,
    }

    def __init__(self, nombre: str, tarifa_hora: float, area: str, nivel: str = "basico"):
        super().__init__(nombre, tarifa_hora)
        # Validar área de asesoría
        if not area or not area.strip():
            raise ServicioInvalidoException("El área de asesoría no puede estar vacía.", campo="area")
        # Validar nivel de especialización
        nivel_lower = nivel.strip().lower()
        if nivel_lower not in self.NIVELES:
            raise ServicioInvalidoException(
                f"Nivel '{nivel}' no válido. Opciones: {list(self.NIVELES.keys())}",
                campo="nivel"
            )
        self._area = area.strip()
        self._nivel = nivel_lower
        # Multiplicador que ajusta la tarifa según el nivel
        self._multiplicador = self.NIVELES[nivel_lower]

    @property
    def area(self) -> str:
        """Retorna el área de especialización de la asesoría."""
        return self._area

    @property
    def nivel(self) -> str:
        """Retorna el nivel de la asesoría."""
        return self._nivel

    def calcular_costo(self, duracion_horas: float) -> float:
        """
        Calcula el costo de la asesoría.
        Aplica multiplicador según el nivel de especialización.
        """
        return round(self._tarifa_hora * self._multiplicador * duracion_horas, 2)

    def describir(self) -> str:
        """Describe la asesoría con todas sus características."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Asesoría Especializada [{self._codigo}]\n"
            f"  Nombre      : {self._nombre}\n"
            f"  Área        : {self._area}\n"
            f"  Nivel       : {self._nivel.capitalize()}\n"
            f"  Tarifa/hora : ${self._tarifa_hora:,.0f}\n"
            f"  Multiplicador: x{self._multiplicador}\n"
            f"  Estado      : {estado}"
        )

    def validar_parametros(self, duracion_horas: float) -> bool:
        """Valida que la duración esté entre 1 y 8 horas por sesión."""
        if duracion_horas <= 0:
            raise ServicioInvalidoException(
                f"La duración debe ser mayor a 0 horas, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if duracion_horas > 8:
            raise ServicioInvalidoException(
                f"Una asesoría no puede durar más de 8 horas por sesión, recibido: {duracion_horas}",
                campo="duracion_horas"
            )
        if not self._disponible:
            raise ServicioNoDisponibleException(self._nombre, "Asesor no disponible actualmente.")
        return True


# =============================================================
# GESTOR DE SERVICIOS
# =============================================================

class GestorServicios:
    """
    Administra el catálogo de servicios disponibles en Software FJ.
    Permite registrar, buscar y listar servicios en memoria.
    """

    def __init__(self):
        # Diccionario con código de servicio como clave
        self._servicios: dict[str, Servicio] = {}

    def registrar(self, servicio: Servicio) -> Servicio:
        """
        Registra un nuevo servicio en el catálogo.

        Parámetros:
            servicio (Servicio): Instancia del servicio a registrar.

        Retorna:
            Servicio: El servicio registrado.
        """
        try:
            # Verificar que no exista ya un servicio con el mismo código
            if servicio.codigo in self._servicios:
                raise ServicioInvalidoException(
                    f"Ya existe un servicio con el código '{servicio.codigo}'.",
                    campo="codigo"
                )
            self._servicios[servicio.codigo] = servicio
            LogHelper.info(f"FINISH: Servicio registrado exitosamente: {servicio.nombre}")
            return servicio
        except ServicioInvalidoException:
            raise
        except Exception as e:
            raise ServicioInvalidoException(f"Error inesperado al registrar servicio: {e}") from e

    def buscar(self, codigo: str) -> Servicio:
        """
        Busca un servicio por su código único.

        Lanza:
            ServicioNoEncontradoException: Si no existe el servicio.
        """
        servicio = self._servicios.get(codigo.strip())
        if not servicio:
            raise ServicioNoEncontradoException(codigo)
        return servicio

    def listar(self) -> list:
        """Retorna todos los servicios registrados."""
        return list(self._servicios.values())

    def total(self) -> int:
        """Retorna el número total de servicios registrados."""
        return len(self._servicios)