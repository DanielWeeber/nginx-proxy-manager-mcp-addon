ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python, uv, and jq
RUN apk add --no-cache python3 py3-pip jq curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Install nginx-proxy-manager-mcp from PyPI
RUN /root/.local/bin/uv pip install --system nginx-proxy-manager-mcp

# Copy s6-overlay service scripts
COPY rootfs /
