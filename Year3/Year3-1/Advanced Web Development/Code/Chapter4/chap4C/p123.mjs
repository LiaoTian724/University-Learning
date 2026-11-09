import { readFile, writeFile } from 'fs/promises';

readFile('mpu-intro.txt', 'utf8').then((data) => {
  // data contains content of the input file
  return writeFile('copy-mpu-intro.txt', data, 'utf8')
}).then(() => {
  console.log("Finish copying");
});



readFile('xxx.txt', 'utf8').then((data)=>{
  return writeFile('yyy.txt', data, 'utf8')
}).then(()=>{
  console.log("FINISH")
});