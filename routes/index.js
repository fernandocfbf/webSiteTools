var express = require('express');
const { type } = require('os');
var router = express.Router();
const axios = require("axios")

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

		var data_to_send = {
			"Manchetes": resposta[0],
			"Links": resposta[1]
		}

		var childPython = spawn('python', ['./machineLearning/ml.py', JSON.stringify(data_to_send)])

		childPython.stdout.on('data', function (data) {
			var data_filtered = data.toString('utf8').split(',').length
			console.log("Results: ", resposta[0].length, '/ ',data_filtered)
			if (data.toString('utf8') == "false") {
				res.json(false)
				res.end()
			} else {
				var json = data.toString('utf8')
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
		var childPython = spawn('python', ['./webScraping/socialFinance.py', url, automation, process.env.NODE_ENV])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			console.log("RUNNED SOCIAL")
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
		var childPython = spawn('python', ['./webScraping/instiglio.py', url, automation, process.env.NODE_ENV])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			console.log("RUNNED INSTIGLIO")
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
		var childPython = spawn('python', ['./webScraping/sector.py', url, automation, process.env.NODE_ENV])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			console.log("RUNNED SECTOR")
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
		var childPython = spawn('python', ['./webScraping/goLab.py', url, automation, process.env.NODE_ENV])

		childPython.stdout.on('data', function (data) {
			var json = data.toString('utf8')
			console.log("RUNNED GOLAB")
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

router.get('/googleAlerts', async function (req, res) {
	var functionHandleCutData = require("../functions/handleCutData")
	var functionHandleFormatData = require("../functions/handleFormatData")

	const period = parseInt(req.query.period) //get filter period
	console.log("Cutting period: ", period)
	const spreed_id = "15GTI2RsLFbTmgN016DIT5k0jvkzvDzP7VgCFhw4JzHQ" //google spreed id
	const url = "https://spreadsheets.google.com/feeds/list/" + spreed_id + "/od6/public/values?alt=json"
	var response_data = []
	await axios.get(url).then(response => {
		const cutData = functionHandleCutData(period, response.data.feed.entry)
		const formatedData = functionHandleFormatData(cutData)
		response_data.push(formatedData)
		res.json({
			"message":"success",
			"data": formatedData
		})
	}).catch(err => {
		res.json({
			"message": "fail",
			"error": err
		})
	})
	res.end()
})

module.exports = router;


