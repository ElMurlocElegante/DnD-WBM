from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def tirar_dados(n_dados, tipo_dado):
    num_caras = int(tipo_dado[1:])
    resultados = [random.randint(1, num_caras) for _ in range(n_dados)]
    return resultados

@app.route('/tirar_dados', methods=['POST'])
def tirar_dados_endpoint():
    data = request.json
    n_dados = data.get('n_dados', 1)
    tipo_dado = data.get('tipo_dado', 'd6')
    resultados = tirar_dados(n_dados, tipo_dado)
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)