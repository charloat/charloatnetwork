#!/usr/bin/env python3
"""CHAR SOCIETY LINUX NETWORK SECURITY - defensive network toolkit."""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

USE_COLOR = sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"

class UI:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GREY = "\033[90m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def paint(cls, value, *styles):
        if not USE_COLOR:
            return value
        return "".join(styles) + value + cls.RESET

KALI_DRAGON = r"""
                 .ood０
              .ood8888
            .ood8888888
           d88888888888
          8888888888888
          888888888888
          `Y8888888P'
            `Y888P'
               ||
          .----||----.
         /  CHAR SOC  \\
        /______________\\
"""

def clear_screen():
    if sys.stdout.isatty():
        os.system("clear")

def splash():
    clear_screen()
    print(UI.paint(KALI_DRAGON, UI.CYAN, UI.BOLD))
    print(UI.paint("       K A L I   L I N U X", UI.WHITE, UI.BOLD))
    print(UI.paint("  CHAR SOCIETY | LINUX NETWORK SECURITY", UI.CYAN, UI.BOLD))
    print(UI.paint("  Defensive Network Toolkit  •  Version 1.2", UI.GREY))
    print(UI.paint("  " + "━" * fifty(), UI.BLUE))
    print(UI.paint("  [SYSTEM]", UI.GREEN, UI.BOLD) + " CLI interface initialized")
    print(UI.paint("  [ENGINE]", UI.GREEN, UI.BOLD) + (" Nmap available" if shutil.which("nmap") else " Nmap not found — install with: sudo apt install nmap"))
    print(UI.paint("  [MODE]  ", UI.GREEN, UI.BOLD) + " Authorized network diagnostics")
    print()

def fifty():
    return 54

def panel(title, rows):
    width = 62
    print(UI.paint("  ╭" + "─" * (width - 2) + "╮", UI.CYAN))
    print(UI.paint("  │ " + title.center(width - 4) + " │", UI.CYAN, UI.BOLD))
    print(UI.paint("  ├" + "─" * (width - 2) + "┤", UI.CYAN))
    for key, label in rows:
        line = f"  {key:<5} {label}"
        print(UI.paint("  │", UI.CYAN) + f" {line:<{width-4}} " + UI.paint("│", UI.CYAN))
    print(UI.paint("  ╰" + "─" * (width - 2) + "╯", UI.CYAN))

def run(cmd, timeout=180):
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        if p.stdout:
            print(p.stdout)
        if p.stderr:
            print(p.stderr, file=sys.stderr)
        if p.returncode:
            print(f"[!] Perintah selesai dengan kode {p.returncode}")
    except FileNotFoundError:
        print(f"[!] Program tidak ditemukan: {cmd[0]}")
    except subprocess.TimeoutExpired:
        print("[!] Waktu proses habis.")

def require_nmap():
    if not shutil.which("nmap"):
        print("[!] Nmap belum terpasang. Jalankan: sudo apt install nmap")
        return False
    return True

def network_info():
    print("\n[+] Informasi interface dan route")
    run(["ip", "-brief", "addr"])
    run(["ip", "route"])

def arp_table():
    print("\n[+] Cache ARP lokal (perangkat yang pernah terlihat)")
    path = Path("/proc/net/arp")
    if not path.exists():
        print("File ARP tidak tersedia.")
        return
    for line in path.read_text(errors="replace").splitlines():
        print(line)

def discover():
    if not require_nmap():
        return
    cidr = input("Masukkan subnet milik sendiri (contoh 192.168.1.0/24): ").strip()
    if not cidr or any(c in cidr for c in ";&|`$><"):
        print("[!] Input subnet tidak valid.")
        return
    if input(f"Konfirmasi scan discovery pada {cidr} (y/N): ").strip().lower() != "y":
        print("Dibatalkan.")
        return
    print("\n[+] Host discovery saja; tidak melakukan eksploitasi.")
    run(["nmap", "-sn", "-n", cidr], timeout=300)

