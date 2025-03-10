#include <Adafruit_NeoPixel.h>

#define PIN 8
#define NUMPIXELS 24

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'
}

void loop() {
    uint32_t colors[] = {strip.Color(255, 0, 0), strip.Color(0, 255, 0), strip.Color(0, 0, 255)}; // Red, Green, Blue
    int numColors = sizeof(colors) / sizeof(colors[0]);

    for(int i=0; i<strip.numPixels(); i++) {
        for(int j=0; j<numColors; j++) {
            strip.setPixelColor(i, colors[j]);
            strip.show();
            delay(50);
            strip.setPixelColor(i, strip.Color(0, 0, 0)); // Turn off the pixel
        }
    }
}