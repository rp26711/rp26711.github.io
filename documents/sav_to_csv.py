import pyreadstat
from pathlib import Path

# Folder containing your .sav files
input_folder = Path("data")

# Convert every .sav file in the folder
for sav_file in input_folder.glob("*.sav"):

    # Read the SPSS file
    df, metadata = pyreadstat.read_sav(sav_file)

    # Create the CSV filename
    csv_file = sav_file.with_suffix(".csv")

    # Export to CSV
    df.to_csv(csv_file, index=False)
