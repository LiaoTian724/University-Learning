import { promises } from 'dns';
const resolver = new promises.Resolver();

const govHost = "www.gov.mo";
resolver.resolve(govHost).then((records) => {
  // succeed 
  console.log(`${govHost} resolves to ${records}`);
}).catch((err) => {
  // fail 
  console.log(`Resolve fails with ${err}`);
});