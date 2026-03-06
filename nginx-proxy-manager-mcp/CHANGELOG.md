# Changelog

## 0.7.0

- Revert to simple approach: b3nw image + run.sh + CMD
- No s6-overlay download needed (GitHub not reachable from build)
- HA Supervisor handles process lifecycle via init: false + startup: services

## 0.6.0

- Failed: s6-overlay download from GitHub not reachable during build

## 0.5.x

- Failed: glibc/musl binary incompatibility

## 0.4.x

- Failed: PyPI package only supports stdio transport
