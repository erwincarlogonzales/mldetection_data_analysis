# import pandas as pd
# import os

# def create_master_dataframe(file_paths):
#     """
#     Reads multiple CSV files, extracts relevant data, calculates total time,
#     and combines them into a single master DataFrame.

#     Args:
#         file_paths (list): A list of file paths to the CSV datasets.

#     Returns:
#         pd.DataFrame: A consolidated DataFrame with all the processed data.
#     """
#     all_data_frames = []

#     # Define the columns that represent individual counts, these might vary
#     # based on the maximum 'Count X' in your files. We'll handle this dynamically.
#     count_columns_base = ['Count 1', 'Count 2', 'Count 3', 'Count 4', 'Count 5',
#                           'Count 6', 'Count 7', 'Count 8', 'Count 9']

#     for file_path in file_paths:
#         try:
#             # Read the CSV, skipping the initial descriptive rows
#             # We assume the actual data starts after 'Ground Truth' and blank rows
#             # Let's find the start of the data dynamically
#             with open(file_path, 'r') as f:
#                 lines = f.readlines()
#                 data_start_row = 0
#                 for i, line in enumerate(lines):
#                     if line.strip().startswith('Round'):
#                         data_start_row = i
#                         break
#             if data_start_row == 0:
#                 print(f"Warning: Could not find 'Round' header in {file_path}. Skipping.")
#                 continue

#             df = pd.read_csv(file_path, skiprows=data_start_row)

#             # Extract header information (Item and Type) from the first few rows
#             # We need to re-read parts of the file for this, or extract from lines
#             item_name = pd.read_csv(file_path, nrows=1, header=None).iloc[0, 1].strip()
#             system_type = pd.read_csv(file_path, nrows=2, header=None).iloc[1, 1].strip()

#             # --- Data Cleaning and Feature Engineering for current DataFrame ---

#             # Add 'Item' and 'System_Type' columns
#             df['Item'] = item_name
#             df['System_Type'] = system_type

#             # Convert Min and Sec to Total_Seconds_Per_Round
#             # Ensure these columns exist before trying to convert
#             if 'Min' in df.columns and 'Sec' in df.columns and 'Sec/100' in df.columns:
#                 df['Total_Seconds_Per_Round'] = (df['Min'] * 60) + df['Sec'] + (df['Sec/100'] / 100)
#             else:
#                 print(f"Missing time columns in {file_path}. Skipping time calculation.")
#                 df['Total_Seconds_Per_Round'] = None # Or handle as appropriate

#             # Ensure 'Observed Total Count for Round' is numeric
#             df['Observed Total Count for Round'] = pd.to_numeric(df['Observed Total Count for Round'], errors='coerce')

#             # Ensure 'Accuracy for Round' is numeric
#             df['Accuracy for Round'] = pd.to_numeric(df['Accuracy for Round'], errors='coerce')

#             # Handle 'Defects for Round': Ensure it's numeric and fill NaN with 0 if appropriate for analysis
#             # UPDATED COLUMN NAME HERE:
#             if 'Defects' in df.columns: # Check for the old name first
#                 df.rename(columns={'Defects': 'Defects for Round'}, inplace=True)
#             df['Defects for Round'] = pd.to_numeric(df['Defects for Round'], errors='coerce').fillna(0)


#             # --- Dynamic handling of Ground Truth and other high-level metrics ---
#             # These are typically in the first few rows of each file, above the 'Round' data.
#             # Let's re-read the top section to get these.
#             meta_data = pd.read_csv(file_path, nrows=data_start_row, header=None, index_col=0)
#             meta_data_dict = meta_data.iloc[:, 0].dropna().to_dict()

#             df['GT_Number_of_Objects'] = float(meta_data_dict.get('number of objects', float('nan')))
#             df['GT_Number_of_Defects'] = float(meta_data_dict.get('number of defects', float('nan')))
#             df['GT_Grand_Total_Count'] = float(meta_data_dict.get('GT Grand Total Count', float('nan')))


#             # Add 'Notes' if available
#             notes_start_row = -1
#             for i, line in enumerate(lines):
#                 if line.strip().lower().startswith('notes'):
#                     notes_start_row = i
#                     break

