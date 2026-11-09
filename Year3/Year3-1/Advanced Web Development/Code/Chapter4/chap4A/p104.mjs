import si from 'systeminformation';

si.cpu()
  .then((data) => console.log(data));
