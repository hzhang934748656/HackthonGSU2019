/*  Connects to the home WiFi network
 *  Asks some network parameters
 *  Starts WiFi server with fix IP and listens
 *  Receives and sends messages to the client
 *  Communicates: wifi_client_01.ino
 */
#include <SPI.h>
#include <ESP8266WiFi.h>

int buf = 0;
int xcoordinate = 0;
int ycoordinate = 0;
int button = 0;
bool debug = true;

byte ledPin = 2;
char ssid[] = "your ssid";               // SSID of your home WiFi
char pass[] = "your password";               // password of your home WiFi
WiFiServer server(80);                    

IPAddress ip(192, 168, 43, 80);            // IP address of the server
IPAddress gateway(192,168,43,93);           // gateway of your network
IPAddress subnet(255,255,255,0);          // subnet mask of your network

void setup() {
  Serial.begin(115200);                   // only for debug
  pinMode(D7, INPUT);
  WiFi.config(ip, gateway, subnet);       // forces to use the fix IP
  WiFi.begin(ssid, pass);                 // connects to the WiFi router
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  server.begin();                         // starts the server
/*  Serial.println("Connected to wifi");
  Serial.print("Status: "); Serial.println(WiFi.status());  // some parameters from the network
  Serial.print("IP: ");     Serial.println(WiFi.localIP());
  Serial.print("Subnet: "); Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: "); Serial.println(WiFi.gatewayIP());
  Serial.print("SSID: "); Serial.println(WiFi.SSID());
  Serial.print("Signal: "); Serial.println(WiFi.RSSI());
  Serial.print("Networks: "); Serial.println(WiFi.scanNetworks());*/
  pinMode(ledPin, OUTPUT);
}

void loop () {
  WiFiClient client = server.available();
  if (Serial.available() > 0)
  {
    readCoordinates();
    if (debug == true)
    {
      Serial.print(xcoordinate);
      Serial.print(", ");
      Serial.print(ycoordinate);
      Serial.print(", ");
      Serial.println(button);     
    }
  }
  if (client) {
    if (client.connected()) {
      digitalWrite(ledPin, LOW);  // to show the communication only (inverted logic)
      Serial.println("");
      String request = client.readStringUntil('\r');    // receives the message from the client
      Serial.print("From client: "); 
      Serial.println(request);
      client.flush();
      //client.println("Hi client! No, I am listening.\r"); // sends the answer to the client
      client.print(xcoordinate);
      client.print(", ");
      client.print(ycoordinate);
      client.print(", ");
      client.print(button); 
      client.print("\r");
      digitalWrite(ledPin, HIGH);
    }
    client.stop();                // tarminates the connection with the client
  }
}

void readCoordinates(){
    button = digitalRead(D7);
    byte character = Serial.read(); //read the first byte on serial
    if(character != 10 && character != ',') //newline(10) and , are special
    { 
        buf = buf*10;
        buf += (int)(character - '0'); //these two lines turn the string into an integer
    } 
    else if(character == ',')
    {
        xcoordinate = buf; //after a comma the buffer has the x coordinate
        buf = 0;
    } 
    else 
    {
        ycoordinate = buf; //after a space the buffer has the y coordinate
        buf = 0;
    }
}
