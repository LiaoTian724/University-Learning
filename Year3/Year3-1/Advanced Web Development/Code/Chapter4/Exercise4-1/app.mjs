import fs from 'fs';
import dns from 'dns';

fs.readFile('./input.txt', 'utf8', (err, data) => {
    if (err) throw err;
    console.log('Domain:', data);

    dns.resolve(data, (err, addresses) => {
        if (err) throw err;
        console.log('Resolved IP addresses:', addresses);

        fs.writeFile('./output.txt', addresses.toString(), 'utf8', (err) => {
            if (err) throw err;
            console.log('First IP address saved to output.txt');
        });
    });
});