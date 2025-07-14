import pandas as pd
import os
import re # Import regex module
import numpy as np # For np.nan

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
            data_header_row_idx = -1
            notes_start_row_idx = -1
            
            # Find the row with 'Round' header
            for i, line in enumerate(lines):
                if line.strip().lower().startswith('round'):
                    data_header_row_idx = i
                    break
            
            if data_header_row_idx == -1:
                print(f"Warning: Could not find 'Round' header in {file_path}. Skipping file.")
                continue
            
            # Find the row with 'notes' header (if any)
            # Search from the line after data_start_row to avoid picking up 'notes' in data header
            for i in range(data_header_row_idx + 1, len(lines)):
                if lines[i].strip().lower().startswith('notes'):
                    notes_start_row_idx = i
                    break

            # --- DETERMINE TRUE END OF DATA ROBUSTLY (NEW LOGIC) ---
            true_data_end_row_idx = notes_start_row_idx if notes_start_row_idx != -1 else len(lines)
            
            # Read potential data lines after the header, but before notes or end of file
            potential_data_lines = lines[data_header_row_idx + 1 : true_data_end_row_idx]
            
            num_valid_data_rows = 0
            for i, line in enumerate(potential_data_lines):
                parts = [p.strip() for p in line.split(',') if p.strip()] # Split by comma, strip, remove empty
                
                # If the line is entirely empty or looks like a trailing blank from Excel export
                if not parts:
                    break # Stop at the first fully empty line after data has started
                
                # Attempt to parse key numerical fields to detect end of actual data
                # Typically, Min, Sec, Observed Total Count should be non-zero for valid rounds
                try:
                    # Assuming Round is the first column, followed by Min, Sec, ...
                    # This needs to be robust to missing columns too if some files lack them,
                    # but for now, rely on common columns.
                    if len(parts) > 1: # Ensure there are enough parts for Min/Sec
                        round_val = pd.to_numeric(parts[0], errors='coerce')
                        min_val = pd.to_numeric(parts[1], errors='coerce') # Min is 2nd column
                        sec_val = pd.to_numeric(parts[2], errors='coerce') # Sec is 3rd column
                        
                        # Observed Total Count is typically 2nd to last before Accuracy
                        # Find its index dynamically or by name if possible, for now assume fixed position
                        # Let's rely on Min/Sec/Round for simplicity here
                        
                        if (pd.isna(round_val) or round_val == 0) and \
                           (pd.isna(min_val) or min_val == 0) and \
                           (pd.isna(sec_val) or sec_val == 0):
                            # Found a row that appears to be zero-filled or invalid after valid data started
                            if num_valid_data_rows > 0: # Only break if we've already found some valid data
                                break
                    
                    num_valid_data_rows += 1
                except IndexError: # Not enough columns in line, implies malformed or end of data
                    if num_valid_data_rows > 0:
                        break
                    else: # If no data yet and malformed, skip this line
                        continue
                except Exception as e: # Catch other parsing errors in this line
                    print(f"Warning: Error parsing line '{line.strip()}' in {file_path} for end-of-data detection: {e}")
                    if num_valid_data_rows > 0: # If we have data, this line is probably bad, so stop
                        break
                    else:
                        continue # If no data yet, this line is just garbage, keep searching


            # Read the main data section using precise skiprows and nrows
            # The header is at data_header_row_idx. Data starts at data_header_row_idx + 1.
            df = pd.read_csv(
                file_path,
                skiprows=data_header_row_idx, # Skip to the header row
                nrows=num_valid_data_rows,     # Only read the actual valid data rows
                header=0,                 # The first row after skipping is the header
                encoding='utf-8'
            )
            
            # Extract header information (Item and Type) from the first few rows
            item_name = pd.read_csv(file_path, nrows=1, header=None, encoding='utf-8').iloc[0, 1].strip()
            system_type = pd.read_csv(file_path, nrows=2, header=None, encoding='utf-8').iloc[1, 1].strip()

            # --- Data Cleaning and Feature Engineering for current DataFrame ---

            # Add 'Item' and 'System_Type' columns
            df['Item'] = item_name
            df['System_Type'] = system_type

            # Ensure 'Round' is numeric and convert to int
            df['Round'] = pd.to_numeric(df['Round'], errors='coerce').astype(int)
            
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
            meta_data = pd.read_csv(file_path, nrows=data_header_row_idx, header=None, index_col=0, encoding='utf-8')
            meta_data_dict = meta_data.iloc[:, 0].dropna().to_dict()

            df['GT_Number_of_Objects'] = float(meta_data_dict.get('number of objects', float('nan')))
            df['GT_Number_of_Defects'] = float(meta_data_dict.get('number of defects', float('nan')))
            df['GT_Grand_Total_Count'] = float(meta_data_dict.get('GT Grand Total Count', float('nan')))


            # --- Robust Notes Extraction ---
            current_file_notes = ''
            if notes_start_row_idx != -1:
                notes_lines_raw = lines[notes_start_row_idx + 1:]
                cleaned_notes = []
                for line in notes_lines_raw:
                    cleaned_line = line.strip().strip('"') # Remove leading/trailing quotes and strip whitespace
                    cleaned_line = re.sub(r',+\s*', '', cleaned_line) # Remove multiple commas or commas followed by whitespace
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
            print(f"Error: File not found at {file_path}. Please ensure it's in the correct directory.")
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
        'data/washer AI.csv',
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

print("Master DataFrame Head (after robust data parsing):")
print(master_df.head())

print("\nMaster DataFrame Info (after robust data parsing):")
master_df.info()

# Only save if the DataFrame is not empty (i.e., if some files were processed)
if not master_df.empty:
    output_filename = "master_data.csv"
    master_df.to_csv(output_filename, index=False)
    print(f"\nMaster DataFrame saved to {output_filename}")
else:
    print("\nNo data was processed successfully, master DataFrame is empty. Not saving to CSV.")