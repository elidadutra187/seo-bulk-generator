<div align="center">
  <strong>φ</strong>
  <h1>SEO Bulk Generator</h1>
  <p><em>Generate SEO-optimized product descriptions at scale using Claude API</em></p>
  <p>
    <a href="https://github.com/elidadutra187/seo-bulk-generator">Repository</a> ·
    <a href="https://github.com/elidadutra187">GitHub Profile</a>
  </p>
</div>


## Positioning

This repository is part of the `φ` portfolio by [Élida Dutra](https://github.com/elidadutra187), focused on practical systems for e-commerce, automation, analytics, content generation and growth operations.

**Repository:** [elidadutra187/seo-bulk-generator](https://github.com/elidadutra187/seo-bulk-generator)  
**GitHub:** [https://github.com/elidadutra187](https://github.com/elidadutra187)  
**Purpose:** Generate SEO-optimized product descriptions at scale using Claude API


> Generate SEO-optimized product descriptions at scale using Claude API

## Overview

SEO Bulk Generator is a Python tool that processes large product catalogs and generates professional, SEO-optimized content using Anthropic's Claude API. It leverages the Batch API for cost-effective processing of thousands of products.

Originally developed for an e-commerce operation that needed to process 14,000+ products, this tool generates complete SEO content packages including HTML descriptions, meta titles, meta descriptions, and relevant tags.

The tool is designed for e-commerce managers, SEO specialists, and developers who need to scale content creation without sacrificing quality.

## Stack

- **Language:** Python 3.11+
- **AI:** Anthropic Claude API (Batch API)
- **Model:** Claude Haiku 4.5 (fast, cost-effective)
- **Data:** CSV input/output

## Features

- **Batch Processing:** Process hundreds of products in a single API call
- **Cost-Effective:** Uses Claude Haiku and Batch API for 50% cost reduction
- **Resume Support:** Automatically resumes interrupted batches
- **Rich Output:** HTML descriptions, SEO titles, meta descriptions, tags
- **Customizable Prompts:** Easy to adapt for different niches
- **Progress Tracking:** Real-time batch status updates

## Quick Start

```bash
# Clone the repository
git clone https://github.com/elidadutra/seo-bulk-generator.git
cd seo-bulk-generator

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Anthropic API key

# Prepare your input CSV
cp sample_products.csv products_input.csv
# Edit with your products

# Run the generator
python seo_generator.py
```

## Input CSV Format

Your input CSV should have these columns (semicolon-separated):

| Column | Required | Description |
|--------|----------|-------------|
| `sku` | Yes | Product SKU/ID |
| `name` | Yes | Product name |
| `category` | Yes | Product category |
| `features` | No | Key features/specs |
| `description` | No | Existing description (will be overwritten) |
| `seo_title` | No | Will be generated |
| `seo_description` | No | Will be generated |
| `tags` | No | Will be generated |

Example:

```csv
sku;name;category;features;description;seo_title;seo_description;tags
SKU001;Wireless Headphones Pro;Electronics;Bluetooth 5.0, 40h battery, ANC;;;;
SKU002;Organic Cotton T-Shirt;Clothing;100% organic, unisex, S-XXL;;;;
```

## Output

The script generates:

1. **HTML Description** (min 200 words)
   - Engaging product narrative
   - Scannable structure with `<p>` tags
   - Natural keyword integration

2. **SEO Title** (max 65 chars)
   - Format: `Product Name | Brand`
   - Primary keyword included

3. **Meta Description** (max 155 chars)
   - Compelling summary
   - Call-to-action implied

4. **Tags** (5-12 tags)
   - Relevant keywords
   - Category terms
   - Feature-based tags

## Project Structure

```
seo-bulk-generator/
├── seo_generator.py      # Main script
├── sample_products.csv   # Example input
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── README.md
└── LICENSE
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Claude API key |
| `INPUT_CSV` | No | Input file path (default: products_input.csv) |
| `OUTPUT_CSV` | No | Output file path (default: products_output.csv) |

### Customizing Prompts

Edit the `SYSTEM_PROMPT` in `seo_generator.py` to match your brand voice:

```python
SYSTEM_PROMPT = """You are an expert e-commerce copywriter...
# Add your brand guidelines here
"""
```

## Cost Estimation

Using Claude Haiku via Batch API:

| Products | Estimated Cost | Time |
|----------|----------------|------|
| 100 | ~$0.50 | 5 min |
| 1,000 | ~$5.00 | 30 min |
| 10,000 | ~$50.00 | 3-4 hours |

*Actual costs depend on description length and API pricing.*

## Use Cases

- **E-commerce Migration:** Generate descriptions for new store
- **Catalog Expansion:** Scale product content quickly
- **SEO Refresh:** Update outdated descriptions
- **Multilingual:** Adapt for translation workflows
- **A/B Testing:** Generate multiple description variants

## Roadmap

- [ ] Multi-language support
- [ ] Image analysis integration (Claude Vision)
- [ ] WordPress/Shopify direct upload
- [ ] A/B variant generation
- [ ] Quality scoring

## Author

**Élida Dutra**
Growth Engineer | E-commerce | AI Marketing Automation

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/elidadutra)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/elidadutra)

## License

MIT

---

<p align="center">
  <strong>φ</strong><br>
  <em>Building intelligent systems at the intersection of marketing, data, and AI</em>
</p>

<div align="center">
  <strong>φ</strong>
  <br />
  <sub>Built and maintained by <a href="https://github.com/elidadutra187">Élida Dutra</a>.</sub>
</div>

