from machine import Pin, PWM, RTC
import time
import network
import ntptime
import urequests as requests

def conectar_wifi(ssid, senha):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Conectando ao Wi-Fi")
        wifi.connect(ssid, senha)
        while not wifi.isconnected():
            pass
    print('Conectado!')

#pino = pino usado pro servo
class Servo:
    def __init__(self, pino):
        self.pwm = PMW (Pin(pino), freq=50) # Frequência de 50Hz se o servo for diferente teq mudar

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
            self.rtc.datetime(tempo_local[0:3] + (0,) + tempo_local[3:6] + (0,))
            
            print("Hora ajustada para o horário local:", tempo_local)

        except:
            print("Erro ao sincronizar com o servidor NTP.")
    
    def hora_atual(self):
        tempo_local = time.localtime(time.time() - 3 * 3600)[3] # Retorna apenas a hora
    
class controlar_servo:
    def __init__(self, servo, timing, url_api):
        self.servo = servo
        self.timing = timing
        self.url_api = url_api
        self.last_hour = -1  # Inicializa com um valor inválido

    def config(self):
        try:
            response = requests.get(self.url_api)
            if response.status_code == 200:
                return response.json()
        
        except:
            print("Erro ao conectar com a API.")

        return {}            


    def rodar(self):
        while True:
            dados = self.config()
            horarios = dados.get("horarios", [])
            ligar_agora = dados.get("ligar_agora", False)

            hora = self.timing.hora_atual()

            if ligar_agora:
                print("acionando servo agora")
                self.servo.acionar()
                time.sleep(60)  # Espera 1 minuto para evitar acionamento repetido

            elif hora in horarios and hora != self.last_hour:
                print(f"horario programado {hora} acionando servo")
                self.servo.acionar()
                self.last_hour = hora

        time.sleep(10)

conectar_wifi("nome_wifi", "senha_wifi")

url_api = "http://api.com/horarios"  # URL da API que fornece os horários


servo = Servo(pino = 1)  # Pino do servo
relogio = Timing()
controlar = controlar_servo(servo, relogio, url_api)
controlar.rodar()