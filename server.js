'use strict';

var express = require('express');
var app = express();
var server = require('http').createServer(app);  
var io = require('socket.io')(server);

var exec = require('child_process').exec;

// Constants
var PORT = 8080;

// App
app.use('/',express.static(__dirname + '/public'));

server.listen(PORT);
console.log('Server: Running on http://localhost:' + PORT);

io.on('connection', function(client) {  
    console.log('Server: Client connected...');

    client.on('join', function(data) {
        console.log("Server: Client joined with -> " + data);
		
    });
	
	client.on('imageUpdated', function(data){
		streamImageWait(client);
	});

	streamImageWait(client);
});

function streamImageWait(client){
	
	var imageCount  = 0;
	
	
	exec('find ./public/stream/ -type f | wc -l',(error, stdout,stderr) => {
		if (error) {
			console.error('exec error: ${error}');
			return;
		}
	  
		if(parseInt(stdout) > 0){
			imageCount = parseInt(stdout);
			
			if(imageCount > 10){
				exec('rm -r ./public/stream/*');
				imageCount = 0;
			}
			console.log("Count", imageCount);
		}
		
		var command = "./imageCapture "+ imageCount.toString();

		exec(command,(error, stdout,stderr) => {
			if (error) {
				console.error('exec error: ${error}');
				return;
			}
			client.emit("image",stdout);
		});
	});
	
	//shell.stdout.on('data', function(data){
	//	client.emit("image",data);
	//	console.log("Server: Image captured.");
	//});
}