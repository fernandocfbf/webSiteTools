function sumAmounts(data) {
    var years = {}
    var fields = {}
    var countries = {}
    var investedSum = 0
    var peopleSum = 0
    for (var i = 0; i < data.length; i++) {
        const el = data[i]
        if (el['gsx$amountinmillionusd']['$t'].toString().length > 0) {
            investedSum += parseFloat(el['gsx$amountinmillionusd']['$t']) //sum investment

            if (fields.hasOwnProperty(el['gsx$target']['$t'])) {
                fields[el['gsx$target']['$t']]['contracts'] += 1
                fields[el['gsx$target']['$t']]['sum'] += parseFloat(el['gsx$amountinmillionusd']['$t'])
            } else {
                fields[el['gsx$target']['$t']] = {
                    'contracts': 1,
                    'sum': parseFloat(el['gsx$amountinmillionusd']['$t'])
                }
            }
        }
        if (el['gsx$country']['$t'].toString().length > 0){
            if (countries.hasOwnProperty(el['gsx$country']['$t'])) {
                countries[el['gsx$country']['$t']] += 1
            } else {
                countries[el['gsx$country']['$t']] = 1
            }
        }

        if (el['gsx$targetpopulationnumber']['$t'].toString().length > 0) peopleSum += parseFloat(el['gsx$targetpopulationnumber']['$t']) //sum beneficiaries
        if (el['gsx$contractannounced']['$t'].toString().length > 0) {
            if (years.hasOwnProperty(el['gsx$contractannounced']['$t'])) {
                years[el['gsx$contractannounced']['$t']] += 1
            } else {
                years[el['gsx$contractannounced']['$t']] = 1
            }
        }
    }
    return {years, investedSum, peopleSum, fields, countries}
}

module.exports = sumAmounts