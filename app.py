from flask import Flask, jsonify, request
from random import randint

app = Flask(__name__)

@app.route('/roll_dice', methods=['POST'])
def roll_dice():
    data = request.get_json()  # Obtener los datos JSON de la solicitud POST
    dice = data.get('dice')  # Obtener el valor de 'dice' de los datos JSON
    
    def index(dice):
        if dice.startswith("d"):
            if dice[1:].isdigit():
                num_caras = int(dice[1:])
                resultado = randint(1, num_caras)
                return jsonify({"resultado": resultado})
        elif "d" in dice:
            num_dados, num_caras = dice.split("d")
            if num_dados.isdigit() and num_caras.isdigit():
                num_dados = int(num_dados)
                num_caras = int(num_caras)
                if num_dados > 0 and num_caras > 0:
                    resultados = [randint(1, num_caras) for _ in range(num_dados)]
                    return jsonify({"resultados": resultados})
        return jsonify({"error": "Formato de dice incorrecto. Debe ser 'dn' o 'ndn', donde 'n' es un número mayor que cero."}), 400
    
    return index(dice)

if __name__ == '__main__':
    app.run(debug=True)