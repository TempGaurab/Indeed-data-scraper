import pandas as pd
from datetime import datetime
import os
import glob
# Define the path to the directory containing the CSV files
directory_path =  os.getcwd() + "\onepage-csvfiles"
# List all files in the directory to verify contents (use try-except to handle errors)
try:
    all_files = os.listdir(directory_path)
    print(f"All files in the directory: {all_files}")
except FileNotFoundError:
    print(f"Error: Directory '{directory_path}' not found.")
    all_files = []

# Use glob to get all CSV files in the directory
csv_files = glob.glob(os.path.join(directory_path, "*.csv"))

if csv_files:
    # Extract role and location from the first file's name
    first_file_name = os.path.basename(csv_files[0])
    parts = first_file_name.split('-')
    
    if len(parts) >= 3:
        role = parts[1]
        location = parts[2].split('Page')[0].rstrip('-')

        # Construct the output path
        output_path = f'combined_{role}_{location}_data.csv'
    else:
        output_path = 'combined_data.csv'
    
    # Read each CSV file into a Pandas dataframe and concatenate them into a single dataframe
    dataframes = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(dataframes, ignore_index=True)

    # Add a new column with the current date
    df['Scraped_On'] = datetime.today().strftime('%Y-%m-%d')

    # Display the dataframe
    print(df)
    output_path = os.getcwd() + "\datasets"+"\\"+ output_path
    # Save the concatenated dataframe to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"Combined data saved to: {output_path}")
else:
    print("No CSV files found in the specified directory.")


