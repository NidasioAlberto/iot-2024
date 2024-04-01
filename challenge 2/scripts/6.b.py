import pyshark
import nest_asyncio

nest_asyncio.apply()

CLIENTS_TOPICS = {38887: "university/department2/floor5",
                  36707: "house/kcbplh/section2",
                  59385: "hospital/kcbplh/#"}


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

counter = 0
for client in CLIENTS_TOPICS:
    # Received messages for the specific client
    query = "mqtt && mqtt.msgtype == 3 && tcp.dstport == " + str(client)
    
    # Open the logs with the created filter
    messages = pyshark.FileCapture(
        "../challenge2.pcapng",display_filter=query)
    
    # For every message, check if the client can read it according to the subscription filter
    for msg in messages:
        print(msg.mqtt.topic)
        if checkIfInTopic(CLIENTS_TOPICS[client], msg.mqtt.topic):
            counter += 1
print(counter)