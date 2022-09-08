function handleCutData(period, arrayToCut) {
  //return the last {dataNumber} elements
  var cutPeriod = period*200
  if(period === '3'){
    arrayToCut
  }

  return arrayToCut.slice(Math.max(arrayToCut.length - cutPeriod, 0))
}

module.exports = handleCutData