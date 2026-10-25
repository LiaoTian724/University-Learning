import sqlite3 from "sqlite3";
import { open } from "sqlite";

const db = await open({
  filename: "./db.sqlite",
  driver: sqlite3.Database
});

import express from "express";
let api = express.Router();

/* your API endpoints here */

export default api;
