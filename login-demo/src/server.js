
import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { login, misNotas, auditLog } from "./auth.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "..", "public")));

app.post("/login", login);
app.get("/notas", misNotas);
app.get("/audit", (_req, res) => res.json(auditLog.slice(-20)));

const PORT = process.env.PORT ?? 3000;
app.listen(PORT, () => {
  const modo = process.env.MODO === "seguro" ? "SEGURO (con control)" : "INSEGURO (sin control)";
  console.log(`Servidor en http://localhost:${PORT} — modo: ${modo}`);
});