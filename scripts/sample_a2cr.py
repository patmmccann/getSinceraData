import os
import random
import time
import json
import requests
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELLERS_DIR = os.path.join(BASE_DIR, 'reference_sellers_lists')

def list_sellers_files():
    return [
        os.path.join(SELLERS_DIR, f)
        for f in os.listdir(SELLERS_DIR)
        if f.endswith('.json')
    ]
API_URL = 'https://open.sincera.io/api/publishers'
RAW_OUTPUT_DIR = 'raw_ac2r'
ANALYSIS_DIR = 'ac2r_analysis'

API_KEY = os.environ.get('SINCERA_API_KEY')

if API_KEY is None:
    raise SystemExit('SINCERA_API_KEY environment variable is not set')

HEADERS = {'Authorization': f'Bearer {API_KEY}'}

def load_domains(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    domains = [s.get('domain') for s in data.get('sellers', []) if s.get('domain')]
    return list(set(domains))

def sample_domains(domains, n=100):
    if len(domains) < n:
        n = len(domains)
    return random.sample(domains, n)

def fetch_a2cr(domain: str, max_retries: int = 5):
    delay = 1
    for _ in range(max_retries):
        resp = requests.get(API_URL, params={'domain': domain}, headers=HEADERS, timeout=30)
        if resp.status_code == 429:
            time.sleep(delay)
            delay = min(delay * 2, 30)
            continue
        if resp.status_code != 200:
            return None, {'error': resp.text, 'status_code': resp.status_code}
        data = resp.json()
        return data.get('avg_ads_to_content_ratio'), data
    return None, {'error': 'max retries exceeded', 'status_code': 429}

def process_group(path: str, name: str):
    domains = load_domains(path)
    sample = sample_domains(domains)
    results = {}
    for d in sample:
        a2cr, resp = fetch_a2cr(d)
        results[d] = {'a2cr': a2cr, 'response': resp}
        time.sleep(2)  # throttle requests to avoid rate limits
    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(RAW_OUTPUT_DIR, f'{name}_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
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
    summary = {}
    for path in sorted(list_sellers_files()):
        name = os.path.splitext(os.path.basename(path))[0]
        stats = process_group(path, name)
        summary[f'{name}_percentiles'] = stats

    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    with open(os.path.join(ANALYSIS_DIR, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
