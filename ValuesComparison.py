import pandas as pd
import zipfile
import PyPDF2
import os

# Define the ZIP file path
zip_file_path = "file.zip"

# Extract files from the ZIP file using context manager and extractall
with zipfile.ZipFile(zip_file_path, "r") as zip_file:
    zip_file.extractall("DecompressedFiles")  # Extract to a directory


# Function to convert PDF to CSV (using a more robust method)
def convert_pdf_to_csv(pdf_file):
    with open(pdf_file, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)  
        num_pages = len(reader.pages)
        data = []
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            data.extend(text.split("\n"))
        return data  # Return all extracted lines

# Extract data from PDF files (using the corrected paths)
file_transmission_data = convert_pdf_to_csv("DecompressedFiles/file_transmission.pdf")
taxDate = convert_pdf_to_csv("DecompressedFiles/tax_benefits.pdf")
guideDate = convert_pdf_to_csv("DecompressedFiles/dar.pdf")

# Extract taxMarketShare values (handling potential IndexError)
file_transmission_values = []
taxValues = []
guideValues = []
for line in file_transmission_data:
    parts = line.split("|")
    if len(parts) > 7:
        file_transmission_values.append(parts[7])
for line in taxDate:
    parts = line.split("|")
    if len(parts) > 5:
        taxValues.append(parts[5])
for line in guideDate:
    parts = line.split("|")
    if len(parts) > 5:
        guideValues.append(parts[5])

# Compare taxMarketShare values with error handling (zip) for better performance
for file_trans, tax, guide in zip(file_transmission_values, taxValues, guideValues):
    if file_trans != tax or tax != guide:  # Check if any pair doesn't match
        print(f"Error: DocumentValue of taxMarketShare doesn't match in line '{file_trans}|{tax}|{guide}'")
        break
else:
    print("All taxMarketShare values match across documents.")  # Indicate success if loop completes



# Create a new Excel spreadsheet in .odt format (OpenDocument format)
taxMarketShare_data = {
    "Date Limit": [line.split("|")[0] for line in file_transmission_data if len(line.split("|")) > 0],  # Error handling for index
    "Code Representation": [line.split("|")[1] for line in file_transmission_data if len(line.split("|")) > 1],
    "Document Value": file_transmission_values[:len(file_transmission_data)]  # Handle length differences
}

taxMarketShare_data_frame = pd.DataFrame(taxMarketShare_data)
taxMarketShare_data_frame.to_excel("SpreadSheet.odt", engine='odf', index=False)  # Save as .odt
