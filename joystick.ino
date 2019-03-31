int xvalue = 0;
int yvalue = 0;

void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin(115200);
}

void loop() {
  xvalue = analogRead(A0); // read X axis value [0..1023]
  yvalue = analogRead(A1); // read Y axis value [0..1023]
  Serial.print(xvalue, DEC);
  Serial.print(",");
  Serial.print(yvalue, DEC);
  Serial.print("\n");

  delay(50);
}
