import zipfile
import os
import pandas as pd

def extract_data_from_files(zip_file_path, file_names, column_names, value_column_name, code_column_name):
    # Extract files from the ZIP file using context manager and extractall
    with zipfile.ZipFile(zip_file_path, "r") as zip:
        zip.extractall("arquivo_descompactado")  # Extract to a directory

    # Extract values from the extracted files
    data_frames = []
    for file_name in file_names:
        file_path = os.path.join("arquivo_descompactado", file_name)  # Construct full file path
        with open(file_path, "r") as file:  # Use the corrected file path
            data_frame = pd.DataFrame()
            for line in file:
                values = line.split("|")

                # Ensure the expected number of values in the line
                if len(values) >= max(value_column_name, code_column_name) + 1: 
                    data_frame = data_frame.append({
                        column_names[0]: values[0],  
                        column_names[1]: values[1],
                        value_column_name: values[value_column_name],
                        "Observations": "Correct"  # You might want to customize this based on your data
                    }, ignore_index=True)
            data_frames.append(data_frame)

    # Merge the extracted data frames
    merged_data_frame = pd.concat(data_frames)

    # Save the merged data frame to an OpenDocument spreadsheet (.ods)
    merged_data_frame.to_excel("planilha.ods", engine='odf', index=False)

# Example usage
zip_file_path = "arquivo.zip"
file_names = ["new_name_1.txt", "new_name_2.txt", "new_name_3.txt"]
column_names = ["Data", "Código"] 
value_column_name = 7
code_column_name = 1

extract_data_from_files(zip_file_path, file_names, column_names, value_column_name, code_column_name)
