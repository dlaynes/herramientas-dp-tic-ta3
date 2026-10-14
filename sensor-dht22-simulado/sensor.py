from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import ssl
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Carga la configuración desde el archivo .env (si existe) junto al script
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Configuración del Broker y Credenciales de Autenticación
BROKER = os.getenv("MQTT_HOST", "localhost")
USE_TLS = os.getenv("MQTT_USE_TLS", "false").lower() == "true"
PORT = int(os.getenv("MQTT_PORT", "8883" if USE_TLS else "1883"))  # 1883 sin cifrar, 8883 TLS
USERNAME = os.getenv("MQTT_USERNAME")  # Usuario creado en EMQX (http://localhost:18083)
PASSWORD = os.getenv("MQTT_PASSWORD")
CA_CERTS = os.getenv("MQTT_CA_CERTS", str(BASE_DIR.parent / "broker" / "certs" / "ca.crt"))
# El client_id debe ser único: dos clientes con el mismo ID se desconectan entre sí
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", f"nodo_iot_python_{random.randint(1000, 9999)}")

# Definición de múltiples sensores simulados (recomendación de la guía)
SENSORES = [
    {"id": "sensor_01", "ubicacion": "Sala"},
    {"id": "sensor_02", "ubicacion": "Cocina"},
    {"id": "sensor_03", "ubicacion": "Exterior"},
]

# Inicialización del cliente MQTT (Callback API Version 2)
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID
)

# Configurar Autenticación por Usuario y Contraseña
if USERNAME:
  client.username_pw_set(USERNAME, PASSWORD)

# Configurar TLS/SSL utilizando el certificado de la CA generado localmente
if USE_TLS:
  client.tls_set(
      ca_certs=CA_CERTS,
      cert_reqs=ssl.CERT_REQUIRED,
      tls_version=ssl.PROTOCOL_TLS_CLIENT
  )

def on_connect(client, userdata, flags, reason_code, properties):
  if reason_code.is_failure:
    print(f"Error al conectar con el broker: {reason_code}")
  else:
    print(f"Conectado al broker {BROKER}:{PORT} como {CLIENT_ID} (TLS: {USE_TLS}, usuario: {USERNAME or 'anónimo'})")

client.on_connect = on_connect

# Conexión al Broker MQTT
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
  while True:
    for sensor in SENSORES:
      # Generación de variables ambientales simuladas
      temperatura = round(random.uniform(20.0, 30.0), 2)
      humedad = round(random.uniform(40.0, 80.0), 2)
      presion = round(random.uniform(1005.0, 1025.0), 2)

      # Obtener timestamp actual en formato ISO 8601 (UTC)
      timestamp = datetime.now(timezone.utc).isoformat()

      # Estructura de datos en JSON
      payload = json.dumps({
          "sensor_id": sensor["id"],
          "ubicacion": sensor["ubicacion"],
          "temperatura": temperatura,
          "humedad": humedad,
          "presion": presion,
          "timestamp": timestamp,
      })

      topic = f"iot/{sensor['id']}/mediciones"
      print(f"Publicando en [{topic}] -> {payload}")

      # Publicación con QoS 1
      client.publish(topic, payload, qos=1)

    # Pausa de 5 segundos entre ciclos
    time.sleep(5)

except KeyboardInterrupt:
  client.loop_stop()
  client.disconnect()
  print("Cerrando programa. Conexión cerrada.")