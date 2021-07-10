function handleFormatData(data) {
  var response = [] //response array
  for (var i = 0; i < data.length; i++) {

    const formated = {
      "data": data[i]['gsx$data']['$t'],
      "de": data[i]['gsx$de']['$t'],
      "hmtl": data[i]['gsx$html']['$t'],
      "resumo": data[i]['gsx$resumo']['$t'],
    }

    response.push(formated)
  }

  return response
}

module.exports = handleFormatData