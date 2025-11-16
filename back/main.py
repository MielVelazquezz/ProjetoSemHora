import sqlite3
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================ isso aqui é pra carregar os arquivos de css e js ================ 
@app.route('/images/<path:filename>')
def serve_images(filename):
    images_path = 'D:/ProjetoSemHora/front/images'
    return send_from_directory(images_path, filename)

@app.route('/<path:filename>')
def serve_static(filename):
    front_path = 'D:/ProjetoSemHora/front'
    return send_from_directory(front_path, filename)


@app.route('/')
def index():
    return "funcionando na porta 5000"

# ======================================= HOME ========================================== 
@app.route('/home')
def home():
    return send_from_directory('D:/ProjetoSemHora/front', 'inicial.html')


# ======================================= IDOSOS ======================================== 
@app.route('/busqueIdoso')
def busque_idoso():
    return send_from_directory('D:/ProjetoSemHora/front', 'busqueIdoso.html')

@app.route('/listarIdosos')
def listarIdosos():
    ativo = 1
    comando = f"SELECT nome_completo, data_nascimento, email, telefone, cpf, endereco, media_avaliacao, foto_perfil, id FROM usuarios WHERE tipo='idoso' AND ativo={ativo};"
    try:
        conn = sqlite3.connect('semHora.db')
        cur = conn.cursor()
        cur.execute(comando)
        idosos = cur.fetchall()
        cur.close()
        conn.close()
        
        tab_linhas = ""
        for i in idosos:
            tab_linhas += f'''
            <div class="card-item" margin_bottom="20px">
                <div class="divTop">
                    <img class="img" src="/images/default.png" alt="foto">
                    <div class="divNome">
                        <p class="textbold">{i[0]}</p>  
                        <p class="textoInfo">Avaliação Média</p>
                        <p class="textoInfo">{i[6]} <img class="star" src="/images/star-svgrepo-fill.svg"></p> 
                    </div>
                </div>
                <p class="cidade">{i[5]}</p> 
                <div class="divLinha"></div>
                <div class="divInfoExtra">
                    <p class="textoInfo"><span class="textbold">Contato:</span> {i[3]} | {i[2]}</p> 
                    <br>
                    <p class="textoInfo"><span class="textbold">Data de Nascimento:</span> {i[1]}</p> 
                    <br>
                    <p class="textoInfo"><span class="textbold">CPF:</span> {i[4]}</p> 
                    <br>
                </div>
                <button class="btnChat" onclick="excluirIdoso({i[8]})">EXCLUIR</button>
            </div>
            '''
        
        return tab_linhas
    except sqlite3.Error as error:
        return "Erro --> "+str(error)
    
@app.route('/cadastro')
def cadastroIdoso():
    return send_from_directory('D:/ProjetoSemHora/front', 'idoso.html')
    
@app.route('/cadIdoso/<nome>/<data_nascimento>/<email>/<telefone>/<cpf>/<endereco>/<senha>')
def cadIdoso(nome, data_nascimento, email, telefone, cpf, endereco, senha):
    comando = """INSERT INTO usuarios 
    (tipo, nome_completo, data_nascimento, email, cpf, telefone, 
    senha_hash, endereco, foto_perfil, data_cadastro, ativo, media_avaliacao)VALUES 
    ('idoso', '{nome}', '{data_nascimento}', '{email}', '{cpf}', '{telefone}', 
    '{senha}', '{endereco}', 'default.png', DATE('now'), 1, NULL);"""    

    try:
        conn = sqlite3.connect('semHora.db')
        cur = conn.cursor()
        cur.execute(comando.format(
            nome=nome,
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            cpf=cpf,
            endereco=endereco,
            senha=senha
        ))

        conn.commit()
        cur.close()
        conn.close()

        return "idoso castrado com sucesso"
    
    except sqlite3.Error as error:
        return "Erro --> "+str(error)
    

@app.route('/excluir/idoso/<id>')
def excluir_idoso(id):
    comando = f"UPDATE usuarios SET ativo=0 WHERE id={id};"
    try:
        conn = sqlite3.connect('semHora.db')
        cur = conn.cursor()
        cur.execute(comando)
        conn.commit()
        cur.close()
        conn.close()
        return "Idoso excluído com sucesso"
    except sqlite3.Error as error:
        return "Erro --> "+str(error)

app.run(debug=True)
