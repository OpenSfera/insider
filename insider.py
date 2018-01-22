import paho.mqtt.client as mqtt
import time
import json
import sferaconfig
from pymongo import MongoClient

interval_time = sferaconfig.getConfig("insider_time_interval", 600)
technician_broadcast_time = sferaconfig.getConfig("technician_broadcast_time", 5)
memory = {}

def on_message(client, userdata, msg):
    global interval_time
    global technician_broadcast_time
    global memory

    message = json.loads(str(msg.payload.decode("UTF-8")))
    message_type = message.get("type", None)
    now = int(time.time())
    if message_type in set(["sensor_alert", "service_alert"]) :
        if message["level"] == "danger":
            zone = "danger"
            send_after = 1 # should send after at least one confirm
        else:
            zone = "warning"
            # should send something only after the confirmation expected in insider_time_interval seconds
            send_after = int(interval_time / technician_broadcast_time )
#todo implent "safe"
        master_key = message["who"]+"_"+zone

        # Is a new packet?
        print(memory.get(master_key, None))
        if memory.get(master_key, None) == None:
            packet = {
                master_key: {
                    "message_type": message_type,
                    "severity": zone,
                    "countdown": send_after,
                    "expire_on": now + int( interval_time * 1.5 )
                }
            }
            packet[master_key].update(message)
            memory.update(packet)
            packet[master_key]["type"] = "user_alert"
        else:
            memory[master_key]["countdown"] = memory[master_key]["countdown"] - 1

    for k in list(memory):
        if memory[k]["expire_on"] >= now:
            if memory[k]["countdown"] == 0:
                client.publish('local/alert', json.dumps(memory[k]))
                memory[k]["countdown"] = int(interval_time / technician_broadcast_time )
                memory[k]["expire_on"] = now + int( interval_time * 1.5 )
        else:
            memory.pop(k, None)



def isDangerZone(m):
    if m["type"] == "service_alert":
        return True
    elif m["who"] == "t1":
        value = int(m["heared"])
        if value > 50 or value < 5:
            return True
        else:
            return False
    elif m["who"] == "h1":
        value = int(m["heared"])
        if value > 90 or value < 5:
            return True
        else:
            return False
    else:
        return False

def on_connect(client, userdata, flags, rc):
    client.subscribe("local/alert")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        now=time.strftime("%Y-%m-%d %H:%M")
        print("Unexpected disconnection."+now)

client = mqtt.Client(client_id="insider")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)

client.loop_forever()
