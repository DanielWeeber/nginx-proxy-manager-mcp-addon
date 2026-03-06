ARG BUILD_FROM
FROM $BUILD_FROM AS base

RUN apk add --no-cache python3 py3-pip curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY npm_mcp_src/pyproject.toml npm_mcp_src/README.md ./
COPY npm_mcp_src/src/ src/

RUN uv pip install --system --no-cache .

ENV PYTHONUNBUFFERED=1 \
    NPM_MCP_TRANSPORT=http \
    NPM_MCP_HOST=0.0.0.0 \
    NPM_MCP_PORT=9115

COPY rootfs /

RUN chmod a+x /etc/services.d/npm-mcp/run \
              /etc/services.d/npm-mcp/finish

EXPOSE 9115
