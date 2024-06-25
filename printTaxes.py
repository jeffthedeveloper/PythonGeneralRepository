import PyPDF2

def extract_taxes(filename):

  # Open the PDF file
  pdf = PyPDF2.PdfFileReader(filename)

  # Get the first page
  page = pdf.getPage(0)

  # Extract the taxes from the page
  taxes = page.extractText().split(";")

  # Return the taxes
  return taxes


# Get the filenames of all the PDF files
filenames = ["file1.pdf", "file2.pdf", "file3.pdf"]

# Extract the taxes from all the files
taxes = []
for filename in filenames:
  taxes.extend(extract_taxes(filename))

# Print the taxes
print(taxes)
