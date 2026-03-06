FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Install jq for parsing /data/options.json
RUN apt-get update && apt-get install -y --no-install-recommends jq curl && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Health check so HA knows the container is ready
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -sf -X POST http://localhost:${NPM_MCP_PORT:-9115}/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -d '{"jsonrpc":"2.0","method":"ping","id":1}' || exit 1

ENTRYPOINT ["/entrypoint.sh"]
