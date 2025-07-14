import pandas as pd
import os

def create_master_dataframe(file_paths):
    """
    Reads multiple CSV files, extracts relevant data, calculates total time,
    and combines them into a single master DataFrame.

    Args:
        file_paths (list): A list of file paths to the CSV datasets.

    Returns:
        pd.DataFrame: A consolidated DataFrame with all the processed data.
    """
    all_data_frames = []

    # Define the columns that represent individual counts, these might vary
    # based on the maximum 'Count X' in your files. We'll handle this dynamically.
    count_columns_base = ['Count 1', 'Count 2', 'Count 3', 'Count 4', 'Count 5',
                          'Count 6', 'Count 7', 'Count 8', 'Count 9']

    for file_path in file_paths:
        try:
            # Read the CSV, skipping the initial descriptive rows
            # We assume the actual data starts after 'Ground Truth' and blank rows
            # Let's find the start of the data dynamically
            with open(file_path, 'r') as f:
                lines = f.readlines()
                data_start_row = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('Round'):
                        data_start_row = i
                        break
            if data_start_row == 0:
                print(f"Warning: Could not find 'Round' header in {file_path}. Skipping.")
                continue

            df = pd.read_csv(file_path, skiprows=data_start_row)

            # Extract header information (Item and Type) from the first few rows
            # We need to re-read parts of the file for this, or extract from lines
            item_name = pd.read_csv(file_path, nrows=1, header=None).iloc[0, 1].strip()
            system_type = pd.read_csv(file_path, nrows=2, header=None).iloc[1, 1].strip()

            # --- Data Cleaning and Feature Engineering for current DataFrame ---

            # Add 'Item' and 'System_Type' columns
            df['Item'] = item_name
            df['System_Type'] = system_type

            # Convert Min and Sec to Total_Seconds_Per_Round
            # Ensure these columns exist before trying to convert
            if 'Min' in df.columns and 'Sec' in df.columns and 'Sec/100' in df.columns:
                df['Total_Seconds_Per_Round'] = (df['Min'] * 60) + df['Sec'] + (df['Sec/100'] / 100)
            else:
                print(f"Missing time columns in {file_path}. Skipping time calculation.")
                df['Total_Seconds_Per_Round'] = None # Or handle as appropriate

            # Ensure 'Observed Total Count for Round' is numeric
            df['Observed Total Count for Round'] = pd.to_numeric(df['Observed Total Count for Round'], errors='coerce')

            # Ensure 'Accuracy for Round' is numeric
            df['Accuracy for Round'] = pd.to_numeric(df['Accuracy for Round'], errors='coerce')

            # Handle 'Defects for Round': Ensure it's numeric and fill NaN with 0 if appropriate for analysis
            # UPDATED COLUMN NAME HERE:
            if 'Defects' in df.columns: # Check for the old name first
                df.rename(columns={'Defects': 'Defects for Round'}, inplace=True)
            df['Defects for Round'] = pd.to_numeric(df['Defects for Round'], errors='coerce').fillna(0)


            # --- Dynamic handling of Ground Truth and other high-level metrics ---
            # These are typically in the first few rows of each file, above the 'Round' data.
            # Let's re-read the top section to get these.
            meta_data = pd.read_csv(file_path, nrows=data_start_row, header=None, index_col=0)
            meta_data_dict = meta_data.iloc[:, 0].dropna().to_dict()

            df['GT_Number_of_Objects'] = float(meta_data_dict.get('number of objects', float('nan')))
            df['GT_Number_of_Defects'] = float(meta_data_dict.get('number of defects', float('nan')))
            df['GT_Grand_Total_Count'] = float(meta_data_dict.get('GT Grand Total Count', float('nan')))


            # Add 'Notes' if available
            notes_start_row = -1
            for i, line in enumerate(lines):
                if line.strip().lower().startswith('notes'):
                    notes_start_row = i
                    break

            if notes_start_row != -1:
                # Read all lines from notes_start_row + 1 to the end
                notes_lines = lines[notes_start_row + 1:]
                # Filter out empty lines and join them
                notes = [note.strip() for note in notes_lines if note.strip()]
                # Assign the notes as a single string to a new column for this item's dataframe
                # This might be tricky if notes are per-round vs. overall.
                # Assuming overall notes for now, apply to all rows of this item/system.
                df['Notes'] = "\n".join(notes)
            else:
                df['Notes'] = None


            # Select and reorder relevant columns
            # We need to make sure 'Count X' columns are handled gracefully
            # Only keep the 'Count X' columns that exist in the current dataframe
            existing_count_cols = [col for col in count_columns_base if col in df.columns]

            # Define the desired final columns
            final_columns = [
                'Item', 'System_Type', 'Round', 'Min', 'Sec', 'Sec/100', 'Total_Seconds_Per_Round',
                'Defects for Round', 'Observed Total Count for Round', 'Accuracy for Round', # UPDATED COLUMN NAME HERE
                'GT_Number_of_Objects', 'GT_Number_of_Defects', 'GT_Grand_Total_Count', 'Notes'
            ] + existing_count_cols

            # Filter df to only include final_columns that actually exist in the df
            df = df[[col for col in final_columns if col in df.columns]]

            all_data_frames.append(df)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    if not all_data_frames:
        print("No data frames were successfully processed.")
        return pd.DataFrame() # Return empty DataFrame

    master_df = pd.concat(all_data_frames, ignore_index=True)

    return master_df

# --- Usage Example ---
if __name__ == "__main__":
    # Assuming your files are in the same directory as this script,
    # or you provide the full paths.
    # Replace 'path/to/your/files/' with the actual directory if different.
    # Or just list the files if they are in the current working directory.

    data_files = [
        'data/black human.csv',
        'data/black screw AI.csv',
        'data/long screw AI.csv',
        'data/long screw human.csv',
        'data/nail AI.csv',
        'data/nail human.csv',
        'data/nut AI.csv',
        'data/nut human.csv',
        'data/rivet human.csv',
        'data/rivet screw AI.csv',
        'data/tek-screw AI.csv',
        'data/tek-screw human.csv',
        'data/washer AI.csv',
        'data/washer human.csv'
    ]

    # Create a list of full file paths
    current_directory = os.getcwd() # Gets the current working directory
    file_paths = [os.path.join(current_directory, f) for f in data_files]

    # Create the master DataFrame
    master_df = create_master_dataframe(file_paths)

    # Display the first few rows of the consolidated DataFrame
    print("Master DataFrame Head:")
    print(master_df.head())

    # Display basic info to check data types and non-null counts
    print("\nMaster DataFrame Info:")
    master_df.info()

    # Display some descriptive statistics
    print("\nMaster DataFrame Describe (Numeric Columns):")
    print(master_df.describe())

    # Check unique items and system types to confirm parsing
    print("\nUnique Items:", master_df['Item'].unique())
    print("Unique System Types:", master_df['System_Type'].unique())