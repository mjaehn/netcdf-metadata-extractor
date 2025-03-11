import csv
import argparse
from pathlib import Path
import xarray as xr
from datetime import timedelta

def ns_to_iso_duration(ns):
    seconds = ns / 1e9
    delta = timedelta(seconds=seconds)
    days = delta.days
    seconds = delta.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    duration = 'P'
    if days > 0:
        duration += f'{days}D'
    if hours > 0 or minutes > 0 or seconds > 0:
        duration += 'T'
        if hours > 0:
            duration += f'{hours}H'
        if minutes > 0:
            duration += f'{minutes}M'
        if seconds > 0:
            duration += f'{seconds}S'
    
    return duration

def extract_metadata(file_path, output_file):
    variables_to_ignore = {'time', 'rotated_pole', 'rlon', 'rlat', 'lon_bnds',
                           'lon', 'lat_bnds', 'lat', 'HFL', 'height', 'height_2', 
                           'height_3', 'height_3_bnds',
                           'height_2m', 'height_10m', 'time_bnds', 'pressure', 
                           'plev', 'plev_bnds', 'plev_2', 'plev_2_bnds', 'plev_3',
                           'plev_3_bnds', 
                           'depth', 'depth_bnds', 'clon', 'clon_bnds', 'clat',
                           'clat_bnds', 'height_bnds', 'depth_2', 'depth_2_bnds'}
    processed_variables = set()
    # Create or open the output file in write mode
    with open(output_file, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(['Variable', 'File', 'Frequency', 'Standard Name', 'Long Name', 'Units'])

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
        for file_path in files_to_process:
            file_name = Path(file_path).name if isinstance(file_path, Path) else Path(file_path).name
            print(f"Processing file: {file_name}")

            # Open the netCDF file
            with xr.open_dataset(file_path) as ds:
                # Calculate the time step
                if 'time' in ds.variables:
                    time_var = ds.variables['time']
                    if len(time_var) > 1:
                        time_step_ns = (time_var[1] - time_var[0]).item()
                        time_step = ns_to_iso_duration(time_step_ns)
                    else:
                        time_step = 'N/A'
                else:
                    time_step = 'N/A'

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
                        rows.append([var_name, file_name, time_step, standard_name, long_name, units])

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
    parser.add_argument('file_path', type=str, help='Path to the netCDF files folder')
    parser.add_argument('-o', '--output_file', type=str, default='output_metadata.csv', help='Output CSV file name')

    args = parser.parse_args()

    extract_metadata(args.file_path, args.output_file)

if __name__ == "__main__":
    main()