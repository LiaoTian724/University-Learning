// A simple HTTP server
import http from 'http';
let server = http.createServer(function (req, res) {
  const now = (new Date()).toLocaleTimeString();
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write(`At ${now}, I made this response for the url "${req.url}"`);
  res.end();
});

server.on('request', (req, resp)=>{
  console.log(`[request] for ${req.url}`);
});

server.on('connection', (sock)=>{
  console.log(`[connection] from ${sock.remoteAddress}:${sock.remotePort}`);  
});

server.on('close', ()=>{
    console.log('[close]');  
});
  
server.listen(8080, ()=>{
  console.log("An HTTP server is running at port 8080. Press Ctrl-C to shut down");    
});

process.on('SIGINT', function() {
  // close the HTTP server
  server.close();
  // shut down the process after 2s
  setTimeout(() => { process.exit() }, 2000);
});