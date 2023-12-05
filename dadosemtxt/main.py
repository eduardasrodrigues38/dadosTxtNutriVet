from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Lista de contatos
contatos = []


def salvar_contatos():
  with open('contatos.txt', 'w') as arquivo:
    json.dump(contatos, arquivo)


def carregar_contatos():
  contatos.clear()  # Limpar a lista antes de carregar
  try:
    with open('contatos.txt', 'r') as arquivo:
      contatos.extend(json.load(arquivo))
  except FileNotFoundError:
    # O arquivo ainda não existe, então não há contatos para carregar
    pass


@app.route('/')
def index():
  carregar_contatos()
  return render_template('index.html', contatos=contatos)


@app.route('/adicionar', methods=['POST'])
def adicionar():
  nome = request.form.get('nome')
  telefone = request.form.get('telefone')
  contato = {'nome': nome, 'telefone': telefone}
  contatos.append(contato)
  salvar_contatos()
  return redirect(url_for('index'))


@app.route('/remover/<int:index>')
def remover(index):
  if 0 <= index < len(contatos):
    del contatos[index]
    salvar_contatos()
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(host="0.0.0.0")
