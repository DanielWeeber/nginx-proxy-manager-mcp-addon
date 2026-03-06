#!/bin/bash
set -e

OPTS=/data/options.json

VERSION=$(cat /data/options.json 2>/dev/null | jq -r '.version // "unknown"' 2>/dev/null || echo "unknown")

export NPM_API_URL=$(jq -r '.npm_api_url' "$OPTS")
export NPM_IDENTITY=$(jq -r '.npm_identity' "$OPTS")
export NPM_SECRET=$(jq -r '.npm_secret' "$OPTS")
export NPM_MCP_HOST=$(jq -r '.mcp_host' "$OPTS")
export NPM_MCP_PORT=$(jq -r '.mcp_port' "$OPTS")
export NPM_MCP_TRANSPORT=http

DEFAULTS=$(jq -r '.npm_proxy_defaults // empty' "$OPTS")
[ -n "$DEFAULTS" ] && export NPM_PROXY_DEFAULTS="$DEFAULTS"

echo "[INFO] ============================================"
echo "[INFO] Nginx Proxy Manager MCP Add-on v0.7.0"
echo "[INFO] ============================================"
echo "[INFO] NPM API:  ${NPM_API_URL}"
echo "[INFO] Identity: ${NPM_IDENTITY}"
echo "[INFO] MCP:      http://${NPM_MCP_HOST}:${NPM_MCP_PORT}/mcp"
echo "[INFO] ============================================"

exec python3 -m npm_mcp.main
