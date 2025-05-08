import os 
import yt_dlp
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QTextEdit, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("YouTube Download")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("https://www.youtube.com/watch?v=BZ5jt517ppU&ab_channel=SoftRock")
        layout.addWidget(self.label)
        
        self.link_input = QLineEdit()
        layout.addWidget(self.link_input)
        
        self.add_button = QPushButton("Adicionar Link")
        self.add_button.clicked.connect(self.add_link)
        layout.addWidget(self.add_button)
        
        self.links_display = QTextEdit()
        self.links_display.setReadOnly(True)
        layout.addWidget(self.links_display)
        
        self.download_mp3_button = QPushButton("Baixar MP3")
        self.download_mp3_button.clicked.connect(self.download_mp3)
        layout.addWidget(self.download_mp3_button)

        self.download_video_button = QPushButton("Baixar Vídeo")
        self.download_video_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_video_button)
        
        self.setLayout(layout)
        
        self.urls = []
        
    def add_link(self):
        url = self.link_input.text().strip()
        if url:
            self.urls.append(url)
            self.links_display.append(url)
            self.link_input.clear()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um link válido!")

    def download_mp3(self):
        if not self.urls:
            QMessageBox.warning(self, "Aviso", "Nenhum link adicionado!")
            return

        destino = QFileDialog.getExistingDirectory(self, "Escolha o diretório de destinos")
        if not destino:
            return

        os.makedirs(destino, exist_ok=True)
        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": os.path.join(destino, "%(title)s.%(ext)s")
        }

        erros = []

        for url in self.urls:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_path = ydl.prepare_filename(info)

                audio_path = os.path.splitext(video_path)[0] + ".mp3"
                comando = [
                    "ffmpeg", "-i", video_path,
                    "-vn", "-ar", "44100", "-ac", "2", "-b:a", "320k",
                    audio_path
                ]
                subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                os.remove(video_path)

            except Exception as e:
                erros.append(f"{url} - {str(e)}")

        if erros:
            erro_msg = "\n\n".join(erros)
            QMessageBox.warning(self, "Erros durante o download", f"Alguns downloads falharam:\n\n{erro_msg}")
        else:
            QMessageBox.information(self, "Concluído", "Todos os downloads de MP3 foram finalizados com sucesso!")

        self.urls.clear()
        self.links_display.clear()

    def download_video(self):
        if not self.urls:
            QMessageBox.warning(self, "Aviso", "Nenhum link adicionado!")
            return
        
        destino = QFileDialog.getExistingDirectory(self, "Escolha o diretório de destino")
        if not destino:
            return
        
        os.makedirs(destino, exist_ok=True)
        ydl_opts = {"format": "bestvideo+bestaudio", "outtmpl": f"{destino}/%(title)s.%(ext)s"}
        
        for url in self.urls:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
        QMessageBox.information(self, "Concluído", "Todos os downloads de vídeo foram finalizados!")
        self.urls.clear()
        self.links_display.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = YouTubeDownloader()
    window.show()
    app.exec()
