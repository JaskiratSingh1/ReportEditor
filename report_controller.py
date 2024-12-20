import pandas as pd

class ReportController:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_from_csv(self, filepath):
        self.df = pd.read_csv(filepath)

    def get_dataframe(self):
        return self.df.copy()

    def update_dataframe(self, df):
        """Replace the current DataFrame with a new one."""
        self.df = df.copy()

    def generate_report(self, report_name, report_date):
        # Placeholder for any processing steps.
        # For demonstration, we just ensure the columns (Name, Role, Department) are present.
        # In real scenario, you might do validation, filtering, aggregation, etc.
        if 'Name' not in self.df.columns or 'Role' not in self.df.columns or 'Department' not in self.df.columns:
            raise ValueError("CSV does not contain required columns for report.")

        # Example: Maybe we sort by Name for a "clean" report.
        self.df = self.df.sort_values(by='Name')

        # The report_name and report_date fields are metadata, not necessarily columns in the DataFrame.
        # They will be saved to the DB along with the records.
        return report_name, report_date, self.df