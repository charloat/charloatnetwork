#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "[+] Memasang dependensi sistem..."
sudo apt update
sudo apt install -y python3 nmap iproute2
chmod +x char_society.py
echo
echo "[✓] Instalasi selesai."
echo "Jalankan:"
echo "  cd \"$(pwd)\""
echo "  python3 char_society.py"
