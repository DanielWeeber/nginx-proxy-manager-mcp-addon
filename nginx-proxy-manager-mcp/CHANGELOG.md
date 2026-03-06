# Changelog

## 0.2.0

- Refactor: Thin wrapper — uses upstream `ghcr.io/b3nw/nginx-proxy-manager-mcp:latest` directly
- No more custom Python source, no s6-overlay
- entrypoint.sh reads /data/options.json and passes env vars to upstream image

## 0.0.x

- Previous iterations with custom Python source and s6-overlay (removed)
