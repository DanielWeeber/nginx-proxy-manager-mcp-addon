ARG BUILD_FROM
FROM $BUILD_FROM

# Install nginx-proxy-manager-mcp from PyPI
RUN pip3 install --no-cache-dir nginx-proxy-manager-mcp

# Copy s6-overlay service scripts and set permissions
COPY rootfs /
RUN chmod a+x /etc/services.d/npm-mcp/run /etc/services.d/npm-mcp/finish
