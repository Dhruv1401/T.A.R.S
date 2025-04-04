#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Ultrasonic.h>
// Uses a Ultrasonic Sensor , ESP8226MOD , 0.96inch OLED DISPLaY
// Define the OLED screen (I2C address is usually 0x3C for most OLED displays)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define OLED_I2C_ADDR 0x3C  // The typical I2C address for most OLEDs

// Define pins for the ultrasonic sensor
#define TRIG_PIN 12  // D6 pin (GPIO12)
#define ECHO_PIN 13  // D7 pin (GPIO13)

// Threshold distance to detect obstacle (in centimeters)
#define OBSTACLE_THRESHOLD 100

// Initialize the OLED display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Initialize the Ultrasonic sensor
Ultrasonic ultrasonic(TRIG_PIN, ECHO_PIN);

void setup() {
  // Start Serial communication
  Serial.begin(115200);

  // Initialize the OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_I2C_ADDR)) {  // Use 0x3C for most OLED displays
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  // Initial message on OLED
  display.setCursor(0, 0);
  display.print(F("Ultrasonic Distance"));
  display.display();  // Update OLED with initial text
  
  delay(1000);  // Give some time for display initialization
}

void loop() {
  // Get distance from ultrasonic sensor
  long distance = ultrasonic.read();  // Distance in centimeters
  
  // Debugging: Print the raw distance to Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);  // Show the raw sensor value

  // Display "Distance:" on the first line
  display.clearDisplay();
  display.setCursor(0, 0);
  display.print(F("Distance:"));

  // Display the actual distance on the second line
  display.setCursor(0, 10);
  display.print(distance);  
  display.print(F(" cm"));

  // Check if there's an obstacle
  display.setCursor(0, 20);  // Start the 3rd line
  
  if (distance < OBSTACLE_THRESHOLD) {
    display.print(F("Obstacle Detected"));
  } else {
    display.print(F("No Obstacle in Range"));
  }

  // Print to Serial Monitor for debugging
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  display.display();  // Update the OLED display
  delay(100);  // Delay for 100 milliseconds before the next reading
}