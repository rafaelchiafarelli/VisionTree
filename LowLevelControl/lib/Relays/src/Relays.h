#ifndef _RELAYS_H_
#define _RELAYS_H_

#define FIRST 36
#define SECOND 34
#define THIRD 32
#define FORTH 30
#define FIFTH 28
#define SIXTH 26
#define SEVENTH 24
#define EIGTH 22

typedef enum{
    ON,
    OFF,
    UNKNOWN
}relay_state;

typedef enum {
    first = 0b00000001,
    second = 0b00000010,
    third = 0b000000100,
    forth = 0b000001000,
    fifth = 0b00010000,
    sixth = 0b00100000,
    seventh = 0b01000000,
    eigth = 0b10000000
}relay;

class Relays{
    private:
        relay_state r[8];
        void switch_relay(bool out, relay r){
            int state = (int)(!out);

            switch (r)
            {
            case first:
                digitalWrite(FIRST,state);
                break;
            case second:
                digitalWrite(SECOND,state);
                break;
            case third:
                digitalWrite(THIRD,state);
                break;
            case forth:
                digitalWrite(FORTH,state);
                break;
            case fifth:
                digitalWrite(FIFTH,state);
                break;
            case sixth:
                digitalWrite(SIXTH,state);
                break;
            case seventh:
                digitalWrite(SEVENTH,state);
                break;
            case eigth:
                digitalWrite(EIGTH,state);
                break;                                                                                                            
            default:
                break;
            }
        }
    public:
        void set_relays(uint8_t r){
            
            
            switch_relay(((r&first) == first),first);
            switch_relay(((r&second) == second),second);
            switch_relay(((r&third) == third),third);
            switch_relay(((r&forth) == forth),forth);
            switch_relay(((r&fifth) == fifth),fifth);
            switch_relay(((r&sixth) == sixth),sixth);
            switch_relay(((r&seventh) == seventh),seventh);
            switch_relay(((r&eigth) == eigth),eigth);
        }

        Relays(){
            pinMode(FIRST,OUTPUT);
            pinMode(SECOND,OUTPUT);
            pinMode(THIRD,OUTPUT);
            pinMode(FORTH,OUTPUT);
            pinMode(FIFTH,OUTPUT);
            pinMode(SIXTH,OUTPUT);
            pinMode(SEVENTH,OUTPUT);
            pinMode(EIGTH,OUTPUT);
        }
};
#endif