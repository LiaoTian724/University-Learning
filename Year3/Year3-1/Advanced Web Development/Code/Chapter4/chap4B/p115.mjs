// p115.mjs - file copy
import fs from 'fs';

fs.readFile('mpu-intro.txt', 'utf8', (err, data) => {
  if (err) throw err;
  // at this moment, file read is done
  // `data` contains content of the input file
  fs.writeFile('copy-mpu-intro.txt', data, 'utf8', (err) => {
    if (err) throw err;
  });
});
