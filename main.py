from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
import webbrowser
import threading
import time

Window.size = (600, 400)

class Horario(BoxLayout):
    def abrir_link(self, link):
        webbrowser.open(link)

class Hour(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "landscape"
        self.start_alarm()

    def build(self):
        return Horario()

    def start_alarm(self):
        threading.Thread(target=self.monitor_time).start()

    def monitor_time(self):
        aulas = [("Matemática", 0, 13, 24),  # Exemplo de horários de início das aulas
                 ("História", 4, 13, 24),
                 ("Inglês", 5, 15, 26)]

        while True:
            current_day = time.localtime().tm_wday
            # Obtenha a hora atual
            current_time = time.localtime()
            # Verifique se é hora de começar alguma aula
            for aula in aulas:
                if (current_day == aula[1]) and (current_time.tm_hour, current_time.tm_min) == (aula[2], aula[3] - 10):
                    # Agende o evento de exibir o popup de alerta para daqui a 10 minutos
                    Clock.schedule_once(lambda dt, aula_nome=aula[0]: self.show_alert_popup(aula_nome), 0)  # Exibe imediatamente
                    break
            time.sleep(60)  # Verifique a cada minuto

    def show_alert_popup(self, aula_nome):
        content = Label(text=f"Faltam 10 minutos para o início da aula de {aula_nome}!")
        popup = Popup(title="Alerta de Aula", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    Hour().run()
