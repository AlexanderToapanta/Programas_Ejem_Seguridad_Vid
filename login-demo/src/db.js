
import crypto from "node:crypto";

export const hash = (pwd) =>
  crypto.createHash("sha256").update(pwd).digest("hex");


export const usuarios = [
  { id: 1, email: "ana@uni.edu.ec",   rol: "estudiante", hash: hash("Sol-2024") },
  { id: 2, email: "juan@uni.edu.ec",  rol: "estudiante", hash: hash("Luna-2024") },
  { id: 3, email: "admin@uni.edu.ec", rol: "admin",      hash: hash("Clave-Admin-2024") },
];


export const notas = {
  1: [{ materia: "Seguridad de Software", nota: 8.5 }],
  2: [{ materia: "Seguridad de Software", nota: 7.2 }],
  3: [{ materia: "Administración", nota: 10 }],
};