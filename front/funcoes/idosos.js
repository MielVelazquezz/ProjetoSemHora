function CarregaIdosos(){
    let container = document.getElementById("divCard"); 
    
    if (!container) {
        console.error("Elemento não encontrado!");
        return;
    }

    let endpoint = "http://127.0.0.1:5000/listarIdosos"
    fetch(endpoint)
    .then(result => result.text())
    .then(dados => {
        console.log("Dados recebidos:", dados)
        container.innerHTML = dados
    })
    .catch(error => {
        console.error("Erro:", error)
    })
}

function cadIdoso(){
    let nome = document.querySelector('[name="nome_idoso"]').value
    let dataNasc = document.querySelector('[name="data_nasc_idoso"]').value
    let email = document.querySelector('[name="email_idoso"]').value
    let cpf = document.querySelector('[name="cpf_idoso"]').value
    let telefone = document.querySelector('[name="tel_idoso"]').value
    let endereco = document.querySelector('[name="end_idoso"]').value
    let senha = document.querySelector('[name="senha_idoso"]').value

    let url = `http://localhost:5000/cadIdoso/${nome}/${dataNasc}/${email}/${telefone}/${cpf}/${endereco}/${senha}`
    
    fetch(url)
    .then(result => result.text())
    .then(dados => {
        alert(dados)
    })
    .catch(error => {
        alert("Erro ao cadastrar!")
        CarregaIdosos()
    })
}

function excluirIdoso(id){
    let url = `http://localhost:5000/excluir/idoso/${id}`
    fetch(url)
    .then(result => result.text())
    .then(dados => {
        alert(dados)
        CarregaIdosos()
    })
    .catch(error => {
        alert("Erro ao excluir!")
    })
}