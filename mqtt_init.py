import paho.mqtt.client as mqtt
import time
import random
import socket

# Configuration
nb = 1  # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com
brokers = [str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('hivemq.com'))]
ports = [80, 1883]
usernames = ['MATZI', '']  # should be modified for HIT
passwords = ['MATZI', '']  # should be modified for HIT
mzs = ['matzi/', '']
sub_topics = [mzs[nb] + '#', '#']
pub_topics = [mzs[nb] + 'test', 'test']

broker_ip = '127.0.0.1'  #brokers[nb]
broker_port = ports[nb]
username = usernames[nb]
password = passwords[nb]
sub_topic = sub_topics[nb]
pub_topic = pub_topics[nb]


def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, rc=0):
    print("Disconnected result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received: ", m_decode)


client = mqtt.Client("IOT_pudfdzfb_ugfefweu_jdksf", clean_session=True)  # create new client instance

client.on_connect = on_connect  # bind call back function
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

if username and password:
    client.username_pw_set(username, password)

print("Connecting to broker ", broker_ip)
client.connect(broker_ip, broker_port)  # connect to broker

try:
    for x in range(21):
        mylist1 = ['open', 'close']
        b = random.choice(mylist1)
        if b == "open":
            message = "There are open windows on floor " + str(x) + " The system will close the windows :)"
        else:
            message = "There are no open windows on the floor " + str(x)

        print(f"Publishing message: {message}")
        client.publish(pub_topic, message)
        time.sleep(5)
    client.publish(pub_topic, "The scan is finished :)")
finally:
    print("Disconnecting from broker")
    client.disconnect()  # disconnect
    print("End publish_client run script")
