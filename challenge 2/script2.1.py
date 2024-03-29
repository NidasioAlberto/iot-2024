import pyshark

def isIndexIn(packets, index):
    for packet in packets:
        if int(packet.udp.stream) == index:
            return True
    return False

failures = pyshark.FileCapture("challenge2.pcapng", 
                              display_filter="udp.port == 5683 && ip.src_host == 134.102.218.18 && coap.code == 133")
posts = pyshark.FileCapture("challenge2.pcapng", 
                            display_filter="udp.port == 5683 && ip.dst_host == 134.102.218.18 && coap.code == 2")

# Look for failures that correspond to posts
result = []
for failure in failures:
    if(isIndexIn(posts, int(failure.udp.stream))):
        result.append(failure)

print(len(result))
