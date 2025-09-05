#!/bin/bash
# Script para capturar screenshot automático da landing do DilsAI

URL="https://dilson123-tech.github.io/dilsai-landing/"
OUT="screenshot.png"
SIZE="1280,800"

echo "📸 Capturando screenshot de $URL..."
chromium --headless --disable-gpu --screenshot="$OUT" --window-size=$SIZE $URL 2>/dev/null

if [ -f "$OUT" ]; then
  echo "✅ Screenshot salvo em $OUT"
else
  echo "❌ Erro: verifique se o Chromium/Google Chrome está instalado"
fi
