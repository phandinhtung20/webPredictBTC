'use strict'

var request = require('request'),
	childProcess= require("child_process");

const updateData = () => {
	request({
			url: 'https://api.coinmarketcap.com/v2/ticker/1/',
			method: 'GET'
		}, function (error, response, body){
		if(!error && response.statusCode == 200){
			var data = JSON.parse(body)
			console.log(data.data.quotes.USD.price);

			var spawn = childProcess.spawn;
			var processPython = spawn('python', ["./python/appendAndPredict.py", data.data.quotes.USD.price] );
			processPython.stdout.on('data', function(data) {
				console.log(data.toString())
		    })
		}
	});
}

module.exports = updateData;
