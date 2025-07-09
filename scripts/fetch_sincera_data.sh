#!/bin/bash
set -euo pipefail

mkdir -p output

# Default to the OpenSincera API endpoint documented in the portal
API_URL="${SINCERA_API_URL:-https://open.sincera.io/api/ecosystem}"

curl -sfSL -H "Authorization: Bearer ${SINCERA_API_KEY}" "$API_URL" -o output/ecosystem_data.json

ls -l output/ecosystem_data.json

if [[ -n "${AWS_BUCKET_NAME:-}" ]]; then
  aws s3 cp output/ecosystem_data.json "s3://${AWS_BUCKET_NAME}/ecosystem_data.json"
fi
