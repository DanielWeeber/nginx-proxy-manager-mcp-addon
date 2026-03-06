# Changelog

## 0.2.0

- Refactor: Thin wrapper — uses upstream `ghcr.io/b3nw/nginx-proxy-manager-mcp:latest` directly
- No more custom Python source, no s6-overlay
- entrypoint.sh reads /data/options.json and passes env vars to upstream image

## 0.1.0

- First attempt at using upstream image (incomplete)

## 0.0.6

- Fix: Switch default transport to `sse`

## 0.0.5

- Add: `mcp_transport` option configurable via HA UI

## 0.0.4

- Fix: MCP endpoint correctly documented as `/mcp`

## 0.0.3

- Fix: s6 service scripts now correctly marked as executable
- Add: Version number logged on startup

## 0.0.2

- Initial Home Assistant add-on release
