import json

import paho.mqtt.client as paho
from kafka import KafkaProducer


class KafkaWrapper:
    def __init__(self, bootstrap_servers, topic):
        """
        :param bootstrap_servers: Accepts list as an argument with as['host1:port1','host2:port2']
        :param topic: Topic name to publish data
        :type bootstrap_servers: list
        :type topic: str
        """
        self.topic = topic
        self.broker = bootstrap_servers
        try:
            self.producer = KafkaProducer(bootstrap_servers=self.broker,
                                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        except ConnectionError as e:
            raise Exception("Connection Error :" + str(e))
        except TimeoutError as e:
            raise Exception("Timeout Error :" + str(e))
        except Exception as e:
            raise Exception("Exception occurred while connecting to a producer :" + str(e))

    def __call__(self, func):
        def publish_data(*args, **kwargs):
            message = func(*args, **kwargs)
            try:
                self.producer.send(self.topic, message)
                return True
            except TimeoutError as e:
                raise Exception("TimeoutError :" + str(e))

        return publish_data


class MQTTWrapper:
    def __init__(self, host, port, topic, **kwargs):
        """
        :type host: str
        :type port: int
        :type topic: str
        """
        self.default_config = {
            'qos': 0,
            'retain': False
        }
        for arg in kwargs:
            if arg in self.default_config:
                self.default_config[arg] = kwargs[arg]
        self.host = host
        self.port = port
        self.topic = topic
        self.mqtt_client = paho.Client()
        try:
            res = self.mqtt_client.connect(host=self.host, port=self.port, keepalive=60)
            connection_error_codes = {1: "incorrect protocol version",
                                      2: "invalid client identifier",
                                      3: "server unavailable",
                                      4: "bad username or password",
                                      5: "not authorised"}
            if res != 0:
                raise Exception("Connection Error : " + str(connection_error_codes[res]))
            else:
                self.mqtt_client.loop_start()
        except KeyError as e:
            raise Exception("KeyError:" + str(e))

    def __call__(self, func):
        def publish_data(*args, **kwargs):
            message = func(*args, **kwargs)
            msg_info = self.mqtt_client.publish(topic=self.topic, payload=json.dumps(message),
                                                qos=self.default_config['qos'],
                                                retain=self.default_config['retain'])
            if msg_info[0] != 0:
                return False
            else:
                status = True
            return status

        return publish_data
