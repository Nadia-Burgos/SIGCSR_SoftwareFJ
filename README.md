# 🏢 Software FJ — Sistema Integral de Gestión (SIGCSR)

**Autora:** Nadia Burgos (NYBP)  
**Curso:** Programación 213023 — UNAD  
**Fecha:** Mayo 2026  

---

## 📋 Descripción

Sistema de gestión de clientes, servicios y reservas para la empresa 
Software FJ, desarrollado en Python con Programación Orientada a Objetos 
y manejo avanzado de excepciones, sin uso de base de datos.

## 🗂️ Estructura

SIGCSR_SoftwareFJ/
├── main.py
├── excepciones/
│   ├── __init__.py
│   └── excepciones_personalizadas.py
├── gestores/
│   ├── __init__.py
│   ├── gestor_clientes.py
│   ├── gestor_servicios.py
│   └── gestor_reservas.py
├── helpers/
│   ├── __init__.py
│   └── log_helper.py
├── simulaciones/
│   ├── __init__.py
│   └── simulador_sistema.py
├── logs/
│   └── YYYY-MM-DD.log
└── README.md
## 🚀 Cómo ejecutar
python main.py

## ✅ Conceptos implementados

- Clases abstractas y herencia
 Se creó la clase abstracta `Servicio` 
  como base para los tres servicios del sistema. `ReservaSala`, 
  `AlquilerEquipo` y `AsesoriaEspecializada` heredan de ella y están 
  obligadas a implementar sus métodos.

- Polimorfismo y encapsulación
  Cada servicio implementa `calcular_costo()` de forma 
  diferente. Por ejemplo, `ReservaSala` aplica un recargo del 15% si tiene 
  proyector, mientras que `AsesoriaEspecializada` ajusta la tarifa según 
  el nivel (básico, intermedio, avanzado).
  Los atributos de `Cliente` y `Servicio` son privados 
  (prefijo `_`) y solo se acceden mediante propiedades (`@property`), 
  evitando modificaciones directas desde fuera de la clase.

- Excepciones personalizadas
  Se definió una jerarquía completa de 
  excepciones propias del sistema, como `ClienteInvalidoException` o 
  `ReservaInvalidaException`, que heredan de `SoftwareFJException`

- Bloques try/except/else/finally
  Usados en cada operación crítica. 
  El bloque `else` ejecuta lógica solo cuando no hay error, y `finally` 
  garantiza que siempre se registre el intento en el log.

- Registro de logs en archivo
  Todos los eventos y errores se guardan 
  automáticamente en un archivo `.log` con fecha, hora y nivel 
  (INFO, WARNING, ERROR), sin interrumpir la ejecución del sistema.

- 15 simulaciones válidas e inválidas
  Se ejecutaron casos válidos e inválidos de 
  clientes, servicios y reservas, demostrando que el sistema continúa 
  funcionando aunque encuentre errores en el camino.

🛡️ Jerarquía de excepciones
SoftwareFJException
├── ClienteInvalidoException
├── ClienteDuplicadoException
├── ClienteNoEncontradoException
├── ServicioInvalidoException
├── ServicioNoDisponibleException
├── ServicioNoEncontradoException
├── ReservaInvalidaException
├── ReservaNoEncontradaException
├── ReservaDuplicadaException
└── DescuentoInvalidoException

📚 Referencias
Van Rossum, G. (2024). El tutorial de Python. https://docs.python.org/es/3.12/tutorial/errors.html
Cuevas Álvarez, A. (2016). Python 3: curso práctico. RA-MA Editorial.
Romano, F., Baka, B., & Phillips, D. (2019). Getting Started with Python. Packt Publishing.