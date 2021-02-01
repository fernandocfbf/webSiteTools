var functionEncontraManchete = require("./encontra_manchete")

function cria_dic(html, manchetes, links){

    var lista = functionEncontraManchete(html) //cria a lista das manchetes
    
    //se a lista tiver alguma manchete...
    if(lista != false){
        
        for(var i=0; i<lista.length; i++){

            var card = lista[i] //pega o card atual
            
            manchetes.push(card['title']) //adiciona o título da manchete
            links.push(card['url']) //adiciona o link da manchete
        }
    }

    return [manchetes, links]
}

module.exports = cria_dic