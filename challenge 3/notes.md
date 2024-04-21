# Assignments Notes


- [x] Every 5 seconds
- [x] Payload:
  - [x] `id` random number between 0 and 50000
  - [x] `timestamp` UNIX timestamp
- [x] Send to `challenge3/id_generator`
- [x] Save also in `id_log.csv` the following:
  - [x] `No.` incremental row number
  - [x] `ID`
  - [x] `TIMESTAMP`

- [x] Subscribe to the topic `challenge3/id_generator`
- [x] Compute $N = ID \space \% \space 7711$
- [x] Process `challenge3.csv` and take the line with `No.` equal to `N`
- [ ] For every MQTT `Publish Message` then
  - [x] Prepare a message with the following payload and for the topic specified by `Info`:
    - [x] `timestamp` the current timestamp
    - [x] `id` message id received from the subscription (not `N`)
    - [x] `payload` from the line payload
  - [x] Limit the messages published to 4 per minute
  - [x] Publish the MQTT message
  - [x] If the published message contains a temperature in fahrenheit, plot its value
    - [x] Temperature from range ((min + max) / 2)
    - [x] When plotting (after the rate limiter) save the payload of the messages in `filtered_pubs.csv` (it will have one message payload per line)
      - [x] Format: `No.`, `LONG`, `RANGE`, `LAT`, `TYPE`, `UNIT`, `DESCRIPTION` where `No.` is an incremental counter
    - [x] If some payload are empty, ignore them
- [ ] If the message is an MQTT ACK
  - [x] Increment a global ACK counter
  - [x] Save the message into `ack_log.csv`
    - [x] Format: `TIMESTAMP,SUB_ID,MSG_TYPE`
      - [x] `TIMESTAMP`  is the current time when the msg is saved in the CSV
      - [x] `SUB_ID` is the message id received from the subscription (not `N`)
      - [x] `MSG_TYPE` is the message type (Connect Ack, ...)
    - [ ] Send the value of the global ACK counter to your thingspeak channel, passing the filed1 of the channel the value of the global ACK counter. Send using HTTP API
- [x] In all other cases ignore the message

- [ ] Stop the flow after receiving exactly 80 id messages from the subscription. Do not process more than 80 messages (also counting discarded messages)
