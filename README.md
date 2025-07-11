# getSinceraData

This repository contains a simple script to fetch the Sincera ecosystem data. The API key is provided via the `SINCERA_API_KEY` GitHub secret. When run, the script stores the result in `output/ecosystem/ecosystem.json`.
When AWS credentials are available, the GitHub Actions workflow uploads the entire `output/` directory to the configured bucket using `scripts/sync_output_to_s3.sh`.

## Usage

Ensure that the `SINCERA_API_KEY` environment variable is available (for example via GitHub Actions secrets). To upload the file to S3 you must also configure the AWS role via `AWS_ROLE_TO_ASSUME` and provide the bucket name in `AWS_BUCKET_NAME`.

```bash
./scripts/fetch_sincera_data.sh
```
## Visualization

The github action deploys data back to this repo, which https://getsinceradata.streamlit.app/ points at.

## Reference sellers lists
When the `trigger_data_pull.txt` file changes on `main`, a GitHub Actions workflow downloads the latest `sellers.json` files from SheMedia, CafeMedia, Mediavine, Freestar, Aditude, and Playwire. The files are committed to the `reference_sellers_lists/` directory.

To trigger the data pull, edit `trigger_data_pull.txt` and change the value after `last_pull =` to a new date or version, for example:

```text
last_pull = 20250709v1
```

Commit the updated file to `main`. Each time you want the workflow to run again, increment the value in `trigger_data_pull.txt` and push the change.

### Sampling publisher A2CR

The `sample_a2cr.py` script reads every `sellers.json` file stored in
`reference_sellers_lists`, takes random samples from the domains listed,
  fetches A2CR data for each domain from OpenSincera and writes the
  raw results to the `output/raw_ac2r/` directory. The summary statistics are
  written to `output/ac2r_analysis/`. Each entry in the summary includes the
  number of domains used to calculate the percentiles.
  In addition to A2CR, the summary contains percentile data for
  `total_supply_paths` and `avg_page_weight`.
  The
  script requires the `SINCERA_API_KEY` environment variable and Python
packages `requests` and `numpy`.

  When both `AWS_BUCKET_NAME` and `AWS_ROLE_TO_ASSUME` are set, the workflow runs
  `scripts/sync_output_to_s3.sh` so the files appear under `raw_ac2r/` and
  `ac2r_analysis/` in the bucket.

  The script automatically respects the OpenSincera API's rate limits of
  45 requests per rolling minute and 5000 requests per day.
 

```bash
SINCERA_API_KEY=your_token SAMPLE_SIZE=5 python scripts/sample_a2cr.py
```
The optional `SAMPLE_SIZE` variable controls how many domains are sampled from each
`sellers.json` file. The default is 20.
