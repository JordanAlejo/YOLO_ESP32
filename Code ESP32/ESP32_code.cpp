#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "TU_WIFI";
const char* password = "TU_CONTRASEÑA";

#define LED_ROJO 25
#define LED_VERDE 26

WebServer server(80);

void controlarLuces() {

  String comando = server.arg("cmd");

  if (comando == "carro") {
    digitalWrite(LED_ROJO, HIGH);
    digitalWrite(LED_VERDE, LOW);
  }

  else if (comando == "moto") {
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, HIGH);
  }

  else if (comando == "apagado") {
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, LOW);
  }

  server.send(200, "text/plain", "OK");
}

void setup() {

  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_VERDE, LOW);

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  server.on("/led", HTTP_GET, controlarLuces);

  server.begin();
}

void loop() {
  server.handleClient();
}