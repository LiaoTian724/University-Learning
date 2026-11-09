import express from 'express';
const app = express();

// a route in the app, which handles GET requests for the path '/'
app.get('/', (req, res) => {
  res.send('hello world');
});

// more routes ...

app.listen(3000);
