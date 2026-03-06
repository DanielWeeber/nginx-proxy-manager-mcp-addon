# Changelog

## 0.2.3

- Fix: Change startup from 'application' to 'services' so HA tracks state correctly
- Fix: Explicitly EXPOSE 9115 in Dockerfile (upstream exposes 8000)
- Fix: Remove Docker HEALTHCHECK (HA Supervisor ignores it anyway)

## 0.2.2

- Fix: Add startup: application and HEALTHCHECK

## 0.2.1

- Add: Verbose startup logging

## 0.2.0

- Refactor: Thin wrapper using upstream b3nw image directly
