BASE="http://127.0.0.1:8000"
TOKEN_ANA="token-ficticio-ana"

echo "======================================================"
echo " PRUEBA 1: Ana consulta SU PROPIA reserva (1001)"
echo "======================================================"
curl -s -o /dev/null -w "Vulnerable -> HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOKEN_ANA" \
  "$BASE/api/reservas/vulnerable/1001"
curl -s -o /dev/null -w "Corregido  -> HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOKEN_ANA" \
  "$BASE/api/reservas/1001"
echo

echo "======================================================"
echo " PRUEBA 2 (ATAQUE): Ana intenta la reserva de Carlos (1002)"
echo "======================================================"
curl -s -o /dev/null -w "Vulnerable -> HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOKEN_ANA" \
  "$BASE/api/reservas/vulnerable/1002"
curl -s -o /dev/null -w "Corregido  -> HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOKEN_ANA" \
  "$BASE/api/reservas/1002"
echo

echo "======================================================"
echo " PRUEBA 3: Reserva inexistente (9999)"
echo "======================================================"
curl -s -o /dev/null -w "Corregido  -> HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOKEN_ANA" \
  "$BASE/api/reservas/9999"
echo

echo "======================================================"
echo " REVISAR LOG DETECTIVO:"
echo "======================================================"
cat logs/accesos.log 2>/dev/null || echo "(sin log aún)"