import os
import random
import time
import json
import requests
import numpy as np
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELLERS_DIR = os.path.join(BASE_DIR, 'reference_sellers_lists')

def list_sellers_files():
    return [
        os.path.join(SELLERS_DIR, f)
        for f in os.listdir(SELLERS_DIR)
        if f.endswith('.json')
    ]
API_URL = 'https://open.sincera.io/api/publishers'
RAW_OUTPUT_DIR = os.path.join('output', 'raw_ac2r')
ANALYSIS_DIR = os.path.join('output', 'ac2r_analysis')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ROLE_TO_ASSUME = os.environ.get('AWS_ROLE_TO_ASSUME')

API_KEY = os.environ.get('SINCERA_API_KEY')

if API_KEY is None:
    raise SystemExit('SINCERA_API_KEY environment variable is not set')

HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def sync_output() -> None:
    """Sync the entire output directory to S3 if bucket and role are set."""
    if not AWS_BUCKET_NAME or not AWS_ROLE_TO_ASSUME:
        return
    script = os.path.join(os.path.dirname(__file__), 'sync_output_to_s3.sh')
    subprocess.run(["bash", script], check=True)

def load_domains(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    domains = [s.get('domain') for s in data.get('sellers', []) if s.get('domain')]
    return list(set(domains))

SAMPLE_SIZE = int(os.environ.get('SAMPLE_SIZE', '100'))

def sample_domains(domains, n=SAMPLE_SIZE):
    if len(domains) < n:
        n = len(domains)
    return random.sample(domains, n)

def fetch_a2cr(domain: str, max_retries: int = 5):
    """Fetch A2CR data for a domain with exponential backoff respecting the Retry-After header."""
    delay = 1.0
    for _ in range(max_retries):
        resp = requests.get(
            API_URL, params={"domain": domain}, headers=HEADERS, timeout=30
        )
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except ValueError:
                    pass
            time.sleep(delay)
            delay *= 2
            continue
        if resp.status_code != 200:
            return None, {"error": resp.text, "status_code": resp.status_code}
        data = resp.json()
        return data.get("avg_ads_to_content_ratio"), data
    return None, {"error": "max retries exceeded", "status_code": 429}

def process_group(path: str, name: str):
    domains = load_domains(path)
    sample = sample_domains(domains)
    results = {}
    for d in sample:
        a2cr, resp = fetch_a2cr(d)
        results[d] = {'a2cr': a2cr, 'response': resp}
        time.sleep(2)  # throttle requests to avoid rate limits
    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    result_file = os.path.join(RAW_OUTPUT_DIR, f'{name}_results.json')
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    # sync will handle uploading this file if AWS_BUCKET_NAME is set
    def calc(values):
        stats = {'n': len(values)}
        if values:
            stats.update(
                {
                    'p25': float(np.percentile(values, 25)),
                    'p50': float(np.percentile(values, 50)),
                    'p75': float(np.percentile(values, 75)),
                }
            )
        return stats

    values_a2cr = [r['a2cr'] for r in results.values() if r['a2cr'] is not None]
    values_tsp = [
        r['response'].get('total_supply_paths')
        for r in results.values()
        if isinstance(r['response'], dict)
        and r['response'].get('total_supply_paths') is not None
    ]
    values_apw = [
        r['response'].get('avg_page_weight')
        for r in results.values()
        if isinstance(r['response'], dict)
        and r['response'].get('avg_page_weight') is not None
    ]

    return {
        'a2cr': calc(values_a2cr),
        'total_supply_paths': calc(values_tsp),
        'avg_page_weight': calc(values_apw),
    }

def main():
    summary = {}
    for path in sorted(list_sellers_files()):
        name = os.path.splitext(os.path.basename(path))[0]
        stats = process_group(path, name)
        summary[f'{name}_percentiles'] = stats

    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    summary_file = os.path.join(ANALYSIS_DIR, 'summary.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)


    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