#             if notes_start_row != -1:
#                 # Read all lines from notes_start_row + 1 to the end
#                 notes_lines = lines[notes_start_row + 1:]
#                 # Filter out empty lines and join them
#                 notes = [note.strip() for note in notes_lines if note.strip()]
#                 # Assign the notes as a single string to a new column for this item's dataframe
#                 # This might be tricky if notes are per-round vs. overall.
#                 # Assuming overall notes for now, apply to all rows of this item/system.
#                 df['Notes'] = "\n".join(notes)
#             else:
#                 df['Notes'] = None


#             # Select and reorder relevant columns
#             # We need to make sure 'Count X' columns are handled gracefully
#             # Only keep the 'Count X' columns that exist in the current dataframe
#             existing_count_cols = [col for col in count_columns_base if col in df.columns]

#             # Define the desired final columns
#             final_columns = [
#                 'Item', 'System_Type', 'Round', 'Min', 'Sec', 'Sec/100', 'Total_Seconds_Per_Round',
#                 'Defects for Round', 'Observed Total Count for Round', 'Accuracy for Round', # UPDATED COLUMN NAME HERE
#                 'GT_Number_of_Objects', 'GT_Number_of_Defects', 'GT_Grand_Total_Count', 'Notes'
#             ] + existing_count_cols

#             # Filter df to only include final_columns that actually exist in the df
#             df = df[[col for col in final_columns if col in df.columns]]

#             all_data_frames.append(df)

#         except Exception as e:
#             print(f"Error processing {file_path}: {e}")
#             continue

#     if not all_data_frames:
#         print("No data frames were successfully processed.")
#         return pd.DataFrame() # Return empty DataFrame

#     master_df = pd.concat(all_data_frames, ignore_index=True)

#     return master_df

# # --- Usage Example ---
# if __name__ == "__main__":
#     # Assuming your files are in the same directory as this script,
#     # or you provide the full paths.
#     # Replace 'path/to/your/files/' with the actual directory if different.
#     # Or just list the files if they are in the current working directory.

#     data_files = [
#         'data/black human.csv',
#         'data/black screw AI.csv',
#         'data/long screw AI.csv',
#         'data/long screw human.csv',
#         'data/nail AI.csv',
#         'data/nail human.csv',
#         'data/nut AI.csv',
#         'data/nut human.csv',
#         'data/rivet human.csv',
#         'data/rivet screw AI.csv',
#         'data/tek-screw AI.csv',
#         'data/tek-screw human.csv',
#         'data/washer AI.csv',
#         'data/washer human.csv'
#     ]

#     # Create a list of full file paths
#     current_directory = os.getcwd() # Gets the current working directory
#     file_paths = [os.path.join(current_directory, f) for f in data_files]

#     # Create the master DataFrame
#     master_df = create_master_dataframe(file_paths)

#     # Display the first few rows of the consolidated DataFrame
#     print("Master DataFrame Head:")
#     print(master_df.head())

#     # Display basic info to check data types and non-null counts
#     print("\nMaster DataFrame Info:")
#     master_df.info()

#     # Display some descriptive statistics
#     print("\nMaster DataFrame Describe (Numeric Columns):")
#     print(master_df.describe())

#     # Check unique items and system types to confirm parsing
#     print("\nUnique Items:", master_df['Item'].unique())
#     print("Unique System Types:", master_df['System_Type'].unique())
    
#     # --- SAVE THE DATAFRAME TO A CSV FILE ---
#     output_filename = "master_data.csv"
#     master_df.to_csv(output_filename, index=False)
#     print(f"\nMaster DataFrame saved to {output_filename}")
    
import pandas as pd
import os
import re # Import regex module

