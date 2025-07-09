#!/bin/bash
set -euo pipefail

mkdir -p ecosystem

# Default to the OpenSincera API endpoint documented in the portal
API_URL="${SINCERA_API_URL:-https://open.sincera.io/api/ecosystem}"

curl -sfSL -H "Authorization: Bearer ${SINCERA_API_KEY}" "$API_URL" -o ecosystem/ecosystem.json

ls -l ecosystem/ecosystem.json

if [[ -n "${AWS_BUCKET_NAME:-}" ]]; then
  aws s3 cp ecosystem/ecosystem.json "s3://${AWS_BUCKET_NAME}/ecosystem/ecosystem.json"
fi
