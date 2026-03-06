# Changelog

## 0.3.0

- Simplify: Minimal Dockerfile, only adds jq + entrypoint.sh on top of b3nw image
- Remove mcp_transport option (always http, as upstream only supports http/stdio)
- Startup: services (correct HA lifecycle)

## 0.2.x

- Various attempts at fixing HA state tracking and SSE transport

## 0.2.0

- Initial thin wrapper using upstream b3nw image
