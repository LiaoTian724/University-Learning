import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const db = await open({filename: "./my-northwind.sqlite", driver: sqlite3.Database});

// your work here
