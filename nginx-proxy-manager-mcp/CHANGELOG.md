# Changelog

## 0.7.1

- Fix: Use ENTRYPOINT ["/run.sh"] to override upstream python entrypoint
- Previously run.sh was passed as argument to python, not executed as entrypoint

## 0.7.0

- Revert to simple b3nw image + run.sh approach
