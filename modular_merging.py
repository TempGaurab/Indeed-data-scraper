import pandas as pd
from datetime import datetime
import os
import glob
import shutil
#DONOT RUN THIS CODE UNTIL YOU HAVE GOT ALL THE PAGES SCRAPED INTO THE Designated onepage-csvfiles folder. Then only execute this code.

def getfiles(directory_path):
    try:
        all_files = os.listdir(directory_path)
        print(f"All files in the directory: {all_files}")
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
        all_files = []
    # Use glob to get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    return csv_files

def output_pathh(csv_files):
    first_file_name = os.path.basename(csv_files[0])
    parts = first_file_name.split('-')
    if len(parts) >= 3:
        role = parts[0]
        location = parts[1].split('Page')[0].rstrip('-')

        # Construct the output path
        output_path = f'combined_{role}_{location}_data.csv'
    else:
        output_path = 'combined_data.csv'
    return output_path

def combine(csv_files):
    # Read each CSV file into a Pandas dataframe and concatenate them into a single dataframe
    dataframes = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(dataframes, ignore_index=True)
    df['Scraped_On'] = datetime.today().strftime('%Y-%m-%d')
    return df

def move_old_files(directory_path, old_files_folder):
    if not os.path.exists(old_files_folder):
        os.makedirs(old_files_folder)
    
    # Move each file from the directory to the old_files folder
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            shutil.move(file_path, os.path.join(old_files_folder, file_name))
            print(f"Moved file: {file_name} to {old_files_folder}")

def main():
    directory_path =  os.getcwd() + "\onepage-csvfiles"
    csv_files = getfiles(directory_path)
    old_files_folder = directory_path +  "\old_files"
    if csv_files:
        output_path = output_pathh(csv_files)
        df = combine(csv_files)
        output_path = os.getcwd() + "\datasets"+"\\"+ output_path
        df.to_csv(output_path, index=False)
        print(f"Combined data saved to: {output_path}")
    else:
        print("No_csv_file_found")
    #now save those datasets to the old_files folder.
    if os.path.exists(old_files_folder):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.csv'):
                shutil.move(file_path, os.path.join(old_files_folder, file_name))
                print(f"Moved file: {file_name} to {old_files_folder}")


if __name__ == "__main__":
    main()