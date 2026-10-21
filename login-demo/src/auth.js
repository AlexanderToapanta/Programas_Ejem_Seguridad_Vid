
import crypto from "node:crypto";
import { usuarios, hash, notas } from "./db.js";


const MAX_INTENTOS = 3;
const VENTANA_MS = 5 * 60 * 1000; 
const intentos = new Map();

const sesiones = new Map();

const crearToken = (userId) => {
  const token = crypto.randomBytes(16).toString("hex");
  sesiones.set(token, userId);
  return token;
};

export const usuarioDesdeToken = (token) => sesiones.get(token);

export const auditLog = [];
const registrarLog = (evento, email, ip) => {
  auditLog.push({ evento, email, ip, ts: new Date().toISOString() });
};

export function login(req, res) {
  const { email, password } = req.body ?? {};
  if (!email || !password) {
    return res.status(400).json({ error: "Faltan credenciales" });
  }

  const ip = req.ip ?? "desconocida";
  const clave = `login:${email}:${ip}`;
  const ahora = Date.now();


  if (process.env.MODO === "seguro") {
    const reg = intentos.get(clave);
    if (reg && ahora - reg.first < VENTANA_MS && reg.count >= MAX_INTENTOS) {
      registrarLog("login_bloqueado", email, ip);
      return res.status(429).json({ error: "Demasiados intentos. Intente más tarde." });
    }
  }

  const usuario = usuarios.find((u) => u.email === email);

  if (usuario && usuario.hash === hash(password)) {
    if (process.env.MODO === "seguro") intentos.delete(clave);
    registrarLog("login_ok", email, ip);
    return res.json({ token: crearToken(usuario.id), rol: usuario.rol });
  }


  if (process.env.MODO === "seguro") {
    const reg = intentos.get(clave);
    if (!reg || ahora - reg.first >= VENTANA_MS) {
      intentos.set(clave, { count: 1, first: ahora });
    } else {
      reg.count += 1;
    }
  }

  registrarLog("login_fallido", email, ip);
  return res.status(401).json({ error: "Credenciales inválidas" });
}

export function misNotas(req, res) {
  const token = (req.headers.authorization ?? "").replace("Bearer ", "");
  const userId = usuarioDesdeToken(token);
  if (!userId) return res.status(401).json({ error: "No autenticado" });
  return res.json({ usuario: userId, notas: notas[userId] ?? [] });
}