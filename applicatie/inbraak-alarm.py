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
        self._previous_status = 'idle'
        self._beveiligingscode = '0000'
        self._userbeveiliginscode = ''

    # Haal de status op
    def get_status(self):
        return self._status

    # Wijzig de status
    def set_status(self, status):
        self._previous_status = self._status
        self._status = status
        print('STATUS: {}'.format(self._status))
        db.child('logs').push({'status': self.get_status(), 'timestamp': str(datetime.datetime.now())})

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
                    # Indien de key Up wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_UP:
                        print('Je kunt je code invoeren')
                        app.global_status = 'inputcode'

                # Werkt alleen als status armed is
                if app.global_status == 'armed':
                    # Indien de key Up wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_UP:
                        print('Je kunt je code invoeren')
                        app.global_status = 'inputcode'

                # Werkt alleen als er een code ingevoerd moet worden
                if app.global_status == 'inputcode':
                    if event.key and event.key != pygame.K_UP:

                        # Alleen nieuwe code cijfers toevoegen indien de vorige code kleiner is dan 4
                        if len(app._userbeveiliginscode) < 4:
                            app._userbeveiliginscode += pygame.key.name(event.key)

                        # Als de code gelijk is aan 4 cijfers, dan check je of de code juist is ingevoerd
                        if len(app._userbeveiliginscode) == 4:
                            if app._beveiligingscode == app._userbeveiliginscode:
                                print('De code is juist ingevoerd, de status wordt ingesteld naar armed')
                                if app._previous_status == 'unarmed' or app._previous_status == 'idle':
                                    app.global_status = 'armed'
                                elif app._previous_status == 'armed':
                                    app.global_status = 'unarmed'
                                app._userbeveiliginscode = ''
                            else:
                                print('De code is onjuist ingevoerd, de status wordt ingesteld naar idle')
                                app.global_status = 'idle'
                                app._userbeveiliginscode = ''
