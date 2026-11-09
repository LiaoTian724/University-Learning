import { readFile, writeFile } from 'fs/promises';

try {
  let data = await readFile('mpu-intro.txt', 'utf8');
  await writeFile('copy-mpu-intro.txt', data, 'utf8');
  console.log("Finish copying");
} catch (err) {
  console.error("promise catch " + err);
}