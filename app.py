from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # Llamada a la API simple-ytdl
        api_url = f"https://api.youtubedownloader.io/api/v1/info?url={url}"
        response = requests.get(api_url)

        if response.status_code != 200:
            return render_template("error.html", mensaje="Error al obtener datos del video.")

        data = response.json()

        # Pasamos los datos al template
        return render_template("resultado.html", video=data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


