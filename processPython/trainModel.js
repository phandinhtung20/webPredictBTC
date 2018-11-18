'use strict'

var childProcess= require("child_process");

const trainModel = () => {
	var spawn = childProcess.spawn;
	var processPython = spawn('python',
			["./python/trainNewModel.py"] );
	processPython.stdout.on('data', function(data) {
		if (data.length < 20) {
			console.log("Train finish: "+data)
		}
	});
}

module.exports = trainModel;