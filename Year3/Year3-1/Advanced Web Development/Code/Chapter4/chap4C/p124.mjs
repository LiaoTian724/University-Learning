import { readFile, writeFile } from 'fs/promises';

readFile('non-exist-mpu-intro.txt', 'utf8').then((data) => {
  writeFile('copy-mpu-intro.txt', data, 'utf8');
}).then(() => {
  console.log("Finish copying");
}).catch((err) => {
  console.error("promise catch " + err);
});