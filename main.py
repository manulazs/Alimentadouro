from machine import Pin, PWM, RTC
import time
import network
import ntptime

def conectar_wifi(ssid, senha):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Conectando ao Wi-Fi")
        wifi.connect(ssid, senha)
        while not wifi.isconnected():
            pass
    print('Conectado! IP:', wifi.ifconfig()[0])

#pino = pino usado pro servo
class servo:
    def __init__(self, pino):
        self.pwm = PMW (Pin(pin), freq=50) # Frequência de 50Hz se o servo for diferente teq mudar

    def set_angle(self, angle):
        # Converte o ângulo para o valor de duty cycle, se ai depende do angle que a gente quer
        duty = int((angle / 180) * 75) + 40
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

        try:
            ntptime.settime()
            