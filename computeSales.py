'''
Compute the total sales cost from a product catalogue and a sales record.

Reads two JSON files:
1) A product catalogue with title and price.
2) A sales record with product names and quantities.

The program calculates the total cost of all valid sales,
prints the results to the console and writes them to SalesResults.txt.

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json
'''

import json
import sys
import time

RESULT_FILE = "SalesResults.txt"


def print_error(message):
    '''
    Print an error message to the console.
    '''
    print(f"ERROR: {message}")


def load_json_file(filename):
    '''
    Load and parse a JSON file.

    Returns the parsed object or terminates if the file cannot be read.
    '''
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print_error(f"File not found: {filename}")
        sys.exit(1)
    except json.JSONDecodeError:
        print_error(f"Invalid JSON format in file: {filename}")
        sys.exit(1)


def build_price_dictionary(catalogue):
    '''
    Build a dictionary with product title as key and price as value.
    Invalid entries are ignored.
    '''
    prices = {}

    for item in catalogue:
        if not isinstance(item, dict):
            print_error("Invalid product entry (skipped)")
            continue

        title = item.get("title")
        price = item.get("price")

        if not isinstance(title, str):
            print_error("Product without valid title (skipped)")
            continue

        if not isinstance(price, (int, float)):
            print_error(f"Product '{title}' has invalid price (skipped)")
            continue

        prices[title] = float(price)

    return prices


def compute_total_sales(sales, prices):
    '''
    Compute the total sales amount using the price dictionary.
    Invalid sales rows are ignored.
    '''
    total = 0.0

    for sale in sales:
        if not isinstance(sale, dict):
            print_error("Invalid sale entry (skipped)")
            continue

        product = sale.get("Product")
        quantity = sale.get("Quantity")

        if not isinstance(product, str):
            print_error("Sale without valid product name (skipped)")
            continue

        if not isinstance(quantity, int):
            print_error(f"Invalid quantity for product '{product}' (skipped)")
            continue

        if product not in prices:
            print_error(
                f"Product '{product}' not found in catalogue (skipped)"
            )
            continue

        total += prices[product] * quantity

    return total


def save_results(text):
    '''
    Save the result text to the output file.
    '''
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    '''
    Main execution of the program.
    '''
    start_time = time.time()

    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )

        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue = load_json_file(catalogue_file)
    sales = load_json_file(sales_file)

    if not isinstance(catalogue, list):
        print_error("Catalogue file must contain a list")
        sys.exit(1)

    if not isinstance(sales, list):
        print_error("Sales file must contain a list")
        sys.exit(1)

    prices = build_price_dictionary(catalogue)
    total_sales = compute_total_sales(sales, prices)

    elapsed_time = time.time() - start_time

    results = (
        "Compute Sales - Results\n"
        "----------------------\n"
        f"Catalogue file: {catalogue_file}\n"
        f"Sales file: {sales_file}\n\n"
        f"TOTAL SALES: {total_sales:.2f}\n\n"
        f"Elapsed time (s): {elapsed_time}\n"
    )

    print(results)
    save_results(results)


if __name__ == "__main__":
    main()
