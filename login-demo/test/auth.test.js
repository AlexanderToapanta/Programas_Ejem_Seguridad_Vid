// tests/auth.test.js
import { test } from "node:test";
import assert from "node:assert/strict";
import express from "express";

process.env.MODO = "seguro";
const { login } = await import("../src/auth.seguro.js");

const app = express();
app.use(express.json());
app.post("/login", login);
const server = app.listen(0);
const port = server.address().port;

const post = (body) =>
  fetch(`http://localhost:${port}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

test("bloquea tras 5 intentos fallidos (429)", async () => {
  const email = "juan@uni.edu.ec";
  for (let i = 0; i < 5; i++) {
    const r = await post({ email, password: "mala" });
    assert.equal(r.status, 401);
  }
  const r = await post({ email, password: "mala" });
  assert.equal(r.status, 429);
  server.close();
});

test("permite login correcto en el primer intento (200)", async () => {
  const r = await post({ email: "ana@uni.edu.ec", password: "Sol-2024" });
  assert.equal(r.status, 200);
  const data = await r.json();
  assert.ok(data.token);
});