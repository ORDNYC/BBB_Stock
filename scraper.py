import requests
import time
import csv

BASE_URL = "https://babelbooksberlin.com"
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/133.0.0.0 Safari/537.36'
    )
}


def get_all_products():
    """Fetch all products from the Babel Books Berlin Shopify store."""
    all_data = []
    page = 1

    print("Starting extraction from products.json...")

    while True:
        url = f"{BASE_URL}/products.json?limit=250&page={page}"
        print(f"Fetching page {page}...")

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Status: {response.status_code}")
                break

            data = response.json()
            products = data.get('products', [])

            if not products:
                print("No more products found. Extraction complete.")
                break

            for product in products:
                title = product.get('title')

                for variant in product.get('variants', []):
                    isbn = variant.get('barcode') or variant.get('sku') or "N/A"

                    price = variant.get('price')
                    if price:
                        price = float(price)

                    all_data.append({
                        'Book Name': title,
                        'ISBN': isbn,
                        'Price (EUR)': price,
                        'Available': variant.get('available')
                    })

            page += 1
            time.sleep(2)  # Be polite: wait 2 seconds between requests

        except requests.exceptions.RequestException as e:
            print(f"Network error on page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    print(f"Total items extracted: {len(all_data)}")
    return all_data


def save_to_csv(data, filename="books_inventory.csv"):
    """Save the extracted book data to a CSV file."""
    keys = ['Book Name', 'ISBN', 'Price (EUR)', 'Available']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved {len(data)} items to '{filename}'")


if __name__ == "__main__":
    inventory = get_all_products()
    if inventory:
        save_to_csv(inventory)
    else:
        print("No data extracted. Please check the site or your connection.")
