"""
simulaciones/simulador_sistema.py

Autora  : Nadia Burgos (NYBP)
Curso   : Programación — UNAD
Fecha   : Mayo 2026

Simula más de 10 operaciones completas del sistema Software FJ,
incluyendo registros válidos e inválidos de clientes, servicios
y reservas, demostrando el manejo robusto de excepciones.
"""

from helpers.log_helper import LogHelper
from gestores.gestor_clientes import GestorClientes, Cliente
from gestores.gestor_servicios import (
    GestorServicios,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from gestores.gestor_reservas import GestorReservas, EstadoReserva
from excepciones.excepciones_personalizadas import (
    SoftwareFJException,
    ClienteInvalidoException,
    ClienteDuplicadoException,
    ServicioInvalidoException,
    ServicioNoDisponibleException,
    ReservaInvalidaException,
    DescuentoInvalidoException,
)


class SimuladorSistema:
    """
    Ejecuta simulaciones completas del sistema Software FJ.
    Cada simulación demuestra un caso de uso válido o inválido.
    """

    def __init__(self):
        # Inicializar los tres gestores principales del sistema
        self.gestorClientes  = GestorClientes()
        self.gestorServicios = GestorServicios()
        self.gestorReservas  = GestorReservas()

    # =============================================================
    # BLOQUE 1: SIMULACIONES DE CLIENTES (1-4)
    # =============================================================

    def _sim_cliente_valido(self):
        """Simulación 1 — Registro exitoso de un cliente con datos correctos."""
        LogHelper.info("START: Simulación 1 — Registrar cliente válido")
        try:
            cliente = self.gestorClientes.registrar(
                nombre="Laura Gómez",
                email="laura.gomez@email.com",
                telefono="3001234567",
                identificacion="12345678"
            )
        except SoftwareFJException as e:
            LogHelper.error(f"Error inesperado en sim 1: {e}")
        else:
            # El bloque else se ejecuta solo si no hubo excepción
            LogHelper.info(f"  Resultado: {cliente}")

    def _sim_cliente_email_invalido(self):
        """Simulación 2 — Intento de registro con email inválido."""
        LogHelper.info("START: Simulación 2 — Cliente con email inválido")
        try:
            self.gestorClientes.registrar(
                nombre="Carlos Ruiz",
                email="correo-sin-arroba",   # Email sin @ → debe fallar
                telefono="3109876543",
                identificacion="87654321"
            )
        except ClienteInvalidoException as e:
            # Capturar el error específico de cliente inválido
            LogHelper.advertencia(f"  Error capturado correctamente: {e}")
        finally:
            # El bloque finally siempre se ejecuta
            LogHelper.info("  Bloque finally: validación de email completada.")

    def _sim_cliente_identificacion_corta(self):
        """Simulación 3 — Intento de registro con identificación muy corta."""
        LogHelper.info("START: Simulación 3 — Cliente con identificación corta")
        try:
            self.gestorClientes.registrar(
                nombre="Ana Torres",
                email="ana@email.com",
                telefono="3201112233",
                identificacion="123"   # Menos de 5 caracteres → debe fallar
            )
        except ClienteInvalidoException as e:
            LogHelper.advertencia(f"  Error capturado: {e}")

    def _sim_cliente_duplicado(self):
        """Simulación 4 — Intento de registrar cliente con identificación ya existente."""
        LogHelper.info("START: Simulación 4 — Cliente duplicado")
        try:
            # Primero registrar el cliente original
            self.gestorClientes.registrar(
                nombre="Pedro Sánchez",
                email="pedro@email.com",
                telefono="3154445566",
                identificacion="99887766"
            )
            # Intentar registrar otro con la misma identificación
            self.gestorClientes.registrar(
                nombre="Pedro Otro",
                email="pedro2@email.com",
                telefono="3154445567",
                identificacion="99887766"   # Misma identificación → debe fallar
            )
        except ClienteDuplicadoException as e:
            LogHelper.advertencia(f"  Duplicado detectado correctamente: {e}")
        except ClienteInvalidoException as e:
            LogHelper.error(f"  Error inesperado: {e}")

    # =============================================================
    # BLOQUE 2: SIMULACIONES DE SERVICIOS (5-8)
    # =============================================================

    def _sim_sala_valida(self):
        """Simulación 5 — Registro exitoso de una sala de reuniones."""
        LogHelper.info("START: Simulación 5 — Registrar sala válida")
        try:
            sala = ReservaSala(
                nombre="Sala Innovación",
                tarifa_hora=80000,
                capacidad=10,
                tiene_proyector=True
            )
            self.gestorServicios.registrar(sala)
        except ServicioInvalidoException as e:
            LogHelper.error(f"  Error al registrar sala: {e}")
        else:
            LogHelper.info(f"  Resultado: {sala}")

    def _sim_equipo_valido(self):
        """Simulación 6 — Registro exitoso de un equipo de alquiler."""
        LogHelper.info("START: Simulación 6 — Registrar equipo válido")
        try:
            equipo = AlquilerEquipo(
                nombre="Laptop Dell XPS",
                tarifa_hora=25000,
                tipo_equipo="Computador portátil",
                deposito_garantia=150000
            )
            self.gestorServicios.registrar(equipo)
        except ServicioInvalidoException as e:
            LogHelper.error(f"  Error al registrar equipo: {e}")
        else:
            LogHelper.info(f"  Resultado: {equipo}")

    def _sim_asesoria_valida(self):
        """Simulación 7 — Registro exitoso de una asesoría especializada."""
        LogHelper.info("START: Simulación 7 — Registrar asesoría válida")
        try:
            asesoria = AsesoriaEspecializada(
                nombre="Consultoría en Ciberseguridad",
                tarifa_hora=120000,
                area="Tecnología",
                nivel="avanzado"
            )
            self.gestorServicios.registrar(asesoria)
        except ServicioInvalidoException as e:
            LogHelper.error(f"  Error al registrar asesoría: {e}")
        else:
            LogHelper.info(f"  Resultado: {asesoria}")

    def _sim_servicio_tarifa_negativa(self):
        """Simulación 8 — Intento de crear servicio con tarifa negativa."""
        LogHelper.info("START: Simulación 8 — Servicio con tarifa negativa")
        try:
            sala_invalida = ReservaSala(
                nombre="Sala Error",
                tarifa_hora=-5000,   # Tarifa negativa → debe fallar
                capacidad=5
            )
            self.gestorServicios.registrar(sala_invalida)
        except ServicioInvalidoException as e:
            LogHelper.advertencia(f"  Error capturado correctamente: {e}")
        finally:
            LogHelper.info("  Bloque finally: intento de registro finalizado.")

    # =============================================================
    # BLOQUE 3: SIMULACIONES DE RESERVAS (9-12)
    # =============================================================

    def _sim_reserva_exitosa(self):
        """Simulación 9 — Flujo completo exitoso de una reserva."""
        LogHelper.info("START: Simulación 9 — Reserva completa exitosa")
        try:
            # Obtener cliente y servicio existentes
            cliente  = self.gestorClientes.listar()[0]
            servicio = self.gestorServicios.listar()[0]

            # Crear la reserva
            reserva = self.gestorReservas.crear(cliente, servicio, duracion_horas=3)

            # Confirmar → procesar → completar (ciclo de vida completo)
            reserva.confirmar()
            reserva.procesar()
            reserva.completar()

        except SoftwareFJException as e:
            LogHelper.error(f"  Error en reserva exitosa: {e}")
        else:
            LogHelper.info(f"  Reserva completada: {reserva.describir()}")

    def _sim_reserva_servicio_no_disponible(self):
        """Simulación 10 — Reserva con servicio marcado como no disponible."""
        LogHelper.info("START: Simulación 10 — Servicio no disponible")
        try:
            cliente  = self.gestorClientes.listar()[0]
            servicio = self.gestorServicios.listar()[0]

            # Marcar el servicio como no disponible
            servicio.disponible = False

            # Intentar reservar → debe fallar
            self.gestorReservas.crear(cliente, servicio, duracion_horas=2)

        except ServicioNoDisponibleException as e:
            LogHelper.advertencia(f"  Error capturado correctamente: {e}")
        finally:
            # Restaurar disponibilidad para otras simulaciones
            self.gestorServicios.listar()[0].disponible = True
            LogHelper.info("  Disponibilidad restaurada en bloque finally.")

    def _sim_reserva_duracion_invalida(self):
        """Simulación 11 — Reserva con duración de 0 horas."""
        LogHelper.info("START: Simulación 11 — Duración inválida (0 horas)")
        try:
            cliente  = self.gestorClientes.listar()[0]
            servicio = self.gestorServicios.listar()[0]

            # Duración 0 → debe fallar en validar_parametros
            self.gestorReservas.crear(cliente, servicio, duracion_horas=0)

        except (ReservaInvalidaException, ServicioInvalidoException) as e:
            LogHelper.advertencia(f"  Error capturado: {e}")

    def _sim_cancelar_reserva(self):
        """Simulación 12 — Cancelar una reserva pendiente."""
        LogHelper.info("START: Simulación 12 — Cancelar reserva")
        try:
            cliente  = self.gestorClientes.listar()[0]
            servicio = self.gestorServicios.listar()[1]   # Segundo servicio

            reserva = self.gestorReservas.crear(cliente, servicio, duracion_horas=2)
            reserva.cancelar(motivo="El cliente cambió de planes.")

        except SoftwareFJException as e:
            LogHelper.error(f"  Error al cancelar: {e}")
        else:
            LogHelper.info(f"  Estado final: {reserva.estado.value}")

    # =============================================================
    # BLOQUE 4: SIMULACIONES DE CÁLCULOS (13-15)
    # =============================================================

    def _sim_calculo_con_iva(self):
        """Simulación 13 — Cálculo de costo con IVA aplicado."""
        LogHelper.info("START: Simulación 13 — Costo con IVA")
        try:
            servicio = self.gestorServicios.listar()[0]
            costo_sin_iva = servicio.calcular_costo(2)
            costo_con_iva = servicio.calcular_costo_con_impuestos(2)
            LogHelper.info(f"  Sin IVA : ${costo_sin_iva:,.0f}")
            LogHelper.info(f"  Con IVA : ${costo_con_iva:,.0f}")
        except SoftwareFJException as e:
            LogHelper.error(f"  Error en cálculo: {e}")

    def _sim_calculo_con_descuento(self):
        """Simulación 14 — Cálculo de costo con descuento del 20%."""
        LogHelper.info("START: Simulación 14 — Costo con descuento")
        try:
            servicio = self.gestorServicios.listar()[1]
            costo_normal   = servicio.calcular_costo(4)
            costo_descuento = servicio.calcular_costo_con_descuento(4, descuento=0.20, aplicar_iva=True)
            LogHelper.info(f"  Sin descuento: ${costo_normal:,.0f}")
            LogHelper.info(f"  Con 20% desc + IVA: ${costo_descuento:,.0f}")
        except SoftwareFJException as e:
            LogHelper.error(f"  Error en cálculo: {e}")

    def _sim_descuento_invalido(self):
        """Simulación 15 — Descuento fuera del rango válido."""
        LogHelper.info("START: Simulación 15 — Descuento inválido")
        try:
            servicio = self.gestorServicios.listar()[0]
            # Descuento de 1.5 (150%) → debe fallar
            servicio.calcular_costo_con_descuento(2, descuento=1.5)
        except DescuentoInvalidoException as e:
            LogHelper.advertencia(f"  Error capturado correctamente: {e}")

    # =============================================================
    # MÉTODO PRINCIPAL: EJECUTAR TODAS LAS SIMULACIONES
    # =============================================================

    def ejecutar_todas(self):
        """
        Ejecuta las 15 simulaciones en orden secuencial.
        El sistema continúa funcionando aunque alguna simulación falle.
        """
        LogHelper.log("\n" + "=" * 60)
        LogHelper.log("   INICIO DEL SISTEMA: Software FJ — Simulaciones")
        LogHelper.log("=" * 60)

        # Lista de todas las simulaciones a ejecutar
        simulaciones = [
            self._sim_cliente_valido,
            self._sim_cliente_email_invalido,
            self._sim_cliente_identificacion_corta,
            self._sim_cliente_duplicado,
            self._sim_sala_valida,
            self._sim_equipo_valido,
            self._sim_asesoria_valida,
            self._sim_servicio_tarifa_negativa,
            self._sim_reserva_exitosa,
            self._sim_reserva_servicio_no_disponible,
            self._sim_reserva_duracion_invalida,
            self._sim_cancelar_reserva,
            self._sim_calculo_con_iva,
            self._sim_calculo_con_descuento,
            self._sim_descuento_invalido,
        ]

        exitosas = 0
        fallidas  = 0

        # Ejecutar cada simulación de forma independiente
        for i, simulacion in enumerate(simulaciones, start=1):
            try:
                simulacion()
                exitosas += 1
            except Exception as e:
                # Si una simulación falla inesperadamente, registrar y continuar
                LogHelper.error(f"Simulación {i} falló inesperadamente: {e}")
                fallidas += 1
            LogHelper.log("")   # Línea en blanco entre simulaciones

        # Resumen final
        LogHelper.log("=" * 60)
        LogHelper.info(f"Results: Total simulaciones ejecutadas : {len(simulaciones)}")
        LogHelper.info(f"Results: Exitosas                      : {exitosas}")
        LogHelper.info(f"Results: Con errores controlados       : {fallidas}")
        LogHelper.log("=" * 60 + "\n")