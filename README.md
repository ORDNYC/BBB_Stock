# 📚 Babel Books Berlin — Inventory Scraper

A lightweight Python scraper that extracts the full book inventory from [Babel Books Berlin](https://babelbooksberlin.com) using their public Shopify `products.json` API and saves it to a CSV file.

## Output

The script generates a `books_inventory.csv` file with the following columns:

| Column | Description |
|---|---|
| `Book Name` | Title of the book |
| `ISBN` | ISBN / barcode (falls back to SKU if unavailable) |
| `Price (EUR)` | Price in euros |
| `Available` | Whether the variant is currently in stock |

## Requirements

- Python 3.8+
- [`requests`](https://pypi.org/project/requests/)

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/babel-books-scraper.git
cd babel-books-scraper

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python scraper.py
```

The script will print progress to the console and save results to `books_inventory.csv` in the current directory.

## How It Works

1. Iterates through pages of `products.json?limit=250&page=N` (Shopify's public API).
2. For each product, extracts all variants (a book may have multiple editions/formats).
3. Reads the barcode field as ISBN, with SKU as a fallback.
4. Waits **2 seconds between pages** to avoid hammering the server.
5. Stops when a page returns no products.

## Notes

- This scraper only accesses **publicly available data** via Shopify's standard read-only API endpoint.
- Please use responsibly and respect the store's terms of service.
- The 2-second delay between requests is intentional — do not remove it.

## License

MIT
