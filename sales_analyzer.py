import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

class SalesAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.summary = {}

    def load_data(self):
        """Reads the CSV file and validates columns."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file '{self.filepath}' was not found.")

        try:
            self.df = pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
            raise ValueError("The CSV file is empty.")
        except pd.errors.ParserError:
            raise ValueError("Error parsing the CSV file.")

        required_columns = {'Product', 'Units Sold', 'Price'}
        if not required_columns.issubset(self.df.columns):
            missing = required_columns - set(self.df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        # Ensure numeric types
        try:
            self.df['Units Sold'] = pd.to_numeric(self.df['Units Sold'])
            self.df['Price'] = pd.to_numeric(self.df['Price'])
        except ValueError:
            raise ValueError("Columns 'Units Sold' and 'Price' must contain numeric data.")

        # Calculate Total Sales per transaction
        self.df['Total Sales'] = self.df['Units Sold'] * self.df['Price']

    def analyze_data(self):
        """Calculates statistics."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Total sales per product
        total_sales_per_product = self.df.groupby('Product')['Total Sales'].sum()

        # Average sales per product (Average transaction value)
        avg_sales_per_product = self.df.groupby('Product')['Total Sales'].mean()

        # Overall total sales
        overall_total_sales = self.df['Total Sales'].sum()

        # Top-selling product (by Revenue)
        if not total_sales_per_product.empty:
            top_product = total_sales_per_product.idxmax()
            top_product_sales = total_sales_per_product.max()
        else:
            top_product = None
            top_product_sales = 0

        self.summary = {
            'total_sales_per_product': total_sales_per_product,
            'avg_sales_per_product': avg_sales_per_product,
            'overall_total_sales': overall_total_sales,
            'top_product': top_product,
            'top_product_sales': top_product_sales
        }

        return self.summary

    def generate_report(self):
        """Generates a text summary."""
        if not self.summary:
            self.analyze_data()

        report = []
        report.append("Sales Summary Report")
        report.append("====================")
        report.append(f"Overall Total Sales: ${self.summary['overall_total_sales']:.2f}")
        report.append("")

        report.append("Top Selling Product:")
        if self.summary['top_product']:
            report.append(f"  {self.summary['top_product']} (${self.summary['top_product_sales']:.2f})")
        else:
            report.append("  N/A")
        report.append("")

        report.append("Sales per Product:")
        for product, sales in self.summary['total_sales_per_product'].items():
            avg = self.summary['avg_sales_per_product'][product]
            report.append(f"  {product}: Total=${sales:.2f}, Avg Transaction=${avg:.2f}")

        return "\n".join(report)

    def plot_sales(self, output_file='sales_chart.png'):
        """Generates a bar chart of sales per product."""
        if not self.summary:
            self.analyze_data()

        data = self.summary['total_sales_per_product']

        if data.empty:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        data.plot(kind='bar', color='skyblue')
        plt.title('Total Sales per Product')
        plt.xlabel('Product')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        try:
            plt.savefig(output_file)
            print(f"Chart saved to {output_file}")
        except Exception as e:
            print(f"Error saving chart: {e}")
        finally:
            plt.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python sales_analyzer.py <csv_file_path>")
        sys.exit(1)

    filepath = sys.argv[1]
    analyzer = SalesAnalyzer(filepath)

    try:
        analyzer.load_data()
        print(analyzer.generate_report())
        analyzer.plot_sales()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
