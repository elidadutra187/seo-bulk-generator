"""
SEO Bulk Generator — Generate SEO descriptions at scale using Claude API

This script processes a CSV of products and generates:
- Rich HTML product descriptions
- SEO-optimized titles (max 65 chars)
- Meta descriptions (max 155 chars)
- Relevant tags

Uses Anthropic Batch API for cost-effective bulk processing.
"""

import os
import csv
import json
import time
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    import anthropic
except ImportError:
    print("Please install: pip install anthropic")
    exit(1)


# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
INPUT_CSV = os.getenv("INPUT_CSV", "products_input.csv")
OUTPUT_CSV = os.getenv("OUTPUT_CSV", "products_output.csv")
BATCH_FILE = "batch_results.json"

MODEL = "claude-haiku-4-5-20251001"  # Fast and cost-effective
MAX_TOKENS = 2048


# ═══════════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are an expert e-commerce copywriter specializing in SEO-optimized product descriptions.

Your writing style:
- Engaging and persuasive, but not pushy
- Focus on benefits, not just features
- Natural keyword integration
- Scannable structure with short paragraphs

NEVER use:
- Generic phrases like "high quality", "best product", "amazing"
- Prices or discounts
- Competitor comparisons
- Unverifiable claims

Return ONLY valid JSON with this structure (no markdown, escape quotes):
{
  "description": "<html description with <p> tags, min 200 words>",
  "seo_title": "max 65 chars — Product Name | Brand",
  "seo_description": "max 155 chars — compelling summary",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}"""


def build_prompt(product_name: str, category: str, features: str) -> str:
    """Build the user prompt for a single product."""
    return f"""Product: {product_name}
Category: {category}
Features: {features}

Generate an SEO-optimized description for this product."""


# ═══════════════════════════════════════════════════════════════
# BATCH PROCESSING
# ═══════════════════════════════════════════════════════════════

def extract_products(input_file: str) -> List[Dict]:
    """Extract products from CSV file."""
    products = []

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row.get('name'):
                continue
            products.append({
                'name': row.get('name', ''),
                'category': row.get('category', ''),
                'features': row.get('features', ''),
                'sku': row.get('sku', ''),
            })

    return products


def sanitize_id(name: str, idx: int) -> str:
    """Generate safe custom_id for Batch API."""
    safe = re.sub(r'[^a-zA-Z0-9_-]', '_', name)[:50]
    return f"{idx:04d}_{safe}"


def submit_batch(products: List[Dict]) -> tuple:
    """Submit batch request to Anthropic API."""
    client = anthropic.Anthropic(api_key=API_KEY)

    requests = []
    id_map = {}

    for idx, product in enumerate(products):
        cid = sanitize_id(product['name'], idx)
        id_map[cid] = product['name']

        prompt = build_prompt(
            product['name'],
            product['category'],
            product['features']
        )

        requests.append({
            "custom_id": cid,
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            }
        })

    print(f"Submitting batch with {len(requests)} requests...")
    batch = client.messages.batches.create(requests=requests)
    print(f"Batch ID: {batch.id}")

    return batch.id, id_map


def wait_for_batch(batch_id: str) -> None:
    """Wait for batch processing to complete."""
    client = anthropic.Anthropic(api_key=API_KEY)

    print(f"Waiting for batch {batch_id}...")
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        done = counts.succeeded + counts.errored + counts.expired + counts.canceled
        total = done + counts.processing

        print(f"  Progress: {done}/{total} (succeeded: {counts.succeeded}, errors: {counts.errored})")

        if batch.processing_status == 'ended':
            print("Batch completed!")
            return

        time.sleep(30)


def collect_results(batch_id: str, id_map: Dict) -> Dict:
    """Collect results from completed batch."""
    client = anthropic.Anthropic(api_key=API_KEY)

    results = {}
    errors = []

    for result in client.messages.batches.results(batch_id):
        cid = result.custom_id
        product_name = id_map.get(cid, cid)

        if result.result.type == 'succeeded':
            text = result.result.message.content[0].text.strip()
            try:
                # Clean markdown code blocks if present
                text = re.sub(r'^```(?:json)?\s*', '', text)
                text = re.sub(r'\s*```$', '', text)
                data = json.loads(text)
                results[product_name] = data
            except json.JSONDecodeError:
                errors.append({'id': cid, 'error': 'json_parse'})
        else:
            errors.append({'id': cid, 'error': result.result.type})

    print(f"Results: {len(results)} OK, {len(errors)} errors")
    return results


def apply_to_csv(results: Dict, input_file: str, output_file: str) -> Dict:
    """Apply generated content back to CSV."""
    stats = {'descriptions': 0, 'titles': 0, 'meta': 0, 'tags': 0}
    rows_out = []

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        headers = reader.fieldnames

        for row in reader:
            name = row.get('name', '')
            if name in results:
                res = results[name]

                if res.get('description'):
                    row['description'] = res['description']
                    stats['descriptions'] += 1

                if res.get('seo_title'):
                    row['seo_title'] = res['seo_title'][:65]
                    stats['titles'] += 1

                if res.get('seo_description'):
                    row['seo_description'] = res['seo_description'][:155]
                    stats['meta'] += 1

                if res.get('tags'):
                    row['tags'] = ', '.join(res['tags'])
                    stats['tags'] += 1

            rows_out.append(row)

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nResults saved to: {output_file}")
    print(f"  Descriptions: {stats['descriptions']}")
    print(f"  SEO Titles: {stats['titles']}")
    print(f"  Meta Descriptions: {stats['meta']}")
    print(f"  Tags: {stats['tags']}")

    return stats


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    if not API_KEY:
        print("Error: ANTHROPIC_API_KEY not set in environment")
        print("Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        return

    # Check for existing batch results
    if os.path.exists(BATCH_FILE):
        print(f"Found existing batch file: {BATCH_FILE}")
        with open(BATCH_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('results'):
            print(f"Using cached results ({len(data['results'])} products)")
            results = data['results']
        else:
            batch_id = data['batch_id']
            with open('id_map.json', 'r', encoding='utf-8') as f:
                id_map = json.load(f)
            wait_for_batch(batch_id)
            results = collect_results(batch_id, id_map)
            data['results'] = results
            with open(BATCH_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        # Extract products
        print(f"Reading products from: {INPUT_CSV}")
        products = extract_products(INPUT_CSV)
        print(f"Found {len(products)} products")

        if not products:
            print("No products found. Check your CSV file.")
            return

        # Submit batch
        batch_id, id_map = submit_batch(products)

        # Save state for resume
        with open(BATCH_FILE, 'w', encoding='utf-8') as f:
            json.dump({'batch_id': batch_id, 'results': None}, f)
        with open('id_map.json', 'w', encoding='utf-8') as f:
            json.dump(id_map, f, ensure_ascii=False, indent=2)

        # Wait and collect
        wait_for_batch(batch_id)
        results = collect_results(batch_id, id_map)

        # Save results
        with open(BATCH_FILE, 'w', encoding='utf-8') as f:
            json.dump({'batch_id': batch_id, 'results': results}, f, ensure_ascii=False, indent=2)

    # Apply to CSV
    apply_to_csv(results, INPUT_CSV, OUTPUT_CSV)


if __name__ == '__main__':
    main()
