from string import Template

sketch_template = Template("""
#include <avr/pgmspace.h>
#include "DigiKeyboard.h"

// Check this for preserving RAM https://web.archive.org/web/20210814101002/http://digistump.com/board/index.php/topic,2554.msg12242.html
#define gp( x ) (strcpy_P(buffer, (char*)x))
char buffer[66];
const char c0[] PROGMEM = "$password";

void setup() {
    // Make sure keyboard is ready
    DigiKeyboard.sendKeyStroke(0);
    DigiKeyboard.delay(250);
    // "Type" the password
    DigiKeyboard.print( gp(c0) );
    DigiKeyboard.delay(100);
    // Click "Enter"
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
}
  
void loop() {
    // This could run things in a loop and Arduino gets mad if you remove it
}
""".strip())
