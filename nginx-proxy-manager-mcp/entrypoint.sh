#!/bin/sh
# ==============================================================================
# HA Add-on entrypoint: reads /data/options.json and starts npm-mcp
# ==============================================================================

OPTIONS=/data/options.json

export NPM_API_URL=$(jq -r '.npm_api_url' "$OPTIONS")
export NPM_IDENTITY=$(jq -r '.npm_identity' "$OPTIONS")
export NPM_SECRET=$(jq -r '.npm_secret' "$OPTIONS")
export NPM_MCP_HOST=$(jq -r '.mcp_host' "$OPTIONS")
export NPM_MCP_PORT=$(jq -r '.mcp_port' "$OPTIONS")
export NPM_MCP_TRANSPORT=$(jq -r '.mcp_transport' "$OPTIONS")

PROXY_DEFAULTS=$(jq -r '.npm_proxy_defaults // empty' "$OPTIONS")
if [ -n "$PROXY_DEFAULTS" ]; then
    export NPM_PROXY_DEFAULTS="$PROXY_DEFAULTS"
fi

echo "[INFO] Starting Nginx Proxy Manager MCP Add-on v0.1.0"
echo "[INFO] NPM API: ${NPM_API_URL}"
echo "[INFO] MCP: ${NPM_MCP_TRANSPORT} on ${NPM_MCP_HOST}:${NPM_MCP_PORT}"

exec python3 -m npm_mcp.main
