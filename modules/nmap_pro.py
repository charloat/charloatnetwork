"""Practical Nmap profiles. Use only on systems/networks you own or are authorized to test."""
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "reports"

def valid_target(value):
    if not value or len(value) > 253:
        return False
    if re.search(r"[^A-Za-z0-9_.:/-]", value):
        return False
    if value.startswith("-") or ".." in value:
        return False
    return True

def run_profile(label, target, args, timeout=900):
    if not shutil.which("nmap"):
        print("[!] Nmap belum terpasang. Jalankan: sudo apt install nmap")
        return
    if not valid_target(target):
        print("[!] Target tidak valid.")
        return
    OUTPUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_label = re.sub(r"[^a-z0-9_-]", "_", label.lower())
    output_file = OUTPUT_DIR / f"{stamp}_{safe_label}.txt"
    cmd = ["nmap", *args, "-oN", str(output_file), target]
    print(f"\n[+] Profil: {label}")
    print(f"[+] Target: {target}")
    print(f"[+] Output: {output_file}")
    print("[+] Menjalankan Nmap...")
    try:
        proc = subprocess.run(cmd, text=True, timeout=timeout)
        if proc.returncode == 0:
            print(f"\n[✓] Scan selesai. Laporan: {output_file}")
        else:
            print(f"\n[!] Nmap keluar dengan kode {proc.returncode}.")
            print(f"[i] Periksa laporan jika sudah dibuat: {output_file}")
    except subprocess.TimeoutExpired:
        print("[!] Scan melewati batas waktu. Hentikan proses dan periksa jaringan/target.")
    except KeyboardInterrupt:
        print("\n[!] Scan dihentikan pengguna.")

def menu():
    while True:
        print("\033[96m" + "  ╭" + "─" * 58 + "╮")
        print("  │" + " CHAR SOCIETY  /  NMAP PRO".center(58) + "│")
        print("  ├" + "─" * 58 + "┤")
        print("  │ [1] Host discovery       Cari host aktif (-sn)          │")
        print("  │ [2] Quick scan           100 port paling umum           │")
        print("  │ [3] Common ports         1.000 port paling umum         │")
        print("  │ [4] Service detection    Versi layanan                  │")
        print("  │ [5] Full TCP ports       Semua port TCP (-p-)           │")
        print("  │ [6] OS detection         Perkiraan sistem operasi       │")
        print("  │ [7] UDP top 20           UDP umum (lebih lama)          │")
        print("  │ [0] Kembali ke menu utama                               │")
        print("  ╰" + "─" * 58 + "╯\033[0m")
        choice = input("NMAP-PRO> ").strip()
        if choice == "0":
            return
        profiles = {
            "1": ("host_discovery", ["-sn", "-n"], 300),
            "2": ("quick_scan", ["-T3", "--top-ports", "100", "-n"], 600),
            "3": ("common_ports", ["-T3", "--top-ports", "1000", "-n"], 900),
            "4": ("service_detection", ["-sV", "-T3", "--top-ports", "1000", "-n"], 1200),
            "5": ("full_tcp_ports", ["-sS", "-T3", "-p-", "-n"], 1800),
            "6": ("os_detection", ["-O", "-T3", "--top-ports", "1000", "-n"], 1200),
            "7": ("udp_top20", ["-sU", "-T3", "--top-ports", "20", "-n"], 1800),
        }
        if choice not in profiles:
            print("[!] Pilihan tidak dikenal.")
            continue
        label, args, timeout = profiles[choice]
        if choice == "7":
            print("[!] UDP scan bisa memakan waktu lama dan memerlukan hak akses raw socket.")
        if choice in ("5", "6", "7"):
            print("[!] Profil ini lebih intensif daripada quick scan.")
        target = input("Target IP/hostname/subnet yang Anda miliki/diizinkan: ").strip()
        if not valid_target(target):
            print("[!] Format target tidak valid.")
            continue
        print(f"\nPerintah yang akan dijalankan: nmap {' '.join(args)} {target}")
        confirm = input("Lanjutkan hanya jika Anda punya izin? (y/N): ").strip().lower()
        if confirm == "y":
            run_profile(label, target, args, timeout)
        else:
            print("Dibatalkan.")
        input("\nTekan Enter untuk kembali ke menu Nmap...")
