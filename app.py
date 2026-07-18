from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Ч</h1>
    <h2>Charlie AI</h2>
    <p>Привет! Я Чарли, твой второй мозг.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)