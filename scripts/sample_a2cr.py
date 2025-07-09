import os
import random
import time
import json
import subprocess
import requests
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAFEMEDIA_FILE = os.path.join(BASE_DIR, 'reference_sellers_lists', 'sellers_cafemedia.json')
MEDIAVINE_FILE = os.path.join(BASE_DIR, 'reference_sellers_lists', 'sellers_mediavine.json')
API_URL = 'https://open.sincera.io/api/publishers'
OUTPUT_DIR = 'data_output'
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

API_KEY = os.environ.get('SINCERA_API_KEY')

if API_KEY is None:
    raise SystemExit('SINCERA_API_KEY environment variable is not set')

HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def upload_to_s3(local_path: str, key: str) -> None:
    """Upload a file to S3 if AWS_BUCKET_NAME is set."""
    if not AWS_BUCKET_NAME:
        return
    subprocess.run(
        ["aws", "s3", "cp", local_path, f"s3://{AWS_BUCKET_NAME}/{key}"],
        check=True,
    )

def load_domains(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    domains = [s.get('domain') for s in data.get('sellers', []) if s.get('domain')]
    return list(set(domains))

def sample_domains(domains, n=100):
    if len(domains) < n:
        n = len(domains)
    return random.sample(domains, n)

def fetch_a2cr(domain: str):
    resp = requests.get(API_URL, params={'domain': domain}, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        return None, {'error': resp.text, 'status_code': resp.status_code}
    data = resp.json()
    return data.get('avg_ads_to_content_ratio'), data

def process_group(path: str, name: str):
    domains = load_domains(path)
    sample = sample_domains(domains)
    results = {}
    for d in sample:
        a2cr, resp = fetch_a2cr(d)
        results[d] = {'a2cr': a2cr, 'response': resp}
        time.sleep(1)  # simple throttle
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result_file = os.path.join(OUTPUT_DIR, f'{name}_results.json')
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    upload_to_s3(result_file, f'a2cr_raw/{name}_results.json')
    values = [r['a2cr'] for r in results.values() if r['a2cr'] is not None]
    percentiles = {}
    if values:
        percentiles = {
            'p25': float(np.percentile(values, 25)),
            'p50': float(np.percentile(values, 50)),
            'p75': float(np.percentile(values, 75)),
        }
    return percentiles

def main():
    cafe_stats = process_group(CAFEMEDIA_FILE, 'cafemedia')
    mediavine_stats = process_group(MEDIAVINE_FILE, 'mediavine')
    summary = {
        'cafemedia_percentiles': cafe_stats,
        'mediavine_percentiles': mediavine_stats,
    }
    summary_file = os.path.join(OUTPUT_DIR, 'summary.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    upload_to_s3(summary_file, 'a2cr_results/summary.json')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
