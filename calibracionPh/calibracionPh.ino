/*
 
 =======================
  ARDUINO UNO   SENSOR PH
 =======================
  GND               GND
  5V                Vcc
  A1                P0
  A2                T0

*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

#define PIN_SENSOR_PH        A1
#define PIN_SENSOR_PH_T      A2

#define mostrarMensaje(x) Serial.print(x); lcd.print(x);

float PH = -100;  

void setup() {
  Serial.begin(115200);  
  lcd.init();
  lcd.backlight();
}

void loop() {
  
  medir_ph();
  delay(200);

}


/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
//    SENSOR DE PH
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/

//========================================================
//  OBTENER DATOS DESDE EL SENSOR ANALOGICO DE PH
//========================================================
int fila=0;
void medir_ph() 
{
  int buffer_lecturas[10];
  int temp;
  
  /* toma de muestras */
  for(int i=0;i<10;i++) { 
    buffer_lecturas[i] = analogRead(PIN_SENSOR_PH);
    delay(100);
  }
  
  /* ordenar las muestas de menor a mayor */
  for(int i=0;i<9;i++){
    for(int j=i+1;j<10;j++){
      if(buffer_lecturas[i]>buffer_lecturas[j]){
        temp=buffer_lecturas[i];
        buffer_lecturas[i]=buffer_lecturas[j];
        buffer_lecturas[j]=temp;
      }
    }
  }

  /* calcular el valor medio despreciando los dos valores menores y los dos mayores */
  float valor_medio = 0; 
  for(int i=2;i<8;i++){
    valor_medio+=buffer_lecturas[i];
  }

  valor_medio = valor_medio/6;

  /* obtener el voltage asociado a la lectura del pin analogico (sin utilidad por ahora) */
  float Vph = valor_medio*5.0/1023;  

  mostrarMensaje(valor_medio);
  mostrarMensaje(" ");
  mostrarMensaje(Vph);
  mostrarMensaje(" ");
  

  /* ---  calculo del PH usando dos medidas de ph conocidas para calibrar --- */
  float ph_bajo = 3.4;        // Vinagre, ph = 3.4
  float adc_ph_bajo = 740;    // valor ADC para ph = 3.4          (ph obtenidos con papel tornasol)

  
  float ph_alto = 8;          // Agua del grifo, ph = 8
  float adc_ph_alto = 640;    // valor ADC para ph = 8  
  
  float PH2 = (valor_medio - adc_ph_alto ) * ((ph_alto-ph_bajo) / ( adc_ph_alto - adc_ph_bajo )) + ph_alto;

  mostrarMensaje(PH2);
  Serial.println(""); lcd.setCursor(0,(fila++)%4);
}
