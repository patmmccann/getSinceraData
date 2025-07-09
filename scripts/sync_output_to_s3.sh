#!/bin/bash
set -euo pipefail

if [[ -z "${AWS_BUCKET_NAME:-}" ]]; then
  echo "AWS_BUCKET_NAME not set; skipping S3 upload" >&2
  exit 0
fi

aws s3 sync output/ "s3://${AWS_BUCKET_NAME}/"