def create_master_dataframe(file_paths):
    """
    Reads multiple CSV files, extracts relevant data, calculates total time,
    and combines them into a single master DataFrame. This version robustly
    handles varying metadata and footer notes.

    Args:
        file_paths (list): A list of file paths to the CSV datasets.

    Returns:
        pd.DataFrame: A consolidated DataFrame with all the processed data.
    """
    all_data_frames = []

    # Define the columns that represent individual counts, these might vary
    count_columns_base = ['Count 1', 'Count 2', 'Count 3', 'Count 4', 'Count 5',
                          'Count 6', 'Count 7', 'Count 8', 'Count 9']

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f: # Added encoding for robustness
                lines = f.readlines()

            # --- Locate data start and end (for notes) ---
            data_start_row = -1
            notes_start_row = -1
            
            # Find the row with 'Round' header
            for i, line in enumerate(lines):
                if line.strip().lower().startswith('round'):
                    data_start_row = i
                    break
            
            if data_start_row == -1:
                print(f"Warning: Could not find 'Round' header in {file_path}. Skipping file.")
                continue
            
            # Find the row with 'notes' header (if any)
            # Search from the line after data_start_row to avoid picking up 'notes' in data header
            for i in range(data_start_row + 1, len(lines)):
                if lines[i].strip().lower().startswith('notes'):
                    notes_start_row = i
                    break

            # Determine the number of data rows to read
            # This logic needs to be careful not to include trailing empty rows or other footers
            num_data_rows = 0
            if notes_start_row != -1:
                # Data ends before the notes section
                num_data_rows = notes_start_row - (data_start_row + 1)
            else:
                # If no notes section, count actual data rows until an empty line or end of file
                for i in range(data_start_row + 1, len(lines)):
                    if lines[i].strip():
                        num_data_rows += 1
                    else:
                        # Stop at the first empty line if data has already started
                        if num_data_rows > 0:
                            break


            # Read the main data section using precise skiprows and nrows
            df = pd.read_csv(
                file_path,
                skiprows=data_start_row,
                nrows=num_data_rows,
                header=0,
                encoding='utf-8',
                # Set dtype to object for columns that might contain mixed types during initial read,
                # then convert numerically later. This prevents DtypeWarning.
                dtype={'Min': float, 'Sec': float, 'Sec/100': float,
                       'Defects': float, 'Observed Total Count for Round': float,
                       'Accuracy for Round': float},
                # Attempt to infer better types later, but for now, be explicit to avoid issues
                # with partial numerical values.
                # Do NOT use skip_blank_lines=True here, it applies to initial skiprows, not nrows.
            )
            
            # Drop any entirely empty rows that might have been read due to slight miscalculation
            df.dropna(how='all', inplace=True)
            
            # Extract header information (Item and Type) from the first few rows
            item_name = pd.read_csv(file_path, nrows=1, header=None, encoding='utf-8').iloc[0, 1].strip()
            system_type = pd.read_csv(file_path, nrows=2, header=None, encoding='utf-8').iloc[1, 1].strip()

            # --- Data Cleaning and Feature Engineering for current DataFrame ---

            # Add 'Item' and 'System_Type' columns
            df['Item'] = item_name
            df['System_Type'] = system_type

            # Ensure 'Round' is numeric first, coerce errors for potentially bad rows
            df['Round'] = pd.to_numeric(df['Round'], errors='coerce')
            
            # Drop rows where 'Round' couldn't be parsed, as they are not valid data rows
            df.dropna(subset=['Round'], inplace=True)
            
            # Convert 'Round' to int
            df['Round'] = df['Round'].astype(int)

            # Convert Min, Sec, Sec/100 to Total_Seconds_Per_Round
            time_cols = ['Min', 'Sec', 'Sec/100']
            for col in time_cols:
                if col not in df.columns:
                    df[col] = 0.0 # Add missing time columns with default 0.0
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # Ensure numeric, fill NaN with 0

            df['Total_Seconds_Per_Round'] = (df['Min'] * 60) + df['Sec'] + (df['Sec/100'] / 100)

            # Ensure 'Observed Total Count for Round' is numeric
            df['Observed Total Count for Round'] = pd.to_numeric(df['Observed Total Count for Round'], errors='coerce')

            # Ensure 'Accuracy for Round' is numeric
            df['Accuracy for Round'] = pd.to_numeric(df['Accuracy for Round'], errors='coerce')

            # Handle 'Defects for Round': Ensure it's numeric and fill NaN with 0 if appropriate for analysis
            if 'Defects' in df.columns:
                df.rename(columns={'Defects': 'Defects for Round'}, inplace=True)
            df['Defects for Round'] = pd.to_numeric(df['Defects for Round'], errors='coerce').fillna(0)


            # --- Dynamic handling of Ground Truth and other high-level metrics ---
            meta_data = pd.read_csv(file_path, nrows=data_start_row, header=None, index_col=0, encoding='utf-8')
            meta_data_dict = meta_data.iloc[:, 0].dropna().to_dict()

            df['GT_Number_of_Objects'] = float(meta_data_dict.get('number of objects', float('nan')))
            df['GT_Number_of_Defects'] = float(meta_data_dict.get('number of defects', float('nan')))
            df['GT_Grand_Total_Count'] = float(meta_data_dict.get('GT Grand Total Count', float('nan')))


            # --- Robust Notes Extraction (RE-FIXED for comma cleaning) ---
            current_file_notes = ''
            if notes_start_row != -1:
                notes_lines_raw = lines[notes_start_row + 1:]
                cleaned_notes = []
                for line in notes_lines_raw:
                    # Remove leading/trailing quotes and strip whitespace
                    cleaned_line = line.strip().strip('"')
                    # Use regex to remove multiple commas or commas followed by whitespace
                    cleaned_line = re.sub(r',+\s*', '', cleaned_line)
                    if cleaned_line: # Only add if not empty after cleaning
                        cleaned_notes.append(cleaned_line)
                
                current_file_notes = "\n".join(cleaned_notes) if cleaned_notes else ''

            df['Notes'] = current_file_notes # Assign to all rows for this specific item's dataframe


            # Select and reorder relevant columns
            existing_count_cols = [col for col in count_columns_base if col in df.columns]
            
            # Ensure all 'Count X' columns are numeric and fill NaNs with 0 where appropriate
            for col in existing_count_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            final_columns = [
                'Item', 'System_Type', 'Round', 'Min', 'Sec', 'Sec/100', 'Total_Seconds_Per_Round',
                'Defects for Round', 'Observed Total Count for Round', 'Accuracy for Round',
                'GT_Number_of_Objects', 'GT_Number_of_Defects', 'GT_Grand_Total_Count', 'Notes'
            ] + existing_count_cols

            df = df[[col for col in final_columns if col in df.columns]]

            all_data_frames.append(df)

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please check the filename or path.")
            # Do NOT continue if file not found, as it might hide other issues or miss data
            # Instead, let the loop continue to process other files and report the specific error
            continue
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    if not all_data_frames:
        print("No data frames were successfully processed.")
        return pd.DataFrame() # Return empty DataFrame

    master_df = pd.concat(all_data_frames, ignore_index=True)

    # Ensure the 'Notes' column is of object (string) type after concatenation,
    # and fill any remaining NaNs (e.g., from files without notes) with empty strings
    master_df['Notes'] = master_df['Notes'].astype(str).fillna('')

    return master_df

