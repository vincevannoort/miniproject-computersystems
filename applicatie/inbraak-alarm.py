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
        self._status = 'unarmed'
        self._previousstatus = 'unarmed'
        self._beveiligingscode = '1111'
        self._userbeveiliginscode = ''
        self._deurdicht = True

    # Haal de status op
    def get_status(self):
        return self._status

    # Wijzig de status
    def set_status(self, status):
        self._previousstatus = self._status
        self._status = status
        print('STATUS: {}'.format(self._status))
        db.child('logs').push({'status': self.get_status(), 'timestamp': str(datetime.datetime.now())})

    global_status = property(get_status, set_status)

    # Haal de status op
    def get_deurstatus(self):
        return self._deurdicht

    # Haal de status op
    def set_deurstatus(self, deurstatus):
        self._deurdicht = deurstatus
        print('Deur dicht is: {}'.format(app._deurdicht))
        if self._status == 'armed' and self._deurdicht == False:
            print('AHHHHH ER WORDT INGEBROKEN :OOOOOO')
            app.global_status = 'burglary'

    global_deurstatus = property(get_deurstatus, set_deurstatus)

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
                if app.global_status == 'unarmed':
                    # Indien de key 0 wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_KP0:
                        app.global_status = 'inputcode'
                        print('Voer beveiliginscode in: ')

                # Werkt alleen als status armed is
                if app.global_status == 'armed':
                    # Indien de key 0 wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_KP0:
                        app.global_status = 'inputcode'
                        print('Voer beveiliginscode in: ')
                
                # Verander de status van de deur door D in te drukken
                if event.key == pygame.K_KP_PERIOD:
                    app.global_deurstatus = (not app.global_deurstatus)

                # Huidige status van het inbraaksysteem
                if event.key == pygame.K_KP_PLUS:
                    print(app._status)

                # Werkt alleen als er een code ingevoerd moet worden
                if app.global_status == 'inputcode':
                    if event.key and event.key != pygame.K_KP0:

                        # Alleen nieuwe code cijfers toevoegen indien de vorige code kleiner is dan 4
                        if len(app._userbeveiliginscode) < 4:
                            app._userbeveiliginscode += pygame.key.name(event.key)[1:-1]
                            print('Nog {} in te voeren.'.format(4 - len(app._userbeveiliginscode)), end='\r')

                        # Als de code gelijk is aan 4 cijfers, dan check je of de code juist is ingevoerd
                        if len(app._userbeveiliginscode) == 4:
                            if app._beveiligingscode == app._userbeveiliginscode:
                                print('De code is juist ingevoerd, de status wordt ingesteld naar armed')
                                if app._previousstatus == 'unarmed':
                                    if app._deurdicht == True:
                                        app.global_status = 'armed'
                                    else:
                                        app.global_status = app._previousstatus
                                        print('De deur is nog open, deze dient eerst dichtgedaan te worden voordat het alarm kan worden ingesteld.')
                                elif app._previousstatus == 'armed' or app._previousstatus == 'burglary':
                                    app.global_status = 'unarmed'
                                app._userbeveiliginscode = ''
                            else:
                                print('De code is onjuist ingevoerd, de status wordt ingesteld naar {}'.format(app._previousstatus))
                                app.global_status = app._previousstatus
                                app._userbeveiliginscode = ''

                # Als het alarm is geactiveerd voor inbraak
                if app.global_status == 'burglary':
                    # Indien de key 0 wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_KP0:
                        app.global_status = 'inputcode'
                        print('Voer beveiliginscode in: ')
