# ReportEditor

**ReportEditor** is a Python-based application showcasing the integration of a graphical user interface (GUI) into an existing report-editing workflow. This project demonstrates how a user-friendly, visually intuitive interface can streamline processes and reduce reliance on command-line operations.

## Key Features

- **Dynamic GUI (wxPython):**
  - A responsive GUI that adjusts dynamically as the window is resized, ensuring usability across various screen sizes.
  - Wrap-around buttons and controls that reorganize themselves when the window width is reduced.
- **Data Manipulation (Pandas):**
  - Efficient loading, editing, and processing of CSV data using Pandas.
  - Features for adding rows and columns dynamically to the loaded dataset.
- **Database Interaction (SQLite):**
  - Seamless integration with an SQLite database for saving and retrieving reports.
  - Persistent data storage ensures that reports can be reloaded and modified across application sessions.
- **Report Customization:**
  - Editable fields for report metadata, including "Report Name" and "Report Date."
  - Real-time updates to the displayed dataset after processing or user interactions.
- **Code Quality & Style:**
  - Clear structure, meaningful variable names, and organized code for maintainability and scalability.

## How It Works

1. **Load Data:**
   - Use the "Load CSV" button to select a CSV file containing report data.
2. **Edit Data:**
   - Add rows or columns dynamically using the respective buttons.
   - Modify "Report Name" and "Report Date" directly in the provided text fields.
3. **Generate Report:**
   - Use the "Generate Report" button to process and display the data in a clean, sorted format.
4. **Save Data:**
   - Save the report (with metadata and table content) to an SQLite database using the "Save to DB" button.
5. **Reload Data:**
   - Retrieve and view previously saved reports using the "Reload from DB" button.

## Future Enhancements

Should this concept proceed beyond the demo stage, the following improvements may be implemented:

- **Enhanced Design:**
  - Adopting formal UI/UX guidelines for a polished, professional interface.
- **Automated Testing:**
  - Implementing unit tests with frameworks like `pytest` to ensure robust, maintainable code.

**Note:** This project is a proof of concept to demonstrate coding practices, GUI design, and data handling workflows. Additional features and refinements can be tailored to meet the specific requirements of a full-scale implementation.
