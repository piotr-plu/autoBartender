from time import sleep, ticks_ms 
from machine import I2C, Pin, PWM
from i2c_lcd import I2cLcd

#Czas testowania
test_time = 2

#Pin przełącznika
switch = Pin(12, Pin.IN)

#Piny diody
led_r = Pin(4, Pin.OUT)
led_g = Pin(2, Pin.OUT)
led_b = Pin(15, Pin.OUT)

#Piny pompki
pomp_one = Pin(33, Pin.OUT)
pomp_two = Pin(25, Pin.OUT)
pomp_three = Pin(26, Pin.OUT)
pomp_four = Pin(27, Pin.OUT)
pomp_five = Pin(14, Pin.OUT)

#Piny przyciski
button_up = Pin(34, Pin.IN, Pin.PULL_UP)
button_ok = Pin(35, Pin.IN, Pin.PULL_UP)
button_down = Pin(32, Pin.IN, Pin.PULL_UP)

#Piny buzzer
p13 = Pin(13, Pin.OUT)
buzzer = PWM(p13)
buzzer.freq(1047)
buzzer.duty(0)

#Konfiguracja wyświetlacza LCD 16x2
DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.move_to(2,0)
buzzer.duty(200)
sleep(0.2)
buzzer.duty(0)
lcd.putstr("AutoBartender")
lcd.move_to(2,1)
lcd.putstr("version 0.6")
sleep(2)
lcd.clear()
lcd.move_to(1,0)
lcd.putstr("Testing Pumps: ")
j = 0
for i in [pomp_one, pomp_two, pomp_three, pomp_four, pomp_five]:
  j = j+1
  lcd.move_to(5,1)
  lcd.putstr(f"{j} of 5")
  i.on()
  sleep(test_time)
  i.off()
lcd.clear()

import main
  