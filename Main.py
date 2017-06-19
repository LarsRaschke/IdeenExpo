#imports
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

#Globale Variablen
mode = 0 #savemode

#GPIO set und reset
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.IN)
GPIO.setup(7,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(11,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

def setInterrupt(channel):
    GPIO.add_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)

def resetInterrupt(channel):
    GPIO.remove_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)

def removeInterrupt(channel):
    GPIO.remove_event_detect(channel, GPIO.RISING, callback=call, bouncetime=500)

#View Class
class View(QtGui.QMainWindow, gui.Ui_Form):

    # Signals
    game = pyqtSignal()#notwendig?

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1) # Bei Autostart wirklich 1 ms da kein System im hintergrund ist

    #Slot
    @pyqtSlot()
    def run(self):
        global mode
        if mode is 0:   #Savemode
            """
            Hier werden alle Werte zurück gesetzt
            """
            setInterrupt(13)
            mode = 1
        elif mode is 1: #Startbildschirm
            pass
        elif mode is 2: #Übergang Erklärphase
            removeInterrupt(13)
            setInterrupt(11)
            mode = 3
        elif mode is 3: #Erklärphase
            pass

        elif mode is 4: #Übergang Spielphase
            removeInterrupt(11)
            mode = 5
        elif mode is 5: #Spielphase
            if gameTime is 0:
                # Spielende
            else:
                pass

#Interrupt
def call(channel):
    global mode
    if channel is 7:    #Startengine
        pass
    elif channel is 11: #Weiter
        pass
    elif channel is 13: #Start
        if mode is 1:
            mode = 2
    else:
        print "Error"

#Programmstart
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    v = View()
    v.show()
    app.exec_()
