var express = require('express');
const { type } = require('os');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});

//machine learning process
router.post('/machineLearning', function (req, res) {

  var functionToString = require("../functions/data_to_string")
  var functionCompileData = require("../functions/compile_data")

  var { spawn } = require('child_process')

  try {

    const manchetes = req.body.manchetes //pega as manchetes do front

    var resposta = functionCompileData(manchetes) //cria as lista de manchete e links

    var data_to_send = {
      "Manchetes": resposta[0],
      "Links": resposta[1]
    }

    var childPython = spawn('python', ['./machineLearning/ml.py', JSON.stringify(data_to_send)])

    childPython.stdout.on('data', function (data) {
      console.log(`stdout: ${data}`)
    })

    childPython.stderr.on('data', (data) => {
      console.error('stderr: ', data.toString('utf8'))
    })

    childPython.on('close', (code) => {
      console.log("child process exited with code ", code)
    })

    res.json()
    res.end()

  } catch (err) {
    console.log(err)
  }
})

module.exports = router;
