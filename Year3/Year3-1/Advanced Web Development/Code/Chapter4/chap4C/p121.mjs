import fs from 'fs';

fs.promises.readFile('mpu-intro.txt', 'utf8').then((data) => {
  console.log("Finish reading.");
}).catch((err) => {
  throw err;
});