// p142.mjs
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const db = await open({
  filename: './my-northwind.sqlite',
  driver: sqlite3.Database
});

const query =
  `SELECT P.id as id, P.ProductName as productName, SalesQuantity
  FROM Product as P
  JOIN (SELECT ProductId, SUM(Quantity) as SalesQuantity
        FROM OrderDetail GROUP BY ProductId)
    as D ON P.id = D.ProductId
  WHERE P.CategoryID = $categoryId
  ORDER BY SalesQuantity DESC`;

const result = await db.all(query, { $categoryId: 7 });
console.log(result);

await db.close();