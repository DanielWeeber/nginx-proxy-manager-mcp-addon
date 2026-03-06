# Changelog

## 0.4.0

- Refactor: Use official HA base-python image + s6-overlay (like example add-on)
- Fix: HA now correctly tracks container state (no more stuck 'Starten')
- Install nginx-proxy-manager-mcp from PyPI via uv
- Proper s6 run/finish scripts

## 0.3.0 and earlier

- Various attempts using upstream b3nw image directly (s6 lifecycle issues)
