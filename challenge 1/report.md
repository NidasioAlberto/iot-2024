# Challenge 1: Wokwi and Power Consumption

The Node aim is to communicate to a central sink node the occupancy of a parking slot.

## Application requirements

The node has to:
- Periodically sample the HC-SR04 sensor
- Understand if a car is present or not
- Transmit the data sample (FREE/OCCUPIED)
- Go in deep sleep state for some time

The node should:
- Consume the less amount of power possible

Parametrs:
- Duty cycle: $(44 \space \% \space 50) + 5 = 49s$
- Battery energy: $5344 + 5 = 5349Joule$

## Assumptions

- The sink node has no energy constraints
- The sink node is always reachable by every sensor node
- A sensor node is present on every parking spot

## Parameters


Send time: 

## 1: Application code

### Overall code structure

The application code is rather simple as there are 4 steps:
1. **Boot**: When the device boots up, the ESP-NOW protocol, transmission power and sensor are initialized
2. **Measurement**: A sensor measurement is performed
3. **Transmission**: The parking spot state is sent via radio
4. **Deep-sleep**: The MCU enters in deep sleep state

### Estimation of state durations

In order to estimate the duration of each of the states, we both made empirical measurements and theoretical calculations.

#### Boot phase

The boot process takes XXX

#### Measurement phase

Measured: max 24ms
Theoretical: 23.53ms + 10uS (from datasheet and theory)

#### Transmission phase

Measured: 825us

#### Deep-sleep phase

This duration is fixed by the project requirements.

## 2: Energy consumption esitmation

Tasks:
- Perform an energy consumption esitmation of the sensor node
  - Esimate the average power consumption for each state of the node (deep slee, idle, transmission state, sensor reading)
  - Estimate the energy consumption of 1 transmission cycle
- Estimate the time the sensor node last before changing the battery

Notes:
- Refer to the power consumption CSV file measurements for the estimation of the power and energy consumption

From the provided log files:
- Deep sleep: 60mW
- Sensor reading: 470mW
- Transmission at 19.5dBm: 800mW
- Transmission at 2dBm: 1250mW

TODO: Compare with datasheet

## 3: Comments on results and possible improvements

Tasks:
- Provide a small comment on the implemented system
- Starting from the system requirements, propose some possible improvements in terms of energy consumption without modifying the main task "notify to a sink node the occupancy state of a parking spot"

## Notes

Does pulseIn have a timeout feature? Or perhaps the sensor itself? Otherwise we could be waiting for a measurement that will be 100% wrong. If we would have a timeout, we could know if the measurement failed, and if it failed we could retry or give up.