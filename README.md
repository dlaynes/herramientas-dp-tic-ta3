# Laboratorio U3 – Nodo IoT simulado con MQTT y EMQX (Grupo 4)

Simulación de un nodo IoT con 3 sensores tipo DHT22 que publican lecturas por MQTT a un broker EMQX local. Los datos se almacenan en InfluxDB y se visualizan en Grafana.

```
sensor.py ──MQTT/TLS──▶ EMQX ──▶ Telegraf ──▶ InfluxDB ──▶ Grafana
```

## Especificaciones

| Componente | Versión | Puerto | Función |
|------------|---------|--------|---------|
| Nodo IoT (`sensor.py`) | Python 3 + paho-mqtt 2 | — | 3 sensores (Sala, Cocina, Exterior): temperatura, humedad y presión cada 5 s |
| EMQX | 6.3.1 | 1883 · 8883 (TLS) · 8083 (WS) · 18083 (panel) | Broker MQTT con autenticación y TLS |
| Telegraf | 1.34 | — | Puente MQTT → InfluxDB |
| InfluxDB | 2.7 | 8086 | Base de datos de series de tiempo (bucket `sensores`) |
| Grafana | 13.0.2 | 3000 | Dashboard con los datos de los sensores |

- **Tópico:** `iot/<sensor_id>/mediciones` (suscribirse a todos con `iot/#`)
- **Mensaje (JSON, QoS 1):** `{"sensor_id", "ubicacion", "temperatura", "humedad", "presion", "timestamp"}`

## Estructura

```
broker/                 docker-compose, certificados TLS, Telegraf y Grafana
sensor-dht22-simulado/  nodo IoT simulado (sensor.py)
capturas/               evidencias del laboratorio
docs/INFORME.md         informe de la práctica
```

## Cómo levantarlo

**Requisitos:** Docker (con Docker Compose) y Python 3.

**1. Levantar los servicios**

```bash
cd broker
cp .env.example .env
docker compose up -d
```

**2. Configurar EMQX** en http://localhost:18083 (`admin` / `public`; pide cambiar la contraseña):

- *Access Control → Authentication → Create* → **Password-Based** → **Built-in Database** → *Create*.
- En *Users*, crear los usuarios `sensor_python`, `telegraf` y `explorer`.
- Poner la contraseña de `telegraf` en `broker/.env` y aplicar el cambio: `docker compose up -d`.

**3. Ejecutar el sensor**

```bash
cd sensor-dht22-simulado
python3 -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # poner la contraseña de sensor_python
python sensor.py
```

Al conectarse debe mostrar: `Conectado al broker localhost:8883 ... (TLS: True, usuario: sensor_python)`.

**4. Verificar**

| Qué | Dónde |
|-----|-------|
| Mensajes en tiempo real | EMQX → *Diagnostics Tools → WebSocket Client* (puerto 8083, usuario `explorer`, tópico `iot/#`) o MQTTX / MQTT Explorer |
| Dashboard | http://localhost:3000 (`admin` / `admin`) → *Dashboards → IoT* |

Más detalle en [`broker/README.md`](broker/README.md) y [`sensor-dht22-simulado/README.md`](sensor-dht22-simulado/README.md).
