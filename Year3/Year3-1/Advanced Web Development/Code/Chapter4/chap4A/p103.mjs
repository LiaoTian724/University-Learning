// p103.mjs
// show basic info about CPU and memory
import os from 'os';

let cpus = os.cpus();
console.log(cpus);

console.log(`CPU: ${cpus[0].model}, ${cpus.length} core`);
console.log(`Total memory: ${os.totalmem() / 1024 ** 3}G`);
