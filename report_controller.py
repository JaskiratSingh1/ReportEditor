import pandas as pd

class ReportController:
    def __init__(self):
        self.df = pd.DataFrame()

    # Load data from a CSV file into a DataFrame
    def load_from_csv(self, filepath):
        self.df = pd.read_csv(filepath)

    # Get the current DataFrame
    def get_dataframe(self):
        return self.df.copy()

    # Replace the current DataFrame with a new one
    def update_dataframe(self, df):
        """Replace the current DataFrame with a new one."""
        self.df = df.copy()

    # Generate a processed report from the current DataFrame
    def generate_report(self, report_name, report_date):
        # For demonstration, just ensure the columns are present.
        # In a real scenario, there will be validation, filtering, aggregation, etc.
        if 'Name' not in self.df.columns or 'Role' not in self.df.columns or 'Department' not in self.df.columns:
            raise ValueError("CSV does not contain required columns for report.")

        # Sort by name for consistency
        self.df = self.df.sort_values(by='Name')

        # The report_name and report_date fields are metadata and they will be saved to the DB along with the records
        return report_name, report_date, self.df