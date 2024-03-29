import pyshark

connections = pyshark.FileCapture("challenge2.pcapng",
                                   display_filter="mqtt && tcp.port == 1883 && mqtt.msgtype == 1")

# For every connection, if there is a different src port count it as client
ports = []
for conn in connections:
    if conn.tcp.srcport not in ports:
        ports.append(conn.tcp.srcport)

print(len(ports))