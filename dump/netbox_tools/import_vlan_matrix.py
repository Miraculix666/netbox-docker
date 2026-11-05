import os
import sys
import pynetbox

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8080")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN", "0123456789abcdef0123456789abcdef01234567")

print("[*] Verbinde mit NetBox unter:", NETBOX_URL)
nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)

try:
    site = nb.dcim.sites.get(name="Schulungszentrum")
    if not site:
        site = nb.dcim.sites.create(name="Schulungszentrum", slug="schulungszentrum", status="active")

    vlans = [
        {"vid": 10, "name": "OOB-Management", "prefix": "10.0.10.0/24", "description": "Physisch isoliert, iLO/iDRAC"},
        {"vid": 20, "name": "Core-Management", "prefix": "10.0.20.0/24", "description": "Admin-VPN, Proxmox, NetBox, Checkmk"},
        {"vid": 30, "name": "DevOps-Backend", "prefix": "10.0.30.0/24", "description": "CI/CD, Git, Ansible, Artefakt-Proxy"},
        {"vid": 40, "name": "Lokaler-LLM-Stack", "prefix": "10.0.40.0/24", "description": "Ollama, LiteLLM, Qdrant (Kein Internet-Gateway)"},
        {"vid": 50, "name": "Schulungs-Lab", "prefix": "10.0.50.0/24", "description": "Client Isolation, Guacamole/Kasm"},
        {"vid": 60, "name": "Dozenten-Netz", "prefix": "10.0.60.0/24", "description": "Praesentations-Zugriff auf Labs"},
        {"vid": 70, "name": "DMZ-Ingress", "prefix": "10.0.70.0/24", "description": "Traefik Reverse Proxy, Guacamole Web-Gateway"}
    ]

    for item in vlans:
        vlan_obj = nb.ipam.vlans.get(vid=item["vid"])
        if not vlan_obj:
            vlan_obj = nb.ipam.vlans.create(
                vid=item["vid"],
                name=item["name"],
                site=site.id,
                status="active",
                description=item["description"]
            )
            print(f"[+] VLAN {item['vid']} ({item['name']}) angelegt.")

        prefix_obj = nb.ipam.prefixes.get(prefix=item["prefix"])
        if not prefix_obj:
            nb.ipam.prefixes.create(
                prefix=item["prefix"],
                site=site.id,
                vlan=vlan_obj.id,
                status="active",
                description=item["description"]
            )
            print(f"[+] Prefix {item['prefix']} zugewiesen.")

    print("[✓] Ziel-VLAN-Matrix erfolgreich in NetBox importiert.")
except Exception as e:
    print("[!] Fehler beim Befuellen von NetBox:", str(e))
