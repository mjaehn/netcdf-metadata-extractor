import csv
import argparse
from pathlib import Path
import xarray as xr

def extract_metadata(folder_path, output_file):
    variables_to_ignore = {'time', 'rotated_pole', 'rlon', 'rlat', 'lon_bnds',
                           'lon', 'lat_bnds', 'lat', 'height', 'height_2m',
                           'height_10m', 'time_bnds', 'pressure', 'depth', 
                           'depth_bnds', 'clon', 'clon_bnds', 'clat', 'clat_bnds'}
    processed_variables = set()
    # Create or open the output file in write mode
    with open(output_file, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(['File', 'Variable', 'Standard Name', 'Long Name', 'Units'])

        # Create a list to store rows
        rows = []

        # Determine if the provided path is a file or a folder
        if Path(file_path).is_file():
            files_to_process = [file_path]
        elif Path(file_path).is_dir():
            files_to_process = Path(file_path).glob('*.nc')
        else:
            raise ValueError("Invalid input. Please provide a valid file or folder path.")

        # Loop through all files in the specified folder
        for file_path in Path(folder_path).glob('*.nc'):
            print(f"Processing file: {file_path.name}")

            # Open the netCDF file
            with xr.open_dataset(file_path) as ds:
                # Loop through variables
                for var_name in ds.variables:
                    if var_name not in variables_to_ignore:
                        # Skip if the variable has already been processed for this file
                        if var_name in processed_variables:
                            print(f"Skipping variable {var_name} as it has already been processed")
                            continue

                        # Get metadata for the variable
                        variable = ds.variables[var_name]
                        standard_name = variable.attrs.get('standard_name', '')
                        long_name = variable.attrs.get('long_name', '')
                        units = variable.attrs.get('units', '-') if 'units' in variable.attrs else '-'

                        # Add the row to the list
                        rows.append([file_path.name, var_name, standard_name, long_name, units])

                        # Mark the variable as processed in the dataset attributes
                        processed_variables.add(var_name)

                        print(f"Processed variable: {var_name}")
        # Sort rows by variable name
        sorted_rows = sorted(rows, key=lambda x: x[1])  # Sort by the second column (variable name)

        # Write the sorted rows to the CSV file
        csv_writer.writerows(sorted_rows)

    print(f"Total number of processed variables: {len(processed_variables)}")


def main():
    parser = argparse.ArgumentParser(description='Extract metadata from netCDF files.')
    parser.add_argument('folder_path', type=str, help='Path to the netCDF files folder')
    parser.add_argument('--output_file', type=str, default='output_metadata.csv', help='Output CSV file name')

    args = parser.parse_args()

    extract_metadata(args.folder_path, args.output_file)

if __name__ == "__main__":
    main()

