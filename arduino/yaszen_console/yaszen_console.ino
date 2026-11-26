// ============================================================
// YASZEN_V01 — Physical Deliberation Console
// "Empowering conscious humans in a world of intelligent machines"
//
// Firmware for the YASZEN physical console.
// Communicates bidirectionally with Python over Serial (9600 baud).
//
// WIRING:
//   Pin D9  --[220Ω]--> Yellow LED (+) --> GND   (Reflection / Sati)
//   Pin D10 --[220Ω]--> Red LED (+)    --> GND   (Ethical Alert / Sīla)
//   Pin D11 --[220Ω]--> Green LED (+)  --> GND   (Human Agency / Cetanā)
//   Pin D2  --> Button 1 --> GND   (Challenge)
//   Pin D3  --> Button 2 --> GND   (Impact)
//   Pin D4  --> Button 3 --> GND   (Decide / Sovereignty)
//
// Buttons use INPUT_PULLUP — no external resistors needed.
// ============================================================

const int BTN_CHALLENGE = 2;
const int BTN_IMPACT    = 3;
const int BTN_DECIDE    = 4;

const int LED_REFLECT   = 9;   // Yellow - PWM capable for breathing effect
const int LED_ETHICS    = 10;  // Red
const int LED_AGENCY    = 11;  // Green

unsigned long lastDebounce = 0;
const int DEBOUNCE_MS = 250;

// Breathing animation state
bool breathing = false;
int breathDirection = 1;
int breathValue = 0;
unsigned long lastBreathStep = 0;

void setup() {
  Serial.begin(9600);
  
  pinMode(BTN_CHALLENGE, INPUT_PULLUP);
  pinMode(BTN_IMPACT, INPUT_PULLUP);
  pinMode(BTN_DECIDE, INPUT_PULLUP);
  
  pinMode(LED_REFLECT, OUTPUT);
  pinMode(LED_ETHICS, OUTPUT);
  pinMode(LED_AGENCY, OUTPUT);

  // Boot sequence — flash all LEDs 3 times
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_REFLECT, HIGH);
    digitalWrite(LED_ETHICS, HIGH);
    digitalWrite(LED_AGENCY, HIGH);
    delay(150);
    digitalWrite(LED_REFLECT, LOW);
    digitalWrite(LED_ETHICS, LOW);
    digitalWrite(LED_AGENCY, LOW);
    delay(150);
  }
  
  Serial.println("YASZEN_READY");
}

void loop() {
  // === RECEIVE commands from Python ===
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "REFLECT_ON") {
      breathing = true;
      breathValue = 0;
      breathDirection = 1;
      digitalWrite(LED_ETHICS, LOW);
      digitalWrite(LED_AGENCY, LOW);
    }
    else if (cmd == "REFLECT_OFF") {
      breathing = false;
      analogWrite(LED_REFLECT, 0);
    }
    else if (cmd == "ETHICS_ON") {
      digitalWrite(LED_ETHICS, HIGH);
      breathing = false;
      analogWrite(LED_REFLECT, 0);
    }
    else if (cmd == "ETHICS_OFF") {
      digitalWrite(LED_ETHICS, LOW);
    }
    else if (cmd == "AGENCY_ON") {
      digitalWrite(LED_AGENCY, HIGH);
      digitalWrite(LED_ETHICS, LOW);
      breathing = false;
      analogWrite(LED_REFLECT, 0);
    }
    else if (cmd == "AGENCY_OFF") {
      digitalWrite(LED_AGENCY, LOW);
    }
    else if (cmd == "ALL_OFF") {
      breathing = false;
      analogWrite(LED_REFLECT, 0);
      digitalWrite(LED_ETHICS, LOW);
      digitalWrite(LED_AGENCY, LOW);
    }
    else if (cmd == "PING") {
      Serial.println("PONG");
    }
  }

  // === Breathing animation for reflection LED ===
  if (breathing && (millis() - lastBreathStep > 12)) {
    breathValue += breathDirection * 3;
    if (breathValue >= 255) {
      breathValue = 255;
      breathDirection = -1;
    } else if (breathValue <= 0) {
      breathValue = 0;
      breathDirection = 1;
    }
    analogWrite(LED_REFLECT, breathValue);
    lastBreathStep = millis();
  }

  // === SEND button presses to Python ===
  if (millis() - lastDebounce > DEBOUNCE_MS) {
    if (digitalRead(BTN_CHALLENGE) == LOW) {
      Serial.println("BTN:CHALLENGE");
      lastDebounce = millis();
    }
    if (digitalRead(BTN_IMPACT) == LOW) {
      Serial.println("BTN:IMPACT");
      lastDebounce = millis();
    }
    if (digitalRead(BTN_DECIDE) == LOW) {
      Serial.println("BTN:DECIDE");
      lastDebounce = millis();
    }
  }
}
