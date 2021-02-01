
var functionCriaDic = require("./cria_dic")

function compile_data(data) {

    var lista_manchetes = [] //cria lista que armazenará as manchetes
    var lista_links = [] //cria lista que armazenará os links

    //percorre todos os html dos dados
    for (var i = 0; i < data.length; i++) {

        [lista_manchetes, lista_links] = functionCriaDic(data[i]["HTML"], lista_manchetes, lista_links) //pega as manchetes
    }

    return [lista_manchetes, lista_links]
}

module.exports = compile_data