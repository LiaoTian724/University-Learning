// p144.mjs
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const db = await open({
  filename: './my-northwind.sqlite',
  driver: sqlite3.Database
});

const query = `SELECT * FROM OrderDetail LIMIT 5 OFFSET 1000`;
const result = await db.each(query, {}, (err, row) => {
  if (err) throw err;
  console.log(row);
});
console.log("count =", result);


const result2 = await db.all(query);
console.log("count =", result2.length);


await db.close();