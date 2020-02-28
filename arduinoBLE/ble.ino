#include <ArduinoBLE.h>

#define UUID_SERVICE "5d6122f8-d277-41d9-a645-0e4648ea9dc3"
#define UUID_CHARACTERISTIC "6d365bb8-4387-4a96-8ac6-ba722671e7da"

BLEService carService(UUID_SERVICE);
BLEByteCharacteristic carMove(UUID_CHARACTERISTIC, BLERead | BLEWrite);


void switchOnLEDs(void);
void switchOffLEDs(void);
void printBits(byte);
void pwm(int, byte);


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

  for (size_t i = 0; i < 4; ++i) {
    switchOnLEDs();
    delay(200);
    switchOffLEDs();
    delay(200);
  }

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

        if (bitRead(value, 7) == 1) { // compat mode = 1
          Serial.println("Extended mode");
        }
        else {
          Serial.println("Compat mode");

          if (bitRead(value, 6) == 1) {
            Serial.println("Feature mode");
          }
          else {
            Serial.println("Manual mode");
            Serial.print("Order : ");

            switch (value & 7) { // on extrait les 3 derniers bits
              case 0x00:
                Serial.println("stop_forward");
                analogWrite(3, 0);
                break;
              case 0x01:
                Serial.println("forward");
                pwm(3, value);
                break;
              case 0x02:
                Serial.println("stop_backward");
                analogWrite(2, 0);
                break;
              case 0x03:
                Serial.println("backward");
                pwm(2, value);
                break;
              case 0x04:
                Serial.println("stop_left");
                digitalWrite(4, LOW);
                break;
              case 0x05:
                Serial.println("left");
                digitalWrite(4, HIGH);
                break;
              case 0x06:
                Serial.println("stop_right");
                digitalWrite(5, LOW);
                break;
              case 0x07:
                Serial.println("right");
                digitalWrite(5, HIGH);
                break;
              default:
                Serial.println("Order not recognized");
                break;

            }
          }
        }
      }
    }

    switchOffLEDs();
    Serial.println("Remote device disconnected");
    delay(1000);
  }
}

void switchOffLEDs(void) {
  analogWrite(2, 0);
  analogWrite(3, 0);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}


void switchOnLEDs(void) {
  analogWrite(2, 255);
  analogWrite(3, 255);
  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
}


void printBits(byte myByte) {
  for (byte mask = 0x80; mask; mask >>= 1) {
    if (mask  & myByte)
      Serial.print('1');
    else
      Serial.print('0');
  }
  Serial.println();
}

void pwm(int pin, byte value) {
  byte speed = (((((value >> 3) - 1) & 7) + 1) << 5) - 1; // pour avoir 000 = 100% (beewii compat) et scale sur 3 bits (0-255)
  analogWrite(pin, speed);
  Serial.print("Speed (0 to 255) :");
  Serial.println(speed);
}
