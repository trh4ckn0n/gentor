import requests
from flask import Flask, request, jsonify, render_template

VPS_API_URL = "http://154.12.234.206:5000"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prefix = request.json.get('prefix', '')
    count = request.json.get('count', 5)

    if not prefix:
        return jsonify({"error": "Préfixe requis"}), 400

    try:
        response = requests.post(f"{VPS_API_URL}/generate",
                                 json={"prefix": prefix, "count": count},
                                 headers={"Authorization": "Bearer MA_SUPER_CLE"})

        data = response.json()  # Convertir la réponse en JSON

        # Convertir en tableau si "onion" est présent
        onion_list = data["onion"].strip().split("\n") if "onion" in data else []

        return jsonify({"onions": onion_list})  # Envoyer un tableau JSON

    except Exception as e:
        print("Erreur connexion VPS :", str(e))
        return jsonify({"error": "Impossible de contacter le VPS"}), 500

# 🔥 Ce bloc doit être en dehors de la fonction !
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
