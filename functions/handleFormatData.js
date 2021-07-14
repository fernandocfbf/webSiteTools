function handleFormatData(data) {
  var response = [] //response array
  for (var i = 0; i < data.length; i++) {

    const formated = {
      "id": i,
      "data": data[i]['gsx$data']['$t'],
      "de": data[i]['gsx$de']['$t'],
      "html": data[i]['gsx$html']['$t'],
      "resumo": data[i]['gsx$resumo']['$t'],
    }

    response.push(formated)
  }

  return response
}

module.exports = handleFormatData