def port_audit():
    if not require_nmap():
        return
    target = input("IP/hostname aset milik sendiri atau yang diizinkan: ").strip()
    if not target or any(c in target for c in " /;&|`$><"):
        print("[!] Target tidak valid.")
        return
    if input(f"Audit layanan pada {target}? (y/N): ").strip().lower() != "y":
        print("Dibatalkan.")
        return
    print("\n[+] Audit TCP top 100 ports, deteksi versi layanan.")
    run(["nmap", "-sV", "--top-ports", "100", "-T3", target], timeout=300)

def traffic_monitor():
    print("\n[+] Monitor byte RX/TX per interface. Ctrl+C untuk berhenti.")
    path = Path("/proc/net/dev")
    previous = {}
    try:
        while True:
            rows = path.read_text().splitlines()[2:]
            current = {}
            for row in rows:
                if ":" not in row:
                    continue
                name, data = row.split(":", 1)
                vals = data.split()
                if len(vals) >= 9:
                    current[name.strip()] = (int(vals[0]), int(vals[8]))
            print("\n" + time.strftime("%H:%M:%S"))
            for name, (rx, tx) in current.items():
                if name in previous:
                    drx = max(0, rx - previous[name][0])
                    dtx = max(0, tx - previous[name][1])
                    print(f"{name:12} RX {drx:>12} B/s?  TX {dtx:>12} B/s? (delta/2 detik)")
                else:
                    print(f"{name:12} mengumpulkan data...")
            previous = current
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nMonitor dihentikan.")

def local_connections():
    print("\n[+] Socket/koneksi lokal (ss)")
    if shutil.which("ss"):
        run(["ss", "-tunap"])
    else:
        print("Perintah ss tidak tersedia. Install iproute2.")

def safe_load_test():
    print("\n[+] Uji beban HTTP lokal untuk aplikasi milik sendiri.")
    print("    Hanya menerima alamat loopback (127.0.0.1 / localhost / ::1).")
    host = input("Host [127.0.0.1]: ").strip() or "127.0.0.1"
    if host not in ("127.0.0.1", "localhost", "::1"):
        print("[!] Ditolak: modul ini hanya berjalan ke loopback.")
        return
    try:
        port = int(input("Port aplikasi lokal: ").strip())
        count = int(input("Jumlah request (1-100): ").strip())
        if not (1 <= port <= 65535 and 1 <= count <= 100):
            raise ValueError
    except ValueError:
        print("[!] Port atau jumlah request tidak valid.")
        return
    if input(f"Kirim maksimal {count} request ke http://{host}:{port}/ ? (y/N): ").strip().lower() != "y":
        print("Dibatalkan.")
        return
    from modules.local_load_test import run_test
    run_test(host, port, count)

def menu():
    options = [
        ("[01]", "Informasi jaringan lokal"),
        ("[02]", "Lihat cache ARP / perangkat yang pernah terlihat"),
        ("[03]", "Device discovery - subnet milik sendiri"),
        ("[04]", "Port & service audit - target berizin"),
        ("[05]", "Network traffic monitor"),
        ("[06]", "Lihat koneksi dan socket lokal"),
        ("[07]", "Localhost HTTP load test - maksimal 100 request"),
        ("[08]", "Nmap Pro - 7 profil pemindaian praktis"),
    ]
    while True:
        splash()
        panel("MAIN MENU  |  NETWORK OPERATIONS", options)
        print("  " + UI.paint("[00]", UI.RED, UI.BOLD) + " Exit")
        print()
        choice = input(UI.paint("  CHAR-SOCIETY", UI.CYAN, UI.BOLD) + UI.paint("  ❯ ", UI.WHITE, UI.BOLD)).strip()
        actions = {"1": network_info, "2": arp_table, "3": discover, "4": port_audit, "5": traffic_monitor, "6": local_connections, "7": safe_load_test}
        if choice in actions:
            actions[choice]()
        elif choice == "8":
            from modules.nmap_pro import menu as nmap_menu
            nmap_menu()
        elif choice in ("0", "00"):
            clear_screen()
            print(UI.paint("\n  CHAR SOCIETY — SESSION CLOSED", UI.CYAN, UI.BOLD))
            print(UI.paint("  Stay curious. Secure your network.", UI.GREY))
            break
        else:
            print(UI.paint("  [!] Pilihan tidak dikenal.", UI.YELLOW))
        input("\n  Tekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    menu()
