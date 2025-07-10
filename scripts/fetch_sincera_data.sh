#!/bin/bash
set -euo pipefail

mkdir -p output/ecosystem

# Default to the OpenSincera API endpoint documented in the portal
API_URL="${SINCERA_API_URL:-https://open.sincera.io/api/ecosystem}"

curl -sfSL -H "Authorization: Bearer ${SINCERA_API_KEY}" "$API_URL" -o output/ecosystem/ecosystem.json

# Validate and pretty-print the JSON without requiring the jsonlint package
python3 -m json.tool output/ecosystem/ecosystem.json \
  > output/ecosystem/ecosystem.json.tmp && mv output/ecosystem/ecosystem.json.tmp output/ecosystem/ecosystem.json

ls -l output/ecosystem/ecosystem.json

