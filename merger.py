# This script merges multiple accelerometer data file for a given day into a single file and deletes the original files.
import os
import re
from datetime import datetime, timedelta

# Folder where your files are located
directory = "./accelerometer_data_from_phone"  # change this to your path if needed

# Define the date range
start_date = datetime.strptime("25-03-2025", "%d-%m-%Y")
end_date = datetime.strptime("04-04-2025", "%d-%m-%Y")

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")  # Match against filenames
    output_date = current_date.strftime("%d-%m-%Y")  # For output file name

    pattern = re.compile(
        rf"accelerometer_data_{date_str}_(\d{{2}}-\d{{2}}-\d{{2}})\.txt"
    )
    files_with_time = []

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            time_part = match.group(1)  # Extract time part
            files_with_time.append((time_part, filename))

    files_with_time.sort()  # Sort by time

    if not files_with_time:
        print(f"No files found for {output_date}")
    else:
        output_file = f"merged_{output_date}.txt"
        with open(output_file, "w") as outfile:
            for time_part, filename in files_with_time:
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Optional: separate entries

        print(f"Merged {len(files_with_time)} files into {output_file}")

        # Delete the original files after merging
        for _, filename in files_with_time:
            filepath = os.path.join(directory, filename)
            try:
                os.remove(filepath)
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")

    current_date += timedelta(days=1)
