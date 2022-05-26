from time import sleep, sleep_ms, ticks_ms
from machine import I2C, Pin, PWM
from i2c_lcd import I2cLcd

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
########################################################################
#/\ Kod z boot.py - tymczasowo tu aby importować potrzebne biblioteki


class Cocktail:
    def __init__ (self, name, amount_ing_1, amount_ing_2, amount_ing_3, amount_ing_4, amount_ing_5, mixer):
        self.cocktail_name = name
        self.amount_ing_1 = amount_ing_1
        self.amount_ing_2 = amount_ing_2
        self.amount_ing_3 = amount_ing_3
        self.amount_ing_4 = amount_ing_4
        self.amount_ing_5 = amount_ing_5
        self.mixer = mixer

# Testowo, Klasa odczytu z karty pamięci będzie pełnić te funkcje
cocktail_1 = Cocktail('Whisky Sour', 50, 35, 12.5, 0, 0, 'Nothing')
cocktail_2 = Cocktail('Clear Whisky',40, 0, 0, 0, 0, 'Nothing')
recipes = [cocktail_1, cocktail_2]

# odliczanie czasu, raczej nie potrzebna funkcja 
def countdown(seconds):
    while seconds != 0:
        lcd.move_to(1,1)
        lcd.putstr(f"Ready in: {seconds}")
        sleep(1)
        lcd.move_to(11,1)
        lcd.putstr("   s")
        seconds -= 1
        
def use_buzzer():
    buzzer.freq(1047)
    buzzer.duty(200)
    sleep(0.2)
    buzzer.duty(0)

def menu_title():
    lcd.clear()
    lcd.putstr('Select cocktail:')
    menu_cocktail(0)
    
def menu_cocktail(position):
    lcd.move_to(0,1)
    lcd.putstr('                ')
    lcd.move_to(0,1)
    lcd.putstr('>'+recipes[position].cocktail_name)

def make_cocktail():
    lcd.clear()
    lcd.move_to(1,0)
    lcd.putstr("Making cocktail")
    countdown(10)
    lcd.clear()
    lcd.putstr("Coctail Ready")
    sleep(1)
    menu_title()
    
pressed_button = 0
lastUse = 0
position = 0

# obsługa zmiennej position
def handle_position(button):
    global position
    
    if button == button_up:
        position += 1
        use_buzzer()
        if position > len(recipes)-1:
            position = 0
        
    elif button == button_ok:
        use_buzzer()
        make_cocktail()
        
    elif button == button_down:
        position -= 1
        use_buzzer()
        if position < 0:
            position = len(recipes)-1

    menu_cocktail(position)
        
# obsługa przerwania   
def handle_button(pin):
    global lastUse
    global pressed_button
    currentTime = ticks_ms()
    if ((currentTime - lastUse) > 300):
        lastUse = currentTime
        pressed_button = pin

# aktywacja przerwań
button_up.irq(trigger=Pin.IRQ_FALLING, handler=handle_button)
button_ok.irq(trigger=Pin.IRQ_FALLING, handler=handle_button)
button_down.irq(trigger=Pin.IRQ_FALLING, handler=handle_button)

menu_title()
buzzer.duty(0)
while True:
        if pressed_button != 0:
            handle_position(pressed_button)
            pressed_button = 0
            
        
        
        
           
      
        

        