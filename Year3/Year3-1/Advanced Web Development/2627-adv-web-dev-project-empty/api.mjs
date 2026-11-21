import sqlite3 from "sqlite3";
import { open } from "sqlite";

const db = await open({
    filename: "./db.sqlite",
    driver: sqlite3.Database
});

import express from "express";
let api = express.Router();


/* your API endpoints here */
api.get("/records", async (req, res) => {
    try {
        const result = await db.all("SELECT * FROM Record ORDER BY id");
        res.status(200).json(result);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Failed to load records" });
    }
});



api.post("/records", async(req, res) => {
    const body = req.body || {};
    const name = body.name;
    const age = body.age;
    const record_1 = body.record_1;
    const record_2 = body.record_2;
    const record_3 = body.record_3;

    if (typeof name !== 'string' || name.trim() === "" || !Number.isInteger(age) || age < 1 ||
        !Number.isInteger(record_1) || record_1 < 0 ||
        !Number.isInteger(record_2) || record_2 < 0 ||
        !Number.isInteger(record_3) || record_3 < 0) {
            return res.status(400).json({error:"Invalid participant data" })
        }
    try {
        const result = await db.run(
            "INSERT INTO Record (name, age, record_1, record_2, record_3) VALUES (?, ?, ?, ?, ?)",
            [name.trim(), age, record_1, record_2, record_3]
        );
        const newRecord = await db.get("SELECT * FROM Record WHERE id = ?", [result.lastID]);
        res.status(201).json(newRecord);    // JavaScript 转成 JSON
    } catch (error) {
        console.error(error);
        res.status(500).json({error: "Failed to add record"});
    }
});



api.delete("/records/:id", async(req, res) => {
    const id = Number(req.params.id);

    if (!Number.isInteger(id) || id < 1) {
        return res.status(400).json({error: "Invalid record ID"});
    }
    try {
        const result = await db.run("DELETE FROM Record WHERE id = ?", [id]);
        if (result.changes === 0) {
            return res.status(404).json({error: "Record not found"});
        }

        res.status(204).end();
    } catch(error) {
        console.log(error);
        res.status(500).json({
            error: "Failed to delete record"
        });
    }
});
export default api;
