import pyshark
import nest_asyncio
from time import *

nest_asyncio.apply()

MQTT_MSG_TYPE_SUBSCRIBE = 8

CLIENTS_PORT = [59385, 38887, 37419, 36707]
TOPIC_TO_CHECK = "metaverse/facility4/area0/light"


def checkIfInTopic(subscription: str, topic: str):
    splitSub = subscription.split("/")
    splitTopic = topic.split("/")

    # More "subtopics"
    if len(splitSub) > len(splitTopic):
        return False

    # Check all the subtopics
    for i in range(len(splitSub)):
        if splitSub[i] == "#":
            return True
        if splitSub[i] == "+" or splitSub[i] == splitTopic[i]:
            continue
        return False

    # Check if the two are equivalent
    if len(splitSub) == len(splitTopic):
        return True

    # subscription identical but not all subtopics present
    return False


for client in CLIENTS_PORT:
    subscriptions = pyshark.FileCapture(
        "../challenge2.pcapng",
        display_filter='mqtt && mqtt.msgtype == {} && ip.dst_host != "127.0.0.1" && tcp.srcport == {}'.format(
            MQTT_MSG_TYPE_SUBSCRIBE, client
        ),
    )

    for subscription in subscriptions:
        if checkIfInTopic(subscription.mqtt.topic, TOPIC_TO_CHECK):
            print("{} -> {}".format(client, subscription.mqtt.topic))
            break
