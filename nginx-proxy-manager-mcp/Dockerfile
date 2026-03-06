ARG BUILD_FROM
FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest AS npm_mcp

# Use HA base image for s6-overlay + bashio
FROM $BUILD_FROM

# Copy the entire Python site-packages from b3nw image (includes npm_mcp + all dependencies)
COPY --from=npm_mcp /usr/local/lib /usr/local/lib
COPY --from=npm_mcp /usr/local/bin/python3 /usr/local/bin/python3

# Copy s6-overlay service scripts
COPY rootfs /
RUN chmod a+x /etc/services.d/npm-mcp/run /etc/services.d/npm-mcp/finish
