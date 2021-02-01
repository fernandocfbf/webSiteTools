function data_to_string(data){

    var resposta = []

    for(var i = 0; i < data.length; i++){

        const string = '""' + data[i]["HTML"].toString() + '""'

        resposta.push(string)
    }

    return resposta
}

module.exports = data_to_string