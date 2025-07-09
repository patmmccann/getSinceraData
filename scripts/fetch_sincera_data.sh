#!/bin/bash
set -euo pipefail

mkdir -p output

API_URL="${SINCERA_API_URL:-https://api.sincera.io/v1/ecosystem}"

curl -sfSL -H "Authorization: Bearer ${SINCERA_API_KEY}" "$API_URL" -o output/ecosystem_data.json

ls -l output/ecosystem_data.json
