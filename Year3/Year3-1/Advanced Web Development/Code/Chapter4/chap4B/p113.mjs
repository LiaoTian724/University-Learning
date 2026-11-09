import fs from 'fs';

fs.readFile('./prime.txt', 'utf8', (err, data) => {
  if (err) throw err;
  let primes = data.split(',');
  console.log(`${primes.length} prime numbers found.`);
  console.log(`The last 5 are ${primes.slice(-5)}`);
});

console.log('Reading prime.txt asynchronously...');