import irsdk
import serial
import time

# Inicializar iRSDKPy
ir = irsdk.IRSDK()
ir.startup()

# Inicializar la conexión serial con Arduino
arduino = serial.Serial('COM3', 9600)  # Cambia 'COM3' al puerto correcto
time.sleep(2)  # Esperar un poco para que Arduino se inicialice

# Loop de ejemplo
try:
    while True:
        if ir.is_initialized and ir.is_connected:
            # Obtener RPM y velocidad del simulador
            speed = ir['Speed']
            rpm = ir['RPM']
            
            # Enviar la velocidad al Arduino
            data = f"{int(speed)},{int(rpm)}\n"
            arduino.write(data.encode('utf-8'))
            
 
        time.sleep(0.1)  # Esperar 100 ms para la siguiente lectura

except KeyboardInterrupt:
    # Cerrar la conexión de manera segura al terminar
    print("Cerrando conexión...")
    arduino.close()
    ir.shutdown()
