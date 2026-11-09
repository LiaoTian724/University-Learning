function tossDice() {
  const timeTaken = 2000;
  const tossFailed = Math.random() < 0.1;
  const tossResult = Math.floor(Math.random() * 6) + 1;
  let promise = new Promise((resolve, reject) => {
    setTimeout(() => {
      if (tossFailed) {
        reject("toss fails");
      } else {
        resolve(tossResult);
      }
    }, timeTaken)
  });
  return promise;
}

// 1. Create a promise to get a toss result
tossDice().then(
  (result) => {console.log(`The result is ${result}`);},
  (err) => {console.log(err);}
);

// 2. Create a Promise Chain to toss the dice 3 times and log the result of each toss. If any toss fails, log the error message and stop tossing.
tossDice().then(
  (result) => {
      console.log(`The result is ${result}`);
      return tossDice();
  }
).then(
  (result) => {
      console.log(`The result is ${result}`);
      return tossDice();
  }
).then(
  (result) => {
      console.log(`The result is ${result}`);
  }
).catch(
  (err) => {
    console.log(err);
  }
)

// 3. Create an asynchronous function that uses await to toss the dice 3 times and log the result of each toss. If any toss fails, log the error message and stop tossing.
async function tossDiceTreeTimes() {
  try{
      let result1 = await tossDice();
      console.log(`The result is ${result1}`);
      let result2 = await tossDice();
      console.log(`The result is ${result2}`);
      let result3 = await tossDice();
      console.log(`The result is ${result3}`);
  } catch {
      console.log("ERROR!")
  }
}
tossDiceTreeTimes();