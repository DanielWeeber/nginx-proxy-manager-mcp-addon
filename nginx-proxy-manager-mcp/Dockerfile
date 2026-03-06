FROM ghcr.io/b3nw/nginx-proxy-manager-mcp:latest

# Install s6-overlay for correct HA lifecycle management
ARG S6_OVERLAY_VERSION=3.2.0.2
ARG BUILD_ARCH=x86_64

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl xz-utils jq \
    && rm -rf /var/lib/apt/lists/*

# Install s6-overlay
RUN curl -fsSL https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz \
    | tar -C / -Jxpf - \
    && curl -fsSL https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${BUILD_ARCH}.tar.xz \
    | tar -C / -Jxpf -

# Install bashio
RUN curl -fsSL https://github.com/hassio-addons/bashio/archive/refs/tags/v0.16.2.tar.gz \
    | tar -xzC /tmp \
    && mv /tmp/bashio-0.16.2/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio

# Copy s6-overlay service scripts
COPY rootfs /
RUN chmod a+x /etc/s6-overlay/s6-rc.d/npm-mcp/run \
                /etc/s6-overlay/s6-rc.d/npm-mcp/finish

ENTRYPOINT ["/init"]
