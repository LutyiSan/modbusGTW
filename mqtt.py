import paho.mqtt.client as mqclient
import json
from loguru import logger


class MyMQTT:
    mqlog = logger

    def create(self, user_name, user_passwd):
        try:
            self.client = mqclient.Client(userdata=None, protocol=mqclient.MQTTv311, transport="tcp")
            self.client.username_pw_set(username=user_name, password=user_passwd)
            self.mqlog.debug("READY create mqtt-client")
            return True
        except Exception as e:
            self.mqlog.exception("FAIL create mqtt-client", e)

    def connect(self, broker, port):
        try:
            self.client.connect(broker, port=port, keepalive=60, bind_address="")
            self.mqlog.debug("READY connect mqtt-client to broker")
            return True
        except Exception as e:
            self.mqlog.exception("FAIL connect mqtt-client to broker", e)

    def send(self, topic, send_data):
        try:
            send_json = json.dumps(send_data)
            self.client.publish(topic, payload=send_json, qos=1, retain=True)
            self.mqlog.debug(f"Sending data {topic} {send_json}....")
            self.mqlog.debug(f"SUCCESSFUL sent data {topic}")
        except Exception as e:
            self.mqlog.exception("FAIL sent data to mqtt\n", e)

    def disconnect(self):
        self.client.disconnect()
