from flask import Flask, render_template, request, jsonify

import random

app = Flask(__name__)

def tirar_dado(tipo_dado):
    num_caras = int(tipo_dado[1:])
    resultado = random.randint(1, num_caras)
    return resultado

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tirar_dado', methods=['POST'])
def handle_tirar_dado():
    tipo_dado = request.json.get('tipo_dado')
    resultado = tirar_dado(tipo_dado)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(debug=True)
