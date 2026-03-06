ARG BUILD_FROM
FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Copy s6-overlay service scripts from HA base
COPY rootfs /
RUN chmod a+x \
    /etc/services.d/npm-mcp/run \
    /etc/services.d/npm-mcp/finish
