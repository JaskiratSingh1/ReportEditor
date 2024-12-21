import wx
import wx.grid as gridlib
import pandas as pd
import os

# Local imports
from database import DatabaseHandler
from report_controller import ReportController

# Main frame for the application
class ReportEditorFrame(wx.Frame):
    def __init__(self, parent, title="ReportEditor"):
        # Set the initial window size to 1000x700 pixels for optimal viewing
        super().__init__(parent, title=title, size=(1000, 700))
        
        # Components
        self.panel = wx.Panel(self)
        self.grid = gridlib.Grid(self.panel)
        self.grid.CreateGrid(0, 0)

        # Data handlers
        self.db = DatabaseHandler()
        self.controller = ReportController()

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Use a WrapSizer so that controls wrap to a new line when width is reduced
        wrap_sizer = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        # Text fields for report name
        self.report_name_label = wx.StaticText(self.panel, label="Report Name:")
        self.report_name_text = wx.TextCtrl(self.panel, value="My Report")

        # Text fields for report date
        self.report_date_label = wx.StaticText(self.panel, label="Report Date (YYYY-MM-DD):")
        self.report_date_text = wx.TextCtrl(self.panel, value="2024-01-01")

        # Button for loading data
        self.load_button = wx.Button(self.panel, label="Load CSV")
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        # Button for report generation
        self.generate_button = wx.Button(self.panel, label="Generate Report")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_report)

        # Buttons for saving data
        self.save_button = wx.Button(self.panel, label="Save to DB")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_to_db)

        # Button for reloading data
        self.reload_button = wx.Button(self.panel, label="Reload from DB")
        self.reload_button.Bind(wx.EVT_BUTTON, self.on_reload_from_db)

        # Button for adding rows
        self.add_row_button = wx.Button(self.panel, label="Add Row")
        self.add_row_button.Bind(wx.EVT_BUTTON, self.on_add_row)

        # Button for adding columns
        self.add_column_button = wx.Button(self.panel, label="Add Column")
        self.add_column_button.Bind(wx.EVT_BUTTON, self.on_add_column)

        # All controls that should wrap to the wrap_sizer
        wrap_sizer.Add(self.report_name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        wrap_sizer.Add(self.report_name_text, 0, wx.ALL, 5)
        wrap_sizer.Add(self.report_date_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        wrap_sizer.Add(self.report_date_text, 0, wx.ALL, 5)
        wrap_sizer.Add(self.load_button, 0, wx.ALL, 5)
        wrap_sizer.Add(self.generate_button, 0, wx.ALL, 5)
        wrap_sizer.Add(self.save_button, 0, wx.ALL, 5)
        wrap_sizer.Add(self.reload_button, 0, wx.ALL, 5)
        wrap_sizer.Add(self.add_row_button, 0, wx.ALL, 5)
        wrap_sizer.Add(self.add_column_button, 0, wx.ALL, 5)

        # Give the grid a proportion of 1 so it expands when the window is resized
        main_sizer.Add(wrap_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)

        # Menu
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit", "Close the application")
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        # Fit the layout to the content and allow dynamic resizing
        self.Layout()
        self.SetMinSize((600, 400)) # Minimum size to prevent clipping
        self.Centre()

    # Exit the application
    def on_exit(self, event):
        self.Close()

    """Load data from a CSV file into the DataFrame"""
    def on_load_csv(self, event):
        with wx.FileDialog(self, "Open CSV", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            
            # If the user cancels the dialog, return early
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled
            path = file_dialog.GetPath()

            # Load the CSV file into the DataFrame
            if os.path.exists(path):
                self.controller.load_from_csv(path)
                self.populate_grid_from_dataframe(self.controller.get_dataframe())

    """Generate a processed report from the current DataFrame"""
    def on_generate_report(self, event):
        # Get the report metadata from the text fields
        report_name = self.report_name_text.GetValue()
        report_date = self.report_date_text.GetValue()
        try:
            # Perform any data manipulation needed for a "final" report
            report_name, report_date, df = self.controller.generate_report(report_name, report_date)
            # Update the UI with the processed/cleaned data
            self.populate_grid_from_dataframe(df)
            wx.MessageBox("Report generated successfully!", "Info", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    """Save the current report data into the database"""
    def on_save_to_db(self, event):
        # Get the report metadata from the text fields
        report_name = self.report_name_text.GetValue()
        report_date = self.report_date_text.GetValue()
        df = self.controller.get_dataframe()

        # If DataFrame doesn't have the required columns, warn the user.
        required_cols = {'Name', 'Role', 'Department'}
        if not required_cols.issubset(set(df.columns)):
            wx.MessageBox("Cannot save to DB. DataFrame missing required columns (Name, Role, Department).", 
                          "Error", wx.OK | wx.ICON_ERROR)
            return

        # Convert DataFrame rows into tuples for DB insertion
        records = [tuple(row) for row in df[['Name', 'Role', 'Department']].to_records(index=False)]
        self.db.insert_report_data(report_name, report_date, records)
        wx.MessageBox("Report saved to the database!", "Info", wx.OK | wx.ICON_INFORMATION)

    """Reload the data from the database to verify round-trip and updates"""
    def on_reload_from_db(self, event):
        # Load data from the database
        report_name, report_date, records = self.db.load_report_data()
        if records:
            # Update metadata fields
            self.report_name_text.SetValue(report_name if report_name else "No Name")
            self.report_date_text.SetValue(report_date if report_date else "2024-01-01")

            # Convert back to DataFrame
            df = pd.DataFrame(records, columns=['Name', 'Role', 'Department'])
            self.controller.update_dataframe(df)
            self.populate_grid_from_dataframe(df)
            wx.MessageBox("Data reloaded from DB!", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("No data found in the database.", "Info", wx.OK | wx.ICON_INFORMATION)

    """Add a new blank row to the current DataFrame"""
    def on_add_row(self, event):
        df = self.controller.get_dataframe()
        if df.empty:
            # If empty, create a default set of columns for demonstration
            df = pd.DataFrame(columns=['Name', 'Role', 'Department'])
        
        # Add a blank row
        new_row = {col: "" for col in df.columns}
        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.controller.update_dataframe(new_df)
        self.populate_grid_from_dataframe(new_df)

    """Prompt for a new column name and add it to the DataFrame"""
    def on_add_column(self, event):
        # Prompt for a new column name
        dlg = wx.TextEntryDialog(self, "Enter the new column name:", "Add Column")
        if dlg.ShowModal() == wx.ID_OK:
            new_col_name = dlg.GetValue().strip()
            if new_col_name:
                df = self.controller.get_dataframe()
                if new_col_name in df.columns:
                    wx.MessageBox("Column already exists. Please choose a different name.", "Error", wx.OK | wx.ICON_ERROR)
                else:
                    # Add the new column with empty strings
                    df[new_col_name] = ""
                    self.controller.update_dataframe(df)
                    self.populate_grid_from_dataframe(df)
        dlg.Destroy()

    """Clear the grid and populate it with DataFrame data"""
    def populate_grid_from_dataframe(self, df):
        existing_rows = self.grid.GetNumberRows()
        existing_cols = self.grid.GetNumberCols()

        # Clear the grid
        if existing_cols > 0:
            self.grid.DeleteCols(pos=0, numCols=existing_cols, updateLabels=True)
        if existing_rows > 0:
            self.grid.DeleteRows(pos=0, numRows=existing_rows, updateLabels=True)

        if df.empty:
            return

        # Add rows and columns to the grid
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

class ReportEditorApp(wx.App):
    def OnInit(self):
        frame = ReportEditorFrame(None)
        frame.Show()
        return True

if __name__ == "__main__":
    app = ReportEditorApp(False)
    app.MainLoop()