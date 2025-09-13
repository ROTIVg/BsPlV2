import os
import subprocess
import platform
import streamlit as st

def listar_dispositivos():
    system = platform.system()
    dispositivos = []
    if system in ["Linux", "Darwin"]:
        media_path = "/media/" if system=="Linux" else "/Volumes/"
        if os.path.exists(media_path):
            dispositivos = [os.path.join(media_path, d) for d in os.listdir(media_path)]
    elif system == "Windows":
        import string
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        dispositivos = drives
    return dispositivos

st.title("YouTube Playlist Downloader")

playlist_url = st.text_input("Cole a URL da playlist:")

local_opcao = st.radio("Onde deseja baixar?", ["Computador", "Dispositivo conectado"])

if local_opcao == "Dispositivo conectado":
    dispositivos = listar_dispositivos()
    if dispositivos:
        dest_path = st.selectbox("Escolha o dispositivo:", dispositivos + ["Outro caminho"])
        if dest_path == "Outro caminho":
            dest_path = st.text_input("Digite o caminho do dispositivo:")
    else:
        st.warning("Nenhum dispositivo encontrado. Baixando no computador.")
        dest_path = st.text_input("Digite o caminho da pasta de destino:")
else:
    dest_path = st.text_input("Digite o caminho da pasta de destino:")

tipo = st.radio("Escolha o tipo de download:", ["Vídeo", "Áudio MP3"])

download_button = st.button("Iniciar Download")

if download_button and playlist_url and dest_path:
    st.info("Iniciando download...")

    if tipo == "Vídeo":
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio",
            "-o", os.path.join(dest_path, "%(playlist_title)s/%(title)s.%(ext)s"),
            playlist_url
        ]
    else:
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", os.path.join(dest_path, "%(playlist_title)s/%(title)s.%(ext)s"),
            playlist_url
        ]

    # Mostrar saída em tempo real
    output_area = st.empty()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    log = ""
    for line in process.stdout:
        log += line
        output_area.text(log)

    process.wait()
    st.success("Download concluído!")