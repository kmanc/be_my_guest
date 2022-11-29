from string import Template

sketch_template = Template("""
#include <avr/pgmspace.h>
#include "DigiKeyboard.h"

// Check this for preserving RAM https://web.archive.org/web/20210814101002/http://digistump.com/board/index.php/topic,2554.msg12242.html
#define gp( x ) (strcpy_P(buffer, (char*)x))
char buffer[66];
const char c0[] PROGMEM = "$password";

void setup() {
    DigiKeyboard.sendKeyStroke(0);
    DigiKeyboard.delay(300);
    DigiKeyboard.print( gp(c0) );
    DigiKeyboard.delay(100);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    // I don't know why this has to be repeated but something isn't working right
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
}
  
void loop() {
    // put your main code here, to run repeatedly
}
""".strip())
