# publisher

import time
import paho.mqtt.client as mqtt
import circuit # 초음파 센서 입력 모듈 임포트

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.connect(broker_ip, 1883)
client.loop_start()

while(True):
        temp = circuit.getTemperature()
        humidity = circuit.getHumidity()

        client.publish("temp", temp, qos=0)
        client.publish("humidity", humidity, qos=0)
        time.sleep(1)

client.loop_stop()
client.disconnect()