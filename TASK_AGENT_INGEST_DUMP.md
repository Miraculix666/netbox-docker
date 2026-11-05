# 🤖 Agent Task Directive: Ingest & Triage NetBox Import Script

**Origin:** Offloaded from `scripts-and-tools/tools/netbox`  
**Location in Repo:** `dump/netbox_tools/import_vlan_matrix.py`  
**Date:** 2026-11-05  

## 🎯 Task Objective
Review `dump/netbox_tools/import_vlan_matrix.py`:

1. **Integration**:
   - Check if the VLAN matrix import script belongs in a dedicated `scripts/` or `automation/` folder in `netbox-docker`.
   - Ensure dependencies (e.g. `pynetbox`) and environment variable configuration conform to repo standards.
2. **Action Plan**:
   - Move to production scripts path and update documentation.
   - Clean up `dump/netbox_tools/`.
