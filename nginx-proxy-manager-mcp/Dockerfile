ARG BUILD_FROM
FROM $BUILD_FROM

# Install nginx-proxy-manager-mcp from PyPI
RUN pip3 install --no-cache-dir nginx-proxy-manager-mcp

# Copy s6-overlay service scripts
COPY rootfs /
