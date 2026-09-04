# Changelog

## v0.6.4 - 2026-09-04

- Declare component `210` before component `197`, satisfying the latter's real
  WeiDU dependency when installing the complete 30-component selection.
- Add a regression that preserves all 31 declarations (including the mutually
  exclusive `900`/`901` pair) and locks the dependency-safe order.
