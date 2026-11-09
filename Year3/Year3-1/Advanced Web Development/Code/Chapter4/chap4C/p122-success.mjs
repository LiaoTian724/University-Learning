import { promises } from 'dns';
const resolver = new promises.Resolver();

const host = "www.gov.mo";
const prom = resolver.resolve(host)
prom.then(
  (rec) => { console.log(`${host} resolves to ${rec}`) }
  ,
  (err) => { console.log(`Name server returns an error: ${err}`) }
);