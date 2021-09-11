
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QListWidgetItem
from clipboardWatcher import ClipboardWatcher
from mainWindowUI import Ui_MainWindow
from pytube import YouTube, Channel
import urllib.request
import threading
class Download_Manger():
    def __init__(self,ui:Ui_MainWindow) -> None:
        self.ui = ui
        self.ui.linkAddButton.clicked.connect(self.get_link_info)
        self.ui.downloadSettingsAudioCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed())
        self.ui.downloadSettingsVideoCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed())
        self.watcher = ClipboardWatcher(self.ui.clipBoardTimer,self.is_youtube_link, 
                               self.update_link_text,
                               500)
        self.watcher.start()
    
    def download_settings_checkBox_state_changed(self):
        self.ui.downloadSettingsVideoComboBox.setEnabled(self.ui.downloadSettingsVideoCheckBox.isChecked())
        self.ui.downloadSettingsAudioComboBox.setEnabled(self.ui.downloadSettingsAudioCheckBox.isChecked())
        

    def is_youtube_link(self,url):
        if url.startswith("https://www.youtube.com/") or url.startswith("https://youtu.be"):
            return True
        return False

    def update_link_text(self,clipboard_content):
        self.ui.linkTextBox.setText(clipboard_content)

    def get_link_info(self):
        if self.is_youtube_link(self.ui.linkTextBox.text()):
            threading.Thread(target=self.get_info, args=[self.ui.linkTextBox.text()],
                     daemon=True).start()

        
    def get_info(self,link):
        self.enable_panel(False)
        yt = YouTube(link, on_progress_callback=self.update_progress)
        streams = yt.streams
        self.ui.mediaInfoTitleLabel.setText(f"Title: {yt.title}")
        self.ui.mediaInfoAuthorLabel.setText(f"Author: {yt.author}")
        self.ui.mediaInfoViewLabel.setText(f"View: {yt.views:,}")
        self.ui.mediaInfoOtherLabel.setText(f"Length: {self.time_format(yt.length)}")
        data = urllib.request.urlopen(yt.thumbnail_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.ui.mediaInfoGraphicsView.setPixmap(QtGui.QPixmap(image))
        videoStreams = streams.filter(type='video')
        audioSteams = streams.filter(type='audio')
        for v in videoStreams:
            self.ui.downloadSettingsVideoComboBox.addItem(f"{v.resolution}-{v.subtype}" ,v)
        for v in audioSteams:
            self.ui.downloadSettingsAudioComboBox.addItem(f"{v.abr}-{v.subtype}",v)
        self.ui.downloadSettingsVideoComboBox.setCurrentIndex(0)
        self.ui.downloadSettingsAudioComboBox.setCurrentIndex(0)
        self.enable_panel(True)
    
    def enable_panel(self, isEnable):
        self.ui.horizontalLayoutWidget.setEnabled(isEnable)
        self.ui.downloadControlLayout.setEnabled(isEnable)
        self.ui.downloadSettingsVideoCheckBox.setEnabled(isEnable)
        self.ui.downloadSettingsAudioCheckBox.setEnabled(isEnable)

        self.ui.downloadSettingsVideoComboBox.setEnabled(self.ui.downloadSettingsVideoCheckBox.isChecked())
        self.ui.downloadSettingsAudioComboBox.setEnabled(self.ui.downloadSettingsAudioCheckBox.isChecked())
    
    def enable_donwload_button(self, isDownloadEnable,isCancelEnable):
        self.ui.downloadSettingsDownloadButton.setEnabled(isDownloadEnable)


    def time_format(self,seconds: int):
        if seconds is not None:
            seconds = int(seconds)
            d = seconds // (3600 * 24)
            h = seconds // 3600 % 24
            m = seconds % 3600 // 60
            s = seconds % 3600 % 60
            if d > 0:
                return '{:02d}D {:02d}H {:02d}m {:02d}s'.format(d, h, m, s)
            elif h > 0:
                return '{:02d}H {:02d}m {:02d}s'.format(h, m, s)
            elif m > 0:
                return '{:02d}m {:02d}s'.format(m, s)
            elif s > 0:
                return '{:02d}s'.format(s)
        return '-'

    def update_progress(self):
        
        pass





