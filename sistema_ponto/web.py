import csv
import hmac
import os
from functools import wraps
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for
from dotenv import load_dotenv

from .cadastro import CadastroFuncionario
from .config import ARQUIVO_RELATORIO
from .reconhecimento import ReconhecimentoFacial
from .treino import TreinadorModelo

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

app = Flask(__name__, template_folder=ROOT_DIR / "templates", static_folder=ROOT_DIR / "static")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

SENHA_ADMIN = os.getenv("ADMIN_PASSWORD")

if (
    not app.secret_key
    or app.secret_key == "gere-uma-chave-aleatoria"
    or len(app.secret_key) < 32
    or not SENHA_ADMIN
    or SENHA_ADMIN == "defina-uma-senha-forte"
    or len(SENHA_ADMIN) < 12
):
    raise RuntimeError(
        "Defina FLASK_SECRET_KEY (mínimo de 32 caracteres) e ADMIN_PASSWORD "
        "(mínimo de 12 caracteres) no ambiente ou em um arquivo .env. "
        "Substitua os valores de exemplo."
    )


def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logado"):
            flash("Faça login como administrador para acessar essa área.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return redirect(url_for("ponto"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha", "").strip()

        if hmac.compare_digest(senha, SENHA_ADMIN):
            session["admin_logado"] = True
            flash("Login realizado com sucesso.")
            return redirect(url_for("admin"))
        else:
            flash("Senha incorreta.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    flash("Você saiu da área administrativa.")
    return redirect(url_for("login"))


@app.route("/admin")
@login_obrigatorio
def admin():
    return render_template("admin.html")


@app.route("/cadastrar", methods=["POST"])
@login_obrigatorio
def cadastrar():
    nome = request.form.get("nome", "").strip()

    if not nome:
        flash("Digite o nome do funcionário.")
        return redirect(url_for("admin"))

    cadastro = CadastroFuncionario(max_fotos=50)
    sucesso = cadastro.cadastrar(nome)

    if sucesso:
        flash(f"Funcionário {nome} cadastrado com sucesso.")
    else:
        flash("Erro ao cadastrar funcionário.")

    return redirect(url_for("admin"))


@app.route("/treinar", methods=["POST"])
@login_obrigatorio
def treinar():
    treinador = TreinadorModelo()
    sucesso = treinador.treinar()

    if sucesso:
        flash("Modelo treinado com sucesso.")
    else:
        flash("Erro ao treinar modelo.")

    return redirect(url_for("admin"))


@app.route("/ponto")
def ponto():
    return render_template("ponto.html", resultado=None)


@app.route("/reconhecer", methods=["POST"])
def reconhecer():
    reconhecimento = ReconhecimentoFacial(
        limite_confianca=65,
        tempo_espera_registro=10
    )

    resultado = reconhecimento.iniciar()

    return render_template("ponto.html", resultado=resultado)


@app.route("/relatorio")
@login_obrigatorio
def relatorio():
    linhas = []

    if ARQUIVO_RELATORIO.exists():
        with ARQUIVO_RELATORIO.open("r", encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.reader(arquivo))

    return render_template("relatorio.html", linhas=linhas)


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG", "0") == "1")
