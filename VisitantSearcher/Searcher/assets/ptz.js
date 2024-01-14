/*
Use: node ptz.js <ip>  <UP|DWON|LEFT|RIGHT>

.. and yes it is DWON not DOWN :)

*/

var net = require('net');

var client = new net.Socket();
var IPAddress = process.argv[2]
var command = process.argv[3]
client.setTimeout(3200);
client.on('timeout', ()=>client.emit('error', new Error('ETIMEDOUT')) );
client.on('error', (e) => retry(e.message));
//find a way to have a timeout and a re-try
client.connect(554,IPAddress, function() {
	console.log('move: '+IPAddress+' to:'+process.argv[3]);
	client.write("SET_PARAMETER rtsp://"+IPAddress+"/onvif1 RTSP/1.0\r\n"+
								"Content-type: ptzCmd: "+command+"\r\n"+
								"CSeq: 2\r\n"+
								"Session:\r\n\r\n");
	console.log('writen');

});

client.on('data', function(data) {
	console.log('Received: ' + data);

	client.destroy(); // kill client after server's response
});

client.on('close', function() {
	console.log('Connection closed');
});
function retry(ErrorMessage){
	console.log((new Date()).toISOString(), 'Error on ptz.js', ErrorMessage);
	

};