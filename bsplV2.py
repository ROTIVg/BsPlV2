import os
import subprocess
import platform
from InquirerPy import inquirer

def listar_dispositivos():
    """Lista dispositivos conectados no sistema."""
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

def escolher_dispositivo():
    dispositivos = listar_dispositivos()
    if not dispositivos:
        print("Nenhum dispositivo encontrado. Baixando no computador.")
        return inquirer.text(message="Digite o caminho da pasta de destino:").execute()
    escolha = inquirer.select(
        message="Escolha um dispositivo:",
        choices=dispositivos + ["Digitar caminho manualmente"]
    ).execute()
    if escolha == "Digitar caminho manualmente":
        return inquirer.text(message="Digite o caminho da pasta de destino:").execute()
    return escolha

def main():
    print("=== YouTube Playlist Downloader ===")

    playlist_url = inquirer.text(message="Cole a URL da playlist:").execute()

    local_opcao = inquirer.select(
        message="Onde deseja baixar?",
        choices=["Computador", "Dispositivo conectado"]
    ).execute()

    if local_opcao == "Dispositivo conectado":
        dest_path = escolher_dispositivo()
    else:
        dest_path = inquirer.text(message="Digite o caminho da pasta de destino:").execute()

    tipo = inquirer.select(
        message="Escolha o tipo de download:",
        choices=["Vídeo", "Áudio MP3"]
    ).execute()

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

    print("Iniciando download...")
    subprocess.run(cmd)
    print("Download concluído!")

if __name__ == "__main__":
    main()