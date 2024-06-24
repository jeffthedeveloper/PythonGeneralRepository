import pandas as pd
import zipfile
import pypdf2
import os

# Name of the ZIP file
zip_filename = "DAR_ICMS_NORMAL_AND_FUNCEP_062024_173135.zip"

# Open the ZIP file
with zipfile.ZipFile(zip_filename, "r") as zip:
    # Extract files from the ZIP file
    zip.extractall("extracted_files")

# Convert PDF files to CSV format
def convert_pdf_to_csv(pdf_file):
    with open(pdf_file, "rb") as pdf:
        reader = pypdf2.PdfFileReader(pdf)
        return reader.getPage(0).extractText().split("\n")

# Names of the PDF files (generic names)
receipt_transmission_filename = "RECEIPT_TRANSMISSION_062024.pdf"
dar_funcep_filename = "DAR_FUNCEP_062024.pdf"
dar_normal_filename = "DAR_ICMS_NORMAL_062024.pdf"

# Full path of the extracted PDF files
receipt_transmission_path = os.path.join("extracted_files", receipt_transmission_filename)
dar_funcep_path = os.path.join("extracted_files", dar_funcep_filename)
dar_normal_path = os.path.join("extracted_files", dar_normal_filename)

# Open the files
receipt_transmission_values = convert_pdf_to_csv(receipt_transmission_path)
dar_funcep_values = convert_pdf_to_csv(dar_funcep_path)
dar_normal_values = convert_pdf_to_csv(dar_normal_path)

# Extract ICMS guide values
receipt_transmission_values = [line.split("|")[7] for line in receipt_transmission_values]
dar_funcep_values = [line.split("|")[5] for line in dar_funcep_values]
dar_values = [line.split("|")[5] for line in dar_normal_values]

# Compare the values of the three files
for i in range(len(receipt_transmission_values)):
    if receipt_transmission_values[i] != dar_funcep_values[i] or receipt_transmission_values[i] != dar_values[i]:
        print("Error: ICMS guide values do not match.")
        break

# Write the extracted values to an existing Excel spreadsheet
data = {'dar_funcep_value': dar_funcep_values, 'dar_icms_value': dar_values}
df = pd.DataFrame(data)

# Path to the existing Excel file
excel_path = 'existing_excel.xlsx'

# Load the existing Excel file
existing_df = pd.read_excel(excel_path)

# Merge the existing DataFrame with the new data (appending the new data)
result_df = pd.concat([existing_df, df], ignore_index=True)

# Save the merged DataFrame back to the Excel file
result_df.to_excel(excel_path, index=False)
