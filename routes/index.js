var express = require('express');
const { type } = require('os');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {
	res.render('index', { title: 'Express' });
});

//machine learning process
router.post('/machineLearning', async function (req, res) {

	var functionToString = require("../functions/data_to_string")
	var functionCompileData = require("../functions/compile_data")

	var { spawn } = require('child_process')

	console.log("running...")

	try {

		const manchetes = req.body.manchetes //pega as manchetes do front

		var resposta = functionCompileData(manchetes) //cria as lista de manchete e links

		console.log(resposta[0].length)

		var data_to_send = {
			"Manchetes": resposta[0],
			"Links": resposta[1]
		}

		var childPython = spawn('python', ['./machineLearning/ml.py', JSON.stringify(data_to_send)])

		childPython.stdout.on('data', function (data) {
			if (data.toString('utf8') == "false") {
				res.json(false)
				res.end()
			} else {
				var json = data.toString('utf8')
				console.log(json)
				res.json(json)
				res.end()
			}

		})

		childPython.stderr.on('data', (data) => {
			console.error('stderr: ', data.toString('utf8'))
		})

		childPython.on('close', (code) => {
			console.log("child process exited with code ", code)
		})

	} catch (err) {
		console.log(err)
	}
})

//web scraping process social finance
router.post('/webScraping_social', async function (req, res) {
	var { spawn } = require('child_process')
	console.log("Running...")

	const url = process.env.MONGO_URL

	const automation = req.body.reconhecer

	try {
		var childPython = spawn('python', ['./webScraping/socialFinance.py', url, automation])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			res.json(json)
			res.end()
		})

		childPython.stderr.on('data', (data) => {
			console.error('stderr: ', data.toString('utf8'))
		})

		childPython.on('close', (code) => {
			console.log("child process exited with code ", code)
		})

	} catch (err) {
		console.log(err)
	}
})

//web scraping process instiglio
router.post('/webScraping_instiglio', async function (req, res) {
	var { spawn } = require('child_process')
	console.log("Running...")

	const automation = req.body.reconhecer

	const url = process.env.MONGO_URL

	try {
		var childPython = spawn('python', ['./webScraping/instiglio.py', url, automation])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			res.json(json)
			res.end()
		})

		childPython.stderr.on('data', (data) => {
			console.error('stderr: ', data.toString('utf8'))
		})

		childPython.on('close', (code) => {
			console.log("child process exited with code ", code)
		})

	} catch (err) {
		console.log(err)
	}

})

//web scraping process third sector
router.post('/webScraping_sector', async function (req, res) {
	var { spawn } = require('child_process')
	console.log("Running...")

	const url = process.env.MONGO_URL

	const automation = req.body.reconhecer

	try {
		var childPython = spawn('python', ['./webScraping/sector.py', url, automation])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			res.json(json)
			res.end()
		})

		childPython.stderr.on('data', (data) => {
			console.error('stderr: ', data.toString('utf8'))
		})

		childPython.on('close', (code) => {
			console.log("child process exited with code ", code)
		})

	} catch (err) {
		console.log(err)
	}
})

//web scraping process Go Lab
router.post('/webScraping_lab', async function (req, res) {
	var { spawn } = require('child_process')
	console.log("Running...")

	const url = process.env.MONGO_URL

	const automation = req.body.reconhecer

	try {
		var childPython = spawn('python', ['./webScraping/sector.py', url, automation])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			res.json(json)
			res.end()
		})

		childPython.stderr.on('data', (data) => {
			console.error('stderr: ', data.toString('utf8'))
		})

		childPython.on('close', (code) => {
			console.log("child process exited with code ", code)
		})

	} catch (err) {
		console.log(err)
	}
})


module.exports = router;

