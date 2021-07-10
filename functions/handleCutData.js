function handleCutData(dataNumber, arrayToCut) {
  //return the last {dataNumber} elements
  return arrayToCut.slice(Math.max(arrayToCut.length - dataNumber, 0))
}

module.exports = handleCutData