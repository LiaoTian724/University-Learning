import dns from 'dns';

const govHost = "www.gov.mo";

dns.resolve(govHost, (err, records) => {
  if (err) {
    console.error(err); return;
  }
  console.log(`${govHost} resolves to ${records}`);
});
