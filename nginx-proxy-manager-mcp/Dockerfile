FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Add jq for parsing /data/options.json and our entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends jq && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
