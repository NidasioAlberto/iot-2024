import pyshark

SERVER_IP = "134.102.218.18"
SERVER_PORT = "5683"

COAP_CODE_POST = 2
COAP_CODE_CLIENT_ERROR_BAD_REQUEST = 128  # 4.0
COAP_CODE_SERVER_ERROR_PROXYING_NOT_SUPPORTED = 165  # 5.5


def isIndexIn(packets, index):
    for packet in packets:
        if int(packet.udp.stream) == index:
            return True
    return False


# First we need to find the ip address of the `coap.me` server
# Query: `dns && dns.resp.name == "coap.me"`
# One of the records: `coap.me: type A, class IN, addr 134.102.218.18`

# Get all post request to the CoAP server
posts = pyshark.FileCapture(
    "../challenge2.pcapng",
    display_filter="ip.dst_host == {} && udp.dstport == {} && coap.code == {}".format(
        SERVER_IP, SERVER_PORT, COAP_CODE_POST
    ),
)

# Get all the failure responses
failures = pyshark.FileCapture(
    "../challenge2.pcapng",
    display_filter="ip.src_host == {} && udp.srcport == {} && coap.code >= {} && coap.code <= {}".format(
        SERVER_IP,
        SERVER_PORT,
        COAP_CODE_CLIENT_ERROR_BAD_REQUEST,
        COAP_CODE_SERVER_ERROR_PROXYING_NOT_SUPPORTED,
    ),
)

# Look for failure responses that correspond to post requests
result = []
for post in posts:
    if isIndexIn(failures, int(post.udp.stream)):
        result.append(post)

# Count the amount of requests to /weirdXX
counter = 0
for res in result:
    if "weird" in res.coap.opt_uri_path_recon:
        counter += 1

print(
    "Number of POST request to a weird resource of coap.me which resulted in a failure: {}".format(
        counter
    )
)
