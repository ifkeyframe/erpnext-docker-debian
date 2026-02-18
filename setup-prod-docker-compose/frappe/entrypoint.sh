#!/usr/bin/env bash
set -e

if [ "${DFP_DISABLE_STARTUP:-}" = "DISABLE_STARTUP" ]; then
  exec sleep infinity
fi

exec "$@"