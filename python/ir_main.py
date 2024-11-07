import irsdk
import serial
import time
import pyvjoy

# Inicializar iRSDKPy
ir = irsdk.IRSDK()
ir.startup()

# Inicializar la conexión serial con Arduino
joystick = pyvjoy.VJoyDevice(1)
arduino = serial.Serial('COM3', 9600)  # Cambia 'COM3' al puerto correcto
time.sleep(2)  # Esperar un poco para que Arduino se inicialice

def update_joystick_button(button_state):
    """
    Emula el estado de un botón en el joystick virtual.
    Si `button_state` es True, el botón estará presionado (1), de lo contrario (0), el botón estará suelto.
    """
    joystick.set_button(1, button_state)  # Botón 1 del joystick


def rpm_map(rpm):
    rpm_min = 2000
    rpm_max = 12000

    if rpm < rpm_min:
        return 0
    elif rpm > rpm_max:
        return 100
    else:
        return (rpm - rpm_min) / (rpm_max - rpm_min) * 100

# Loop de ejemplo
try:
    while True:
        if ir.is_initialized and ir.is_connected:
            # Obtener RPM y velocidad del simulador
            speed = ir['Speed']
            rpm = ir['RPM']
            
            # Enviar la velocidad y rpm a Arduino
            data = f"{int(rpm_map(rpm))}\n"
            arduino.write(data.encode('utf-8'))
            
            # Leer el estado del botón de Arduino
            if arduino.in_waiting > 0:  # Verifica si hay datos disponibles desde Arduino
                button_state = int(arduino.readline().strip())
                update_joystick_button(button_state == 0)
                if button_state == 1:
                    print("Botón presionado")
            
            # Imprimir la información de velocidad y RPM
            print(f"Velocidad: {speed} km/h, RPM: {rpm}")
        
        time.sleep(0.1)  # Esperar 100 ms para la siguiente lectura

except KeyboardInterrupt:
    # Cerrar la conexión de manera segura al terminar
    print("Cerrando conexión...")
    arduino.close()
    ir.shutdown()
