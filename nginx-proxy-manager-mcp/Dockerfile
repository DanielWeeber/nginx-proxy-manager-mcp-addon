ARG BUILD_FROM
FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Copy bashio entrypoint script that reads HA options and sets env vars
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
