const countries_coordinates = require('../utils/countries') 

function sumAmounts(data) {
    var years = {}
    var fields = {}
    var countries = []
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
        if (el['gsx$country']['$t'].toString().length > 0 ){
            var current = countries.find(elem => elem.country == el['gsx$country']['$t'])
            if (current) {
                current['sum'] += 1
            } else {                
                const country = countries_coordinates.find(elem => elem.country == el['gsx$country']['$t'])
                countries.push({
                    'country': el['gsx$country']['$t'],
                    'sum': 1,
                    'latitude': country.latitude,
                    'longitude': country.longitude
                })
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