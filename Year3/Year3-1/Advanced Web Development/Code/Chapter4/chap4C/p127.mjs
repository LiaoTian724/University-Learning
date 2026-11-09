import { readFile, writeFile } from 'fs/promises';

async function copyFile(sourceFileName) {
  let data = await readFile(sourceFileName, 'utf8');
  await writeFile('copy-' + sourceFileName, data, 'utf8');
}

copyFile('mpu-intro.txt').then(() => {
  console.log("Finish copying");
}).catch((err) => {
  console.error("promise catch " + err);
});
