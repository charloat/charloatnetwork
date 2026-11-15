"""Strictly loopback-only, bounded HTTP smoke/load test."""
import time
import urllib.request

def run_test(host, port, count):
    url = f"http://{host}:{port}/"
    ok = 0
    failed = 0
    started = time.time()
    for i in range(count):
        req = urllib.request.Request(url, headers={"User-Agent": "CharSociety-Local-Test/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                response.read(256)
                ok += 1
                print(f"[{i+1}/{count}] HTTP {response.status}")
        except Exception as exc:
            failed += 1
            print(f"[{i+1}/{count}] gagal: {exc}")
        time.sleep(0.1)
    elapsed = time.time() - started
    print(f"\nSelesai: sukses={ok}, gagal={failed}, durasi={elapsed:.2f}s")
