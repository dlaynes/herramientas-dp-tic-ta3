## TA Semana 10 - Grupo 4 - Simulación de sensor DHT-22

### 1. Crear y activar entorno virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
python -m pip install --upgrade pip   # opcional
python -m pip install -r requirements.txt
```

### 3. Configurar la conexión

Copiar `.env.example` como `.env` y completar los valores (el archivo `.env` no se sube al repositorio):

| Variable         | Descripción                                   | Por defecto |
|------------------|-----------------------------------------------|-------------|
| `MQTT_HOST`      | Dirección del broker                          | `localhost` |
| `MQTT_USE_TLS`   | `true` para conexión cifrada                  | `false`     |
| `MQTT_PORT`      | Puerto del broker                             | `8883` con TLS, `1883` sin TLS |
| `MQTT_CA_CERTS`  | Certificado de la CA                          | `../broker/certs/ca.crt` |
| `MQTT_USERNAME`  | Usuario creado en EMQX                        | (anónimo)   |
| `MQTT_PASSWORD`  | Contraseña del usuario                        |             |
| `MQTT_CLIENT_ID` | Identificador MQTT (debe ser único)           | `nodo_iot_python_<aleatorio>` |

Sin `.env` el sensor se conecta de forma anónima y sin cifrar a `localhost:1883`.

### 4. Correr la aplicación (solo si el servidor MQTT se encuentra activo)

```bash
python sensor.py
```

Cada sensor publica un JSON cada 5 segundos en `iot/<sensor_id>/mediciones`:

```json
{"sensor_id": "sensor_01", "ubicacion": "Sala", "temperatura": 22.11, "humedad": 52.31, "presion": 1020.57, "timestamp": "2026-10-13T23:51:50.490004+00:00"}
```
