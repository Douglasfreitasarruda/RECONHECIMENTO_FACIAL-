# Sistema de ponto facial

Aplicação local de registro de ponto por reconhecimento facial. O sistema tem uma interface web Flask e um menu alternativo de terminal.

> **Privacidade:** fotos faciais, nomes, modelos treinados e relatórios de ponto são dados pessoais e não fazem parte do repositório. A pasta `data/` é mantida apenas como diretório vazio e seu conteúdo é ignorado pelo Git.

## Tecnologias

- Python 3.10–3.12
- Flask para servidor e páginas HTML com Jinja
- OpenCV (`opencv-contrib-python`) para câmera, detecção Haar e reconhecimento LBPH (`cv2.face`)
- NumPy para os dados usados no treinamento
- HTML, CSS e JavaScript na interface
- CSV para o relatório de registros

## Estrutura

```text
app.py                  Inicialização do servidor web
main.py                 Menu de terminal
sistema_ponto/          Código Python da aplicação
templates/              Páginas HTML/Jinja
static/                 CSS e JavaScript
data/                   Fotos, modelo treinado, nomes e registros CSV
requirements.txt        Dependências Python
tests/                  Testes automatizados das rotas web
.github/workflows/      Verificação automática executada pelo GitHub Actions
```

## Instalação e execução

Crie e ative um ambiente virtual, instale as dependências e inicie o servidor:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edite o .env e substitua os valores de exemplo antes de continuar.
python app.py
```

Abra `http://127.0.0.1:5000`. A câmera precisa estar conectada à máquina que executa o Python; o reconhecimento é iniciado pelo servidor.

Para o menu de terminal, execute `python main.py` em uma sessão com acesso à câmera e interface gráfica.

## Testes

Com o ambiente virtual ativado e o `.env` configurado, execute:

```powershell
python -m unittest discover -s tests -v
```

## Dados e treinamento

Os dados ficam em `data/`. O cadastro grava imagens em `data/rostos/`; a opção **Treinar modelo** cria `data/modelo_lbph.yml` e `data/nomes.txt`. Os registros de ponto são anexados a `data/relatorio_ponto.csv`. Faça cópias de segurança dessa pasta para preservar os dados. Todo o conteúdo de `data/` é ignorado pelo Git para evitar a publicação acidental de dados biométricos e registros pessoais.

O login administrativo usa as variáveis obrigatórias `ADMIN_PASSWORD` (mínimo de 12 caracteres) e `FLASK_SECRET_KEY` (mínimo de 32 caracteres). Defina valores próprios no arquivo `.env`, que também é ignorado pelo Git. Para gerar uma chave segura, execute `python -c "import secrets; print(secrets.token_hex(32))"`. Por padrão o servidor escuta apenas em `127.0.0.1` e o modo de depuração fica desligado.

## Antes de publicar

- Confirme com `git status --short --ignored` que `.env` e os arquivos de `data/` aparecem como ignorados.
- Nunca adicione fotos faciais, modelos treinados, relatórios ou credenciais com `git add -f`.
- Revise a legislação e obtenha consentimento apropriado antes de usar reconhecimento facial com dados reais.

## Limitações

Este é um projeto local e educacional. Ele não inclui proteção contra força bruta, redefinição de senha, trilha de auditoria ou controles necessários para uma implantação pública na internet.
