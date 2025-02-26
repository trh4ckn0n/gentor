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
        response = requests.post(VPS_API_URL, json={"prefix": prefix, "count": count})
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Impossible de contacter le VPS"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
