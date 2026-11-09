import fs from 'fs';

function genPrime(upLimit) {
  let primes = [2, 3, 5, 7];
  // give a label to the first for loop
  loop1:
  for (let k = 9; k < upLimit; k += 2) {
    for (let n of primes) {
      // if k is divisible by a prime in primes, continue onto k+2
      if (k % n == 0) continue loop1;
    }
    // after the above for loop, k is verified as prime
    primes.push(k);
  }
  return primes;
}

const textData = genPrime(200).toString();
fs.writeFile('./prime.txt', textData, 'utf8', (err) => {
  if (err) throw err;
  console.log('Some prime numbers are written to prime.txt');
});

console.log('Writing prime.txt asynchronously...');