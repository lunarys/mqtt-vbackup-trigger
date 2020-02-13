import os
import paho.mqtt.client as mqtt
import sys
import time
import signal

#####################################################
def backup(action, force):
    options=""
    if force:
        options=options + "-f"

    script="/usr/local/bin/vbackup"

    if os.path.isfile(script):
        print("================================== START ====================================")
        os.system(script + " " + action + " " + options)
        print("=================================== END =====================================")
    else:
        print("    Backup script is not in expected location, is vbackup installed?")
####################################################
def on_message(client, usr, msg):
    global shutdown_desired

    recv = msg.payload.decode("utf-8").lower()
    split = recv.split(" ")
    topic = msg.topic
    print("[R] Received", recv, "on", topic)

    if len(split) > 2:
        return

    force=(len(split) == 2 and split[1] == "force")

    if split[0] in ["run", "backup", "sync"]:
        print("    Received expected message for backup, running backup routine: {} (force={})".format(split[0], force))
        backup(split[0], force)

#####################################################
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscription")
#####################################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("[C] Connected OK")

        for t in topic.split(","):
            result=client.subscribe(t, qos)
            print("[T] Subscribed to topic", t)
    else:
        print("[C] Bad connection: Returned code=", rc)
#####################################################
def on_disconnect(client, userdata, rc):
    print("[C] Disconnected: ", rc)
    client.connected_flag = False
#####################################################
def interrupt_handler(sig, frame):
    print("Received interrupt, terminating...")
    client.disconnect()
    exit()
#####################################################

# Get iterator for command line arguments and skip first item (script call)
arg_it = iter(sys.argv)
next(arg_it)

# Listen to interrupt and termination
signal.signal(signal.SIGINT, interrupt_handler)
signal.signal(signal.SIGTERM, interrupt_handler)

# Set default values
broker_address="localhost"
port=1883
qos=1
config_file="config-example.yaml"
topic=None

user_set = False
password_set = False

# Parse environment variables
topic = os.environ.get('MQTT_TOPIC')
broker_address = os.getenv('MQTT_BROKER', broker_address)
port = int(os.getenv('MQTT_PORT', port))
qos = int(os.getenv('MQTT_QOS', qos))
user = os.environ.get('MQTT_USER')
password = os.environ.get('MQTT_PASSWORD')

if user != None:
    user_set = True

if password != None:
    password_set = True

#################################################
# Parse command line arguments
#################################################
for arg in arg_it:
    if arg == '-a':
        broker_address=next(arg_it)

    elif arg == '-q':
        qos=next(arg_it)

    elif arg == '-c':
        config_file=next(arg_it)

    elif arg == '-p':
        port = next(arg_it)

    elif arg == '-u':
        user = next(arg_it)
        user_set = True

    elif arg == '-pw' or arg == '-P':
        password = next(arg_it)
        password_set = True

    elif arg == "-t":
        topic = next(arg_it)

    elif arg == '-f':
        import configparser
        configParser = configparser.RawConfigParser()
        configParser.read(next(arg_it))

        if configParser.has_option('settings', 'address'):
            broker_address = configParser.get('settings', 'address')

        if configParser.has_option('settings', 'qos'):
            qos = configParser.getint('settings', 'qos')

        if configParser.has_option('settings', 'port'):
            port = configParser.getint('settings', 'port')

        if configParser.has_option('settings', 'user'):
            user = configParser.get('settings', 'user')
            user_set = True

        if configParser.has_option('settings', 'password'):
            password = configParser.get('settings', 'password')
            password_set = True

        if configParser.has_option('settings', 'topic'):
            topic = configParser.get('settings', 'topic')

    elif arg == '-h':
        print("Usage:", sys.argv[0], "[-f <broker-config-file>] [-a <ip>] [-p <port>] [-q <qos>] [-u <username>] [-pw <password>] [-c <listener-config-file>]")
        exit()

    else:
        print("Use \'", sys.argv[0], " -h\' to print available arguments.")
        exit()

if topic == None:
    print("Topic needs to be set for listening")
    exit()

# User and password need to be set both or none
if user_set != password_set:
    print("Please set either both username and password or none of those")
    exit()

############################################
# Set up MQTT client
############################################
client = mqtt.Client()
client.on_message = on_message
#client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Set username and password
if user_set and password_set:
    client.username_pw_set(user, password)

# Connect to broker
client.connect(broker_address, port)
# Start client loop (automatically reconnects after connection loss)
client.loop_forever()
