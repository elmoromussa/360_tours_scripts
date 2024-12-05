import os
import subprocess

# Ruta d'origen dels vídeos
source_folder = input("Introdueix la ruta de la carpeta amb els vídeos MP4 estereoscòpics: ").strip()

# Demanar la carpeta de sortida
output_folder = input("Introdueix la ruta de la carpeta de sortida: ").strip()

# Crear carpeta de sortida si no existeix
os.makedirs(output_folder, exist_ok=True)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except FileNotFoundError:
        print("❌ Error: FFmpeg no està instal·lat o no es troba al PATH")
        return False

# Al principi del script
if not check_ffmpeg():
    exit(1)

if not os.path.exists(source_folder):
    print(f"❌ Error: La carpeta d'origen '{source_folder}' no existeix")
    exit(1)

retain_upper = input("Vols mantenir la meitat superior del vídeo? (s/n): ").lower().startswith('s')

# Funció per retallar un vídeo
def convert_to_monoscopic(input_file, output_file, retain_upper_half=True):
    # Comanda FFmpeg
    if retain_upper_half:
        crop_filter = "crop=iw:ih/2:0:0"  # Retalla la meitat superior
    else:
        crop_filter = "crop=iw:ih/2:0:ih/2"  # Retalla la meitat inferior
    
    # Afegim metadades per a vídeo 360 monoscòpic i eliminem stereo3d
    command = [
        "ffmpeg", "-i", input_file,
        "-filter:v", crop_filter,
        "-c:a", "copy",
        "-metadata:s:v:0", "spherical=true",
        "-metadata:s:v:0", "projection=equirectangular",
        "-metadata:s:v:0", "stereo_mode=mono",
        "-map_metadata", "-1",  # Elimina totes les metadades
        output_file
    ]
    subprocess.run(command, check=True)

# Processar tots els fitxers MP4 a la carpeta
for file_name in os.listdir(source_folder):
    if file_name.endswith(".mp4"):
        input_path = os.path.join(source_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        try:
            print(f"Processant: {file_name}")
            convert_to_monoscopic(input_path, output_path, retain_upper_half=retain_upper)  # Cambia a False per retallar la part inferior
            print(f"✔ Vídeo convertit: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al processar {file_name}: {e}")

print(f"Tots els vídeos s'han processat. Els resultats estan a: {output_folder}")
