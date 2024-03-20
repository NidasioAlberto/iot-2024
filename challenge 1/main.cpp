#include <esp_now.h>
#include <WiFi.h>

// PIN number definition
#define PIN_TRIG 13
#define PIN_ECHO 14

// Constants
#define S_TO_US 1e6
#define HC_SR04_CONV 1.0 / 340.0 * 2.0 * 1e6 / 1e2

// Time to sleep calculation
#define PERSONAL_CODE 10665344
#define TIME_TO_SLEEP ((PERSONAL_CODE % 50) + 5) * S_TO_US

// Distance threshold to detect the precense of a car
#define DISTANCE_THRESHOLD 50.0

// MAC receiver
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90};

// Enable debug features
#define DEBUG

// Flag to notify the transmission of the data packet
long sent = 0;

esp_now_peer_info_t peerInfo;

void setup()
{
    String state;

#ifdef DEBUG
    long start_us = micros();
#endif

    // Setup phase
    {
        // Wifi configuration
        WiFi.mode(WIFI_STA);
        WiFi.setTxPower(WIFI_POWER_2dBm);
        esp_now_init();

        // Register callback setup
        esp_now_register_send_cb(OnDataSent);

        // Peer Registration
        memcpy(peerInfo.peer_addr, broadcastAddress, 6);
        peerInfo.channel = 0;
        peerInfo.encrypt = false;
        esp_now_add_peer(&peerInfo);

        // Add wakeup after deep sleep
        esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP);

        // Pins definition
        pinMode(PIN_TRIG, OUTPUT);
        pinMode(PIN_ECHO, INPUT);
    }

#ifdef DEBUG
    long end_of_setup_us = micros();
#endif

    // Measurement phase
    {
        // Get distance from the sensor
        float distance_cm = readDistanceCM();

        // Interpret distance
        state = distance_cm <= DISTANCE_THRESHOLD ? "OCCUPIED" : "FREE";
    }

#ifdef DEBUG
    long end_of_measure_us = micros();
#endif

    // Transmission phase
    {
        esp_now_send(broadcastAddress, (uint8_t *)state.c_str(), state.length() + 1);

        // Wait until the sendCallback is called
        while (sent == 0)
        {
            delayMicroseconds(1);
        }
    }

#ifdef DEBUG
    long end_of_transmission_us = micros();
#endif

    // Debug section to calculate and print each phase duration
#ifdef DEBUG
    Serial.begin(115200);

    long total_duration_us = end_of_transmission_us - start_us;
    long setup_duration_us = end_of_setup_us - start_us;
    long measure_duration_us = end_of_measure_us - end_of_setup_us;
    long transmission_duration_us = end_of_transmission_us - end_of_measure_us;

    Serial.println("Total execution: " + String(total_duration_us) + "us");
    Serial.println("Setup:           " + String(setup_duration_us) + "us");
    Serial.println("Measurement:     " + String(measure_duration_us) + "us");
    Serial.println("Transmission:    " + String(transmission_duration_us) + "us");
    Serial.println("State:           " + state);
    Serial.flush();
#endif

    // Go into deep-sleep
    esp_deep_sleep_start();
}

void loop()
{
    // Unused part of the code
    delay(10);
}

float readDistanceCM()
{
    // Generate a pulse of 10us to generate a sound wave
    digitalWrite(PIN_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_TRIG, LOW);

    // Measure signal
    int duration = pulseIn(PIN_ECHO, HIGH);

    // Return the distance in cm
    return duration / HC_SR04_CONV;
}

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
    // Get timestamp to calculate the time to send and to stop waiting in the main
    sent = micros();
}