import sqlite3

class DatabaseHandler:
    def __init__(self, db_path='my_report_data.db'):
        # Use a file-based database for persistence
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        # Create a table for report data if it doesn’t exist.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS report_data (
                ReportName TEXT,
                ReportDate TEXT,
                Name TEXT,
                Role TEXT,
                Department TEXT
            )
        ''')
        self.conn.commit()

    """
    Insert records into the database.
    Returns: a list of tuples: [(Name, Role, Department), ...]
    """
    def insert_report_data(self, report_name, report_date, records):
        cursor = self.conn.cursor()
        
        # Clear old data for demonstration purposes
        cursor.execute("DELETE FROM report_data")

        # Insert new data
        for rec in records:
            cursor.execute(
                'INSERT INTO report_data (ReportName, ReportDate, Name, Role, Department) VALUES (?, ?, ?, ?, ?)',
                (report_name, report_date) + rec
            )

        # Commit the transaction
        self.conn.commit()
        print("Inserted", len(records), "records into the database.")

    """
    Load data from the database into a list of tuples.
    Returns: (report_name, report_date, [(Name, Role, Department), ...])
    """
    def load_report_data(self):
        # Fetch all records from the table
        cursor = self.conn.cursor()
        cursor.execute("SELECT ReportName, ReportDate, Name, Role, Department FROM report_data")
        rows = cursor.fetchall()
        if rows:
            # Assume all rows have the same report name and date for demonstration
            report_name = rows[0][0]
            report_date = rows[0][1]
            records = [(r[2], r[3], r[4]) for r in rows]
            return report_name, report_date, records
        return None, None, []