# PythonGeneralRepository
A repository with the purpose to concentrate the maximum programs content files with small programs that demonstrate a big part of my python habilities skills

# PdfToCsvConversion

Converts PDF documents to CSV format, extracts specific values, and compares them.

This Python script extracts values from PDF documents (receipts and tax forms) that are compressed in a ZIP file. It utilizes the `pypdf2` library to convert PDF files into CSV format and then extracts specific data fields from these files. The script ensures that the extracted values from different PDF documents are compared for consistency, printing an error message if discrepancies are found. Additionally, it appends these extracted values to an existing Excel spreadsheet.

## Installation

1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install pandas pypdf2
