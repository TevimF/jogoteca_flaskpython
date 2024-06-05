from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Estêvão Felipe", "Estevuf", "senha")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")
usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3}


Jogo1 = Jogo('Valorant', 'FPS', 'PC')
Jogo2 = Jogo('Counter Strike 2', 'FPS', 'PC')
lista = [Jogo1, Jogo2]

app = Flask(__name__)
app.secret_key = 'alura'


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if session['usuario_logado'] is not None:
        return render_template('novo.html', titulo='Novo Jogo')
    else:
        flash('Faça o login para poder efetuar novos cadastros!')
        return redirect(url_for('login', proxima=url_for('novo')))


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout bem sucedido!')
    return redirect(url_for('index'))


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso ')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))


app.run(debug=True)
