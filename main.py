import os
import pandas as pd
import tabula
from PyPDF2 import PdfReader

def extract_tables_from_pdf(file_path, template_path, template_path_2):
    EXPECTED_NUMBER = 5
    test = tabula.read_pdf_with_template(file_path, "./template_perma.json", pages="1", encoding="ISO-8859-1")
    if EXPECTED_NUMBER != len(test[0]):
        print(f"Shift detected in {file_path}. Using the second template.")
        return tabula.read_pdf_with_template(file_path, template_path_2, pages="1", encoding="ISO-8859-1"), True
    return tabula.read_pdf_with_template(file_path, template_path, pages="1", encoding="ISO-8859-1"), False

def select_tables_from_first_pdf(tables):
    selected_tables = []
    for index, table in enumerate(tables):
        print(table)
        user_decision = input(f"Do you want to keep tables like {index}? (y/n): ").lower()
        if user_decision == 'y':
            selected_tables.append(len(table.columns))
    return selected_tables

def get_matching_tables(tables, selected_tables):
    matching_tables = []
    for table in tables:
        if len(table.columns) in selected_tables:
            matching_tables.append(table)
    return matching_tables

def flatten_df(df):
    """Flattens a DataFrame to a single row, including the column names."""
    if df.empty:
        flat_data = df.columns.tolist()
    else:
        flat_data = df.values.flatten().tolist()
    return pd.DataFrame([flat_data])

def main():
    directory = input("Enter path to your directory containing the PDFs: ")
    template_path = input("Enter path to your template JSON file: ")
    template_path_2 = input("Enter path to your template JSON file 2: ")
    all_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    first_pdf_path = os.path.join(directory, all_files[0])
    tables_from_first_pdf, _ = extract_tables_from_pdf(first_pdf_path, template_path, template_path_2)
    selected_tables = select_tables_from_first_pdf(tables_from_first_pdf)
    
    all_selected_data = []
    all_selected_data_shifted = []
    for file in all_files:
        pdf_path = os.path.join(directory, file)
        print(f"Processing {pdf_path}")
        tables, shifted = extract_tables_from_pdf(pdf_path, template_path, template_path_2)
        matching_tables_data = get_matching_tables(tables, selected_tables)
        
        flattened_tables = [flatten_df(table) for table in matching_tables_data]
        
        try:
            single_row = pd.concat(flattened_tables, axis=1, ignore_index=True)
            if shifted:
                all_selected_data_shifted.append(single_row)
            else:
                all_selected_data.append(single_row)
        except ValueError:
            print(f"Error in {pdf_path}. Please check the PDF manually.")
            continue
    
    final_df = pd.concat(all_selected_data, ignore_index=True)
    final_df.to_csv("consolidated_data.csv", index=False)
    
    if all_selected_data_shifted:
        final_df_shifted = pd.concat(all_selected_data_shifted, ignore_index=True)
        final_df_shifted.to_csv("consolidated_data_shifted.csv", index=False)

    print("Processing completed.")

if __name__ == "__main__":
    main()