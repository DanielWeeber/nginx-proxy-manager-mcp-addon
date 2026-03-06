FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Install jq for parsing /data/options.json
RUN apt-get update && apt-get install -y --no-install-recommends jq && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Override upstream EXPOSE 8000 with our port
EXPOSE 9115

ENTRYPOINT ["/entrypoint.sh"]
