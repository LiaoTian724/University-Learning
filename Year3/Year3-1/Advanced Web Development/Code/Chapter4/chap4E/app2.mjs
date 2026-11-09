// app1.js
// simple routes
import express from 'express';
let app = express();

app.get('/', (req, res) => {
	res.send(`<!DOCTYPE html>
    <html><body>Menu: <ul>
    <li><a href="/hello">Path /hello</a>
    <li><a href="/lecture/comp312">Path /lecture/comp312</a>
    <li><a href="/lecture/comp311">Path /lecture/comp311</a>
    <li><a href="/lecture/no-such-code">Path /lecture/no-such-code</a>
    <li><a href="/notfound">Path /notfound</a>
    </ul></body></html>`);
});

app.get('/hello', (req, res) => {
	res.send('hello world!');
});

// retrieve the lecture time
app.get('/lecture/:code', (req, res) => {
  // in a real app, we'd query a database ...
  if (req.params.code === 'comp312') {
    res.send('comp312 Tue, Thu: 10:00-11:30am');
  } else if (req.params.code === 'comp311') {
	  res.send('comp311 Mon, Fri: 11:30-01:00pm');
  } else {
	  res.status(404).send('Lecture not found');
  }
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
