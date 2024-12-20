import wx
import wx.grid as gridlib
import pandas as pd
import os

from database import DatabaseHandler
from report_controller import ReportController

class ReportEditorFrame(wx.Frame):
    def __init__(self, parent, title="ReportEditor"):
        super().__init__(parent, title=title, size=(1000, 700))
        
        # Components
        self.panel = wx.Panel(self)
        self.grid = gridlib.Grid(self.panel)
        self.grid.CreateGrid(0, 0)

        self.db = DatabaseHandler()
        self.controller = ReportController()

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Text fields for report metadata
        self.report_name_label = wx.StaticText(self.panel, label="Report Name:")
        self.report_name_text = wx.TextCtrl(self.panel, value="My Report")

        self.report_date_label = wx.StaticText(self.panel, label="Report Date (YYYY-MM-DD):")
        self.report_date_text = wx.TextCtrl(self.panel, value="2024-01-01")

        self.load_button = wx.Button(self.panel, label="Load CSV")
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        self.generate_button = wx.Button(self.panel, label="Generate Report")
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_report)

        self.save_button = wx.Button(self.panel, label="Save to DB")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_to_db)

        self.reload_button = wx.Button(self.panel, label="Reload from DB")
        self.reload_button.Bind(wx.EVT_BUTTON, self.on_reload_from_db)

        # Add controls to sizer
        control_sizer.Add(self.report_name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        control_sizer.Add(self.report_name_text, 0, wx.ALL, 5)
        control_sizer.Add(self.report_date_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        control_sizer.Add(self.report_date_text, 0, wx.ALL, 5)
        control_sizer.Add(self.load_button, 0, wx.ALL, 5)
        control_sizer.Add(self.generate_button, 0, wx.ALL, 5)
        control_sizer.Add(self.save_button, 0, wx.ALL, 5)
        control_sizer.Add(self.reload_button, 0, wx.ALL, 5)

        main_sizer.Add(control_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)

        # Menu
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit", "Close the application")
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def on_exit(self, event):
        self.Close()

    def on_load_csv(self, event):
        with wx.FileDialog(self, "Open CSV", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled
            path = file_dialog.GetPath()
            if os.path.exists(path):
                self.controller.load_from_csv(path)
                self.populate_grid_from_dataframe(self.controller.get_dataframe())

    def on_generate_report(self, event):
        """Generate a processed report from the current DataFrame."""
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

    def on_save_to_db(self, event):
        """Save the current report data into the database."""
        report_name = self.report_name_text.GetValue()
        report_date = self.report_date_text.GetValue()
        df = self.controller.get_dataframe()

        # Convert DataFrame rows into tuples for DB insertion
        records = [tuple(row) for row in df[['Name', 'Role', 'Department']].to_records(index=False)]
        self.db.insert_report_data(report_name, report_date, records)
        wx.MessageBox("Report saved to the database!", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_reload_from_db(self, event):
        """Reload the data from the database to verify round-trip and updates."""
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

    def populate_grid_from_dataframe(self, df):
        """Clear the grid and populate it with DataFrame data."""
        existing_rows = self.grid.GetNumberRows()
        existing_cols = self.grid.GetNumberCols()

        if existing_cols > 0:
            self.grid.DeleteCols(pos=0, numCols=existing_cols, updateLabels=True)
        if existing_rows > 0:
            self.grid.DeleteRows(pos=0, numRows=existing_rows, updateLabels=True)

        if df.empty:
            return

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