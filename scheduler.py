import paho.mqtt.publish as publish
from datetime import datetime
import time
broker = "157.173.101.159"
port = 1883
topic = "relay/laurent"
on_time = "15:08"
off_time = "15:09"
while True:
    now = datetime.now().strftime('%H:%M')
    print(f"Current time: {now}")
    if now == on_time:
        publish.single(topic, payload="1", hostname=broker, port=port)
        print("Published: Relay ON")
    elif now == off_time:
        publish.single(topic, payload="0", hostname=broker, port=port)
        print("Published: Relay OFF")
    time.sleep(30)