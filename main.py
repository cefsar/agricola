from gpiozero import Motor
from time import sleep

# Configuracion de motores
motor_izquierdo = Motor(forward=17, backward=18)
motor_derecho = Motor(forward=22, backward=23)

print("Robot agricola iniciado")

try:
    print("Avanzando...")
    motor_izquierdo.forward(0.8)
    motor_derecho.forward(0.8)
    sleep(2)

    print("Deteniendo...")
    motor_izquierdo.stop()
    motor_derecho.stop()
    sleep(1)

    print("Retrocediendo...")
    motor_izquierdo.backward(0.8)
    motor_derecho.backward(0.8)
    sleep(2)

    print("Deteniendo motores...")
    motor_izquierdo.stop()
    motor_derecho.stop()

except KeyboardInterrupt:
    print("Prueba interrumpida")

finally:
    motor_izquierdo.stop()
    motor_derecho.stop()
