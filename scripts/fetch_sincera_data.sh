#!/bin/bash
set -euo pipefail

mkdir -p data_output

# Default to the OpenSincera API endpoint documented in the portal
API_URL="${SINCERA_API_URL:-https://open.sincera.io/api/ecosystem}"

curl -sfSL -H "Authorization: Bearer ${SINCERA_API_KEY}" "$API_URL" -o data_output/ecosystem.json

ls -l data_output/ecosystem.json

if [[ -n "${AWS_BUCKET_NAME:-}" ]]; then
  aws s3 cp data_output/ecosystem.json "s3://${AWS_BUCKET_NAME}/ecosystem.json"
fi
