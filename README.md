# getSinceraData

This repository contains a simple script to fetch the Sincera ecosystem data. The API key is provided via the `SINCERA_API_KEY` GitHub secret. When run, the script stores the result in `data_output/ecosystem.json` and uploads it to an S3 bucket if `AWS_BUCKET_NAME` is set. The file is uploaded under the `ecosystem/` prefix within the bucket.

## Usage

Ensure that the `SINCERA_API_KEY` environment variable is available (for example via GitHub Actions secrets). To upload the file to S3 you must also configure the AWS role via `AWS_ROLE_TO_ASSUME` and provide the bucket name in `AWS_BUCKET_NAME`.

```bash
./scripts/fetch_sincera_data.sh
```

## Reference sellers lists
On every merge into `main`, a GitHub Actions workflow downloads the latest `sellers.json` files from SheMedia, CafeMedia, Mediavine, Freestar, and Aditude. The files are committed to the `reference_sellers_lists/` directory.

### Sampling publisher A2CR

The `sample_a2cr.py` script reads the CafeMedia and Mediavine
`sellers.json` files stored in `reference_sellers_lists`, takes random
samples from those domains, fetches A2CR data for each domain from
OpenSincera and writes the responses to the `data_output/` directory. The
script requires the `SINCERA_API_KEY` environment variable and Python
packages `requests` and `numpy`. When `AWS_BUCKET_NAME` is set, the raw files
are uploaded to `a2cr_raw/` in the bucket and the summary is uploaded to
`a2cr_results/`.

```bash
SINCERA_API_KEY=your_token python scripts/sample_a2cr.py
```
