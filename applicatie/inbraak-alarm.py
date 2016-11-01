import pyrebase
import datetime
import pygame

# Configuratie voor de firebase database
config = {
  'apiKey': 'AIzaSyDse4S8imxqiaDRELr58a8P45r7G5Af2go',
  'authDomain': 'miniproject-computersystems.firebaseapp.com',
  'databaseURL': 'https://miniproject-computersystems.firebaseio.com',
  'storageBucket': 'miniproject-computersystems.appspot.com',
  'serviceAccount': 'database/miniproject-computersystems-c79e0f2b03d3.json'
}

# Initaliseer applicatie via pyrebase & PyGame
firebase = pyrebase.initialize_app(config)
pygame.init()
screen = pygame.display.set_mode((1,1))

# Authenticeer applicatie
auth = firebase.auth()

# Firebase database connectie
db = firebase.database()

# Class inbraakalarm
class InbraakAlarm():

    # Initalisatie inbraakalarm
    # Statussen -> idle, armed, unarmed, settings
    def __init__(self):
        self._status = 'idle'

    # Haal de status op
    def get_status(self):
        return self._status

    # Wijzig de status
    def set_status(self, status):
        self._status = status
        db.child('logs').push({'status': self.get_status(), 'timestamp': str(datetime.datetime.now())})
        print('status wijziging')

    global_status = property(get_status, set_status)

# Begin de applicatie
if __name__ == '__main__':
    app = InbraakAlarm()

    # Laat de applicatie runnen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
            if event.type == pygame.KEYDOWN:

                # Werkt alleen als status unarmed is of idle
                if app.global_status == 'unarmed' or app.global_status == 'idle':
                    if event.key == pygame.K_LEFT:
                        app.global_status = 'armed'

                # Werkt alleen als status armed is
                if app.global_status == 'armed':
                    if event.key == pygame.K_RIGHT:
                        app.global_status = 'unarmed'
