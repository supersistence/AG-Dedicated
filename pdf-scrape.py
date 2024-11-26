import os
import tabula
import pandas as pd
import re

# Directory containing the PDF files
pdf_dir = '/Users/hh/Library/Mobile Documents/com~apple~CloudDocs/Documents/GitHub/AG-Dedicated/Dedication History'

# Output directory for CSV files
output_dir = os.path.join(pdf_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

# Extract tables from PDFs
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        output_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}.csv')
        try:
            tabula.convert_into(pdf_path, output_path, output_format='csv', pages='all')
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Tables have been extracted and saved as CSV files.")

# Merge CSV files
dfs = []
year_pattern = re.compile(r'(19|20)\d{2}')  # Matches any 4-digit year starting with 19 or 20

for filename in os.listdir(output_dir):
    if filename.endswith('.csv'):
        csv_path = os.path.join(output_dir, filename)
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            if df.empty:
                print(f"Skipping empty file: {filename}")
                continue

            # Extract year
            match = year_pattern.search(filename)
            year = match.group(0) if match else 'Unknown'

            # Debug filename and extracted year
            print(f"Filename: {filename} | Extracted Year: {year}")

            # Add year to DataFrame
            df['Year'] = year
            dfs.append(df)

        except Exception as e:
            print(f"Error reading {filename}: {e}")

if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_output_path = os.path.join(output_dir, 'merged_output.csv')
    merged_df.to_csv(merged_output_path, index=False)
    print(f"CSV files have been merged into: {merged_output_path}")
else:
    print("No valid CSV files were processed for merging.")

# Check the out 
# Path to the merged_output.csv file
merged_output_path = '/Users/hh/Library/Mobile Documents/com~apple~CloudDocs/Documents/GitHub/AG-Dedicated/Dedication History/output/merged_output.csv'  # Update this to your actual file path


# Review row counts by year in the merged CSV file

# Load the merged CSV file into a DataFrame
try:
    merged_df = pd.read_csv(merged_output_path)
    
    # Check if the 'Year' column exists
    if 'Year' in merged_df.columns:
        # Count the number of rows for each year
        year_counts = merged_df['Year'].value_counts().sort_index()  # Sorted by year for easier reading
        
        # Display the counts
        print("Row counts for each year:")
        print(year_counts)
    else:
        print("The 'Year' column is not present in the merged_output.csv file.")
except FileNotFoundError:
    print("The file 'merged_output.csv' was not found at the specified location.")
except pd.errors.EmptyDataError:
    print("The file 'merged_output.csv' is empty or unreadable.")
except Exception as e:
    print(f"An error occurred: {e}")

# Path to the merged_output.csv file
merged_output_path = '/Users/hh/Library/Mobile Documents/com~apple~CloudDocs/Documents/GitHub/AG-Dedicated/Dedication History/output/merged_output.csv'

# Load the merged CSV file
try:
    # Load the file into a DataFrame
    merged_df = pd.read_csv(merged_output_path)
    
    # Filter rows where 'Petition Number' contains only numeric values
    cleaned_df = merged_df[merged_df['Petition Number'].apply(lambda x: str(x).isdigit())]
    
    # Save the cleaned DataFrame to a new file
    cleaned_output_path = merged_output_path.replace('merged_output.csv', 'cleaned_output.csv')
    cleaned_df.to_csv(cleaned_output_path, index=False)
    
    print(f"Cleaned file saved to: {cleaned_output_path}")
    
except FileNotFoundError:
    print("The file 'merged_output.csv' was not found at the specified location.")
except KeyError:
    print("The 'Petition Number' column was not found in the CSV file.")
except pd.errors.EmptyDataError:
    print("The file 'merged_output.csv' is empty or unreadable.")
except Exception as e:
    print(f"An error occurred: {e}")
