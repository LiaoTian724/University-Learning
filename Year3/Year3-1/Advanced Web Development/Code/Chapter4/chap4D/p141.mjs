// p141.mjs
// import sqlite3 driver
import sqlite3 from 'sqlite3';
// import database open function 
import { open } from 'sqlite';

// open connection to the database file
const db = await open({
  // the database file  
  filename: './my-northwind.sqlite',
  // tell sqlite to use the standard 'sqlite3' driver
  driver: sqlite3.Database
});

const query = "SELECT * FROM Product WHERE Id = 14";
// get a single row from the result set of the query
const tofu = await db.get(query);
console.log(tofu);

// close the database connection
await db.close();