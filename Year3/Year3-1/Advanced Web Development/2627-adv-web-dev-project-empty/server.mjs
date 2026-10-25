import { fileURLToPath } from "url";
import { dirname } from "path";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

import express from "express";
let app = express();

import morgan from "morgan";
app.use(morgan("tiny"));

import api from "./api.mjs";
app.use("/api", api);

app.use(express.static(__dirname + "/dist"));

const port = 8000;
app.listen(port, () => {
  console.log(`This server presents a Web API at http://localhost:${port}/api`);
  console.log("It also serves static files at ./dist.");
  console.log("Before you run this server, \"npm run build\" to build the sample web app.");
  console.log(`Next, point your browser to http://localhost:${port}/`);
});