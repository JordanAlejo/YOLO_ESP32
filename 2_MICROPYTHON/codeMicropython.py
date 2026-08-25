
# Desarrollar en Wokwi el desarrollo en micropython del siguiente esquema:

from machine import Pin
import uasyncio as asyncio


# =====================================================
# GPIO DEFINITIONS
# =====================================================

BUTTON1_GPIO = 13
BUTTON2_GPIO = 14

LED1_GPIO = 25
LED2_GPIO = 26


# =====================================================
# GPIO CONFIGURATION
# =====================================================

led1 = Pin(LED1_GPIO, Pin.OUT)
led2 = Pin(LED2_GPIO, Pin.OUT)

button1 = Pin(BUTTON1_GPIO, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON2_GPIO, Pin.IN, Pin.PULL_UP)


# LEDs inicialmente apagados
led1.value(0)
led2.value(0)


# =====================================================
# EVENTS
# =====================================================

button1_event = asyncio.Event()
button2_event = asyncio.Event()


# =====================================================
# BUTTON 1 INTERRUPT
# =====================================================

def button1_isr(pin):
    button1_event.set()


# =====================================================
# BUTTON 2 INTERRUPT
# =====================================================

def button2_isr(pin):
    button2_event.set()


# =====================================================
# CONFIGURE INTERRUPTS
# =====================================================

button1.irq(
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
    handler=button1_isr
)

button2.irq(
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
    handler=button2_isr
)


# =====================================================
# PRODUCER TASK
#
# Generates sensor data and sends it to the queue.
# =====================================================

async def producer_task(queue):

    count = 0

    while True:

        count += 1

        print("[PRODUCER] Sending sensor data:", count)

        # Enviar dato a la cola
        await queue.put(count)

        print("[PRODUCER] Data sent successfully")

        # Esperar 1 segundo
        await asyncio.sleep(1)


# =====================================================
# CONSUMER TASK
#
# Receives sensor data from the queue.
# =====================================================

async def consumer_task(queue):

    while True:

        # Esperar un dato de la cola
        received_value = await queue.get()

        print(
            "[CONSUMER] Received Sensor Data:",
            received_value
        )


# =====================================================
# BUTTON 1 TASK
#
# Waits for semaphore/event from Button 1 ISR.
# =====================================================

async def button1_task():

    while True:

        # Esperar a que se produzca una interrupción
        await button1_event.wait()

        # Limpiar el evento
        button1_event.clear()

        # Leer estado del botón
        button_state = button1.value()

        # Debido al PULL_UP:
        #
        # GPIO13 = 0 -> botón presionado
        # GPIO13 = 1 -> botón liberado

        if button_state == 0:

            led1.value(1)

            print(
                "[BUTTON 1] PRESSED -> LED1 ON"
            )

        else:

            led1.value(0)

            print(
                "[BUTTON 1] RELEASED -> LED1 OFF"
            )


# =====================================================
# BUTTON 2 TASK
#
# Waits for semaphore/event from Button 2 ISR.
# =====================================================

async def button2_task():

    while True:

        # Esperar a que se produzca una interrupción
        await button2_event.wait()

        # Limpiar el evento
        button2_event.clear()

        # Leer estado del botón
        button_state = button2.value()

        # Debido al PULL_UP:
        #
        # GPIO14 = 0 -> botón presionado
        # GPIO14 = 1 -> botón liberado

        if button_state == 0:

            led2.value(1)

            print(
                "[BUTTON 2] PRESSED -> LED2 ON"
            )

        else:

            led2.value(0)

            print(
                "[BUTTON 2] RELEASED -> LED2 OFF"
            )


# =====================================================
# MAIN APPLICATION
# =====================================================

async def main():

    print()
    print("========================================")
    print(" ESP32 MicroPython IPC Demonstration")
    print("========================================")

    print("[INIT] GPIO initialized")


    # -------------------------------------------------
    # Crear Queue
    # -------------------------------------------------

    sensor_queue = asyncio.Queue(10)

    print("[INIT] Sensor queue created")


    # -------------------------------------------------
    # Crear tareas
    # -------------------------------------------------

    asyncio.create_task(
        producer_task(sensor_queue)
    )

    asyncio.create_task(
        consumer_task(sensor_queue)
    )

    asyncio.create_task(
        button1_task()
    )

    asyncio.create_task(
        button2_task()
    )


    print("[INIT] All MicroPython tasks created")

    print("----------------------------------------")
    print("Button 1 : GPIO13")
    print("Button 2 : GPIO14")
    print("LED 1    : GPIO25")
    print("LED 2    : GPIO26")
    print("----------------------------------------")

    print("[READY] System ready!")


    # -------------------------------------------------
    # Mantener el programa funcionando
    # -------------------------------------------------

    while True:

        await asyncio.sleep(1)


# =====================================================
# START PROGRAM
# =====================================================

try:

    asyncio.run(main())

finally:

    asyncio.new_event_loop()