import sqlite3
import datetime
import pygame
# import RPi.GPIO as GPIO -> MOET AANWORDEN GEZET
from threading import Timer

# Setup twilio voor SMS service
from twilio.rest import TwilioRestClient
account_sid = 'AC71a18fed2f8b0a539569ea8e1f271359'
auth_token = '789143f9e3f7dd896db124a30ab0eeaa'
client = TwilioRestClient(account_sid, auth_token)

# Initaliseer applicatie via PyGame
pygame.init()
screen = pygame.display.set_mode((1,1))

# Firebase database connectie
conn = sqlite3.connect('logs.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

# Class inbraakalarm
class InbraakAlarm():

    # Initalisatie inbraakalarm
    # Statussen -> idle, armed, unarmed, settings
    def __init__(self):
        self._status = ''
        self._previousstatus = ''
        self._beveiligingscode = '1111'
        self._userbeveiligingscode = ''
        self._deurdicht = True
        self._timer = Timer(3.0, self.start_anti_inbraak)
        self._closesettings = 0

    # Haal de status op
    def get_status(self):
        return self._status

    # Wijzig de status
    def set_status(self, status):
        self._previousstatus = self._status
        self._status = status
        print('Status gewijzigd: {}'.format(self._status))
        c.execute("INSERT INTO logs (status) VALUES ('{}')".format(self.get_status()))

        # Wijzig led status wanneer status wordt veranderd
        if status == 'unarmed':
            print('-> WIJZIG LEDS HIER <-')
        elif status == 'armed':
            print('-> WIJZIG LEDS HIER <-')
        elif status == 'inputcode':
            print('-> WIJZIG LEDS HIER <-')
        elif status == 'lockdown':
            print('-> WIJZIG LEDS HIER <-')
        elif status == 'settings':
            print('-> WIJZIG LEDS HIER <-')

    global_status = property(get_status, set_status)

    # Haal de deurstatus op
    def get_deurstatus(self):
        return self._deurdicht

    # Wijzig de deurstatus
    def set_deurstatus(self, deurstatus):
        if deurstatus:
            print('De deur wordt \033[31mdichtgedaan\033[30m.')
        else:
            print('De deur wordt \033[32mopengedaan\033[30m.')
        self._deurdicht = deurstatus
        if self._status == 'armed' and self._deurdicht == False:
            app.global_status = 'lockdown'
            self._timer.start()

    # Check of de status is veranderd
    def start_anti_inbraak(self):
        print('GET OUT, INITIATE \033[91mLOCKDOWN!\033[30m CALL 911!')
        client.calls.create(to='+31652144206', from_='+1 415-742-2845', url='https://raw.githubusercontent.com/vincevannoort/miniproject-computersystems/master/applicatie/inbraak-alarm-response.xml')

    global_deurstatus = property(get_deurstatus, set_deurstatus)

# Begin de applicatie
if __name__ == '__main__':
    app = InbraakAlarm()
    app.global_status = 'unarmed'

    # Laat de applicatie runnen
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit();
                conn.commit()
                conn.close()

            if event.type == pygame.KEYDOWN:

                # Verander de status van de deur door D in te drukken
                if event.key == pygame.K_KP_PLUS:
                    app.global_deurstatus = (not app.global_deurstatus)

                # Werkt alleen wanneer je de settingsknop indrukt als de status unarmed is
                if event.key == pygame.K_KP_PERIOD and app.global_status == 'unarmed':
                    app.global_status = 'settings'

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

                # Als het alarm is geactiveerd voor inbraak
                if app.global_status == 'lockdown':
                    # Indien de key 0 wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_KP0:
                        app.global_status = 'inputcode'
                        print('Voer beveiliginscode in: ')

                # Werkt alleen als de settings worden veranderd
                if app.global_status == 'settings':
                    # Return als er weer op het puntje wordt gedrukt
                    if event.key == pygame.K_KP_PERIOD:
                        if app._closesettings == 0: 
                            app._closesettings+= 1
                        elif app._closesettings == 1: 
                            app.global_status = app._previousstatus
                            app._closesettings = 0

                    # Indien de key 0 wordt ingedrukt, kun je een 4 cijferige code invoeren
                    if event.key == pygame.K_KP0:
                        app.global_status = 'settings-check' # set previous state
                        app.global_status = 'inputcode'
                        print('Voer de oude beveiliginscode in om een nieuwe in te stellen: ')

                    # Indien de key 1 wordt ingedrukt, wordt er algemene info getoond
                    if event.key == pygame.K_KP1:
                        print('Verander code via sms indien nodig (als je het bent vergeten.')

                # Wordt voor meerdere doeleinden gebruikt qua codeinvoeren
                if app.global_status == 'inputcode':
                    if event.key and event.key != pygame.K_KP0:

                        # Alleen nieuwe code cijfers toevoegen indien de vorige code kleiner is dan 4
                        if len(app._userbeveiligingscode) < 4:
                            app._userbeveiligingscode += pygame.key.name(event.key)[1:-1]
                            print('Nog {} in te voeren.'.format(4 - len(app._userbeveiligingscode)))

                        # Als de code gelijk is aan 4 cijfers, dan check je of de code juist is ingevoerd
                        if len(app._userbeveiligingscode) == 4:
                            if app._beveiligingscode == app._userbeveiligingscode or app._previousstatus == 'settings-new':
                                print('Code is: \033[32mjuist\033[30m.')
                                print('-> WIJZIG LEDS HIER <-')
                                pygame.time.wait(1000) # wacht even, zodat de indicatie led kan worden getoond.
                                if app._previousstatus == 'unarmed':
                                    if app._deurdicht == True:
                                        app.global_status = 'armed'
                                    else:
                                        app.global_status = app._previousstatus
                                        print('De deur is nog open, deze dient eerst dichtgedaan te worden voordat het alarm kan worden ingesteld.')
                                elif app._previousstatus == 'armed' or app._previousstatus == 'lockdown':
                                    app.global_status = 'unarmed'
                                    app._timer.cancel()
                                    app._timer = Timer(3.0, app.start_anti_inbraak) # reset timer
                                elif app._previousstatus == 'settings-check':
                                    print('Voer een nieuwe beveiligingscode in:')
                                    app.global_status = 'settings-new' # set previous state
                                    app.global_status = 'inputcode'
                                elif app._previousstatus == 'settings-new':
                                    print('Gelukt, je oude code \033[32m{}\033[30m wordt veranderd in \033[32m{}\033[30m.'.format(app._beveiligingscode, app._userbeveiligingscode))
                                    app._beveiligingscode = app._userbeveiligingscode
                                    app.global_status = 'unarmed'
                                # reset altijd de userbeveiligingscode
                                app._userbeveiligingscode = ''
                            else:
                                print('Code is: \033[31monjuist\033[30m.')
                                print('-> WIJZIG LEDS HIER <-')
                                pygame.time.wait(1000) # wacht even, zodat de indicatie led kan worden getoond.
                                if app._previousstatus == 'settings-check':
                                    app.global_status = 'settings'
                                else:
                                    app.global_status = app._previousstatus
                                # reset altijd de userbeveiligingscode
                                app._userbeveiligingscode = ''