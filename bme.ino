/**
 * Copyright (C) 2021 Bosch Sensortec GmbH
 *
 * SPDX-License-Identifier: BSD-3-Clause
 * 
 */

#include <M5Core2.h>
#include "bme68xLibrary.h"

#define NEW_GAS_MEAS (BME68X_GASM_VALID_MSK | BME68X_HEAT_STAB_MSK | BME68X_NEW_DATA_MSK)
#define MEAS_DUR 140
#define MEAS_NUM 9

// CORE2
#define SDA_PIN 32
#define SCL_PIN 33

// Grove
//#define SDA_PIN 26
//#define SCL_PIN 32

#define BME688_I2C_ADDR 0x76

#include <math.h>
Bme68x bme;

typedef struct _sensor_data{
  float temperature;
  float humid;
  float pressure;
  float sensor[MEAS_NUM];
};
_sensor_data sd;

// initialize
void setup(void)
{
  M5.begin(true, true, true);
  delay(100);

  M5.Lcd.setTextColor(YELLOW);
  M5.Lcd.setTextSize(3);
  M5.Lcd.println("M5Core2");
    
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);

  while (!Serial)
  {
    delay(140);
  }

  /* initializes the sensor based on SPI library */
  bme.begin(BME688_I2C_ADDR, Wire);
  if(bme.checkStatus())
  {
    if (bme.checkStatus() == BME68X_ERROR)
    {
      Serial.println("Sensor error:" + bme.statusString());
      M5.Lcd.println("BME ERROR");
      M5.Lcd.println(bme.statusString());
      delay(5000);
      return;
    }
    else if (bme.checkStatus() == BME68X_WARNING)
    {
      Serial.println("Sensor Warning:" + bme.statusString());
      M5.Lcd.println("BME Warning");
      M5.Lcd.println(bme.statusString());
      delay(5000);
    }
  }
  
  M5.Lcd.println("BME setup");
  delay(1000);

  /* Set the default configuration for temperature, pressure and humidity */
  bme.setTPH();

  /* Heater temperature in degree Celsius */
  uint16_t tempProf[10] = { 320, 100, 100, 100, 200, 200, 320, 320,320 };
  /* Multiplier to the shared heater duration */
  uint16_t mulProf[10] = { 5, 2, 10, 5, 5, 5, 5, 5, 5 };
  /* Shared heating duration in milliseconds */
  uint16_t sharedHeatrDur = MEAS_DUR - (bme.getMeasDur(BME68X_PARALLEL_MODE) / 1000);

  bme.setHeaterProf(tempProf, mulProf, sharedHeatrDur, 10);
  bme.setOpMode(BME68X_PARALLEL_MODE);
}

// main loop
void loop(void)
{
  bme68xData data;
  uint8_t nFieldsLeft = 0;
  
  /* data being fetched for every 140ms */
  delay(MEAS_DUR);

  if (bme.fetchData())
  {
    do
    {
      nFieldsLeft = bme.getData(data);
      if (data.status == NEW_GAS_MEAS)
      {
        // for display
        if(data.gas_index==0){
          M5.Lcd.clearDisplay();
          M5.Lcd.setCursor(0,0);
          M5.Lcd.println("tempe: " + String(data.temperature));
          M5.Lcd.println("humid: " + String(data.humidity));
          M5.Lcd.println("press: " + String(data.pressure));
          M5.Lcd.println("resis: " + String((data.gas_resistance)/1000));
        }
        
        // for serial-output
        if(data.gas_index==0){
          // Serial.print("data,");
          // Serial.print(String(data.temperature) + ",");
          // Serial.print(String(data.humidity) + ",");
          // Serial.print(String(data.pressure/100,2) + ",");

          sd.temperature = data.temperature;
          sd.pressure = data.pressure;
          sd.humid = data.humidity;

          for (int i=0; i < MEAS_NUM; i++){
            sd.sensor[i] = 0;
          }  
        }
        
        float current = log(data.gas_resistance);
        sd.sensor[data.gas_index] = current;

        if(data.gas_index==MEAS_NUM -1 ){
          Serial.print("data");Serial.print(",");
          Serial.print(sd.temperature);Serial.print(",");
          Serial.print(sd.humid);Serial.print(",");
          Serial.print(sd.pressure);Serial.print(",");

          for (int i=0; i < MEAS_NUM; i++){
            Serial.print(String(sd.sensor[i],3));Serial.print(",");
          }          
          Serial.println();
        }
          
      }
    } while (nFieldsLeft);
  } else {
    //M5.Lcd.clearDisplay();
    //M5.Lcd.setCursor(0,0);
    //M5.Lcd.println("....No DATA");
    //delay(30);
  }
}