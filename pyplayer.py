import sys
import time
from PyQt5 import QtGui, QtWidgets, QtCore, uic
import pygame
from mutagen.mp3 import MP3

app = QtWidgets.QApplication([])
window = uic.loadUi("pyplayer.ui")

#Music player 
pygame.mixer.init()
musicPlayer = pygame.mixer.music

#Play music from local directory
songPath = '../music.mp3'
musicPlayer.load(songPath)
musicTag = MP3(songPath)

isPause   = 0
playTime  = 0
pauseTime = 0
seekTime  = 0

def currentPlayTime():
  global isPause
  global seekTime
  if musicPlayer.get_busy() and not isPause:
    playTime =  seekTime + (musicPlayer.get_pos()/1000)
    mins, secs = divmod(playTime, 60)
    mins = round(mins)
    secs = round(secs)
    window.label_playtime.setText('{:02d}:{:02d}'.format(mins, secs))
#   window.Slider_songtime.setValue(playTime)

def play():
  global isPause
  if isPause:
    musicPlayer.unpause()
    isPause = 0
  else:
    musicPlayer.play()
  time.sleep(0.5)

def pause():
  global isPause
  musicPlayer.pause()
  isPause = 1

def seek():
  global seekTime
  seekTime = window.Slider_songtime.value()
  musicPlayer.pause()
  musicPlayer.play(0,seekTime)
  print(seekTime)

window.pushButton_play.clicked.connect(play)
window.pushButton_pause.clicked.connect(pause)

songLength = musicTag.info.length
# div - total_length/60, mod - total_length % 60
mins, secs = divmod(songLength, 60)
mins = round(mins)
secs = round(secs)
window.label_songtime.setText('{:02d}:{:02d}'.format(mins, secs))

#Slider
window.Slider_songtime.setRange(0,songLength)
#window.Slider_songtime.setTickInterval(20)
#window.Slider_songtime.setSingleStep(2)
window.Slider_songtime.sliderMoved.connect(seek)

timer = QtCore.QTimer()
timer.timeout.connect(currentPlayTime)
timer.start(10)

window.show()
app.exec()
