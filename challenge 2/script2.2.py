import pyshark

def isIndexIn(packets, index):
    for packet in packets:
        if int(packet.udp.stream) == index:
            return True
    return False

failures = pyshark.FileCapture("challenge2.pcapng", 
                              display_filter="udp.port == 5683 && ip.src_host == 134.102.218.18 && >= 128 &&  coap.code <= 165")
posts = pyshark.FileCapture("challenge2.pcapng", 
                            display_filter="udp.port == 5683 && ip.dst_host == 134.102.218.18 && coap.code == 2")

# Look for failures that correspond to posts
result = []
for post in posts:
    if(isIndexIn(failures, int(post.udp.stream))):
        result.append(post)

# Count the amount of requests indexed to /weirdXX
counter = 0
for res in result:
    if("weird" in res.coap.opt_uri_path_recon):
        counter += 1

print(counter)