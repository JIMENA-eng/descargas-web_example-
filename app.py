from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = "clave-super-secreta"

# Función para extraer el ID del video de YouTube
def extraer_id_youtube(url):
    patron = r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})"
    coincidencia = re.search(patron, url)
    return coincidencia.group(1) if coincidencia else None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        formato = request.form.get("formato")

        if not url:
            flash("⚠️ Debes ingresar una URL de YouTube.")
            return redirect(url_for("index"))

        video_id = extraer_id_youtube(url)
        if not video_id:
            flash("❌ URL de YouTube no válida.")
            return redirect(url_for("index"))

        # Generar enlace según el formato elegido
        if formato == "mp3":
            enlace = f"https://yt-download.org/api/button/mp3/{video_id}"
        else:
            enlace = f"https://yt-download.org/api/button/videos/{video_id}"

        # Mostrar el enlace en la plantilla
        return render_template("resultado.html", enlace=enlace, formato=formato)

    return render_template("index.html")


@app.route("/about")
def about():
    return "<h3>Descargador Web Flask - Usando API externa (yt-download.org)</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

