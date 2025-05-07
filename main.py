from machine import Pin, PWM, RTC
import time
import network
import ntptime
import urequests as requests
import json

class Servo:
    def __init__(self, pino):
        self.pwm = PWM(Pin(pino), freq=50)

    def set_angle(self, angle):
        duty = int((angle / 180) * 75) + 40
        self.pwm.duty(duty)

    def acionar(self):
        print(">> Servo acionado")
        self.set_angle(90)
        time.sleep(1)
        self.set_angle(0)
        time.sleep(1)

class Timing:
    def __init__(self):
        self.rtc = RTC()
        try:
            ntptime.settime()
            tempo_local = time.localtime(time.time() - 3 * 3600)  # UTC-3
            self.rtc.datetime(tempo_local[0:3] + (0,) + tempo_local[3:6] + (0,))
            print("Hora sincronizada:", tempo_local)
        except:
            print("Erro ao sincronizar NTP")

    def hora_atual(self):
        return time.localtime(time.time() - 3 * 3600)[3]  # Só a hora (HH)

class ControlarServo:
    def __init__(self, servo, timing, url):
        self.servo = servo
        self.timing = timing
        self.last_hour = -1
        self.url = url

    def rodar(self):
        while True:
            try:
                resposta = requests.get(self.url)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    horarios = dados.get("horarios", [])
                    ligar_agora = dados.get("ligar_agora", False)

                    hora_atual = self.timing.hora_atual()
                    print("Hora atual:", hora_atual)

                    if ligar_agora:
                        print(">> Ação remota solicitada!")
                        self.servo.acionar()
                        self.last_hour = hora_atual

                    elif hora_atual in horarios and hora_atual != self.last_hour:
                        print(">> Ação por horário!")
                        self.servo.acionar()
                        self.last_hour = hora_atual

                resposta.close()
            except Exception as e:
                print("Erro ao consultar API:", e)

            time.sleep(10)  # Verifica a cada 10 segundos

def conectar_wifi(ssid, senha):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Conectando ao Wi-Fi...")
        wifi.connect(ssid, senha)
        while not wifi.isconnected():
            pass
    print("Wi-Fi conectado:", wifi.ifconfig())

conectar_wifi("nomewifi", "senha")
servo = Servo(pino=1) #pino do servo motor
tempo = Timing()


url_api = "url da api" #url da api
controlador = ControlarServo(servo, tempo, url_api)
controlador.rodar()
