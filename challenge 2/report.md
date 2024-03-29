# Challenge 2: CoAP and MQTT Traffic Analysis

The goal of this challenge is to analyze the CoAP and MQTT traffic given a log

## Questions

The questions to be answered are:

1.  - How many different CoAP clients sent a GET request to a temperature resource (../temperature)?
    - For each of the clients found in 1a, write the MID of the longest
      CoAP response (any response) received by the client
2.  - How many CoAP POST requests directed to the "coap.me" server
      did NOT produce a successful result?
    - How many requests from 2a are directed to a "weird"
      resource? (resources like /weirdXX)?
3.  - How many MQTT Publish messages with qos=2 are RECEIVED by
      the clients running in the machine capturing the traffic?
    - How many clients are involved in the messages found in 3a?
    - What are the MQTT Message identifiers (ID) of the subscribe
      requests that let the client receive the messages found in 3a?
4.  - How many MQTT clients sent a subscribe message to a public broker
      using at least one wildcard?
    - Considering clients found in 4a, how many of them WOULD receive
      a publish message directed to the topic:
      "metaverse/facility4/area0/light“
5.  - How many MQTT ACK messages in total are received by clients
      who connected to brokers specifying a client identifier shorter than
      15 bytes and using MQTT version 3.1.1?
6.  - How many MQTT subscribe requests with message ID=1 are directed
      to the HiveMQ broker?
    - How many publish messages are received by the clients thanks to the
      subscribe requests found in 6a
7.  - How many MQTT-SN (on port 1885) publish messages sent after the
      hour 3.59PM (Milan Time) are directed to topic 6?
    - Explain possible reasons why messages in 7a are not handled by the
      server

## Answers

1. - `udp.dstport == 5683 && coap.code == 1 && coap.opt.uri_path == "temperature"`
   - sort with respect to length\
     `udp.srcport == 5683 && ip.dst_host == 127.0.0.1`\
     64488 should be the answer
2. - Script 2.1 (17)
   - Script 2.2 (8)
