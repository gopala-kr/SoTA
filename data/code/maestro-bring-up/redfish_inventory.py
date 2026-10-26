"""redfish_inventory.py — inventory nodes through their BMCs (DMTF Redfish)
and flag firmware drift before anything boots an OS.

Redfish is the standard REST API of server baseboard management
controllers: /redfish/v1/Systems, /Chassis, /UpdateService/FirmwareInventory.
Run with no arguments, it starts a small MOCK BMC (three fake nodes) in a
thread and inventories that, so the code path can be checked without
hardware. On a real cluster: python3 redfish_inventory.py bmc1 bmc2 ...
(add authentication and TLS verification for real BMCs).
"""
import json, sys, threading, urllib.request
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer

MOCK = {  # node -> (serial, BIOS, BMC firmware, GPU VBIOS, NIC firmware, health)
    "node001": ("SN-1001", "1.4.2", "24.09", "96.00.99.00.01", "28.42.1000", "OK"),
    "node002": ("SN-1002", "1.4.2", "24.09", "96.00.99.00.01", "28.42.1000", "OK"),
    "node003": ("SN-1003", "1.3.7", "24.09", "96.00.99.00.01", "28.39.1002", "Warning"),
}

class BMC(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        node, path = self.path.split("/", 2)[1], "/" + self.path.split("/", 2)[2]
        sn, bios, bmc, vb, nic, health = MOCK[node]
        if path == "/redfish/v1/Systems/1":
            body = {"SerialNumber": sn, "BiosVersion": bios, "Status": {"Health": health},
                    "ProcessorSummary": {"Count": 2}, "MemorySummary": {"TotalSystemMemoryGiB": 2048}}
        elif path == "/redfish/v1/UpdateService/FirmwareInventory":
            body = {"Members": [{"Id": "BMC", "Version": bmc}, {"Id": "GPU_VBIOS", "Version": vb},
                                {"Id": "NIC", "Version": nic}]}
        else:
            self.send_response(404); self.end_headers(); return
        data = json.dumps(body).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.end_headers(); self.wfile.write(data)

def get(base, path):
    with urllib.request.urlopen(base + path, timeout=5) as r:
        return json.load(r)

def inventory(base):
    s = get(base, "/redfish/v1/Systems/1")
    fw = {m["Id"]: m["Version"] for m in get(base, "/redfish/v1/UpdateService/FirmwareInventory")["Members"]}
    return {"serial": s["SerialNumber"], "health": s["Status"]["Health"], "BIOS": s["BiosVersion"], **fw}

def main():
    if sys.argv[1:]:
        targets = {h: f"https://{h}" for h in sys.argv[1:]}
    else:
        srv = HTTPServer(("127.0.0.1", 0), BMC)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        targets = {n: f"http://127.0.0.1:{srv.server_port}/{n}" for n in MOCK}
    inv = {n: inventory(b) for n, b in targets.items()}
    keys = ["BIOS", "BMC", "GPU_VBIOS", "NIC"]
    print(f"{'node':8s} {'serial':8s} {'health':8s} " + " ".join(f"{k:15s}" for k in keys))
    for n, r in inv.items():
        print(f"{n:8s} {r['serial']:8s} {r['health']:8s} " + " ".join(f"{r[k]:15s}" for k in keys))
    for k in keys:
        golden, _ = Counter(r[k] for r in inv.values()).most_common(1)[0]
        odd = [n for n, r in inv.items() if r[k] != golden]
        if odd:
            print(f"DRIFT {k}: golden {golden}, different on {', '.join(odd)}")
    sick = [n for n, r in inv.items() if r["health"] != "OK"]
    print("hold back before OS install:", ", ".join(sorted(set(sick + [n for k in keys for n, r in inv.items()
          if r[k] != Counter(x[k] for x in inv.values()).most_common(1)[0][0]]))) or "none")

if __name__ == "__main__":
    main()
