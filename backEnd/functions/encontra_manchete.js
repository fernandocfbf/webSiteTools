function encontra_manchete(html){

    if(html.includes('type="application/json"')){ //verifica se é manchete

        var json = "" //cria a variável quer armazenará o json final

        var comecou = false //verifica se o json desejado comecou

        //percorre o hmtl
        for(var i = 0; i<html.length; i++){

            var letter = html[i] //pega a letra atual

            //se comecou o json adiciona
            if(letter == "{" && comecou == false){ 
                comecou = true
                json += letter
            }

            //se já passou do começo adiciona
            else if(comecou == true && html.substring(i, i+9).toString() != "</script>"){
                json += letter
            }

            //se acabou para o for
            else if(comecou == true && html.substring(i, i+9).toString() == "</script>"){
                break
            }
        }

        var json_true = JSON.parse(json) //transformar a string em json

        var manchetes = json_true["cards"][0]["widgets"]

        return manchetes
    }

    else{

        return false
    }

}

module.exports = encontra_manchete