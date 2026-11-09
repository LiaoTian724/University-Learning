import { readFile, writeFile } from 'fs/promises';

async function copyFile(sourceFileName) {
  try {
    let data = await readFile(sourceFileName, 'utf8');
    await writeFile('copy-' + sourceFileName, data, 'utf8');
    console.log("Finish copying");
  } catch (err) {
    console.error("promise catch " + err);
  }
}

copyFile('mpu-intro.txt');