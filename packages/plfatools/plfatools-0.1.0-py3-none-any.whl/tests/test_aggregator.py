import unittest
import pathlib
import pandas as pd
from plfatools.aggregator import Aggregator

class Test_Aggregator(unittest.TestCase):
    
    def test_transform_raw_to_stacked_returns_expected_format(self):
        # Arrange
        path_to_formatted_xlsx = pathlib.Path.cwd() / "tests" / "assets" /  "PlfaToolAggregator_exampleTransformations.xlsx"
        formatted_xlsx = pd.ExcelFile(str(path_to_formatted_xlsx))
        expected = formatted_xlsx.parse("stacked")
        
        # Act
        actual = Aggregator().transform_raw_to_stacked(
            formatted_xlsx.parse(sheet_name="raw", header=None))

        # Assert
        # Check for same number of columns and same names
        self.assertIsInstance(actual, pd.DataFrame)
        self.assertEqual(len(expected.columns), len(actual.columns))
        self.assertEqual(len(expected.columns.difference(actual.columns)),0)

        # make sure to have the test_ for the unit test.

    def test_transform_stacked_to_tidy_returns_expected_format(self):
        
        path_to_formatted_xlsx = pathlib.Path.cwd() / "tests" / "assets" /  "PlfaToolAggregator_exampleTransformations.xlsx"
        formatted_xlsx = pd.ExcelFile(str(path_to_formatted_xlsx))
        expected = formatted_xlsx.parse("tidy")

        actual = Aggregator().transform_stacked_to_tidy(
            formatted_xlsx.parse(sheet_name="stacked"))

        # Assert
        # Check for same number of columns and same names
        self.assertIsInstance(actual, pd.DataFrame)
        self.assertEqual(len(expected.columns), len(actual.columns))
        self.assertEqual(len(expected.columns.difference(actual.columns)),0)


    def test_read_file_returns_expected_result(self):
        path_to_formatted_xlsx = pathlib.Path.cwd() / "tests" / "assets" /  "PlfaToolAggregator_exampleActualData.xlsx"
        
        actual = Aggregator().read_file(path_to_formatted_xlsx)

        # Assert
        self.assertEqual(4, len(actual))
        self.assertEqual(16, len(actual.columns))
        self.assertEqual(47283.86, round(actual["General FAME"].values[3], 2))


    def test_read_dir_returns_expected_result(self):
        path_to_directory = pathlib.Path.cwd() / "tests" / "assets" / "read_dir"

        actual = Aggregator().read_dir(path_to_directory)

        # Assert
        self.assertEqual(8, len(actual))
        self.assertEqual(16, len(actual.columns))
        self.assertEqual(47283.86, round(actual["General FAME"].values[3], 2))


if __name__ == "__main__":
    unittest.main()