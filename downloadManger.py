
from logging import fatal
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QListWidgetItem
from clipboardWatcher import ClipboardWatcher
from mainWindowUI import Ui_MainWindow
from pytube import YouTube,Stream,request
import traceback, sys, uuid, helper, string, unicodedata, os, threading,pathlib,urllib.request
import moviepy.editor as mpe
class Download_Manger():


    def __init__(self,ui:Ui_MainWindow) -> None:
        self.ui = ui
        self.ui.linkAddButton.clicked.connect(self.get_link_info)
        self.ui.downloadSettingsAudioCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed())
        self.ui.downloadSettingsVideoCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed())
        self.ui.downloadSettingsDownloadButton.clicked.connect(lambda x: self.start_download())
        self.ui.downloadSettingsCancelButton.clicked.connect(lambda x: self.stop_download())
        self.watcher = ClipboardWatcher(self.ui.clipBoardTimer,self.is_youtube_link, 
                               self.update_link_text,
                               500)
        self.watcher.start()
        home = os.path.expanduser('~')
        self.videoFolderPath = os.path.join(home, 'Videos')
        self.enable_donwload_button(False,False)
        self.applicationDataPath = helper.get_user_data_dir("YoutubeDownloaderQT")
        self.threadpool = QtCore.QThreadPool()

    def start_download(self):
        audio = self.ui.downloadSettingsAudioComboBox.currentData()
        video = self.ui.downloadSettingsVideoComboBox.currentData()
        media = []
        if self.ui.downloadSettingsVideoCheckBox.isChecked():
            media.append(video)
            extension = video.subtype
        else:
             extension = audio.subtype
        if self.ui.downloadSettingsAudioCheckBox.isChecked():
            media.append(audio)

        fileName = f"{self.clean_filename(media[0].default_filename)}"
        filePath = os.path.join(self.videoFolderPath,fileName)

        self.enable_panel(False)
        self.enable_donwload_button(False,True)
        
        #self.currentThread = threading.Thread(target=self.download, args=[filePath,media],
        #             daemon=True)
        #self.currentThread.start()

        worker = Worker(self.download,filePath,media) # Any other args, kwargs are passed to the run function
        #worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.donwload_completed)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.error.connect(self.error)
        # Execute
        self.threadpool.start(worker)

    def error(self,error):
        pass

    def donwload_completed(self):
        self.ui.progressBar.setValue(0)
        self.enable_panel(True)
        self.enable_donwload_button(True,False)

    def download(self,path,medias,progress_callback):
        media_stream:Stream
        if os.path.isfile(path):
            os.remove(path)
        file =[]
        
        self.is_paused = self.is_cancelled = False
        for media_stream in medias:
            extenstion = media_stream.subtype
            filePathName = os.path.join(self.applicationDataPath,f"{str(uuid.uuid1())}.{extenstion}")
            file.append(filePathName)
            with open(filePathName, 'wb') as f:
                filesize = media_stream.filesize
                stream = request.stream(media_stream.url) # get an iterable stream
                downloaded = 0
                while True:
                    if self.is_cancelled:
                        break
                    chunk = next(stream, None) # get next chunk of video
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress_callback.emit(downloaded,filesize)
                    else:
                        break
            progress_callback.emit(0,1)
            
        if self.is_cancelled == False and len(file) == 2:
            self.ui.progressBar.setMaximum(0)
            my_clip = mpe.VideoFileClip(file[0])
            audio_background = mpe.AudioFileClip(file[1])
            final_clip = my_clip.set_audio(audio_background)
            final_clip.write_videofile(path)

        self.ui.progressBar.setMaximum(100)
        self.is_cancelled = False



    def stop_download(self):
        self.is_cancelled = True

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

    def clean_filename(self,filename,replace=' '):
        # replace spaces
        valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        char_limit = 255
        for r in replace:
            filename = filename.replace(r,'_')
        
        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        
        # keep only whitelisted chars
        cleaned_filename = ''.join(c for c in cleaned_filename if c in valid_filename_chars)
        if len(cleaned_filename)>char_limit:
            print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
        return cleaned_filename[:char_limit]  


    def get_info(self,link):
        self.enable_panel(False)
        self.enable_donwload_button(False,False)
        yt = YouTube(link)
        streams = yt.streams
        self.ui.mediaInfoTitleLabel.setText(f"Title: {yt.title}")
        self.ui.mediaInfoAuthorLabel.setText(f"Author: {yt.author}")
        self.ui.mediaInfoViewLabel.setText(f"View: {yt.views:,}")
        self.ui.mediaInfoOtherLabel.setText(f"Length: {self.time_format(yt.length)}")
        data = urllib.request.urlopen(yt.thumbnail_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.ui.mediaInfoGraphicsView.setPixmap(QtGui.QPixmap(image))
        for s in streams:
            print(s)
        print('-----------------')
        videoStreams = streams.filter(only_video=True)
        for s in videoStreams:
            print(s)
        audioSteams = streams.filter(only_audio=True)
        for v in videoStreams:
            self.ui.downloadSettingsVideoComboBox.addItem(f"{v.resolution}-{v.subtype}" ,v)
        for v in audioSteams:
            self.ui.downloadSettingsAudioComboBox.addItem(f"{v.abr}-{v.subtype}",v)
        self.ui.downloadSettingsVideoComboBox.setCurrentIndex(0)
        self.ui.downloadSettingsAudioComboBox.setCurrentIndex(0)
        self.enable_panel(True)
        self.enable_donwload_button(True,False)
    

    def enable_panel(self, isEnable):
        self.ui.horizontalLayoutWidget.setEnabled(isEnable)
        self.ui.downloadSettingsVideoCheckBox.setEnabled(isEnable)
        self.ui.downloadSettingsAudioCheckBox.setEnabled(isEnable)
        if isEnable:
            self.ui.downloadSettingsVideoComboBox.setEnabled(self.ui.downloadSettingsVideoCheckBox.isChecked())
            self.ui.downloadSettingsAudioComboBox.setEnabled(self.ui.downloadSettingsAudioCheckBox.isChecked())
        else:
            self.ui.downloadSettingsVideoComboBox.setEnabled(isEnable)
            self.ui.downloadSettingsAudioComboBox.setEnabled(isEnable)
    
    def enable_donwload_button(self, isDownloadEnable,isCancelEnable):
        self.ui.downloadSettingsDownloadButton.setEnabled(isDownloadEnable)
        self.ui.downloadSettingsCancelButton.setEnabled(isCancelEnable)


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

    def update_progress(self,downloaded,filesize):
        rem = downloaded
        percent = int((rem / filesize) * 100)
        self.ui.progressBar.setValue(percent)





class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int,int)

class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
    
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.Slot()
    def run(self):
        
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done