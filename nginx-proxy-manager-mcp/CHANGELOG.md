# Changelog

## 0.5.1

- Fix: Copy /usr/local/lib instead of specific binaries (uvicorn is a module, not a binary)
- Fix: Copy entire python lib directory from b3nw image

## 0.5.0

- Multi-stage build: b3nw Python into HA base image for s6-overlay support

## 0.4.x

- Failed attempts: PyPI package (v2.14.0) only supports stdio, not HTTP
