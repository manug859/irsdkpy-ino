// Definir los pines de los LEDs como constantes globales
const int ledPins[] = {2, 3, 4};  // Pines para los LEDs
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);  // Cantidad de LEDs

// Variables para el parpadeo de los LEDs
unsigned long previousMillis = 0;  // Guarda el tiempo del último parpadeo
bool ledState = false;  // Estado de los LEDs
bool flashing = false;  // Variable para saber si los LEDs deben parpadear

// Configuración inicial: definir pines como salida
void setup() {
  // Configurar los pines como salida
  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(9600);  // Inicializa la comunicación serial a 9600 baudios
}

// Función para controlar los LEDs en función de los valores de RPM
void controlLeds(int rpm) {
  // Apagar todos los LEDs inicialmente
  for (int i = 0; i < ledCount; i++) {
    digitalWrite(ledPins[i], LOW);
  }

  // Encender LEDs según los valores de RPM
  if (rpm > 40) digitalWrite(ledPins[0], HIGH);  // LED 2
  if (rpm > 60) digitalWrite(ledPins[1], HIGH);  // LED 3
  if (rpm > 80) digitalWrite(ledPins[2], HIGH);  // LED 4
}

// Función para hacer parpadear los LEDs
void flash(int vel) {
  unsigned long currentMillis = millis();

  // Si ha pasado el tiempo de intervalo, cambiar el estado de los LEDs
  if (currentMillis - previousMillis >= vel) {
    previousMillis = currentMillis;  // Actualizar el tiempo del último cambio
    ledState = !ledState;  // Cambiar el estado de los LEDs

    // Encender o apagar los LEDs según el estado
    for (int i = 0; i < ledCount; i++) {
      digitalWrite(ledPins[i], ledState ? HIGH : LOW);
    }
  }
}

// Bucle que se repite continuamente
void loop() {
  if (Serial.available() > 0) {
    // Leer los datos enviados desde Python
    String data = Serial.readStringUntil('\n');

    // Controlar los LEDs en función del valor de RPM
    int rpm = data.toInt();

    // Si RPM >= 95, activar el parpadeo
    if (rpm >= 95) {
      flashing = true;  // Habilitar el modo de parpadeo
    } else {
      flashing = false;  // Desactivar el modo de parpadeo
      controlLeds(rpm);  // Control normal de los LEDs
    }
  }

  // Si está habilitado el parpadeo, ejecutar la función de parpadeo
  if (flashing) {
    flash(50);  // Parpadear cada 50 ms
  }
}
