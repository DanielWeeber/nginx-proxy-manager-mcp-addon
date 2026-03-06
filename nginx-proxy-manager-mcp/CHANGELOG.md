# Changelog

## 0.2.2

- Fix: Add `startup: application` to config.yaml so HA correctly tracks container state
- Fix: Add HEALTHCHECK to Dockerfile so HA knows when container is truly ready
- Add: curl installed for healthcheck

## 0.2.1

- Add: Verbose startup logging (all env vars except password)
- Add: Config validation with error output if options.json unreadable
- Fix: Default mcp_transport back to 'http'

## 0.2.0

- Refactor: Thin wrapper — uses upstream `ghcr.io/b3nw/nginx-proxy-manager-mcp:latest` directly
- No more custom Python source, no s6-overlay
- entrypoint.sh reads /data/options.json and passes env vars to upstream image
