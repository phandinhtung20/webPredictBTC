var express = require('express'),
	request = require('request'),
	childProcess= require("child_process"),
	app = express(),
	trainModel = require('./processPython/trainModel.js'),
	updateData = require('./processPython/updateData.js'),
	fs = require("fs");

var port = process.env.PORT || 3000;
app.listen(port, function() {
	console.log('Server start on port: ' + port);
});
app.set('view engine','ejs')
app.set('views','./views')

app.get('/', function(req, res){
	fs.readFile('./python/predict.json', 'utf8', function (err, data) {
		if (err) throw err;
		var lines = data.split('\r\n')
		var predict = lines[0].split(',')
		var realData = lines[1].split(',')

		var all = realData.slice(5, 7).concat(predict)
		var max = Math.max(...all)
		var min = Math.min(...all)

		for (let i = 0; i < predict.length; i++) {
			// predict[i] = parseInt(predict[i]);
			// realData[i] = parseInt(realData[i]);
		}

		res.render('home', {predict: predict, realData: realData, max: max, min: min})
	});
});

var timeRepeat = 0;
setInterval(function() {
	timeRepeat++;

	if (timeRepeat == 96) {
		timeRepeat = 0;
		trainModel();
	}

	updateData();
}, 1000 * 15 * 60);