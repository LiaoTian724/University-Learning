// p116.mjs - file copy, with mistake in ordering the file read and write
import fs from 'fs';

let fileContent = '';

fs.readFile('mpu-intro.txt', 'utf8', (err, data) => {
  if (err) throw err;
  // copy the file content to the global variable
  fileContent = data;
});

// Mistake!
// at this moment, file read is not done yet
// fileContent is still undefined

fs.writeFile('copy-mpu-intro.txt', fileContent, 'utf8', (err) => {
  if (err) throw err;
});
