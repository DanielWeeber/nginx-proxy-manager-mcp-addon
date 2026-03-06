# Changelog

## 0.5.0

- Fix: Multi-stage build - copy Python + npm_mcp from b3nw image into HA base image
- This gives us s6-overlay (correct HA state) AND the b3nw HTTP transport

## 0.4.x

- Failed attempts: PyPI package (v2.14.0) only supports stdio, not HTTP

## 0.4.0

- Refactor: HA base-python image + s6-overlay
