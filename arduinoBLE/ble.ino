#include <ArduinoBLE.h>

#define UUID_SERVICE "5d6122f8-d277-41d9-a645-0e4648ea9dc3"
#define UUID_CHARACTERISTIC "6d365bb8-4387-4a96-8ac6-ba722671e7da"

BLEService carService(UUID_SERVICE);
BLEByteCharacteristic carMove(UUID_CHARACTERISTIC, BLERead | BLEWrite);


void switchOnLEDs(void);
void switchOffLEDs(void);
void printBits(byte);


void setup()
{

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

  Serial.begin(9600);


  while (!Serial)
    ;
  if (!BLE.begin())
  {
    Serial.println("starting BLE failed!");
    while (1)
      ;
  }

  Serial.println("starting BLE succeed");

  BLE.setLocalName("RCCar"); // name you'll see when scannig

  BLE.setAdvertisedService(carService);

  carService.addCharacteristic(carMove);

  BLE.addService(carService);

  carMove.writeValue(0);

  BLE.advertise();

  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop()
{

  // listen for BLE peripherals to connect:
  BLEDevice remote_device = BLE.central();

  // if a central is connected to peripheral:
  if (remote_device)
  {
    Serial.println("Connected to central: ");
    // print the central's MAC address:
    Serial.println(remote_device.address());

    while (remote_device.connected())
    {
      BLE.poll();
      if (carMove.written())
      {
        byte value = carMove.value();
        Serial.print("Value received : 0b");
        printBits(value);
        Serial.println();
        
        if (bitRead(value, 7) == 1) { // compat mode = 1
          switchOnLEDs();
          Serial.println("Extended mode");
        }
        else {
          switchOffLEDs();
          Serial.println("Compat mode");

          if (bitRead(value, 6) == 1) {
            Serial.println("Feature mode");
          }
          else {
            Serial.println("Manual mode");
            byte mask = (1 << 3) - 1;

            Serial.print("Order : ");

            switch (mask & value) {
              case 0x00:
                Serial.println("stop_forward");
                break;
              case 0x01:
                Serial.println("forward");
                break;
              case 0x02:
                Serial.println("stop_backward");
                break;
              case 0x03:
                Serial.println("backward");
                break;
              case 0x04:
                Serial.println("stop_left");
                break;
              case 0x05:
                Serial.println("left");
                break;
              case 0x06:
                Serial.println("stop_right");
                break;
              case 0x07:
                Serial.println("right");
                break;
              default:
                Serial.println("Order not recognized");
                break;

            }
          }
        }
      }
    }

    Serial.println("Remote device disconnected");
    delay(1000);
  }
}



void switchOnLEDs() {
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
}
void switchOffLEDs() {
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}

void printBits(byte myByte){
 for(byte mask = 0x80; mask; mask >>= 1){
   if(mask  & myByte)
       Serial.print('1');
   else
       Serial.print('0');
 }
}
