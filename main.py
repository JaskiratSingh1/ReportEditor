import wx
import wx.grid as gridlib
import pandas as pd
import sqlite3  # Example of a simple SQL integration (in-memory SQLite)
import os

class ReportEditorFrame(wx.Frame):
    def __init__(self, parent, title="ReportEditor"):
        super().__init__(parent, title=title, size=(800, 600))
        
        # Initialize UI components
        self.panel = wx.Panel(self)
        self.grid = gridlib.Grid(self.panel)
        self.grid.CreateGrid(0, 0)
        
        # Database placeholder: Create an in-memory SQLite database for demonstration
        self.conn = sqlite3.connect(':memory:')

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Buttons
        self.load_button = wx.Button(self.panel, label="Load CSV")
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        self.sql_button = wx.Button(self.panel, label="Run SQL Query")
        self.sql_button.Bind(wx.EVT_BUTTON, self.on_run_sql)

        button_sizer.Add(self.load_button, 0, wx.ALL, 5)
        button_sizer.Add(self.sql_button, 0, wx.ALL, 5)

        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)

        # Create a menu for demonstration
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit", "Close the application")
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def on_exit(self, event):
        self.Close()

    def on_load_csv(self, event):
        """Open a file dialog to load a CSV using Pandas and display it in the grid."""
        with wx.FileDialog(self, "Open CSV", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled

            path = file_dialog.GetPath()
            if os.path.exists(path):
                self.load_data_into_grid(path)

    def load_data_into_grid(self, filepath):
        """Load CSV data into Pandas DataFrame and then populate the wxGrid."""
        try:
            df = pd.read_csv(filepath)
            self.populate_grid_from_dataframe(df)

            # Also load DataFrame into SQLite for demonstration
            df.to_sql('report_data', self.conn, if_exists='replace', index=False)
        except Exception as e:
            wx.MessageBox(f"Error loading file: {e}", "Error", wx.ICON_ERROR)

    def populate_grid_from_dataframe(self, df):
        """Clear the grid and populate it with DataFrame data."""
        # Clear the grid first only if there are existing rows/columns
        existing_rows = self.grid.GetNumberRows()
        existing_cols = self.grid.GetNumberCols()

        if existing_cols > 0:
            self.grid.DeleteCols(pos=0, numCols=existing_cols, updateLabels=True)
        if existing_rows > 0:
            self.grid.DeleteRows(pos=0, numRows=existing_rows, updateLabels=True)

        # Set column and row counts based on DataFrame
        self.grid.AppendCols(len(df.columns))
        self.grid.AppendRows(len(df.index))

        # Set column headers
        for col_index, col_name in enumerate(df.columns):
            self.grid.SetColLabelValue(col_index, col_name)

        # Fill the grid
        for row_index in range(len(df.index)):
            for col_index in range(len(df.columns)):
                self.grid.SetCellValue(row_index, col_index, str(df.iat[row_index, col_index]))

        self.grid.AutoSizeColumns()

    def on_run_sql(self, event):
        """Demonstration of running a SQL query on loaded data."""
        # If no data loaded yet, show a message
        cursor = self.conn.cursor()
        try:
            # Example query: select all rows
            cursor.execute("SELECT * FROM report_data")
            results = cursor.fetchall()

            if not results:
                wx.MessageBox("No data available. Please load a CSV file first.", "No Data", wx.ICON_INFORMATION)
                return

            # Convert results back into a DataFrame to show in the grid
            col_names = [description[0] for description in cursor.description]
            df = pd.DataFrame(results, columns=col_names)
            self.populate_grid_from_dataframe(df)

        except sqlite3.OperationalError:
            wx.MessageBox("No table found. Please load CSV data first.", "SQL Error", wx.ICON_ERROR)
        finally:
            cursor.close()

class ReportEditorApp(wx.App):
    def OnInit(self):
        frame = ReportEditorFrame(None)
        frame.Show()
        return True

if __name__ == "__main__":
    app = ReportEditorApp(False)
    app.MainLoop()