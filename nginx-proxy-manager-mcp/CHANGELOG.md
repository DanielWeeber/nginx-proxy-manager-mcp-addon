# Changelog

## 0.4.2

- Fix: Correct base image tag (3.13-alpine3.21, not 3.12)
- Fix: Use pip3 directly (Alpine compatible)

## 0.4.1

- Fix: pip3 instead of uv

## 0.4.0

- Refactor: HA base-python image + s6-overlay like example add-on
- Proper s6 run/finish scripts for correct HA state tracking
