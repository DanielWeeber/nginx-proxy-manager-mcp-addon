# Changelog

## 0.0.4

- Fix: MCP endpoint is now reachable at `http://<ha-ip>:9115/` (root path, not `/mcp`)
- Fix: Set `mount_path="/"` in FastMCP to match original Docker container behavior

## 0.0.3

- Fix: s6 service scripts now correctly marked as executable (chmod in Dockerfile)
- Add: Version number logged on startup

## 0.0.2

- Initial Home Assistant add-on release
- Based on nginx-proxy-manager-mcp v0.0.2 by b3nw
- Supports HTTP transport mode on configurable port
- All NPM connection settings configurable via HA UI
