# imports
# -*- coding: utf-8 -*-
import sys

sys.path.append('/home/pi/Public/Gui/')
picPath = '/home/pi/Public/bilder/'

from score import Score
import RPi.GPIO as GPIO
import smbus
import random
import gui
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from omxplayer import OMXPlayer

# Globale Variablen
mode = 0
explainTextStep = 0
videoStart = True
startGame = False

# GPIO set und reset
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def setInterrupt(channel):
    GPIO.add_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)


def resetInterrupt(channel):
    GPIO.remove_event_detect(channel)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)


def removeInterrupt(channel):
    GPIO.remove_event_detect(channel)


# View Class
class View(QtGui.QMainWindow, gui.Ui_Form):
    
    # Signals
    game = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)

        self.time1.setValue(1)
        self.time2.setValue(1)
        self.time1.setMaximum(1)
        self.time2.setMaximum(1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1)  # Bei Autostart wirklich 1 ms da kein System im Hintergrund ist

        self.logo.setPixmap(QtGui.QPixmap("/home/pi/Public/bilder/logoS.png"))
        self.logoR.setPixmap(QtGui.QPixmap("/home/pi/Public/bilder/logo.png"))
        self.hintergrund.setPixmap(QtGui.QPixmap("/home/pi/Public/bilder/bg.png"))
        
        
    # Slot
    @pyqtSlot()
    def run(self):
        global mode
        global videoStart
        global explainTextStep
        global startGame
        if mode is 0:  # Savemode
            """
            Hier werden alle Werte zurück gesetzt
            """
            videoStart = True
            setInterrupt(13)
            explainTextStep = 0
            startGame = False
            self.startBildschirm.setVisible(True)
            mode = 1
        elif mode is 1:  # Startbildschirm
            pass
        elif mode is 2:  # Übergang Erklärphase
            removeInterrupt(13)
            setInterrupt(11)            
            self.startBildschirm.setVisible(False)
            self.sensorTexte.setVisible(True)
            mode = 3
        elif mode is 3:  # Erklärphase
            """
            Text anzeigen durch "explainTextStep"
            """
            if explainTextStep is 5:
                if not startGame:
                    startGame = True
                    setInterrupt(13)
                    removeInterrupt(11)
                    self.text.setText("Start Game")
            # Texte Anzeigen lassen
            else:
                self.text.setText(str(explainTextStep))
            pass
        elif mode is 4:  # Übergang Spielphase
            removeInterrupt(11)
            removeInterrupt(13)
            self.sensorTexte.setVisible(False)
            self.startBildschirm.setVisible(False)
            mode = 5
        elif mode is 5:  # Spielphase
            if videoStart:
                self.player = OMXPlayer('/home/pi/Public/Videos/teil1Neu.mp4')        
                self.time1.setMaximum(int(self.player.duration()))
                self.time2.setMaximum(int(self.player.duration()))
                self.player.set_video_pos(260, 300, 1690, 1080)
                videoStart = False
            if self.player.is_playing():                
                restTime = int(self.player.duration())-int(self.player.position())
                self.time1.setValue(restTime)
                self.time2.setValue(restTime)
                pass
                # Spielläuft
            else:
                # Spielfertig
                self.player.quit()
                mode = 0
        else:
            pass


# Interrupt
def call(channel):
    global mode
    global explainTextStep
    print channel
    if channel is 7:  # Startengine
        pass
    elif channel is 11:  # Weiter
        if mode is 3:
            if explainTextStep is 5:
                pass
            else:
                explainTextStep = explainTextStep + 1
        pass
    elif channel is 13:  # Start
        if mode is 1:
            mode = 2
        elif mode is 3:
            mode = 4
    else:
        print "Error"

# Programmstart
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    v = View()
    v.show()    
    try:
        app.exec_()
    except KeyboardInterrupt:
        v.player.quit()
