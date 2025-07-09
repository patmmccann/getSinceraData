#!/usr/bin/env bash
set -euo pipefail

API_KEY="${SINCERA_API_KEY:-}"
if [[ -z "$API_KEY" ]]; then
  echo "SINCERA_API_KEY environment variable is not set" >&2
  exit 1
fi

API_URL="https://open.sincera.io/api/ecosystem"

# Fetch the ecosystem data and store in file
response=$(curl -H "Authorization: Bearer $API_KEY" "$API_URL")
status="${response: -3}"
body="${response::-3}"

if [[ "$status" != "200" ]]; then
  echo "Request failed with status $status" >&2
  echo "$body" >&2
  exit 1
fi

echo "$body" > ecosystem.json
echo "Data written to ecosystem.json"
