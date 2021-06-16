#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from TouchStyle import *
import sys
from os import system

DIRS=["/media/sdcard"]

class SongListWidget(QListWidget):
    play = pyqtSignal(bool)
 
    def __init__(self, parent=None):
        super(SongListWidget, self).__init__(parent)
        self.songs = self.scan()
        self.proc_mpg123 = None
        self.proc_txt_snd_cat = None

       
        for i in self.songs:
            item = QListWidgetItem(i)
            item.setData(Qt.UserRole, i)
            self.addItem(item)
            
        self.itemClicked.connect(self.onItemClicked)
        
    def __del__(self):
        self.stop_player()
        
    def stop_player(self):
        pass
        
    def stop(self):
        self.stop_player()
        self.clearSelection()
        self.play.emit(False)
        
    def onItemClicked(self, item):
        # stop whatever is currently playing
        cmd = "mpg123 -q --stdout --encoding u8 --rate 22050 --mono ",item.text()," | /opt/ftc/apps/user/44bd8baa-2de3-4ba5-b26e-2db41994a212/txt_snd_cat &"
        ccmd = str(cmd).replace(",", "")
        cccmd = str(ccmd).replace("'", "")
        ccccmd = str(cccmd).replace("(", "")
        cccccmd = str(ccccmd).replace(")", "")
        system(str(cccccmd))
        #print(cccccmd)

       
    def get_id3(self, file):
        tags = { }
        
        return file
        
    def scan(self):
        songs = []
        mp3_files = []
        for i in DIRS:
            mp3_files += self.scan_dir(i)
            
        # try to fetch id3 tags for all files
        for i in mp3_files:
            tags = self.get_id3(i)
            songs.append(tags)
            
        # sort by title
        return songs
        
    def scan_dir(self, dir):
        mp3_files = []
        dir = os.path.expanduser(dir)  # path may start with ~
        
        try:
            files = os.listdir(dir)
            for i in files:
                fullpath = os.path.join(dir, i)
                if os.path.isfile(fullpath):
                    if fullpath.lower().endswith(('.mp3','.mpeg3')):
                        mp3_files.append(fullpath)
                elif os.path.isdir(fullpath):
                    mp3_files += self.scan_dir(fullpath)
        except:
            pass
        #print(mp3_files)
        return mp3_files

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)
        
        # create the empty main window
        self.w = TouchWindow("MP3 Player")
        
        self.vbox = QVBoxLayout()
        
        self.songlist = SongListWidget(self.w)
        self.vbox.addWidget(self.songlist)

       
        self.stop_but = QPushButton("Stop")
        self.stop_but.clicked.connect(self.stop)
        self.vbox.addWidget(self.stop_but)
        self.w.centralWidget.setLayout(self.vbox)
        self.w.show()
        
        self.exec_()

    def stop(self):
        system("pidof txt_snd_cat | xargs kill -9")
        
if __name__ == "__main__":
    FtcGuiApplication(sys.argv)