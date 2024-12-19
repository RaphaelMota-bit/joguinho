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


# Caminho para as imagens dentro da pasta 'static/imagens'
#IMAGEM_DIR = os.path.join("static" , "imagens")

# Listar todas as imagens na pasta 'static/imagens'
imagens = [f for f in os.listdir(IMAGEM_DIR) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Lista de nomes
nomes = []

# Rotas
@app.route("/", methods=["GET", "POST"])
def index():
    global nomes
    if request.method == "POST":
        # Receber nomes do formulário
        nomes_input = request.form.get("nomes")
        if nomes_input:
            nomes = [nome.strip() for nome in nomes_input.split(",") if nome.strip()]
        return redirect(url_for("resultado"))
    return render_template("index.html")

@app.route("/resultado", methods=["GET"])
def resultado():
    global nomes, imagens

    if not nomes or not imagens:
        return render_template("resultado.html", nome=None, imagem=None)

    # Sortear um nome e uma imagem
    nome_sorteado = random.choice(nomes)
    nomes.remove(nome_sorteado)

    imagem_sorteada = random.choice(imagens)
    imagens.remove(imagem_sorteada)

    # Caminho da imagem sorteada
    caminho_imagem = os.path.join(IMAGEM_DIR, imagem_sorteada)
# Apenas envie o nome do arquivo (sem o caminho 'static/imagens')
    return render_template("resultado.html", nome=nome_sorteado, imagem=imagem_sorteada)


if __name__ == "__main__":
    app.run(debug=True)