# --- Usage Example ---
if __name__ == "__main__":
    data_files = [
        'data/nail AI.csv',
        'data/nail human.csv',
        'data/tek-screw AI.csv',
        'data/tek-screw human.csv',
        'data/long screw AI.csv',
        'data/long screw human.csv',
        'data/washer AI.csv', # This file needs to be checked by you!
        'data/washer human.csv',
        'data/nut AI.csv',
        'data/nut human.csv',
        'data/black screw AI.csv',
        'data/black human.csv',
        'data/rivet screw AI.csv',
        'data/rivet human.csv'
    ]

    current_directory = os.getcwd()
    file_paths = [os.path.join(current_directory, f) for f in data_files]

    master_df = create_master_dataframe(file_paths)

    print("Master DataFrame Head (after Notes and Data Fix):")
    print(master_df.head())

    print("\nMaster DataFrame Info (after Notes and Data Fix):")
    master_df.info()

    # Only save if the DataFrame is not empty (i.e., if some files were processed)
    if not master_df.empty:
        output_filename = "master_data_for_analysis.csv"
        master_df.to_csv(output_filename, index=False)
        print(f"\nMaster DataFrame saved to {output_filename}")
    else:
        print("\nNo data was processed successfully, master DataFrame is empty. Not saving to CSV.")