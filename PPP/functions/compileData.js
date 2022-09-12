

function compile_data(data) {

    var lista_manchetes = [] //cria lista que armazenará as manchetes
    var lista_links = [] //cria lista que armazenará os links

    //percorre todos os html dos dados
    for (var i = 0; i < data.length; i++) {

        //[lista_manchetes, lista_links] = functionCriaDic(data[i]["Machete"], lista_manchetes, lista_links) //pega as manchetes
        lista_manchetes.push(data[i]["Manchete"]) //adiciona o título da manchete
        lista_links.push(data[i]["Link"]) //adiciona o link da manchete
    }

    return [lista_manchetes, lista_links]
}

module.exports = compile_data