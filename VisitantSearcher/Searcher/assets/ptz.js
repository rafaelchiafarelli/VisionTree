/*
Use: node ptz.js <ip>  <UP|DWON|LEFT|RIGHT>

.. and yes it is DWON not DOWN :)

*/

var net = require('net');

var client = new net.Socket();
client.setTimeout(2000);
client.on('timeout', ()=>client.emit('error', new Error('ETIMEDOUT')) );
client.on('error', (e) => console.log((new Date()).toISOString(), 'Error', e.message));
//find a way to have a timeout and a re-try
client.connect(554,process.argv[2], function() {
	console.log('move: '+process.argv[2]+' to:'+process.argv[3]);
	client.write("SETUP rtsp://"+process.argv[2]+"/onvif1/track1 RTSP/1.0\r\n"+
								"CSeq: 1\r\n"+
								"User-Agent: LibVLC/2.2.6 (LIVE555 Streaming Media v2016.02.22)\r\n"+
								"Transport: RTP/AVP/TCP;unicast;interleaved=0-1\r\n\r\n");
});

client.on('data', function(data) {
	//console.log('Received: ' + data);
	client.write("SET_PARAMETER rtsp://"+process.argv[2]+"/onvif1 RTSP/1.0\r\n"+
								"Content-type: ptzCmd: "+process.argv[3]+"\r\n"+
								"CSeq: 2\r\n"+
								"Session:\r\n\r\n");
	client.destroy(); // kill client after server's response
});

client.on('close', function() {
	//console.log('Connection closed');
});