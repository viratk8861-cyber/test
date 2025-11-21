# Sales Data Analyzer

This Python program analyzes sales data from a CSV file and generates a summary report and a bar chart visualization.

## Prerequisites

You need Python 3.x installed. This script relies on `pandas` and `matplotlib`.

To install the required libraries, run:

```bash
pip install pandas matplotlib
```

## Usage

The script accepts a CSV file path as an argument.

```bash
python sales_analyzer.py <path_to_csv_file>
```

### Example

1. Create a `sales_data.csv` file (or use the provided sample if available).
2. Run the script:

```bash
python sales_analyzer.py sales_data.csv
```

3. The script will print a text summary to the console and generate a `sales_chart.png` file in the current directory.

## Input File Format

The CSV file must contain the following columns:
* `Product`: Name of the product
* `Units Sold`: Number of units sold (numeric)
* `Price`: Price per unit (numeric)

Example:

```csv
Product,Units Sold,Price
Widget A,10,5.00
Widget B,5,10.00
```

## Testing

To run the automated tests:

```bash
python test_sales_analyzer.py
```
