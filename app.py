from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "clave-secreta"  # necesaria para los mensajes flash

# 📂 Ruta donde se guardarán las descargas
CARPETA_DESCARGAS = os.path.join(os.getcwd(), "descargas")
os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

# 📂 Ruta de FFmpeg (ajusta a la tuya)
RUTA_FFMPEG = r"C:\ffmpeg\ffmpeg-2025-10-21-git-535d4047d3-essentials_build\bin"

def descargar_youtube(url, formato):
    """Descarga un video de YouTube en MP3 o MP4"""
    if formato == "mp3":
        opciones = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(CARPETA_DESCARGAS, '%(title)s.%(ext)s'),
            'ffmpeg_location': RUTA_FFMPEG,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
        }
    else:
        opciones = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(CARPETA_DESCARGAS, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'ffmpeg_location': RUTA_FFMPEG,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'postprocessor_args': [
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k'
            ],
            'noplaylist': True,
            'quiet': True,
        }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        nombre_archivo = ydl.prepare_filename(info)
        if formato == "mp3":
            nombre_archivo = os.path.splitext(nombre_archivo)[0] + ".mp3"
        else:
            nombre_archivo = os.path.splitext(nombre_archivo)[0] + ".mp4"
        return os.path.basename(nombre_archivo)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        formato = request.form["formato"]

        if not url:
            flash("⚠️ Debes ingresar una URL de YouTube.")
            return redirect(url_for("index"))

        try:
            nombre_archivo = descargar_youtube(url, formato)
            flash("✅ Descarga completada correctamente.")
            return redirect(url_for("descargar", nombre_archivo=nombre_archivo))
        except Exception as e:
            flash(f"❌ Error al descargar: {e}")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/descargar/<nombre_archivo>")
def descargar(nombre_archivo):
    return send_from_directory(CARPETA_DESCARGAS, nombre_archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
