from machine import Pin, PWM, RTC
import time

#pino = pino usado pro servo
class servo:
    def __init__(self, pino):
        self.pwm = PMW (Pin(pin), freq=50) # Frequência de 50Hz se o servo for diferente teq mudar

    def set_angle(self, angle):
        # Converte o ângulo para o valor de duty cycle, se ai depende do angle que a gente quer
        duty = int(((angle / 180) * 75) + 25)
        self.pwm.duty(duty)

    def acionar(self):
        self.set_angle(90)
        time.sleep(1)
        self.set_angle(0)
        time.sleep(1)
        print("Servo acionado")

class Timing:
    def __init__(self):
        self.rtc = RTC()
        self.rtc.datetime((2023, 10, 1, 0, 0, 0, 0, 0)) # Define a data e hora inicial

    def set_time(self, year, month, day, hour, minute, second):
        self.rtc.datetime((year, month, day, 0, hour, minute, second, 0))

    def get_time(self):
        return self.rtc.datetime()