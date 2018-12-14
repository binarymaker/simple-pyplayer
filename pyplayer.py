import sys
import time
from PyQt5 import QtGui, QtWidgets, QtCore, uic
import pygame
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

app = QtWidgets.QApplication([])
window = uic.loadUi("pyplayer.ui")

#Music player 
pygame.mixer.init()
musicPlayer = pygame.mixer.music

# Song informations
def musicChange(songPath):
  musicProperty = MP3(songPath)
  musicTag = EasyID3(songPath)
  global musicPlayer
  try:
    window.label_title.setText(musicTag["title"][0])
  except:
    window.label_title.setText('Unknown')
  try:
    window.label_album.setText(musicTag["album"][0])
  except:
    window.label_album.setText('Unknown')
  try:
    window.label_artist.setText(musicTag["artist"][0])
  except:
    window.label_artist.setText('Unknown')

  songLength = musicProperty.info.length
  # div - total_length/60, mod - total_length % 60
  mins, secs = divmod(songLength, 60)
  mins = round(mins)
  secs = round(secs)
  window.label_songtime.setText('{:02d}:{:02d}'.format(mins, secs))
  #Song seek slider
  window.Slider_songtime.setRange(0,songLength)
  #window.Slider_songtime.sliderReleased.connect(seek)
  musicPlayer.load(songPath)

isPause   = 0
playTime  = 0
pauseTime = 0
seekTime  = 0
playVolume = 1.0

def currentPlayTime():
  global isPause
  global seekTime
  if musicPlayer.get_busy() and not isPause:
    playTime =  seekTime + (musicPlayer.get_pos()/1000)
    mins, secs = divmod(playTime, 60)
    mins = round(mins)
    secs = round(secs)
    window.label_playtime.setText('{:02d}:{:02d}'.format(mins, secs))
    window.Slider_songtime.setValue(playTime)

def play():
  global isPause
  if isPause:
    musicPlayer.unpause()
    isPause = 0
  else:
    if(not musicPlayer.get_busy()):
      musicPlayer.play()
  time.sleep(0.5)

def pause():
  global isPause
  musicPlayer.pause()
  isPause = 1

def stop():
  global isPause 
  isPause = 0
  musicPlayer.stop()
  window.label_playtime.setText('00:00')
  window.Slider_songtime.setValue(0)

def seek():
  global seekTime
  seekTime = window.Slider_songtime.value()
  musicPlayer.play(0,seekTime)
  time.sleep(0.5)
  print(seekTime)

def volumeUp():
  global playVolume
  playVolume = min(1.0, playVolume + 0.1) # limit max value to 1.0
  musicPlayer.set_volume(playVolume)
  window.Slider_volume.setValue(round(playVolume*10))

def volumeDown():
  global playVolume
  playVolume = max(0.0, playVolume - 0.1) # limit min value to 0.0
  musicPlayer.set_volume(playVolume)
  window.Slider_volume.setValue(round(playVolume*10))

def volumeChange():
  global playVolume
  playVolume = window.Slider_volume.value()/10
  musicPlayer.set_volume(playVolume)

def manuSelect(selection):
  if(selection.text() == 'Open Folder'):
    songPath = QtWidgets.QFileDialog.getOpenFileName(window, 'Open file', 'c:\\',"Music files (*.mp3)")
    songPath = songPath[0]
    print(songPath)
    musicChange(songPath)
    musicPlayer.load(songPath)
    stop()
  if(selection.text() == 'About'):
    QtWidgets.QMessageBox.about(window, "About", " simple pyplayer V1.0 \nAuthor : importfunfromcode@gmail.com ")

window.menubar.triggered[QtWidgets.QAction].connect(manuSelect)
window.pushButton_play.clicked.connect(play)
window.pushButton_pause.clicked.connect(pause)
window.pushButton_stop.clicked.connect(stop)
window.pushButton_volUp.clicked.connect(volumeUp)
window.pushButton_volDown.clicked.connect(volumeDown)



#Volume slider
window.Slider_volume.setRange(0,10)
window.Slider_volume.setValue(10) # Volume default is maximun
window.Slider_volume.valueChanged.connect(volumeChange)

timer = QtCore.QTimer()
timer.timeout.connect(currentPlayTime)
timer.start(10)


window.show()
app.exec()
