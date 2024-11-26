import pandas as pd

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
