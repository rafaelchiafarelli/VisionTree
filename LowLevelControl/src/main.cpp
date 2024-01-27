#include <Arduino.h>
#include <Communication.h>
#include <Relays.h>
#include <SoftwareSerial.h>

Relays rs;
#define HART_BEAT 8192
#define MAX_SIZE 50
#define HART_BEAT_ERROR 10
size_t a;
long int counter;
/* {r:255}\r */
/* {r:000}\r */
uint8_t buffer[MAX_SIZE]; 
char param[4];
uint8_t relays;
char hart_beat[10];
long int hart_beat_counter;

void setup() {
  // put your setup code here, to run once:
  hart_beat_counter = 0;
  Serial.begin(115200);
  Serial.setTimeout(1000);
  a = 0;
  counter = 0;
  relays = 0;
}

void loop() {
  // put your main code here, to run repeatedly:

  if(Serial.available())
  {
    a = Serial.readBytesUntil('\n',buffer,(size_t)MAX_SIZE);
    Serial.println((char *)buffer);
  }
  if(a >= 6)
  {
    if(buffer[0] == '{' && buffer[6] == '}')
    {
      param[0] = buffer[3];
      param[1] = buffer[4];
      param[2] = buffer[5];
      param[3] = 0;
      relays = atoi(param);      
      hart_beat_counter = 0;
    }
  }
  rs.set_relays(relays);
  memset(buffer,0,MAX_SIZE);
  a = 0;
  counter+=1;
  if(counter > HART_BEAT)
  {
    

    sprintf(hart_beat,"{r:%03d}\r\n",relays);
    Serial.print(hart_beat);
    counter = 0;
    hart_beat_counter+=1;
    if (hart_beat_counter > HART_BEAT_ERROR)
    {
      relays = 0;
      hart_beat_counter = 0;
      Serial.println("ERROR - SHUTDOWN ALL OUTPUTS");
    }
  }
  

}
