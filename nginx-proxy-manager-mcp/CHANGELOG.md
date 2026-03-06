# Changelog

## 0.1.0

- Refactor: Use upstream image ghcr.io/b3nw/nginx-proxy-manager-mcp:latest directly
- No more custom Python build — just a thin wrapper around the upstream container

## 0.0.6

- Fix: Switch default transport to `sse` for better compatibility with mcp-remote

## 0.0.5

- Add: `mcp_transport` option configurable via HA UI

## 0.0.4

- Fix: MCP endpoint correctly documented as `/mcp`

## 0.0.3

- Fix: s6 service scripts now correctly marked as executable
- Add: Version number logged on startup

## 0.0.2

- Initial Home Assistant add-on release
