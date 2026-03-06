#!/bin/sh
OPTS=/data/options.json

export NPM_API_URL=$(jq -r '.npm_api_url' "$OPTS")
export NPM_IDENTITY=$(jq -r '.npm_identity' "$OPTS")
export NPM_SECRET=$(jq -r '.npm_secret' "$OPTS")
export NPM_MCP_HOST=$(jq -r '.mcp_host' "$OPTS")
export NPM_MCP_PORT=$(jq -r '.mcp_port' "$OPTS")
export NPM_MCP_TRANSPORT=http

DEFAULTS=$(jq -r '.npm_proxy_defaults // empty' "$OPTS")
[ -n "$DEFAULTS" ] && export NPM_PROXY_DEFAULTS="$DEFAULTS"

echo "[npm-mcp] NPM_API_URL: ${NPM_API_URL}"
echo "[npm-mcp] NPM_IDENTITY: ${NPM_IDENTITY}"
echo "[npm-mcp] NPM_MCP_HOST: ${NPM_MCP_HOST}:${NPM_MCP_PORT}"
echo "[npm-mcp] NPM_MCP_TRANSPORT: ${NPM_MCP_TRANSPORT}"

exec python -m npm_mcp.main
