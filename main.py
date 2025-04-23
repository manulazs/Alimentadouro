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
            tempo_local = time.localtime(time() - 3 * 3600)  # Ajuste para UTC-3
            self.rtc.datetime(tempo_local)
            print("Hora ajustada para o horário local:", tempo_local)

        except:
            print("Erro ao sincronizar com o servidor NTP.")
    
    def hora_atual(self):
        return self.rtc.datetime()[4]  # Retorna a hora
    
class controlar_servo:
    def __init__(self, servo, timing):
        self.servo = servo
        self.timing = timing
        self.last_hour = -1  # Inicializa com um valor inválido

    def rodar(self):
        while True:
            hora = self.timing.hora_atual()
            if hora != self.last_hour:
                self.servo.acionar()
                self.last_hour = hora
            time.sleep(60)

conectar_wifi("nome_wifi", "senha_wifi")
servo = servo(x)  # Pino do servo
relogio = Timing()
controlar = controlar_servo(servo, relogio)
