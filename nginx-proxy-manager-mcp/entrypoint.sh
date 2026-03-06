#!/bin/sh
OPTS=/data/options.json

echo "[INFO] ============================================"
echo "[INFO] Nginx Proxy Manager MCP Add-on starting..."
echo "[INFO] ============================================"

# Read config
export NPM_API_URL=$(jq -r '.npm_api_url' "$OPTS")
export NPM_IDENTITY=$(jq -r '.npm_identity' "$OPTS")
export NPM_SECRET=$(jq -r '.npm_secret' "$OPTS")
export NPM_MCP_HOST=$(jq -r '.mcp_host' "$OPTS")
export NPM_MCP_PORT=$(jq -r '.mcp_port' "$OPTS")
export NPM_MCP_TRANSPORT=$(jq -r '.mcp_transport' "$OPTS")

DEFAULTS=$(jq -r '.npm_proxy_defaults // empty' "$OPTS")
[ -n "$DEFAULTS" ] && export NPM_PROXY_DEFAULTS="$DEFAULTS"

# Verbose config output (no password)
echo "[INFO] Configuration:"
echo "[INFO]   NPM_API_URL       = ${NPM_API_URL}"
echo "[INFO]   NPM_IDENTITY      = ${NPM_IDENTITY}"
echo "[INFO]   NPM_SECRET        = (hidden)"
echo "[INFO]   NPM_MCP_HOST      = ${NPM_MCP_HOST}"
echo "[INFO]   NPM_MCP_PORT      = ${NPM_MCP_PORT}"
echo "[INFO]   NPM_MCP_TRANSPORT = ${NPM_MCP_TRANSPORT}"
if [ -n "$NPM_PROXY_DEFAULTS" ]; then
    echo "[INFO]   NPM_PROXY_DEFAULTS= ${NPM_PROXY_DEFAULTS}"
else
    echo "[INFO]   NPM_PROXY_DEFAULTS= (not set)"
fi
echo "[INFO] ============================================"
echo "[INFO] MCP endpoint: http://${NPM_MCP_HOST}:${NPM_MCP_PORT}/mcp"
echo "[INFO] ============================================"

# Verify options.json was readable
if [ "$NPM_API_URL" = "null" ] || [ -z "$NPM_API_URL" ]; then
    echo "[ERROR] Could not read npm_api_url from /data/options.json!"
    echo "[ERROR] Contents of /data/options.json:"
    cat "$OPTS" 2>/dev/null || echo "[ERROR] File not found or not readable!"
    exit 1
fi

echo "[INFO] Starting upstream npm-mcp server..."
exec python -m npm_mcp.main
