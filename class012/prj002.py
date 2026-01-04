#########################匯入模組#########################
import time
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"IP = {wi.ip}")
mqtt_client = mcu.MQTT(
    "Kao", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqtt_client.connect()
#########################主程式#########################
while True:
    msg = input("Enter publish message:")
    mqtt_client.publish("hi", msg)
    time.sleep(1)
