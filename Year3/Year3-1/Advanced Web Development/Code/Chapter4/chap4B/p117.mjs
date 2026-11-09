// p117.mjs - concatenate two files
import fs from 'fs';

fs.readFile('p115.mjs', 'utf8', (err, file1Data) => {
  if (err) throw err;
  fs.readFile('p116-mistake.mjs', 'utf8', (err, file2Data) => {
    if (err) throw err;
    fs.writeFile('combined.txt', file1Data + file2Data, 'utf8', (err) => {
      if (err) throw err;
    });
  });
});
