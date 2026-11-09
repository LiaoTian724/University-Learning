// p143.mjs
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const db = await open({
  filename: './my-northwind.sqlite',
  driver: sqlite3.Database
});

async function getOrderAmount(orderId) {
  // Note: the unitPrice in OrderDetail does not match those in Product
  const queryOrderAmount =
    `SELECT SUM(UnitPrice*Quantity) as amount 
    FROM OrderDetail
    WHERE OrderId = $orderId`;
  const result = await db.get(queryOrderAmount,
    { $orderId: orderId });
  return result.amount;
}

async function getXmasOrders() {
  const queryOrders =
    `SELECT Id as id, OrderDate as orDate
    FROM 'Order'
    WHERE orDate BETWEEN $startDate AND $endDate`;
  const xmasOrders = await db.all(queryOrders, {
    $startDate: "2012-12-01",
    $endDate: "2012-12-31"
  });
  for (let ord of xmasOrders) {
    ord.amount = await getOrderAmount(ord.id);
  }
  return xmasOrders;
}

const xmasOrders = await getXmasOrders();
console.table(xmasOrders);

await db.close();