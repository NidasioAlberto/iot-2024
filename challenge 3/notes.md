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

- [ ] Subscribe to the topic `challenge3/id_generator`
- [ ] Compute $N = ID \space \% \space 7711$
- [ ] Process `challenge3.csv` and take the line with `No.` equal to `N`
- [ ] For every MQTT `Publish Message` then
  - [ ] Send a message on the specified topic with payload
    - [ ] `timestamp` the current timestamp
    - [ ] `id` message id received from the subscription (not `N`)
    - [ ] `payload` from the line payload
  - [ ] Limit the messages published to 4 per minute
  - [ ] If the published message contains a temperature in fahrenheit, plot its value
    - [ ] Only temperature in Fahrenheit
    - [ ] Temperature from range ((min + max) / 2)
    - [ ] When plotting (after the rate limiter) save the payload of the messages in `filtered_pubs.csv` (it will have one message payload per line)
      - [ ] Format: `No.`, `LONG`, `RANGE`, `LAT`, `TYPE`, `UNIT`, `DESCRIPTION` where `No.` is an incremental counter
    - [ ] If some payload are empty, ignore them
- [ ] If the message is an MQTT ACK
  - [ ] Increment a global ACK counter
  - [ ] Save the message into `ack_log.csv`
    - [ ] Format: `TIMESTAMP,SUB_ID,MSG_TYPE`
      - [ ] `TIMESTAMP`  is the current time when the msg is saved in the CSV
      - [ ] `SUB_ID` is the message id received from teh subscription (not `N`)
      - [ ] `MSG_TYPE` is the message type (Connect Ack, ...)
    - [ ] Send the value of the global ACK counter to your thingspeak channel, passing the filed1 of the channel the value of the global ACK counter. Send using HTTP API
- [ ] In all other cases ignore the message

- [ ] Stop the flow after receiving exactly 80 id messages from the subscription. Do not process more than 80 messages (also counting discarded messages)
