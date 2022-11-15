from string import Template

sketch_template = Template("""
#include <avr/pgmspace.h>
#include "DigiKeyboard.h"

// Check this for preserving RAM http://digistump.com/board/index.php/topic,2554.msg12242.html#msg12242
#define gp( x ) (strcpy_P(buffer, (char*)x))
char buffer[66];

const char c0[] PROGMEM = "$password";

// Enter
void en() {
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
}

// Print
void pr(String text) {
    DigiKeyboard.print(text);   
}

// Sleep
void sl(int time) {
    DigiKeyboard.delay(time);
}

void setup() {
    DigiKeyboard.sendKeyStroke(0);
    sl(300);
    pr( gp(c0) );
    sl(100);
    en();
    en();
}
  
void loop() {
    // put your main code here, to run repeatedly
}
""".strip())
