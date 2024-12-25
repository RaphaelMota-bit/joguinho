import os
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Obter o diretório onde o script está sendo executado
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo para as imagens
IMAGEM_DIR = os.path.join(base_dir, "static", "imagens")

# Verificar se o diretório existe
if not os.path.exists(IMAGEM_DIR):
    print(f"O diretório {IMAGEM_DIR} não foi encontrado.")
else:
    print(f"O diretório das imagens é: {IMAGEM_DIR}")

# Listar todas as imagens na pasta 'static/imagens'
todas_imagens = [f for f in os.listdir(IMAGEM_DIR) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Lista de nomes e contador
nomes_originais = []
nomes = []
imagens_disponiveis = todas_imagens.copy()
contador = 0

# Rotas
@app.route("/", methods=["GET", "POST"])
def index():
    global nomes_originais, nomes, contador
    if request.method == "POST":
        # Receber nomes do formulário
        nomes_input = request.form.get("nomes")
        if nomes_input:
            nomes_originais = [nome.strip() for nome in nomes_input.split(",") if nome.strip()]
            nomes = nomes_originais.copy()
            contador = len(nomes)  # Inicializar o contador com o número de nomes
        return redirect(url_for("resultado"))
    return render_template("index.html")

@app.route("/resultado", methods=["GET"])
def resultado():
    global nomes, imagens_disponiveis, contador

    if not nomes or not imagens_disponiveis:
        return render_template(
            "resultado.html",
            nome=None,
            imagem=None,
            mensagem="Não há nomes ou imagens suficientes para o sorteio."
        )

    # Sortear um nome e uma imagem
    nome_sorteado = random.choice(nomes)
    nomes.remove(nome_sorteado)

    imagem_sorteada = random.choice(imagens_disponiveis)
    imagens_disponiveis.remove(imagem_sorteada)

    # Decrementar o contador
    contador -= 1

    # Reiniciar listas e contador se o contador chegar a 0
    if contador == 0:
        nomes = nomes_originais.copy()
        imagens_disponiveis = todas_imagens.copy()
        contador = len(nomes)  # Reiniciar o contador

    return render_template(
        "resultado.html",
        nome=nome_sorteado,
        imagem=imagem_sorteada,
        mensagem=None,
        contador=contador
    )

if __name__ == "__main__":
    app.run(debug=True)
