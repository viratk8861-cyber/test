import unittest
import pandas as pd
import os
from sales_analyzer import SalesAnalyzer

class TestSalesAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.test_file = 'test_sales_data.csv'
        data = {
            'Product': ['A', 'B', 'A', 'C'],
            'Units Sold': [10, 5, 2, 1],
            'Price': [5.0, 10.0, 5.0, 20.0]
        }
        # A: 10*5 + 2*5 = 50 + 10 = 60. Avg: 30
        # B: 5*10 = 50. Avg: 50
        # C: 1*20 = 20. Avg: 20
        # Total: 130
        # Top: A

        df = pd.DataFrame(data)
        df.to_csv(self.test_file, index=False)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists('test_chart.png'):
            os.remove('test_chart.png')

    def test_load_data_success(self):
        analyzer = SalesAnalyzer(self.test_file)
        analyzer.load_data()
        self.assertIsNotNone(analyzer.df)
        self.assertEqual(len(analyzer.df), 4)
        self.assertIn('Total Sales', analyzer.df.columns)

    def test_file_not_found(self):
        analyzer = SalesAnalyzer('non_existent.csv')
        with self.assertRaisesRegex(FileNotFoundError, "not found"):
            analyzer.load_data()

    def test_missing_columns(self):
        bad_file = 'bad_sales_data.csv'
        pd.DataFrame({'Product': [], 'Price': []}).to_csv(bad_file, index=False)
        analyzer = SalesAnalyzer(bad_file)
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            analyzer.load_data()
        os.remove(bad_file)

    def test_calculations(self):
        analyzer = SalesAnalyzer(self.test_file)
        analyzer.load_data()
        summary = analyzer.analyze_data()

        self.assertEqual(summary['overall_total_sales'], 130.0)
        self.assertEqual(summary['top_product'], 'A')
        self.assertEqual(summary['top_product_sales'], 60.0)

        # Check 'A' sales
        self.assertEqual(summary['total_sales_per_product']['A'], 60.0)
        self.assertEqual(summary['avg_sales_per_product']['A'], 30.0)

    def test_plot_generation(self):
        analyzer = SalesAnalyzer(self.test_file)
        analyzer.load_data()
        analyzer.plot_sales('test_chart.png')
        self.assertTrue(os.path.exists('test_chart.png'))

    def test_empty_file(self):
        empty_file = 'empty.csv'
        open(empty_file, 'w').close()
        analyzer = SalesAnalyzer(empty_file)
        with self.assertRaisesRegex(ValueError, "is empty"):
            analyzer.load_data()
        os.remove(empty_file)

if __name__ == '__main__':
    unittest.main()
