from mqtt import MQTTClient 
from machine import Pin
import time
import os
import network

# ========================CONEXÃO WIFI===============================

conexao_wifi = network.WLAN(network.STA_IF)
conexao_wifi.active(True)
conexao_wifi.connect('Inteli-COLLEGE', 'QazWsx@123')

tempo_maximo = 30 
inicio = time.time()
while not conexao_wifi.isconnected() and time.time() - inicio < tempo_maximo:
    print("conectando ao wi-fi...")
    time.sleep(1)

if conexao_wifi.isconnected():
    print("conectado ao wi-fi com sucesso!")
    print(conexao_wifi.ifconfig())
else:
    print("faalha ao conectar ao wi-fi após 30 segundos")



# ========================ENVIO DOS DADOS===============================

BROKER_ENDPOINT = "industrial.api.ubidots.com"
TLS_PORT = 8883
MQTT_USERNAME = "BBUS-QyIPspKJSJpEYSsDEPozYSNFDjOUPl"
MQTT_PASSWORD = ""
DEVICE_LABEL = "truck"

# MQTT Topic
TOPIC = f"/v1.6/devices/{DEVICE_LABEL}"

client = MQTTClient(
    client_id=DEVICE_LABEL,
    server=BROKER_ENDPOINT,
    port=TLS_PORT,
    user=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    ssl=True  
)

# Connect to the MQTT broker
connected = False
try:
    client.connect()
    print("Connected to the broker")
    connected = True
except Exception as e:
    print(f"Failed to connect to the broker: {e}")

if connected:
  PIN_TRIG = 13 #pino 12 será usado como pino de disparo
  PIN_ECHO = 12 #pino 13 será usado como pino de escuta
  trig = Pin(PIN_TRIG, Pin.OUT) #configura o pino trig como saída
  echo = Pin(PIN_ECHO, Pin.IN) #configura o pino escuta como entrada
  while True:
      trig.on() 
      time.sleep_us(10)
      trig.off()
      duration = machine.time_pulse_us(echo, 1, 30000) #mede o tempo para o pulso ultrassônico ser refletido de volta ao sensor.
      distance_cm = duration / 58
      time.sleep(1)
      
      payload = '{"distance":'+distance_cm+'}'
      client.publish(TOPIC, payload.encode())
      print("Data published")
