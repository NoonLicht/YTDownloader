import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from pytube import YouTube

class DownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(600, 300, 500, 525)
        self.setStyleSheet('''
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop: 0 #2C3E50,
                                            stop: 0.3 #2C3E50,
                                            stop: 0.7 #22313F,
                                            stop: 1 #22313F);
            }
        ''')

        self.url_label = QLabel('', self)
        self.url_label.move(20, 20)

        self.url_box = QLineEdit(self)
        self.url_box.setGeometry(25, 375, 400, 30)
        self.url_box.setStyleSheet('''
          border-top-left-radius: 15px;
          border-bottom-left-radius: 15px;
          font-size: 14px;
          padding-left: 5px;
          padding-right: 5px;
          background-color: #F2F1EF;
        ''')

        self.get_url_button = QPushButton('→', self)
        self.get_url_button.setGeometry(425, 375, 50, 30)
        self.get_url_button.clicked.connect(self.get_url)
        self.get_url_button.setStyleSheet('''
            QPushButton {
                background-color: #2574A9;
                border-bottom-right-radius: 15px;
                border-top-right-radius: 15px;
                font: normal bold 20px "Microsoft Yahei";
            }
            QPushButton:pressed {
                background-color: #3A539B;
            }
        ''')

        self.preview_image_label = QLabel(self)
        self.preview_image_label.setGeometry(25, 25, 450, 250)
        self.preview_image_label.setStyleSheet('''
            background-color: #34495F;
            border-radius: 10px;  
        ''')
        self.preview_image_label.setScaledContents(True)

        self.preview_text_label = QLabel('', self)
        self.preview_text_label.setGeometry(25, 300, 450, 50)
        self.preview_text_label.setStyleSheet('''
            background-color: #F2F1EF;
            border-radius: 10px;  
            font: normal normal 14px "Microsoft Yahei";
            padding-left: 5px;
            padding-right: 5px;
            
        ''')
        self.preview_text_label.setWordWrap(True)

        self.choose_folder_button = QPushButton('🖿', self)
        self.choose_folder_button.setGeometry(375, 455, 30, 40)
        self.choose_folder_button.clicked.connect(self.choose_folder)
        self.choose_folder_button.setStyleSheet('''
            QPushButton {
            background-color: #2574A9;
            border-radius: 7px;
            font: normal normal 20px "Microsoft Yahei";
            }
            QPushButton:pressed {
                background-color: #3A539B;
            }
        ''')

        self.download_button = QPushButton('Download', self)
        self.download_button.setGeometry(150, 450, 200, 50)
        self.download_button.clicked.connect(self.download_video)
        self.download_button.setStyleSheet('''
            QPushButton {
            background-color: #2574A9;
            border-radius: 15px;
            font: normal bold 20px "Microsoft Yahei";
            }
            QPushButton:pressed {
                background-color: #3A539B;
            }
        ''')

    def get_url(self):
        url = self.url_box.text()
        try:
            yt = YouTube(url)
            self.preview_text_label.setText(yt.title)
            thumbnail_url = yt.thumbnail_url
            thumbnail = QPixmap()
            thumbnail.loadFromData(requests.get(thumbnail_url).content)
            self.preview_image_label.setPixmap(thumbnail)
        except Exception as e:
            print(e)

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if folder_path:
            self.folder_path = folder_path
        else:
            self.folder_path = os.path.expanduser("~")

    def download_video(self):
        if not hasattr(self, 'folder_path'):
            self.folder_path = os.path.expanduser("~")

        url = self.url_box.text()
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
            if video:
                highest_resolution_video = video
                highest_resolution_bitrate = video.bitrate
                for stream in yt.streams.filter(file_extension='mp4', progressive=True):
                    if stream.resolution == highest_resolution_video.resolution and stream.bitrate > highest_resolution_bitrate:
                        highest_resolution_video = stream
                        highest_resolution_bitrate = stream.bitrate
                highest_resolution_video.download(output_path=self.folder_path)
                print("Video downloaded successfully!")
            else:
                print("No MP4 video found")
        except Exception as e:
            print(e)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = DownloaderApp()
    downloader.show()
    sys.exit(app.exec_())
