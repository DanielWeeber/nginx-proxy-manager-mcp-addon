#!/bin/sh
OPTS=/data/options.json

export NPM_API_URL=$(jq -r '.npm_api_url' "$OPTS")
export NPM_IDENTITY=$(jq -r '.npm_identity' "$OPTS")
export NPM_SECRET=$(jq -r '.npm_secret' "$OPTS")
export NPM_MCP_HOST=$(jq -r '.mcp_host' "$OPTS")
export NPM_MCP_PORT=$(jq -r '.mcp_port' "$OPTS")
export NPM_MCP_TRANSPORT=$(jq -r '.mcp_transport' "$OPTS")

DEFAULTS=$(jq -r '.npm_proxy_defaults // empty' "$OPTS")
[ -n "$DEFAULTS" ] && export NPM_PROXY_DEFAULTS="$DEFAULTS"

echo "[INFO] NPM API: ${NPM_API_URL}"
echo "[INFO] MCP: ${NPM_MCP_TRANSPORT} on ${NPM_MCP_HOST}:${NPM_MCP_PORT}"

exec python -m npm_mcp.main
