var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});

//machine learning process
router.post('/machineLearning', function (req, res) {

  var functionToString = require("../functions/data_to_string")
  var functionEncontraManchete = require("../functions/encontra_manchete")

  var { spawn } = require('child_process')

  try {

    const manchetes = req.body.manchetes //pega as manchetes do front


    console.log("RODOU O DATA: ", functionEncontraManchete(manchetes[0]["HTML"]))

    res.json()
    res.end()

    // var childPython = spawn('python', ['./machineLearning/ml_test.py', data_to_send])

    // childPython.stdout.on('data', function (data) {
    //   console.log(`stdout: ${data}`)
    // })

    // childPython.stderr.on('data', (data) => {
    //   console.error('stderr: ', data.toString('utf8'))
    // })

    // childPython.on('close', (code) => {
    //   console.log("child process exited with code ", code)
    // })

  } catch (err) {
    console.log(err)
  }
})

module.exports = router;
