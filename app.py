import os
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
        response = requests.post("http://154.12.234.206:5000/generate",
                                 json={"prefix": prefix, "count": count},
                                 headers={"Authorization": "Bearer MA_SUPER_CLE"})

        data = response.json()  # Convertir la réponse en JSON

        # Lire les fichiers de clé
        if "onion" in data:
            onion_list = data["onion"].strip().split("\n")  # Split par ligne
        else:
            onion_list = []

        # Récupérer les clés générées (les fichiers)
        keys = {}
        folder_path = f"/path/to/your/folder/{prefix}/"  # Remplace par le chemin correct
        if os.path.exists(folder_path):
            try:
                with open(os.path.join(folder_path, "hs_ed25519_public_key"), "r") as f:
                    keys["public_key"] = f.read().strip()
                with open(os.path.join(folder_path, "hs_ed25519_secret_key"), "r") as f:
                    keys["secret_key"] = f.read().strip()
            except Exception as e:
                return jsonify({"error": f"Erreur de lecture des clés : {str(e)}"}), 500

        return jsonify({"onions": onion_list, "keys": keys})  # Ajouter les clés au JSON de réponse
    except Exception as e:
        print("Erreur connexion VPS :", str(e))
        return jsonify({"error": "Impossible de contacter le VPS"}), 500
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
