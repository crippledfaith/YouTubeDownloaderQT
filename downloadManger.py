
from logging import fatal
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from clipboardWatcher import ClipboardWatcher
from mainWindowUI import Ui_MainWindow
from pytube import YouTube,Stream,request
import traceback, sys, uuid, helper, string, unicodedata, os, threading,urllib.request,time
import subprocess
from shutil import copyfile
import psutil


class Download_Manger():


    def __init__(self,ui:Ui_MainWindow) -> None:
        self.ui = ui
        self.isVideoAudio = True
        self.ui.linkAddButton.clicked.connect(self.get_link_info)
        self.ui.downloadSettingsShowMoreButton.clicked.connect(self.show_more_controls)
        self.ui.downloadSettingsAudioCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed(self.ui.downloadSettingsAudioCheckBox))
        self.ui.downloadSettingsVideoCheckBox.stateChanged.connect(lambda x: self.download_settings_checkBox_state_changed(self.ui.downloadSettingsVideoCheckBox))
        self.ui.downloadSettingsDownloadButton.clicked.connect(lambda x: self.start_download())
        self.ui.downloadSettingsCancelButton.clicked.connect(lambda x: self.stop_download())
        self.ui.downloadSettingsVideoComboBox.currentTextChanged.connect(self.video_on_combobox_changed)
        self.ui.downloadSettingsAudioComboBox.currentTextChanged.connect(self.audio_on_combobox_changed)
        self.ui.downloadSettingsVideoAudioComboBox.currentTextChanged.connect(self.video_on_combobox_changed)
        self.watcher = ClipboardWatcher(self.ui.clipBoardTimer,self.is_youtube_link, 
                               self.update_link_text,
                               500)
        self.watcher.start()
        home = os.path.expanduser('~')
        self.videoFolderPath = os.path.join(home, 'Videos')
        self.enable_donwload_button(False,False)
        self.applicationDataPath = helper.get_user_data_dir("YoutubeDownloaderQT")
        self.threadpool = QtCore.QThreadPool()
        self.inProgress = False
        self.process = None
    
    def show_more_controls(self):
        if self.isVideoAudio :
            self.ui.downloadSettingsVideoComboBox.setVisible(True)
            self.ui.downloadSettingsAudioComboBox.setVisible(True)
            self.ui.downloadSettingsVideoCheckBox.setVisible(True)
            self.ui.downloadSettingsAudioCheckBox.setVisible(True)

            self.ui.downloadSettingsVideoAudioComboBox.setVisible(False)
            self.ui.downloadSettingsVideoAudioLabel.setVisible(False)

            self.isVideoAudio = False
        else:
            self.ui.downloadSettingsVideoAudioComboBox.setVisible(True)
            self.ui.downloadSettingsVideoAudioLabel.setVisible(True)

            self.ui.downloadSettingsVideoComboBox.setVisible(False)
            self.ui.downloadSettingsAudioComboBox.setVisible(False)
            self.ui.downloadSettingsVideoCheckBox.setVisible(False)
            self.ui.downloadSettingsAudioCheckBox.setVisible(False)

            self.isVideoAudio = True
        self.update_download_size()


    def start_download(self):
        audio = self.ui.downloadSettingsAudioComboBox.currentData()
        video = self.ui.downloadSettingsVideoComboBox.currentData()
        mediaType=""
        media = []
        if self.isVideoAudio:
            video = self.ui.downloadSettingsVideoAudioComboBox.currentData()
            media.append(video)
        else:
            if self.ui.downloadSettingsVideoCheckBox.isChecked():
                media.append(video)
                if self.ui.downloadSettingsAudioCheckBox.isChecked() == False:
                    mediaType="-(video only)"
            
            if self.ui.downloadSettingsAudioCheckBox.isChecked():
                media.append(audio)
                if self.ui.downloadSettingsVideoCheckBox.isChecked() == False:
                    mediaType="-(audio only)"
        filenameWithoutExtension =os.path.splitext(media[0].default_filename)[0]
        filenameExtension =os.path.splitext(media[0].default_filename)[1]
        fullFileName = f"{filenameWithoutExtension}{mediaType}{filenameExtension}"
        fileName = f"{self.clean_filename(fullFileName)}"
        filePath = os.path.join(self.videoFolderPath,fileName)
        self.filePath = QFileDialog.getSaveFileName(self.ui.MainWindow,"Save File", filePath,f"Video File (*{filenameExtension})")[0]
        if self.filePath=='':
            return

        # if os.path.isfile(self.filePath):
        #     result = self.show_message(f'You have downloaded this media and the file already exist.\n{self.filePath}?\n Are you sure you want to download this file?',QMessageBox.Yes|QMessageBox.No)
        #     if result==QMessageBox.No:
        #         return
        #     else:
        #         os.remove(self.filePath)
        self.enable_panel(False)
        self.enable_donwload_button(False,True)
        
        worker = Worker(self.download,self.filePath,media)

        worker.signals.finished.connect(self.donwload_completed)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.error.connect(self.error)
        self.threadpool.start(worker)

    def error(self,error):
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        self.enable_panel(True)
        self.enable_donwload_button(True,False)
        self.is_cancelled= False
        _,err,_ =error
        if type(err).__name__ == "TypeError":
            err:TypeError
            self.show_message(str(err))
        elif type(err).__name__ == "OSError":
            err:OSError
            type(err).__name__
            type(str(err)).__name__
            self.show_message(str(err))

        
    def show_message(self,messgae,buttons= QMessageBox.Ok):
        msgBox = QMessageBox()
        msgBox.setText(messgae)
        msgBox.setWindowTitle("Youtube Downloader QT")
        #msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(buttons)
        msgBox.setDefaultButton(QMessageBox.Ok)
        return msgBox.exec()
        
    def donwload_completed(self):
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        self.enable_panel(True)
        self.enable_donwload_button(True,False)
        if self.is_cancelled == False:
            result =self.show_message(f"Download Completed.\nFile:{self.filePath}\n\nWould like to open the containing folder?",QMessageBox.Yes|QMessageBox.No)
            if result==QMessageBox.Yes:
                path = self.filePath.replace("/","\\")
                arg = f'explorer /select, "{path}"'
                subprocess.Popen(arg)
        self.is_cancelled= False

    def download(self,path,medias,progress_callback):
        self.inProgress = True
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
                        progress_callback.emit(1,1)
                        time.sleep(.2)
                        break
            progress_callback.emit(0,1)
        
        if self.is_cancelled == False and len(file) == 2:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            elif __file__:
                application_path = os.path.dirname(__file__)
            ffmpegName = 'ffmpeg.exe'
            ffmpegPath = os.path.join(application_path, ffmpegName)
            print(ffmpegPath)
            self.ui.progressBar.setMaximum(0)
            # video_stream = ffmpeg.input(file[0])
            # audio_stream = ffmpeg.input(file[1])
            # ffmpeg.output(audio_stream, video_stream, path).run(overwrite_output=True, cmd=ffmpegPath, quiet=False)

            self.process  = subprocess.Popen(f'{ffmpegPath} -i "{ file[0] }" -i "{ file[1] }" -c copy -c:a aac -b:a 192k "{path}" -y',creationflags = subprocess.CREATE_NO_WINDOW)
            self.process.wait()

        if self.is_cancelled == False and len(file) == 1:
            copyfile(file[0], path)

        if os.path.isfile(file[0]):
            os.remove(file[0])
        if len(file) == 2:
            if os.path.isfile(file[1]):
                os.remove(file[1])
        self.ui.progressBar.setMaximum(100)
        self.inProgress = False

    
    def stop_download(self):
        self.ui.downloadSettingsCancelButton.setEnabled(False)
        self.is_cancelled = True
        if(self.process !=  None):
            subprocess.Popen.terminate(self.process)
        self.process = None
    
    

    # def kill(self, process_name):
    #     try:
    #         print(f'Killing processes {process_name}')
    #         processes = psutil.process_iter()
    #         for process in processes:
    #             try:
    #                 if process_name == process.name() or process_name in process.cmdline():
    #                     print(f'found {process.name()} | {process.cmdline()}')
    #                     process.terminate()
    #             except Exception:
    #                 pass
    #     except Exception:
    #         pass

    def download_settings_checkBox_state_changed(self,checkbox):
        if self.ui.downloadSettingsVideoCheckBox.isChecked() == False and self.ui.downloadSettingsAudioCheckBox.isChecked()== False:
            if checkbox == self.ui.downloadSettingsVideoCheckBox:
                self.ui.downloadSettingsAudioCheckBox.setChecked(True)
            else:
                self.ui.downloadSettingsVideoCheckBox.setChecked(True)
        self.ui.downloadSettingsVideoComboBox.setEnabled(self.ui.downloadSettingsVideoCheckBox.isChecked())
        self.ui.downloadSettingsAudioComboBox.setEnabled(self.ui.downloadSettingsAudioCheckBox.isChecked())
        self.update_download_size() 

    def video_on_combobox_changed(self):
        self.update_download_size() 

    def audio_on_combobox_changed(self):
        self.update_download_size()

    def update_download_size(self):
        audio = self.ui.downloadSettingsAudioComboBox.currentData()
        video = self.ui.downloadSettingsVideoComboBox.currentData()
        vidioAudio = self.ui.downloadSettingsVideoAudioComboBox.currentData()
        size=0
        if self.isVideoAudio:
            size = vidioAudio.filesize
        else:
            if self.ui.downloadSettingsAudioCheckBox.isChecked():
                size = audio.filesize
            if self.ui.downloadSettingsVideoCheckBox.isChecked():
                size = size + video.filesize
        strSize = self.convert_bytes(size)
        self.ui.downloadSettingsDownloadButton.setText(strSize)

    def convert_bytes(self,size):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

        return size

    def is_youtube_link(self,url):
        if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/"):
            return True
        return False

    def update_link_text(self,clipboard_content):
        if(self.inProgress == False):
            self.ui.linkTextBox.setText(clipboard_content)
            self.get_link_info()


    def get_link_info(self):
        if self.is_youtube_link(self.ui.linkTextBox.text()):
            threading.Thread(target=self.get_info, args=[self.ui.linkTextBox.text()],
                     daemon=True).start()

    def clean_filename(self,filename,replace=' '):
        valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        char_limit = 255
        for r in replace:
            filename = filename.replace(r,'_')

        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        cleaned_filename = ''.join(c for c in cleaned_filename if c in valid_filename_chars)
        if len(cleaned_filename)>char_limit:
            print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
        return cleaned_filename[:char_limit]  


    def get_info(self,link):
        self.enable_panel(False)
        self.enable_donwload_button(False,False)
        self.inProgress = True
        try:
            self.ui.progressBar.setMaximum(0)
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

            videoStreams = streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc()
            audioSteams = streams.filter(only_audio=True).order_by('abr').desc()
            videoAudioSteams = streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

            self.ui.downloadSettingsVideoComboBox.clear()
            self.ui.downloadSettingsAudioComboBox.clear()
            for v in videoStreams:
                self.ui.downloadSettingsVideoComboBox.addItem(f"{v.resolution}-{v.subtype}" ,v)
            for v in audioSteams:
                self.ui.downloadSettingsAudioComboBox.addItem(f"{v.abr}-{v.subtype}",v)
            for v in videoAudioSteams:
                self.ui.downloadSettingsVideoAudioComboBox.addItem(f"{v.resolution} {v.abr}-{v.subtype}",v)
            self.ui.downloadSettingsVideoComboBox.setCurrentIndex(0)
            self.ui.downloadSettingsAudioComboBox.setCurrentIndex(0)
            self.ui.downloadSettingsVideoAudioComboBox.setCurrentIndex(0)
        except:
            pass
        self.enable_panel(True)
        self.enable_donwload_button(True,False)
        self.ui.progressBar.setMaximum(100)
        self.inProgress = False

    

    def enable_panel(self, isEnable):
        self.ui.downloadSettingsShowMoreButton.setEnabled(isEnable)
        self.ui.horizontalLayoutWidget.setEnabled(isEnable)
        self.ui.downloadSettingsVideoCheckBox.setEnabled(isEnable)
        self.ui.downloadSettingsAudioCheckBox.setEnabled(isEnable)
        self.ui.downloadSettingsVideoAudioComboBox.setEnabled(isEnable)
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
            self.signals.finished.emit()
              