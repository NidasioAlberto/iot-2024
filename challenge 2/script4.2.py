import pyshark
import nest_asyncio
from time import *

nest_asyncio.apply()


def checkIfInTopic(subscription: str, topic: str):
    splitSub = subscription.split("/")
    splitTopic = topic.split("/")

    # More "subtopics"
    if (len(splitSub) > len(splitTopic)):
        return False

    # Check all the subtopics
    for i in range(len(splitSub)):
        if (splitSub[i] == "#"):
            return True
        if (splitSub[i] == "+" or splitSub[i] == splitTopic[i]):
            continue
        return False

    # Check if the two are equivalent
    if (len(splitSub) == len(splitTopic)):
        return True

    # subscription identical but not all subtopics present
    return False


# Client ports
clients = [59385, 38887, 37419, 36707]

# Topic to check
topic = "metaverse/facility4/area0/light"

for client in clients:
    query = 'mqtt && mqtt.msgtype == 8 && ip.dst_host != "127.0.0.1" && tcp.srcport == ' + \
        str(client)

    subscriptions = pyshark.FileCapture(
        "challenge2.pcapng", display_filter=query)

    for subscription in subscriptions:
        if checkIfInTopic(subscription.mqtt.topic, topic):
            print(str(client) + " -> " + subscription.mqtt.topic)
            break
