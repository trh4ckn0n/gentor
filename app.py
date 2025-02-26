from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# Fonction pour générer l'adresse .onion avec un préfixe donné et un nombre donné
def generate_onion(prefix, count):
    try:
        command = ["go", "run", "main.go", f"^{prefix}", str(count)]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n")  # Retourne une liste d'adresses
    except subprocess.CalledProcessError as e:
        return [f"Erreur: {e.stderr.strip()}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prefix = data.get('prefix', '').strip()
    count = data.get('count', 5)  # Valeur par défaut: 5

    if not prefix:
        return jsonify({"error": "Préfixe requis"}), 400

    try:
        count = int(count)
        if count < 1 or count > 20:  # Limitation pour éviter les abus
            return jsonify({"error": "Le nombre d'adresses doit être entre 1 et 20"}), 400
    except ValueError:
        return jsonify({"error": "Nombre invalide"}), 400

    onion_addresses = generate_onion(prefix, count)

    return jsonify({"onions": onion_addresses})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
