#!/usr/bin/env bash
# Avvia server.js e controlla con curl i 7 esiti richiesti. Uso: bash test/curl.sh
cd "$(dirname "$0")/.." || exit 1
node server.js > /dev/null 2>&1 &
PID=$!
trap 'kill $PID' EXIT
sleep 0.5
U=http://127.0.0.1:3000
ok=0; ko=0

controlla() { # descrizione, atteso, ottenuto
    if [ "$2" = "$3" ]; then echo "OK   $1 -> $3"; ok=$((ok+1));
    else echo "FAIL $1 -> atteso $2, ottenuto $3"; ko=$((ko+1)); fi
}
stato() { curl -s -o /dev/null -w '%{http_code}' "$@"; }

controlla "login giusto (mario/Rossi2026)" 200 "$(stato -d 'nome=mario&pass=Rossi2026' $U/login)"
controlla "password errata"                401 "$(stato -d 'nome=mario&pass=sbagliata' $U/login)"
controlla "campi vuoti"                    400 "$(stato -d 'nome=&pass=' $U/login)"
controlla "campi mancanti"                 400 "$(stato -d '' -X POST $U/login)"
controlla "username di 31 caratteri"       400 "$(stato -d "nome=$(printf 'a%.0s' {1..31})&pass=x" $U/login)"
controlla "GET su /login"                  405 "$(stato $U/login)"
controlla "URL inesistente"                404 "$(stato $U/nonesiste)"
controlla "body troppo grande (5000 byte)" 413 "$(stato -d "nome=$(head -c 5000 /dev/zero | tr '\0' a)&pass=x" $U/login)"
controlla "GET / (index.html)"             200 "$(stato $U/)"
controlla "GET /stile.css"                 200 "$(stato $U/stile.css)"
controlla "POST su /"                      405 "$(stato -d 'x=1' $U/)"

xss=$(curl -s --data-urlencode 'nome=<script>alert(1)</script>' -d 'pass=x' $U/login | grep 'name="nome"')
echo "     username con <script> ->$xss"
case "$xss" in *'&lt;script&gt;alert(1)&lt;/script&gt;'*) controlla "<script> escapato" si si;; *) controlla "<script> escapato" si no;; esac
case "$(curl -s -d 'nome=mario&pass=sbagliata' $U/login)" in *'Username o password errati.'*) controlla "messaggio 401 unico" si si;; *) controlla "messaggio 401 unico" si no;; esac
case "$(curl -s -d 'nome=mario&pass=sbagliata' $U/login | grep 'name="pass"')" in *value=*) controlla "password ripresentata vuota" si no;; *) controlla "password ripresentata vuota" si si;; esac
controlla "Content-Type con charset" "text/html; charset=utf-8" "$(curl -s -o /dev/null -w '%{content_type}' -d 'nome=mario&pass=Rossi2026' $U/login)"

echo "---- $ok ok, $ko falliti"
[ $ko -eq 0 ]
