#getSinceraData

This repository contains a simple script to fetch the Sincera ecosystem data. The API key is provided via the `SINCERA_API_KEY` GitHub secret. When run, the script stores the result as `ecosystem.json`.

## Usage

Ensure that the `SINCERA_API_KEY` environment variable is available (for example via GitHub Actions secrets). Optionally assume the AWS role defined in `AWS_ROLE_TO_ASSUME` before running the script if you need to upload the file to S3.

```bash
./scripts/fetch_ecosystem.sh
```
