
#define IN1 5
#define IN2 6
#define ENA 7

#define IN3 8
#define IN4 9
#define ENB 10

// X-axis Values
#define min_x 0
#define mid_x 128
#define max_x 255

#define min_y 0
#define mid_y 128
#define max_y 255

#define min_speed 70

int Xaxis;
int Yaxis;
int speedA;
int speedB;

void setup() {
  // put your setup code here, to run once:
  initialize_motor();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    process_commands();
    control_rover();
  }
  else{
    stop_rover();
    speed();
  }

}


void process_commands(){
    String cmd = Serial.readStringUntil('\n');
    Xaxis = getValue(cmd, "X-axis");
    Yaxis = getValue(cmd, "Y-axis");
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