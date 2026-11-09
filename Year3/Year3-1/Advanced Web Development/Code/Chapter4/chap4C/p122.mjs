import fs from 'fs';

fs.promises.readFile('mpu-intro.txt', 'utf8').then((data) => {
  console.log("Finish reading.");
  return fs.promises.writeFile('copy-mpu-intro.txt', data, 'utf8');
}).then(() => {
    console.log("Finish copying.");
  }).catch((err) => {
  throw err;
});