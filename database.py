import sqlite3

class DatabaseHandler:
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        # Create a table for report data if it doesn’t exist
        # Adjust schema as needed (here we assume 'report_data' with Name, Role, Department plus meta fields)
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

    def insert_report_data(self, report_name, report_date, records):
        """
        Insert records into the database.
        records is a list of tuples: [(Name, Role, Department), ...]
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM report_data")  # Clear old data for demo purposes
        for rec in records:
            cursor.execute('INSERT INTO report_data (ReportName, ReportDate, Name, Role, Department) VALUES (?, ?, ?, ?, ?)',
                           (report_name, report_date) + rec)
        self.conn.commit()

    def load_report_data(self):
        """
        Load data from the database into a list of tuples.
        Returns:
          (report_name, report_date, [(Name, Role, Department), ...])
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT ReportName, ReportDate, Name, Role, Department FROM report_data")
        rows = cursor.fetchall()
        if rows:
            # We assume all rows have the same report name and date for simplicity
            report_name = rows[0][0]
            report_date = rows[0][1]
            records = [(r[2], r[3], r[4]) for r in rows]
            return report_name, report_date, records
        return None, None, []