import network
import ujson as json
from machine import Pin
from machine import SoftI2C
from umqtt.simple import MQTTClient
import time


# WLAN-Verbindungsinformationen
WLAN_SSID = "FritzboxMetzlerGastzugang"
WLAN_PASSWORD = "mmetzler_gast"

# MQTT-Verbindungsinformationen
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "acceleration_data"
MQTT_PORT = 1883


# MPU-6050 I2C-Adresse
MPU6050_I2C_ADDR = 0x68

# Verbindung zum WLAN herstellen
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WLAN_SSID, WLAN_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected to WiFi")
    print("IP address:", wlan.ifconfig()[0])

# MQTT-Nachricht senden
def send_mqtt_message(data):
    client = MQTTClient("esp32", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    client.publish(MQTT_TOPIC, json.dumps(data))
    client.disconnect()

# Hauptprogramm
def main():
    # Verbindung zum WLAN herstellen
    connect_to_wifi()

    # SoftI2C-Objekt initialisieren
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

    accel_data = {}

    while True:
        # Beschleunigungsdaten lesen
        accel_data['x'] = i2c.readfrom_mem(MPU6050_I2C_ADDR, 0x3B, 2)
        accel_data['y'] = i2c.readfrom_mem(MPU6050_I2C_ADDR, 0x3D, 2)
        accel_data['z'] = i2c.readfrom_mem(MPU6050_I2C_ADDR, 0x3F, 2)

        # MQTT-Nachricht senden
        send_mqtt_message(accel_data)

        # Pause zwischen den Messungen
        time.sleep(1)

# Programm starten
if __name__ == '__main__':
    main()




