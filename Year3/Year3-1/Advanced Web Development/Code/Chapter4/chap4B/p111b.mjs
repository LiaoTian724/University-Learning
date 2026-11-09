import dns from 'dns';

dns.resolve("not-exist.ipm.edu.mo", (err, records) => {
  if (err) {
    console.error(err); return;
  }
  console.log(records);
});
