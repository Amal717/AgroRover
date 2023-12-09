#define LEDX 5
#define LEDY 6

int Xaxis;
int Yaxis;

void setup() {
  pinMode(LEDX, OUTPUT);
  pinMode(LEDY, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    String cmd = Serial.readStringUntil('\n');
    Xaxis = getValue(cmd, "X-axis");
    Yaxis = getValue(cmd, "Y-axis");
    analogWrite(LEDX, Xaxis);
    analogWrite(LEDY, Yaxis);
  }
}



int getValue(String data, String key) {
  // Find the position of the key in the string
  int keyIndex = data.indexOf(key);

  // If the key is found
  if (keyIndex != -1) {
    // Find the position of the colon after the key
    int colonIndex = data.indexOf(':', keyIndex);

    // Extract the value substring
    String valueStr = data.substring(colonIndex + 1);

    // Convert the value substring to an integer
    int value = valueStr.toInt();

    return value;
  }

  // Return an error value if the key is not found
  return -1;
}