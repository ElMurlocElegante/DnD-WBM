from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dados = []
        for i in range(1, 5):
            dado = request.form.get(f"dado{i}")
            if dado and dado.startswith("d") and dado[1:].isdigit() and int(dado[1:]) != 0:
                dados.append(int(dado[1:]))
            else:
                error = f"Dado incorrecto: {dado}. Debe tener el formato 'dn', donde 'n' es un número mayor que cero."
                return render_template('index.html', error=error)
        if len(dados) <= 4:
            return render_template('resultado.html', dados=dados)
        else:
            error = "Solo se permiten hasta 4 dados."
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
