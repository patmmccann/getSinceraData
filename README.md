#getSinceraData

This repository contains a simple script to fetch the Sincera ecosystem data. The API key is provided via the `SINCERA_API_KEY` GitHub secret. When run, the script stores the result as `ecosystem.json`.

## Usage

Ensure that the `SINCERA_API_KEY` environment variable is available (for example via GitHub Actions secrets). Make sure the AWS role is defined in `AWS_ROLE_TO_ASSUME` before running the script to upload the file to S3 and put the bucket name in AWS_BUCKET_NAME.

```bash
./scripts/fetch_ecosystem.sh
```
