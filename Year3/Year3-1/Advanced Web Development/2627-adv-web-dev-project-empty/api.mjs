import sqlite3 from "sqlite3";
import { open } from "sqlite";

const db = await open({
    filename: "./db.sqlite",
    driver: sqlite3.Database
});

import express from "express";
let api = express.Router();


/* your API endpoints here */
api.put('/records/:id', async (req, res) => {
    const id = Number(req.params.id);
    if (!Number.isInteger(id) || id < 1) {
        return res.status(400).json({error: "Invalid record ID"});
    }
    if (
        !req.body || 
        typeof req.body.name !== 'string' || req.body.name.trim() === "" || !Number.isInteger(req.body.age) || req.body.age < 1 ||
        !Number.isInteger(req.body.record_1) || req.body.record_1 < 0 ||
        !Number.isInteger(req.body.record_2) || req.body.record_2 < 0 ||
        !Number.isInteger(req.body.record_3) || req.body.record_3 < 0) {
            return res.status(400).json({error:"Invalid participant data" })
    }

    const values = [
        req.body.name.trim(),
        req.body.age,
        req.body.record_1,
        req.body.record_2,
        req.body.record_3,
        id
    ];
    const q1 = `UPDATE Record SET name = ?, age = ?, record_1 = ?, record_2 = ?, record_3 = ? WHERE id = ?`;
    try {
        const result = await db.run(q1, values);
        if (result.changes === 0) {
            return res.status(404).json({error: "Record not found"});
        }
        const updateRecord = await db.get("SELECT * FROM Record WHERE id = ?", [id]);
        res.status(200).json(updateRecord);
    } catch(error) {
        res.status(500).json({error: "Failed to update record"});
    }
});



api.get("/records", async (req, res) => {
    try {
        const result = await db.all("SELECT * FROM Record ORDER BY id");
        res.status(200).json(result);
    } catch (error) {
        res.status(500).json(error);
    }
});



api.post("/records", async(req, res) => {
    if (!req.body || typeof req.body.name !== 'string' || req.body.name.trim() === "" || !Number.isInteger(req.body.age) || req.body.age < 1 ||
        !Number.isInteger(req.body.record_1) || req.body.record_1 < 0 ||
        !Number.isInteger(req.body.record_2) || req.body.record_2 < 0 ||
        !Number.isInteger(req.body.record_3) || req.body.record_3 < 0) {
            return res.status(400).json({error:"Invalid participant data" });
    }

    const q1 = `INSERT INTO Record (name, age, record_1, record_2, record_3) VALUES (?, ?, ?, ?, ?)`;
    const values = [
        req.body.name.trim(),
        req.body.age,
        req.body.record_1,
        req.body.record_2,
        req.body.record_3
    ];
    try {
        const result = await db.run(q1, values);
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
        res.status(500).json({error: "Failed to delete record"});
    }
});

export default api;
