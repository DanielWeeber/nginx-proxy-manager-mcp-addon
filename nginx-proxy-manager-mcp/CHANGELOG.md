# Changelog

## 0.6.0

- Fix: Install s6-overlay + bashio directly into b3nw Debian image
- No more cross-architecture library issues (glibc vs musl)
- Use s6-overlay v3 service structure (s6-rc.d)

## 0.5.x

- Failed: Multi-stage build - b3nw (glibc) Python binary incompatible with Alpine (musl)

## 0.4.x

- Failed: PyPI package v2.14.0 only supports stdio, not HTTP

## 0.4.0

- Refactor: HA base-python image + s6-overlay
