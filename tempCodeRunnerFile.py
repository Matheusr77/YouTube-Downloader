from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def baixar_youtube_para_mp3(url, pasta_destino='.'):
    try:
        # Baixar o vídeo do YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        caminho_video = video.download(output_path=pasta_destino)

        # Converter para MP3
        caminho_mp3 = os.path.splitext(caminho_video)[0] + ".mp3"
        audio = AudioFileClip(caminho_video)
        audio.write_audiofile(caminho_mp3)

        # Remover o arquivo original (opcional)
        os.remove(caminho_video)

        print(f"Download concluído: {caminho_mp3}")
    except Exception as e:
        print(f"Erro: {e}")

# URL do vídeo que deseja converter
url_video = input("Digite a URL do vídeo do YouTube: ")
baixar_youtube_para_mp3(url_video)
